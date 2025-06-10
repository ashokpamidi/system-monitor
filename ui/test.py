from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the WebSocket connection
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            # Echo the message back to the client
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        # Handle disconnection or errors
        print(f"Error: {e}")
    finally:
        # Close the WebSocket connection
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)