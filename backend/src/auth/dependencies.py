
from fastapi.security import HTTPBearer
from fastapi.security.http import  HTTPAuthorizationCredentials
from fastapi import Request

from Dbs.DataBaseSetting.redis import get_jit_to_blocklist
from auth.utils import decode_token
from fastapi import HTTPException


class TokenBearer(HTTPBearer):


    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request) -> HTTPAuthorizationCredentials | None:

        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(status_code=401, detail={
                "error": "this token is invalid or expired",
                "resolution": "Please get new token"
            })

        if await get_jit_to_blocklist(token_data["jti"]):
            raise HTTPException(status_code=401, detail={
                "error":"This token is invalid or has been revoked",
                "resolution":"Please get new token"
            })

        self.verify_token(token_data)

        return creds



    def token_valid(self,token_data:str) -> bool:

        token = decode_token(token_data)

        return True if token is not None else False

    def verify_token(self,token_data:dict) -> bool:
        raise NotImplementedError(" Implement this method ")


class AccessTokenBearer(TokenBearer):

      def verify_token(self, token_data:dict):
          if token_data and token_data["refresh"]:
              raise HTTPException(status_code=401, detail="Invalid or expired token")


class RefreshTokenBearer(TokenBearer):

    def verify_token(self, token_data: dict):
        if token_data and not token_data["refresh"]:
            raise HTTPException(status_code=401, detail="provide refresh token")






