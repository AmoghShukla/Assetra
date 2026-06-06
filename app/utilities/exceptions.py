from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, status_code : int, detail : str):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(AppException):
    def __init__(self, resource : str = "Resource"):
        super().__init__(status.HTTP_404_NOT_FOUND, f"{resource} not found")


class UnauthorizedException(AppException):
    def __init__(self, detail : str = "Unauthorized"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


class ForbiddenException(AppException):
    def __init__(self, detail : str = "Forbidden"):
        super().__init__(status.HTTP_403_FORBIDDEN, detail)


class ConflictException(AppException):
    def __init__(self, detail : str = "Conflict"):
        super().__init__(status.HTTP_409_CONFLICT, detail)


class BadRequestException(AppException):
    def __init__(self, detail : str = "Bad request"):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class InvalidAssetCodeException(BadRequestException):
    def __init__(self):
        super().__init__("Asset code must be 1 uppercase letter followed by 4 digits (e.g. A1234)")


class InvalidTicketTransitionException(BadRequestException):
    def __init__(self, from_status: str, to_status : str):
        super().__init__(f"Cannot transition ticket from {from_status} to {to_status}")


class PermissionRevokedException(ForbiddenException):
    def __init__(self):
        super().__init__("Your asset management permissions have been revoked by Superadmin")

class DatabaseError(AppException):
    def __init__(self, detail: str = "Error While Interacting with the Database"):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)
