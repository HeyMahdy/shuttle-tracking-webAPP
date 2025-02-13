from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Dbs.DataBaseSetting.DatabaseConfig import get_async_db
from Dbs.Schemas.modelSchemas import  UserCreate, LoginData, Response
from auth.auth_Service import create_user, get_users
from auth.dependencies import TokenBearer, AccessTokenBearer
from auth.utils import verify_password_hash, create_access_token

router = APIRouter()
acceess = TokenBearer()
hh = AccessTokenBearer()

exp_time = 1



@router.post("/Signup", response_model=Response, status_code=201)
async def create_user_endpoint(user: UserCreate,_user_detail=Depends(acceess),db: AsyncSession = Depends(get_async_db)):
     User = await create_user(user, db)
     if User is None:
         raise HTTPException(status_code=404, detail="User not found")
     return Response(
         text="Account created successfully",
         data={
             "created_at": User.created_at
         }
     )

@router.post("/login")
async def login(Data : LoginData, db: AsyncSession = Depends(get_async_db)):
    email = Data.email
    password = Data.password
    user = await get_users(email,db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password_hash(password , user.password):
        raise HTTPException(status_code=404, detail="Incorrect password")


    payload = {
        "email": user.email,
        "uuid": str(user.id)
    }
    payload1 = {
        "email": user.email,
        "uuid":  str(user.id),
        "exp": (datetime.utcnow() + timedelta(hours=exp_time)).timestamp()
    }
    access_token = create_access_token(payload)
    redresh_token = create_access_token(payload1,refresh= True , expiry= timedelta(hours=exp_time))
    return {
        "access_token": access_token,
        "refresh_token": redresh_token,
    }


@router.get("/hello")
async def hello(_user_detail=Depends(hh)):
    return {
        "hello": "world"
    }







