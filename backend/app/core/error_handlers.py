from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.core.exceptions import AppError
from app.core.responses import error_response


async def app_error_handler(request: Request, exc: AppError):
    return error_response(code=exc.code, message=exc.message, status_code=exc.status_code)


async def validation_error_handler(request: Request, exc: RequestValidationError):
    primer_error = exc.errors()[0]
    campo = ".".join(str(parte) for parte in primer_error["loc"] if parte != "body")
    mensaje = f"Dato inválido en '{campo}': {primer_error['msg']}" if campo else "Los datos enviados no son válidos"
    return error_response(code="VALIDATION_ERROR", message=mensaje, status_code=422)


async def unhandled_exception_handler(request: Request, exc: Exception):
    return error_response(code="INTERNAL_ERROR", message="Ocurrió un error inesperado en el servidor", status_code=500)


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)