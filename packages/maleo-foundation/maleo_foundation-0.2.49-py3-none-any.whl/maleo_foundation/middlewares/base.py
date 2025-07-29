import json
import threading
import time
import traceback
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from typing import Awaitable, Callable, Optional, Sequence
from maleo_foundation.authentication import Authentication
from maleo_foundation.enums import BaseEnums
from maleo_foundation.client.manager import MaleoFoundationClientManager
from maleo_foundation.models.schemas import BaseGeneralSchemas
from maleo_foundation.models.responses import BaseResponses
from maleo_foundation.models.transfers.general.token \
    import MaleoFoundationTokenGeneralTransfers
from maleo_foundation.models.transfers.parameters.token \
    import MaleoFoundationTokenParametersTransfers
from maleo_foundation.models.transfers.parameters.signature \
    import MaleoFoundationSignatureParametersTransfers
from maleo_foundation.utils.extractor import BaseExtractors
from maleo_foundation.utils.logging import MiddlewareLogger

RequestProcessor = Callable[[Request], Awaitable[Optional[Response]]]
ResponseProcessor = Callable[[Response], Awaitable[Response]]

class BaseMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app:FastAPI,
        keys:BaseGeneralSchemas.RSAKeys,
        logger:MiddlewareLogger,
        maleo_foundation:MaleoFoundationClientManager,
        allow_origins:Sequence[str] = (),
        allow_methods:Sequence[str] = ("GET",),
        allow_headers:Sequence[str] = (),
        allow_credentials:bool = False,
        limit:int = 10,
        window:int = 1,
        cleanup_interval:int = 60,
        ip_timeout:int = 300
    ):
        super().__init__(app)
        self._keys = keys
        self._logger = logger
        self._maleo_foundation = maleo_foundation
        self._allow_origins = allow_origins
        self._allow_methods = allow_methods
        self._allow_headers = allow_headers
        self._allow_credentials = allow_credentials
        self._limit = limit
        self._window = timedelta(seconds=window)
        self._cleanup_interval = timedelta(seconds=cleanup_interval)
        self._ip_timeout = timedelta(seconds=ip_timeout)
        self._requests:dict[str, list[datetime]] = defaultdict(list)
        self._last_seen: dict[str, datetime] = {}
        self._last_cleanup = datetime.now()
        self._lock = threading.RLock()  #* Use RLock for thread safety

    def _cleanup_old_data(self) -> None:
        """
        Periodically clean up old request data to prevent memory growth.
        Removes:
        1. IPs with empty request lists
        2. IPs that haven't been seen in ip_timeout period
        """
        now = datetime.now()
        if now - self._last_cleanup > self._cleanup_interval:
            with self._lock:
                #* Remove inactive IPs (not seen recently) and empty lists
                inactive_ips = []
                for ip in list(self._requests.keys()):
                    #* Remove IPs with empty timestamp lists
                    if not self._requests[ip]:
                        inactive_ips.append(ip)
                        continue
                        
                    #* Remove IPs that haven't been active recently
                    last_active = self._last_seen.get(ip, datetime.min)
                    if now - last_active > self._ip_timeout:
                        inactive_ips.append(ip)
                
                #* Remove the inactive IPs
                for ip in inactive_ips:
                    if ip in self._requests:
                        del self._requests[ip]
                    if ip in self._last_seen:
                        del self._last_seen[ip]
                
                # Update last cleanup time
                self._last_cleanup = now
                self._logger.debug(f"Cleaned up request cache. Removed {len(inactive_ips)} inactive IPs. Current tracked IPs: {len(self._requests)}")

    def _check_rate_limit(
        self,
        client_ip:str
    ) -> bool:
        """Check if the client has exceeded their rate limit"""
        with self._lock:
            now = datetime.now() #* Define current timestamp
            self._last_seen[client_ip] = now #* Update last seen timestamp for this IP

            #* Filter requests within the window
            self._requests[client_ip] = [
                timestamp for timestamp in self._requests[client_ip]
                if now - timestamp <= self._window
            ]

            #* Check if the request count exceeds the limit
            if len(self._requests[client_ip]) >= self._limit:
                return True

            #* Add the current request timestamp
            self._requests[client_ip].append(now)
            return False

    def _add_response_headers(
        self,
        request:Request,
        authentication:Authentication,
        response:Response,
        request_timestamp:datetime,
        response_timestamp:datetime,
        process_time:int
    ) -> Response:
        response.headers["X-Process-Time"] = str(process_time) #* Add Process Time Header
        response.headers["X-Request-Timestamp"] = request_timestamp.isoformat() #* Add request timestamp header
        response.headers["X-Response-Timestamp"] = response_timestamp.isoformat() #* Define and add response timestamp header
        #* Generate signature header
        message = f"{request.method}|{request.url.path}|{request_timestamp.isoformat()}|{response_timestamp.isoformat()}|{str(process_time)}"
        sign_parameters = (
            MaleoFoundationSignatureParametersTransfers
            .Sign(key=self._keys.private, password=self._keys.password, message=message)
        )
        sign_result = self._maleo_foundation.services.signature.sign(parameters=sign_parameters)
        if sign_result.success:
            response.headers["X-Signature"] = sign_result.data.signature
        if (authentication.user.is_authenticated
            and authentication.credentials.token.type == BaseEnums.TokenType.REFRESH
            and (response.status_code >= 200 and response.status_code < 300)
        ):
            #* Regenerate new authorization
            payload = (
                MaleoFoundationTokenGeneralTransfers
                .BaseEncodePayload
                .model_validate(authentication.credentials.token.payload.model_dump())
            )
            parameters = (
                MaleoFoundationTokenParametersTransfers
                .Encode(key=self._keys.private, password=self._keys.password, payload=payload)
            )
            result = self._maleo_foundation.services.token.encode(parameters=parameters)
            if result.success:
                response.headers["X-New-Authorization"] = result.data.token
        return response

    def _build_response(
        self,
        request:Request,
        authentication:Authentication,
        authentication_info:str,
        response:Response,
        request_timestamp:datetime,
        response_timestamp:datetime,
        process_time:int,
        log_level:str = "info",
        client_ip:str = "unknown"
    ) -> Response:
        response = self._add_response_headers(
            request,
            authentication,
            response,
            request_timestamp,
            response_timestamp,
            process_time
        )
        log_func = getattr(self._logger, log_level)
        log_func(
            f"Request {authentication_info} | IP: {client_ip} | Host: {request.client.host} | Port: {request.client.port} | Method: {request.method} | URL: {request.url.path} | "
            f"Headers: {dict(request.headers)} - Response | Status: {response.status_code}"
        )
        return response

    def _handle_exception(
        self,
        request:Request,
        authentication:Authentication,
        authentication_info:str,
        error,
        request_timestamp:datetime,
        response_timestamp:datetime,
        process_time:int,
        client_ip:str = "unknown"
    ):
        traceback_str = traceback.format_exc().split("\n")
        error_details = {
            "error": str(error),
            "traceback": traceback_str,
            "client_ip": client_ip,
            "method": request.method,
            "url": request.url.path,
            "headers": dict(request.headers),
        }

        response = JSONResponse(
            content=BaseResponses.ServerError().model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        self._logger.error(
            f"Request {authentication_info} | IP: {client_ip} | Host: {request.client.host} | Port: {request.client.port} | Method: {request.method} | URL: {request.url.path} | "
            f"Headers: {dict(request.headers)} - Response | Status: 500 | Exception:\n{json.dumps(error_details, indent=4)}"
        )

        return self._add_response_headers(
            request,
            authentication,
            response,
            request_timestamp,
            response_timestamp,
            process_time
        )

    async def _request_processor(self, request:Request) -> Optional[Response]:
        return None

    async def dispatch(self, request:Request, call_next:RequestResponseEndpoint):
        self._cleanup_old_data() #* Run periodic cleanup
        request_timestamp = datetime.now(tz=timezone.utc) #* Record the request timestamp
        start_time = time.perf_counter() #* Record the start time
        client_ip = BaseExtractors.extract_client_ip(request) #* Get request IP with improved extraction
        authentication = Authentication(
            credentials=request.auth,
            user=request.user
        )
        if not authentication.user.is_authenticated:
            authentication_info = "| Unauthenticated"
        else:
            authentication_info = f"| Token type: {authentication.credentials.token.type} | Username: {authentication.user.display_name} | Email:{authentication.user.identity}"

        try:
            #* 1. Rate limit check
            if self._check_rate_limit(client_ip):
                return self._build_response(
                    request=request,
                    authentication=authentication,
                    authentication_info=authentication_info,
                    response=JSONResponse(
                        content=BaseResponses.RateLimitExceeded().model_dump(),
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    ),
                    request_timestamp=request_timestamp,
                    response_timestamp=datetime.now(tz=timezone.utc),
                    process_time=time.perf_counter() - start_time,
                    log_level="warning",
                    client_ip=client_ip,
                )

            #* 2. Optional preprocessing
            pre_response = await self._request_processor(request)
            if pre_response is not None:
                return self._build_response(
                    request=request,
                    authentication=authentication,
                    authentication_info=authentication_info,
                    response=pre_response,
                    request_timestamp=request_timestamp,
                    response_timestamp=datetime.now(tz=timezone.utc),
                    process_time=time.perf_counter() - start_time,
                    log_level="info",
                    client_ip=client_ip,
                )

            #* 3. Main handler
            response = await call_next(request)
            response = self._build_response(
                request=request,
                authentication=authentication,
                authentication_info=authentication_info,
                response=response,
                request_timestamp=request_timestamp,
                response_timestamp=datetime.now(tz=timezone.utc),
                process_time=time.perf_counter() - start_time,
                log_level="info",
                client_ip=client_ip,
            )

            return response

        except Exception as e:
            return self._handle_exception(
                request=request,
                authentication=authentication,
                authentication_info=authentication_info,
                error=e,
                request_timestamp=request_timestamp,
                response_timestamp=datetime.now(tz=timezone.utc),
                process_time=time.perf_counter() - start_time,
                client_ip=client_ip
            )

def add_base_middleware(
    app:FastAPI,
    keys:BaseGeneralSchemas.RSAKeys,
    logger:MiddlewareLogger,
    maleo_foundation:MaleoFoundationClientManager,
    allow_origins:Sequence[str] = (),
    allow_methods:Sequence[str] = ("GET",),
    allow_headers:Sequence[str] = (),
    allow_credentials:bool = False,
    limit:int = 10,
    window:int = 1,
    cleanup_interval:int = 60,
    ip_timeout:int = 300
) -> None:
    """
    Adds Base middleware to the FastAPI application.

    Args:
        app: FastAPI
            The FastAPI application instance to which the middleware will be added.

        logger: Logger
            The middleware logger to be used.

        limit: int
            Request count limit in a specific window of time

        window: int
            Time window for rate limiting (in seconds).

        cleanup_interval: int
            How often to clean up old IP data (in seconds).

        ip_timeout: int
            How long to keep an IP in memory after its last activity (in seconds).
            Default is 300 seconds (5 minutes).

    Returns:
        None: The function modifies the FastAPI app by adding Base middleware.

    Note:
        FastAPI applies middleware in reverse order of registration, so this middleware
        will execute after any middleware added subsequently.

    Example:
    ```python
    add_base_middleware(app=app, limit=10, window=1, cleanup_interval=60, ip_timeout=300)
    ```
    """
    app.add_middleware(
        BaseMiddleware,
        keys=keys,
        logger=logger,
        maleo_foundation=maleo_foundation,
        allow_origins=allow_origins,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
        allow_credentials=allow_credentials,
        limit=limit,
        window=window,
        cleanup_interval=cleanup_interval,
        ip_timeout=ip_timeout
    )