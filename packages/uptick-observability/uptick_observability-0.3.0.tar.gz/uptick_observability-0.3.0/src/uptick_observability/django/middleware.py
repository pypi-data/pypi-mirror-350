import time
from collections.abc import Callable
from contextlib import ExitStack
from logging import getLogger
from typing import Any

from django.db import connections
from django.urls import resolve

from . import settings

access_logger = getLogger("access")


class _SqlCounterQueryWrapper:
    def __init__(self, carrier: Any, controller: str) -> None:
        self.carrier = carrier
        self.controller = controller

    def count_one_query(self) -> None:
        count = getattr(self.carrier, "query_count", 0)
        self.carrier.query_count = count + 1

    def __call__(
        self, execute: Callable, sql: str, params: Any, many: Any, context: Any
    ) -> Any:
        # Inject comment here
        safe_controller = self.controller.replace("%", "")
        if self.controller:
            sql = f"/* controller={safe_controller} */\n{sql}"

        self.count_one_query()
        return execute(sql, params, many, context)


class UptickSqlCounterDjangoMiddleware:
    """
    Middleware to count sql queries executed during a request.

    Also injects a comment into the sql query with the controller name to help
    debug where a slow query is coming from.
    """

    def __init__(self, get_response: Any) -> None:
        self.get_response = get_response

    def __call__(self, request: Any) -> Any:
        resolver = resolve(request.path)
        controller = resolver.view_name if resolver else ""

        with ExitStack() as stack:
            for db_alias in connections:
                stack.enter_context(
                    connections[db_alias].execute_wrapper(
                        _SqlCounterQueryWrapper(request, controller=controller)
                    )
                )
            return self.get_response(request)


class AccessLoggingMiddleware:
    """
    Access logger (alternative to daphne access logger)

    This allows us to log the user_id, number of sql queries executed and more per request.

    Example access log output:
        127.0.0.1:58689  "GET /api/v2/groups/" SC:200 3806b 0.166s SQL110 User1  VERY_SLOW_SQL
    """

    access_log_format = (
        '{ip}:{port} "{method} {path}" {status} {size} {duration} {sql_count}'
        " {user_id}{duration_tag}{sql_tag}"
    )

    def __init__(self, get_response) -> None:  # type: ignore[no-untyped-def]
        self.get_response = get_response

    def __call__(self, request):  # type: ignore[no-untyped-def]
        start = time.time()

        response = self.get_response(request)

        # We do not want to access log these endpoints. We want to keep a clean papertrail.
        if request.path in settings.PATHS_WITHOUT_INSTRUMENTATION:
            return response

        duration = time.time() - start
        status_code = getattr(response, "status_code", 0)
        user = getattr(request, "user", None)
        user_id = getattr(user, "id", None) or "Anonymous"
        ip = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR")
        port = request.META.get("REMOTE_PORT")
        sql_count = getattr(request, "query_count", 0)
        response.sql_count = sql_count
        size = len(getattr(response, "content", []))

        duration_tag = (
            ""
            if duration < settings.REQUEST_DURATION_SLOW
            else (
                " SLOW_DUR"
                if duration < settings.REQUEST_DURATION_VERY_SLOW
                else " VERY_SLOW_DUR"
            )
        )
        sql_tag = (
            ""
            if sql_count < settings.SQL_COUNT_SLOW
            else (
                " SLOW_SQL"
                if sql_count < settings.SQL_COUNT_VERY_SLOW
                else " VERY_SLOW_SQL"
            )
        )

        access_logger_method = (
            access_logger.info if status_code < 400 else access_logger.warning
        )

        access_logger_method(
            self.access_log_format.format(
                ip=ip,
                port=port,
                method=request.method,
                path=request.get_full_path(),
                status=f"SC{status_code}",
                size=f"{size}b",
                duration=f"{duration:0.3f}s",
                sql_count=f"SQL{sql_count}",
                user_id=f"USER{user_id}",
                duration_tag=duration_tag,
                sql_tag=sql_tag,
                source_tag="",
                # source_tag=request.user_agent.platform_icon,
            ),
            extra={
                "user_id": user_id,
                "status_code": status_code,
                "sql_count": sql_count,
                "size": size,
                # "user_agent": request.user_agent,
                # "platform": str(request.user_agent.platform),
                "duration": duration,
                "path": getattr(request, "path", "").removesuffix("/"),
            },
        )

        return response
