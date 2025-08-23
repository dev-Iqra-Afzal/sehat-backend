from typing import List, Optional

from fastapi import APIRouter, Request, Response
import httpx


def create_proxy_router(prefix: str, target_url: str, tags: Optional[List[str]] = None) -> APIRouter:
    """Create a router that proxies all requests to another service."""
    router = APIRouter(prefix=prefix, tags=tags)

    @router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
    async def proxy(request: Request, path: str) -> Response:
        async with httpx.AsyncClient(base_url=target_url) as client:
            resp = await client.request(
                request.method,
                path,
                headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
                params=request.query_params,
                content=await request.body(),
            )
        return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))

    return router