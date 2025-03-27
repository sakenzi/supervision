import websocket


def on_open(ws):
    print("Connection opened")
    ws.send("Hello")

def on_message(ws, message):
    print(f"message: {message}")

def on_close(ws):
    print("connection closed")

ws = websocket.WebSocketApp("ws://127.0.0.1:8000/tasks/ws",
                            on_open=on_open,
                            on_message=on_message,
                            on_close=on_close)

ws.run_forever()
