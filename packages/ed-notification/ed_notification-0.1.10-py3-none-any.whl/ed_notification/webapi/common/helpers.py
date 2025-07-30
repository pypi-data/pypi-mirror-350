from enum import StrEnum
from functools import wraps
from typing import Awaitable, Callable, Generic, Optional, TypeVar

from fastapi.types import DecoratedCallable
from pydantic import BaseModel, Field

from ed_notification.application.common.responses.base_response import \
    BaseResponse

T = TypeVar("T")


class _ApiResponse(BaseModel):
    is_success: bool = Field(...)
    message: str = Field(...)


class GenericResponse(_ApiResponse, Generic[T]):
    data: Optional[T] = None
    errors: list[str] = []

    @staticmethod
    def from_response(base_response: BaseResponse[T]) -> "GenericResponse[T]":
        return GenericResponse[T](
            is_success=base_response.is_success,
            message=base_response.message,
            data=base_response.data,
            errors=base_response.errors,
        )

    def to_dict(self) -> dict:
        return {
            "success": self.is_success,
            "message": self.message,
            "data": self.data,
            "errors": self.errors,
        }


def rest_endpoint(
    func: Callable[..., Awaitable[BaseResponse]],
) -> Callable[..., Awaitable[GenericResponse]]:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> GenericResponse:
        response = await func(*args, **kwargs)
        return GenericResponse.from_response(response)

    return wrapper


def controller_class(cls: type) -> type:
    router_exists = False
    for attr_name in cls.__dict__.keys():
        attr = getattr(cls, attr_name)
        router_exists |= attr_name == "router"
        print(attr_name, router_exists)

        for verb, end_point in getattr(attr, "routes", []):
            print(attr)
            print(verb, end_point)
            # getattr(cls._router, verb.value.lower())(end_point)(attr)

    if not router_exists:
        raise ValueError(f"Class {cls} is not a valid controller class. ")

    return cls


class HttpVerb(StrEnum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


def route(
    verb: HttpVerb,
    end_point: str,
) -> Callable:
    def wrapper(func: DecoratedCallable) -> DecoratedCallable:
        func.__dict__.setdefault("routes", []).append((verb, end_point))

        return func

    return wrapper
