from datetime import timedelta, datetime
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from Dbs.DataBaseSetting.DatabaseConfig import get_async_db
from Dbs.DataBaseSetting.redis import add_jit_to_blocklist
from Dbs.Schemas.modelSchemas import  UserCreate, LoginData, Response
from auth.auth_Service import create_user, get_users
from auth.dependencies import  AccessTokenBearer, RefreshTokenBearer
from auth.utils import verify_password_hash, create_access_token, decode_token

router = APIRouter()


exp_time = 1



@router.post("/Signup", response_model=Response, status_code=201)
async def create_user_endpoint(user: UserCreate,db: AsyncSession = Depends(get_async_db)):
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
async def hello(_user_detail=Depends(AccessTokenBearer())):




    return {
        "hello": "world"
    }

@router.get("/access_token")
async def new_token_for_access(token_deta:HTTPAuthorizationCredentials=Depends(RefreshTokenBearer())):

      token_details = decode_token(token_deta.credentials)

      if datetime.fromtimestamp(token_details["exp"]) > datetime.now():
          new_access_token = create_access_token(token_details)
          return {
              "access_token": new_access_token
          }

      raise HTTPException(status_code=404, detail="Incorrect token or expired")

@router.get("/loggout")
async def revoked_token(token_details:HTTPAuthorizationCredentials = Depends(AccessTokenBearer())):

    decoded_token = decode_token(token_details.credentials)

    jit = decoded_token["jti"]

    await add_jit_to_blocklist(jti=jit)

    return JSONResponse(
        content={
            "message": "logged out",
        },
        status_code=HTTPStatus.OK
    )





