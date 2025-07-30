import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from ed_optimization.common.exception_helpers import ApplicationException
from ed_optimization.common.logging_helpers import get_logger
from ed_optimization.webapi.common.helpers import GenericResponse
from ed_optimization.webapi.controllers import (order_controller,
                                                rabbitmq_controller)

LOG = get_logger()


class API(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def start(self) -> None:
        LOG.info("Starting api...")
        self._include_routers()
        self._contain_exceptions()

        uvicorn.run(self, host="0.0.0.0", port=8000)

    def stop(self) -> None:
        LOG.info("API does not need to be stopped...")

    def _include_routers(self) -> None:
        LOG.info("Including routers...")
        self.include_router(order_controller.router)
        self.include_router(rabbitmq_controller.router)

    def _contain_exceptions(self) -> None:
        @self.exception_handler(ApplicationException)
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
