from typing import Callable
from fastapi import Request, Response
from ...core.exception import RequestException


__all__ = (
    'InternalUserAgentRestriction',
)


class InternalUserAgentRestriction:
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        ua = request.headers.get('user-agent') or ''
        if ua != 'DealerTower-Service/1.0':
            raise RequestException(
                controller='dtpyfw.middlewares.user_agent.InternalUserAgentRestriction',
                message='Wrong credential.',
                status_code=403,
            )
