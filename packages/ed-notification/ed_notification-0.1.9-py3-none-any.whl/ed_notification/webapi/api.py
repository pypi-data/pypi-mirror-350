import uvicorn
from ed_domain.common.exceptions import ApplicationException
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from ed_notification.common.logging_helpers import get_logger
from ed_notification.common.singleton_helpers import SingletonMeta
from ed_notification.webapi.common.helpers import GenericResponse
from ed_notification.webapi.controllers import (notification_controller,
                                                rabbitmq_controller)

LOG = get_logger()


class API(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._app = FastAPI(title="EasyDrop Notification Service")

    @property
    def app(self):
        return self._app

    def start(self) -> None:
        LOG.info("Starting api...")
        self._include_routers()
        self._contain_exceptions()

        uvicorn.run(self._app, host="0.0.0.0", port=8000)

    def stop(self) -> None:
        LOG.info("API does not need to be stopped...")

    def _include_routers(self) -> None:
        LOG.info("Including routers...")
        self._app.include_router(notification_controller.router)
        self._app.include_router(rabbitmq_controller.router)

    def _contain_exceptions(self) -> None:
        @self._app.exception_handler(ApplicationException)
        async def application_exception_handler(
            request: Request, exception: ApplicationException
        ) -> JSONResponse:
            return JSONResponse(
                status_code=exception.error_code,
                content=GenericResponse(
                    is_success=False,
                    message=exception.message,
                    errors=exception.errors,
                    data=None,
                ).to_dict(),
            )
