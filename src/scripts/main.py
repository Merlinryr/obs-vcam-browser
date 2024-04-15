import cv2
import asyncio
import websockets
import ssl
from glasses_detector import GlassesClassifier



ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
cap = cv2.VideoCapture(2) # OBS Virtual Camera
classifier = GlassesClassifier(kind="anyglasses")

clients = set()

async def register(websocket):
    clients.add(websocket)

async def unregister(websocket):
    clients.remove(websocket)

async def send_predictions(websocket):
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imwrite('temp_frame.jpg', frame)
            predictions = classifier.process_file('temp_frame.jpg', "./")
            print(predictions)
            await websocket.send(str(predictions))

            cv2.imshow('Webcam Feed - Press Q to Exit', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except websockets.exceptions.ConnectionClosed:
        await unregister(websocket)
    finally:
        cap.release()
        cv2.destroyAllWindows()

async def handler(websocket, path):
    await register(websocket)
    await send_predictions(websocket)  

async def main():
    async with websockets.serve(handler, "localhost", 3000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
