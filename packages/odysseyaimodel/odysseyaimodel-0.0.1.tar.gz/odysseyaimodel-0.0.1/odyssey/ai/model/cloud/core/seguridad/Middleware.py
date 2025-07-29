'''Módulo Middlware'''
from __future__ import annotations

import time
from collections import OrderedDict

from fastapi import FastAPI, Request
from requests import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware

from odyssey.ai.model.cloud.configuracion.Configuracion import origins
from odyssey.ai.model.cloud.core.utilerias.Constantes import SELF


def add_secure_middleware(app: FastAPI):
    '''
        add_secure_middleware
    '''
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Aqui manejar el middleware de api
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        '''
        add_process_time_header
        :param request: request
        :param call_next: next
        :return: response
        '''
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    @app.middleware("http")
    async def secure_headers(request: Request, call_next):
        '''
        secure_headers middleware de seguridad para control origin
        :param request: request
        :param call_next: next
        :return: response
        '''
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = origins.__str__()
        response.headers["Access-Control-Allow-Credentials"] = "True"
        #   "response.headers["Content-Security-Policy"] = (
        #    "default-src 'self'; script-src 'self';frame-src 'self'" +
        #    "'unsafe-inline' 'unsafe-eval' data: 'unsafe-hashes' 'self'")

        return response


CSP: dict[str, str | list[str]] = {
    "default-src": "'" + SELF + "'",
    "img-src": [
        "*",
        # For SWAGGER UI
        "data:",
    ],
    "connect-src": "'" + SELF + "'",
    "script-src": "'" + SELF + "'",
    "style-src": ["'" + SELF + "'", "'unsafe-inline'"],
    "script-src-elem": [
        # For SWAGGER UI
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
        "'sha256-1I8qOd6RIfaPInCv8Ivv4j+J0C6d7I8+th40S5U/TVc='",
    ],
    "style-src-elem": [
        # For SWAGGER UI
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
    ],
}


def parse_policy(policy: dict[str, str | list[str]] | str) -> str:
    """Parse a given policy dict to string."""
    if isinstance(policy, str):
        # parse the string into a policy dict
        policy_string = policy
        policy = OrderedDict()

        for policy_part in policy_string.split(";"):
            policy_parts = policy_part.strip().split(" ")
            policy[policy_parts[0]] = " ".join(policy_parts[1:])

    policies = []
    for section, content in policy.items():
        if not isinstance(content, str):
            content = " ".join(content)
        policy_part = f"{section} {content}"

        policies.append(policy_part)

    parsed_policy = "; ".join(policies)

    return parsed_policy


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    def __init__(self, app: FastAPI, csp: bool = True) -> None:
        """Init SecurityHeadersMiddleware.

        :param app: FastAPI instance
        :param no_csp: If no CSP should be used;
            defaults to :py:obj:`False`
        """
        super().__init__(app)
        self.csp = csp

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Dispatch of the middleware.

        :param request: Incoming request
        :param call_next: Function to process the request
        :return: Return response coming from from processed request
        """
        headers = {
            "Content-Security-Policy": "" if not self.csp else parse_policy(CSP),
            "Cross-Origin-Opener-Policy": "same-origin",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Strict-Transport-Security": "max-age=31556926; includeSubDomains",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
        }
        response = await call_next(request)
        response.headers.update(headers)

        return response
