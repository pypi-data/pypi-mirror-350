""" FastAPI ServiceMon"""
import logging
import time
from fastapi import Request
from ipulse_shared_base_ftredge import DataResource, Action, ProgressStatus, LogLevel
from starlette.middleware.base import BaseHTTPMiddleware
from . import Servicemon


class FastAPIServiceMon(Servicemon):
    """
    Extension of Servicemon designed specifically for FastAPI applications.
    Adds integration with FastAPI request/response lifecycle.
    """

    @staticmethod
    def get_fastapi_middleware():
        """
        Creates a FastAPI middleware class that uses ServiceMon for request logging.

        Returns:
            A middleware class that can be registered with FastAPI
        """


        class ServiceMonMiddleware(BaseHTTPMiddleware):
            """
            Middleware class for integrating ServiceMon into FastAPI request/response lifecycle.
            """
            async def dispatch(self, request: Request, call_next):
                # Create ServiceMon instance
                logger_name = f"{request.app.state.env_prefix}__dp_core_api_live__apilogger"
                logger = logging.getLogger(logger_name)

                path = request.url.path
                method = request.method

                # Skip monitoring for certain paths
                skip_paths = ["/health", "/metrics", "/docs", "/redoc", "/openapi.json"]
                if any(path.startswith(skip_p) for skip_p in skip_paths):
                    return await call_next(request)

                # Initialize ServiceMon
                servicemon = Servicemon(
                    logger=logger,
                    base_context=f"API: {path}\nMethod: {method}",
                    service_name=f"API_{method}_{path.replace('/', '_')}"
                )

                # Start monitoring
                client_ip = request.client.host if request.client else "unknown"
                user_agent = request.headers.get("user-agent", "unknown")
                servicemon.start(f"API Request {method} {path}")


                # Add request info
                servicemon.log(
                    level=LogLevel.INFO,
                    description=f"Request received for {method} {path}. Client IP: {client_ip}. User Agent: {user_agent}",
                    resource=DataResource.API_INTERNAL,
                    action=Action.EXECUTE,
                    progress_status=ProgressStatus.STARTED,
                )

                # Process the request and catch any errors
                try:
                    # Store ServiceMon in request state for handlers to access
                    request.state.svcmon = servicemon

                    # Process request
                    start_time = time.time()
                    response = await call_next(request)
                    process_time = int((time.time() - start_time) * 1000)

                    # Log response
                    status_code = response.status_code
                    progress_status = (
                        ProgressStatus.DONE
                        if 200 <= status_code < 300
                        else ProgressStatus.FINISHED_WITH_ISSUES
                    )

                    log_level = (
                        LogLevel.ERROR if status_code >= 500
                        else LogLevel.WARNING if status_code >= 400
                        else LogLevel.INFO
                    )

                    servicemon.log(
                        level=log_level,
                        description=f"Response sent: {status_code} in {process_time}ms for {method} {path}",
                        resource=DataResource.API_INTERNAL,
                        action=Action.EXECUTE,
                        progress_status=progress_status

                    )

                    # Finalize monitoring
                    servicemon.end(status=progress_status)
                    return response

                except Exception as exc:
                    # Log error and re-raise
                    servicemon.log(
                        level=LogLevel.ERROR,
                        description=f"Error processing request: {exc}",
                        resource=DataResource.API_INTERNAL,
                        action=Action.EXECUTE,
                        progress_status=ProgressStatus.FAILED
                    )

                    servicemon.end(status=ProgressStatus.FAILED)
                    raise

        return ServiceMonMiddleware

    # @staticmethod
    # def setup_fastapi(app):
    #     """
    #     Configure a FastAPI application with ServiceMon integration.

    #     Args:
    #         app: The FastAPI application instance
    #     """
    #     from fastapi import FastAPI

    #     if not isinstance(app, FastAPI):
    #         raise TypeError("Expected FastAPI application instance")

    #     # Register middleware
    #     app.add_middleware(FastAPIServiceMon.get_fastapi_middleware())

    #     # Add dependency for route handlers
    #     from fastapi import Depends, Request

    #     async def get_servicemon(request: Request):
    #         """Dependency for accessing the current ServiceMon instance."""
    #         return getattr(request.state, "svcmon", None)

    #     app.dependency_overrides[FastAPIServiceMon] = get_servicemon
