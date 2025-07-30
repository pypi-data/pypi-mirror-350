import logging
from typing import List, Optional, Union

from asgi_logger.middleware import AccessInfo, AccessLogAtoms, AccessLoggerMiddleware
from asgiref.typing import ASGI3Application, ASGIReceiveCallable, ASGISendCallable, HTTPScope


class FilteredAccessLoggerMiddleware(AccessLoggerMiddleware):
    """The lib asgi-logger wrapped to exclude prtg and health checks from being logged
    Furthermore it adds logging of the incoming requests
    """

    def __init__(
        self,
        app: ASGI3Application,
        format: Union[str, None],
        logger: Union[logging.Logger, None],
        excluded_paths: Optional[List[str]] = None,
        exclude_header: Optional[str] = None,
    ) -> None:
        super().__init__(app, format, logger)
        self.excluded_paths = excluded_paths or []
        self.exclude_header = exclude_header.strip().lower() if exclude_header else ""

    async def __call__(
        self, scope: HTTPScope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:  # pragma: no cover
        if self._should_log(scope):
            self.logger.info("Received: %s %s", scope["method"], scope["path"])

        await super().__call__(scope, receive, send)

    def log(self, scope: HTTPScope, info: AccessInfo) -> None:
        if self._should_log(scope):
            extra_args = {"execution_time": info["end_time"] - info["start_time"]}
            if info["response"].get("status") and str(info["response"]["status"])[0] == "2":  # type: ignore
                self.logger.info(self.format, AccessLogAtoms(scope, info), extra=extra_args)
            else:
                self.logger.warning(self.format, AccessLogAtoms(scope, info), extra=extra_args)

    def _should_log(self, scope: HTTPScope) -> bool:
        return (
            scope["type"] == "http"
            and not FilteredAccessLoggerMiddleware._is_excluded_via_path(scope, self.excluded_paths)
            and not FilteredAccessLoggerMiddleware._is_excluded_via_header(scope, self.exclude_header)
        )

    @staticmethod
    def _is_excluded_via_path(scope: HTTPScope, excluded_paths: List[str]) -> bool:
        if not excluded_paths:
            return False

        path: str = str(scope["path"])
        return any(excluded in path for excluded in excluded_paths)

    @staticmethod
    def _is_excluded_via_header(scope: HTTPScope, exclude_header: str) -> bool:
        if not exclude_header:
            return False

        headers = scope.get("headers", [])
        target_header_bytes = exclude_header.encode("latin-1").lower()

        for header_key, _ in headers:
            if header_key.lower() == target_header_bytes:
                return True
        return False
