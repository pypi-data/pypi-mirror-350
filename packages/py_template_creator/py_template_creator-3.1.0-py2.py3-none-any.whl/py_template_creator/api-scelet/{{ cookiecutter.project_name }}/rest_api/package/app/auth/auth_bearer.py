from fastapi import Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth_handler import AuthHandler
from package.app.utilities import (
    CustomHTTPException,
)
import logging

logger = logging.getLogger(__name__)


class JWTBearer(HTTPBearer):
    payload = None

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, response: Response):
        credentials: HTTPAuthorizationCredentials = None
        try:
            credentials = await super(JWTBearer, self).__call__(request)
        except Exception as e:
            logger.warning(f"Issue with bearer {str(e)}")
            raise CustomHTTPException(
                status_code=401, message="Invalid or no token."
            )
        if credentials:
            if not credentials.scheme == "Bearer":
                raise CustomHTTPException(
                    status_code=401, message="Invalid authentication scheme."
                )
            token = self.verify_jwt(credentials.credentials)
            if not token:
                raise CustomHTTPException(
                    status_code=401, message="Invalid or expired token."
                )
            request.credentials = self.payload
            return credentials.credentials

    def verify_jwt(self, jwtoken: str) -> bool:
        self.payload = None
        try:
            self.payload = AuthHandler.decodeJWT(jwtoken, "access")
        except Exception as e:
            logger.warning(f"Issue decoding JWT token. Error {str(e)}")
        return self.payload
