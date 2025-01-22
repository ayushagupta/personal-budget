from fastapi.responses import JSONResponse
from typing import Any

class ResponseHandler:
    @staticmethod
    def success_response(data: Any, message: str = "Request was successful", status_code: int = 200):
        return JSONResponse(
            status_code=status_code,
            content={"status": "success", "message": message, "data": data}
        )
    
    @staticmethod
    def not_found_response(message: str = "Resource not found", status_code: int = 404):
        return JSONResponse(
            status_code=status_code,
            content={"status": "error", "message": message}
        )
    
    @staticmethod
    def bad_request_response(message: str = "Bad request", status_code: int = 400):
        return JSONResponse(
            status_code=status_code,
            content={"status": "error", "message": message}
        )
    
    @staticmethod
    def error_response(message: str, status_code: int = 500):
        return JSONResponse(
            status_code=status_code,
            content={"status": "error", "message": message}
        )
    
    @staticmethod
    def unauthorized_response(message: str = "Unauthorized", status_code: int = 401):
        return JSONResponse(
            status_code=status_code,
            content={"status": "error", "message": message}
        )

    @staticmethod
    def forbidden_response(message: str = "Forbidden", status_code: int = 403):
        return JSONResponse(
            status_code=status_code,
            content={"status": "error", "message": message}
        )