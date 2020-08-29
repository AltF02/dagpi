from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse

router = APIRouter()


@router.get("/api", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@router.get("/server", include_in_schema=False)
async def server_redirect():
    return RedirectResponse(url="https://discord.gg/4R72Pks")


@router.get("/wrappers", include_in_schema=False)
async def coming_soon():
    return JSONResponse(status_code=404, content={"In the works": "Wrappers soon"})
