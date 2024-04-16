import cv2
import asyncio
import websockets

from Detector import YOLOV5_Detector

video_path = 2 # 0 for integrated Camera / 2 for OBS Virtual Camera
# desired_width = 640
# desired_height = 480

desired_width = 450
desired_height = 800


clients = set()

async def register(websocket):
    clients.add(websocket)

async def unregister(websocket):
    clients.remove(websocket)

vid = cv2.VideoCapture(video_path)
detector = YOLOV5_Detector(weights='best.pt',
                           img_size=640,
                           confidence_thres=0.1,
                           iou_thresh=0.45,
                           agnostic_nms=True,
                           augment=True)

async def send_predictions(websocket):
  try:
    while True:
        ret, frame = vid.read()
        if ret:
            
            frame = cv2.resize(frame, (desired_width, desired_height))
            res = detector.Detect(frame)
            await websocket.send(str(detector.last_detection_count))

            cv2.imshow("Detection", res)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            
            await asyncio.sleep(0)
            
  except websockets.exceptions.ConnectionClosed:
      await unregister(websocket)
  finally:
      vid.release()
      cv2.destroyAllWindows()

async def handler(websocket, path):
    await register(websocket)
    await send_predictions(websocket)

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

