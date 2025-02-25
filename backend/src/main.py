import typing

from fastapi import FastAPI, Depends
from starlette.websockets import WebSocketDisconnect

from auth.auth_endpoints import router as auth_router

app = FastAPI()

app.include_router(auth_router)


from fastapi import  WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectManager:

    def __init__(self):
        self.active_websocket : list[WebSocket] = []

    async def Connect(self,websocket: WebSocket):
        await websocket.accept()
        self.active_websocket.append(websocket)


    async def Disconnect(self,websocket: WebSocket):
        self.active_websocket.remove(websocket)

    async def Send(self, message:str,websocket: WebSocket ):
        await websocket.send_text(message)

    async def broadcast(self,message:str):
        for websocket in self.active_websocket:
            await websocket.send_text(message)


connectmanager = ConnectManager()

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
     await connectmanager.Connect(websocket)
     try:
         while True:
            message = await websocket.receive_text()
            await connectmanager.broadcast(message)
     except WebSocketDisconnect:
          await connectmanager.Disconnect(websocket)


































