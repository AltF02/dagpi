import asyncio
import aiohttp
from app import config
import sentry_sdk
import wand.exceptions as we

from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.staticfiles import StaticFiles
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware

from app.utils.tokencheck import tokenprocess
from app.utils.logogame import logogame
from app.utils.exceptions import *

from .router import redirect, api

sentry_sdk.init(dsn=config.sentry)

loop, logGameClass = asyncio.get_event_loop(), logogame()
makePool, session, tkc = loop.create_task(logGameClass.makepool()), aiohttp.ClientSession(), tokenprocess()

app = FastAPI()
wsgi_app = SentryWsgiMiddleware(app)

# /.well-known/acme-challenge
app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/bin", StaticFiles(directory="bin"), name="bin")


@app.exception_handler(we.TypeError)
async def wandtypehandler(request: Request, exec: we.TypeError):
    return JSONResponse(status_code=415, content={'error': 'There was no image at the url you provided'})


@app.exception_handler(BadImage)
async def badimage(request: Request, exec: BadImage):
    return JSONResponse(status_code=415, content={'error': 'There was no image at the url you provided'})


@app.exception_handler(BadUrl)
async def badurl(request: Request, exec: BadUrl):
    return JSONResponse(status_code=400, content={'error': 'The url provided for the image was incorrectly framed'})


@app.exception_handler(FileLarge)
async def largefile(request: Request, exec: FileLarge):
    return JSONResponse(status_code=413, content={'error': 'The file you provided was too large'})


@app.exception_handler(ServerTimeout)
async def servertimeout(request: Request, exec: ServerTimeout):
    return JSONResponse(status_code=408, content={'error': 'The time taken to get the image at your url was too long'})


@app.exception_handler(RateLimit)
async def ratelimit(request: Request, exec: RateLimit):
    return JSONResponse(status_code=429,
                        content={'error': 'You are being ratelimited. Please stick to 60 requests per minute'})


@app.exception_handler(InvalidToken)
async def badimage(request: Request, exec: InvalidToken):
    return JSONResponse(status_code=401,
                        content={'error': 'The token you provided is invalid. Please apply for a token'})


@app.get("/docs", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


@app.get("/playground", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - API playground",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/", include_in_schema=False)
def read_root():
    return {
        "Hello": "World",
        "Join our discord server to get a token": "http://server.daggy.tech",
        "Read the documentation at ": "http://dagpi.tk/docs",
        "Play around with the api (needs token)": "http://dagpi.tk/playground",
        "Check out dagbot": "https://dagbot-is.the-be.st",
    }


@app.post('/gettoken', include_in_schema=False)
async def gettoken(enhanced_token: str = Header(None), user_id: int = Header(None)):
    # y = await checkenhcanced(enhanced_token)
    stat, tok = tkc.gettoken(user_id)
    if stat:
        return JSONResponse(status_code=200, content={'token': tok})
    else:
        return JSONResponse(status_code=500, content={'error': 'We were unable to find a tokenfrom that userid'})


@app.post('/tokenapply', include_in_schema=False)
async def token_apply(enhanced_token: str = Header(None), user_id: int = Header(None)):
    # y = await checkenhcanced(enhanced_token)
    stat, co = tkc.adduser(user_id)
    if stat is True:
        return JSONResponse(status_code=200, content={'token': co})
    elif stat is False:
        if co == 1:
            # tok = tkc.gettoken(user_id)
            return JSONResponse(status_code=200, content={'User aldready exists': co})
        else:
            return JSONResponse(status_code=500, content={'error': 'we were unable to insert your token'})


@app.get('/tokenlist', include_in_schema=False)
async def user_stats(enhanced_token: str = Header(None)):
    # y = await checkenhcanced(enhanced_token)
    stats = tkc.getstats()
    return JSONResponse(status_code=200, content={'data': stats})


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Dagpi",
        version="1.0",
        description="The Number 1 Image generation api",
        routes=app.routes
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://dagbot-is.the-be.st/logo.png"}
    app.openapi_schema = openapi_schema
    app.include_router(redirect.router)
    app.include_router(api.router, prefix='/api')
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(redirect.router)


async def main():
    while True:
        tkc.resetlimits()
        await asyncio.sleep(60)


if __name__ == "__main__":
    task = loop.create_task(main())

    try:
        task
    except asyncio.CancelledError:
        pass
