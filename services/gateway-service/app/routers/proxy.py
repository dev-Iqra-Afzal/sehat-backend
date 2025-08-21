from fastapi import APIRouter, Request, Response
import httpx


def create_proxy_router(prefix: str, target_url: str, tags: list[str] | None = None) -> APIRouter:
    """Create a proxy router forwarding requests to the target service."""
    router = APIRouter(prefix=prefix, tags=tags or [])

    async def proxy(request: Request, path: str = ""):
        url = target_url.rstrip("/")
        if path:
            url = f"{url}/{path}"

        async with httpx.AsyncClient() as client:
            resp = await client.request(
                request.method,
                url,
                params=request.query_params,
                content=await request.body(),
                headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
            )

        headers = dict(resp.headers)
        return Response(content=resp.content, status_code=resp.status_code, headers=headers)

    router.add_api_route("/{path:path}", proxy, methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    router.add_api_route("", proxy, methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    return router