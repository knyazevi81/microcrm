from fastapi import HTTPException, status


class UserException(HTTPException):
    def __init__(
        self,
        detail: str = "Base user exception",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(status_code=status_code, detail=detail)


class JWTException(HTTPException):
    def __init__(
        self, detail: str = "", status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail)


class ServerException(HTTPException):
    def __init__(
        self, detail: str = "", status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail)


class ServerDisconnect(ServerException):
    def __init__(self):
        super().__init__(
            detail="I can't connect to the server",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UserAlreadyExist(UserException):
    def __init__(self):
        super().__init__(
            detail="User already exist", status_code=status.HTTP_400_BAD_REQUEST
        )


class IncorrectLoginOrPasswordException(UserException):
    def __init__(self):
        super().__init__(
            detail="Incorrect login or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class TokenExpireException(JWTException):
    def __init__(self):
        super().__init__(detail="Токен истек", status_code=status.HTTP_401_UNAUTHORIZED)


class TokenAbsentException(JWTException):
    def __init__(self):
        super().__init__(
            detail="Токен отсутствует", status_code=status.HTTP_401_UNAUTHORIZED
        )


class IncorrectTokenFormatException(JWTException):
    def __init__(self):
        super().__init__(
            detail="Неверный формат токена", status_code=status.HTTP_401_UNAUTHORIZED
        )


class UserIsNotPresentException(JWTException):
    def __init__(self):
        super().__init__(
            detail="Пользователь не найден", status_code=status.HTTP_401_UNAUTHORIZED
        )
