const socket = new WebSocket("ws://localhost:3000");

export const connect = async () => {
  socket.onopen = () => {
    // now we are connected
    const interval = setInterval(() => {
      if (socket.readyState !== WebSocket.OPEN) {
        clearInterval(interval)
      }
  
      socket.send("some text") // send some text to server
    }, 1000)
  }
  
  socket.onmessage = (m) => {
    // here we got something sent from the server
    console.log(m.data)
  }
  
  socket.onclose = () => {
    // connection closed
    console.log("Connection closed")
  }
}
