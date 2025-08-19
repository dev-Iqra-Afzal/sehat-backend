from fastapi import APIRouter, Request, Response, HTTPException
import httpx
from ..core.config import settings

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def blood_service_proxy(request: Request, path: str):
    """
    Proxy all requests to the blood service
    """
    client = httpx.AsyncClient(base_url=settings.BLOOD_SERVICE_URL)
    
    # Forward the request to the blood service
    url = f"/{path}"
    headers = {key: value for key, value in request.headers.items() if key.lower() != "host"}
    
    body = await request.body()
    
    try:
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            cookies=request.cookies,
        )
        
        # Return the response from the blood service
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Blood service unavailable: {str(exc)}")
    finally:
        await client.aclose()
