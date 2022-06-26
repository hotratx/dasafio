from fastapi import HTTPException
from app.core.jwt import JWTBackend
from app.core.logger import logger
from app.resources.error_messages import get_error_message


class UserModel:
    """
    Setup the user object, this is called by the authx framework, you can override this method to setup your own user object
    """

    def __init__(self, data: dict | None = None):
        """
        Initialize the user object

        Args:
            data (dict): A dictionary containing the user's data
        """
        self.data = data
        try:
            self.id = self.data.get("id")
            self.nome = self.data.get("nome")
            self.email = self.data.get("email")
        except AttributeError:
            raise HTTPException(403, detail=get_error_message("only staff"))

    @classmethod
    async def create(cls, token: str, backend: JWTBackend):
        """
        Create a user object from a token

        Args:
            token (str): The token to create the user object from
            backend (authx): The backend to use to create the user object
        Returns:
            User: The user object
        """
        data = await backend.decode_token(token)
        logger.info(f"DECODE TOKEN FROM COOKIE: {data}")
        return cls(data)
