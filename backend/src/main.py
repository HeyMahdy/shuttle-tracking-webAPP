import typing

from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect

from Dbs.DataBaseSetting.DatabaseConfig import get_async_db
from auth.auth_Service import get_role_by_email
from auth.auth_endpoints import router as auth_router
from auth.dependencies import AccessTokenBearer
from auth.utils import decode_token

app = FastAPI()

app.include_router(auth_router)


from fastapi import  WebSocket
from fastapi.responses import HTMLResponse


x = AccessTokenBearer()

class ConnectManager:
    def __init__(self):
        self.active_websocket_driver: set[WebSocket] = set()
        self.active_websocket_student: set[WebSocket] = set()

    async def ConnectDriver(self,websocket: WebSocket):
        await websocket.accept()
        self.active_websocket_driver.add(websocket)

    async def ConnectStudent(self,websocket: WebSocket):
        await websocket.accept()
        self.active_websocket_student.add(websocket)


    async def Disconnect(self,websocket: WebSocket):
        self.active_websocket_driver.remove(websocket)

    async def Send(self, message:str,websocket: WebSocket ):
        await websocket.send_text(message)

    async def broadcast(self,message:dict):
        for websocket in self.active_websocket_student:
            await websocket.send_json(message)


connectmanager = ConnectManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket , token : str = Query(...),db: AsyncSession = Depends(get_async_db)):

     token_data = decode_token(token)

     x.verify_token(token_data)

     print(token_data)

     role = await get_role_by_email(token_data['user']['email'],db)

     if role == "driver":
         await connectmanager.ConnectDriver(websocket)
     elif role == "student":
         await connectmanager.ConnectStudent(websocket)

     try:
         while True:
            message = await websocket.receive_json()
            await connectmanager.broadcast(message)
     except WebSocketDisconnect:
          await connectmanager.Disconnect(websocket)



