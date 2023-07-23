from fastapi import HTTPException, status


class HTTPNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Страница не найдена",
        )


class UniqueConstraintError(HTTPException):
    def __init__(self, column_name):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Значение поля "{column_name}" должно содержать уникальное значение',
        )


class WrongOldPassword(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Введен не правильный пароль",
        )
