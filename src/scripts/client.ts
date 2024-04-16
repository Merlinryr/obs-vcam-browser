export const connect = async () => {
  const ws = new WebSocket('ws://127.0.0.1:8000')

  try {
    ws.onopen = () => {
      console.log('Websocket is connected')
    }

    ws.onmessage = (event: MessageEvent) => {
      console.log(`Received predictions: ${event.data}`)
    }

    ws.onclose = () => {
      console.log('WebSocket connection closed.')
    }
  } catch (error) {
    console.error(`WebSocket connection error: ${error}`)
  }
}
