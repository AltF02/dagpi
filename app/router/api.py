from fastapi import APIRouter
import json

from functools import partial

from fastapi import Header
from fastapi.responses import JSONResponse

from app.main import loop, logGameClass
from app.utils.img import *
from app.utils.responses import rdict
from app.utils.exceptions import *

router = APIRouter()


@router.post("/wanted", response_model=Item, responses=rdict)
async def wanted(token: str = Header(None), url: str = Header(None)):
    """Get a wanted poster of a person by supplying a url"""
    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getwanted, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/obamameme", response_model=Item, responses=rdict)
async def obamameme(token: str = Header(None), url: str = Header(None)):
    """Get a wanted poster of a person by supplying a url"""
    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getobama, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/bad", response_model=Item, responses=rdict)
async def bad(token: str = Header(None), url: str = Header(None)):
    """Generate an image pointing at someone calling them bad"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(badimg, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


# @app.post('/api/deepfry')
# async def deepfry(token: str = Header(None),url:str = Header(None)):
# 
#     # r = await checktoken(token)
#     if r:
#         byt = await getimg(url)
#         if byt == False:
#             return JSONResponse(status_code=400,content={'error':"We were unable to use the link your provided"})
#         else:
#             fn = partial(get,byt)
#             # loop = asyncio.get_event_loop() remove this
#             img = await loop.run_in_executor(None,fn)
#             if isinstance(img,BytesIO):
#                 return StreamingResponse(img, status_code=200,media_type="image/png")
# 
#             else:
#                 return JSONResponse(status_code=500,content={"error":"The Image manipulation had a small"})
#     else:
#         return JSONResponse(status_code=401,content={'error':'Invalid token'})

@router.post("/hitler", response_model=Item, responses=rdict)
async def hitler(token: str = Header(None), url: str = Header(None)):
    """Make a person worse than hitler by supplying a url"""
    # # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(gethitler, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/tweet", response_model=Item, responses=rdict)
async def tweet(token: str = Header(None), url: str = Header(None), name: str = Header(None),
                text: str = Header(None), ):
    """Generate a realistic fake tweet of someone by supplying a url, the text and their name"""
    # # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(tweetgen, name, byt, text)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/quote", response_model=Item, responses=rdict)
async def quote(token: str = Header(None), url: str = Header(None), name: str = Header(None),
                text: str = Header(None), ):
    """Get a realistic discord message of someone """
    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(quotegen, name, text, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/thoughtimage", response_model=Item, responses=rdict)
async def thoughtimage(
        token: str = Header(None), url: str = Header(None), text: str = Header(None)
):
    """Help a person think aloud by simply adding text to a thought bubble"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getthoughtimg, byt, text)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/angel", response_model=Item, responses=rdict)
async def angel(token: str = Header(None), url: str = Header(None)):
    """Divine and angelic person"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getangel, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/trash", response_model=Item, responses=rdict)
async def trash(token: str = Header(None), url: str = Header(None)):
    """Denotes someone is trash aka garbage"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(gettrash, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/satan", response_model=Item, responses=rdict)
async def satan(token: str = Header(None), url: str = Header(None)):
    """Depcits the true form of a devil in disguise"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getsatan, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/sobel", response_model=Item, responses=rdict)
async def sobel(token: str = Header(None), url: str = Header(None)):
    """Vividly colored image with a pretty background"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getsobel, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/hog", response_model=Item, responses=rdict)
async def hogend(token: str = Header(None), url: str = Header(None)):
    """Histogram of oriented ggradients (trippy dashes)"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(gethog, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/paint", response_model=Item, responses=rdict)
async def paint(token: str = Header(None), url: str = Header(None)):
    """Turn a boring old picture/gif into a work of art"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getpaint, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/night", response_model=Item, responses=rdict)
async def night(token: str = Header(None), url: str = Header(None)):
    """Turn a   picture/gif into a nighttime scene"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getnight, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/polaroid", response_model=Item, responses=rdict)
async def polaroid(token: str = Header(None), url: str = Header(None)):
    """Turn a   picture/gif into a polarid image"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getpolaroid, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/solar", response_model=Item, responses=rdict)
async def solar(token: str = Header(None), url: str = Header(None)):
    """make an image/gif be tripping with weird effects"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getsolar, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/edge", response_model=Item, responses=rdict)
async def edge(token: str = Header(None), url: str = Header(None)):
    """make an image/gif be tripping with weird effects"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getedged, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/evil", response_model=Item, responses=rdict)
async def evil(token: str = Header(None), url: str = Header(None)):
    """*Laughs in Sithlord*"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getsithorld, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/whyareyougay", response_model=Item, responses=rdict)
async def whyareyougay(token: str = Header(None), url: str = Header(None), url2: str = Header(None)):
    """The why are you gay meme"""

    # r = await checktoken(token)
    byta = await get_img(url)
    bytb = await get_img(url2)
    fn = partial(getwhyareyougay, byta, bytb)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/5g1g", response_model=Item, responses=rdict)
async def fourguysonegirl(token: str = Header(None), url: str = Header(None), url2: str = Header(None)):
    """You know the meme, 5 guys surrounding 1 girl"""

    # r = await checktoken(token)
    byta = await get_img(url)
    bytb = await get_img(url2)
    fn = partial(get5g1g, byta, bytb)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/blur", response_model=Item, responses=rdict)
async def blur(token: str = Header(None), url: str = Header(None)):
    """Blur an image/gif"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getblur, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/invert", response_model=Item, responses=rdict)
async def invert(token: str = Header(None), url: str = Header(None)):
    """A fliperroni , swithc the colors of an image/gif"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getinvert, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


# uvicorn main:app --reload
@router.post("/pixel", response_model=Item, responses=rdict)
async def pixel(token: str = Header(None), url: str = Header(None)):
    """Retro 8but version of an image/gif"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getpixel, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/ascii", response_model=Item, responses=rdict)
async def ascii(token: str = Header(None), url: str = Header(None)):
    """Hackify an image by turning it into ascii chars"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(asciiart, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/deepfry", response_model=Item, responses=rdict)
async def deepfry(token: str = Header(None), url: str = Header(None)):
    """Deepfry a gif/static image"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getdeepfry, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/sepia", response_model=Item, responses=rdict)
async def sepia(token: str = Header(None), url: str = Header(None)):
    """Add a cool brown filter on an image/gif"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getsepia, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/wasted", response_model=Item, responses=rdict)
async def wasted(token: str = Header(None), url: str = Header(None)):
    """GTA V Wasted screen on any image/gif"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getwasted, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/triggered", response_model=Item, responses=rdict)
async def triggered(token: str = Header(None), url: str = Header(None)):
    """GTA V Wasted screen on any image/gif"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(gettriggered, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/jail", response_model=Item, responses=rdict)
async def jail(token: str = Header(None), url: str = Header(None)):
    """Put someone behind bars"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getjail, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/gay", response_model=Item, responses=rdict)
async def gay(token: str = Header(None), url: str = Header(None)):
    """Pride flag on any image/gif. Show some love <3"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getgay, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/charcoal", response_model=Item, responses=rdict)
async def charcoal(token: str = Header(None), url: str = Header(None)):
    """Turn an image/gif into an artistic sketch"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getcharc, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/colors", response_model=Item, responses=rdict)
async def imagecolors(token: str = Header(None), url: str = Header(None)):
    """TScans an Image and returns an image with data about colors in the image"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(top5colors, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/rgbdata", response_model=Item, responses=rdict)
async def rgbdata(token: str = Header(None), url: str = Header(None)):
    """TAnalyses the RGB values for an image and returns a dioramawith graphs and other imagedata"""

    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(getrgbgraph, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("qrcode")
async def qrcodegen(token: str = Header(None), text: str = Header(None)):
    # r = await checktoken(token)
    fn = partial(makeqr, text)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )

    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.get("/wtp")
async def whosethatpokemon(token: str = Header(None)):
    """Get a full whose that pokemon response"""
    # r = await checktoken(token)
    rst = str((random.randint(1, 890)))
    with open('assets/pokemons.json', 'r') as file:
        cont = json.load(file)
        mondict = cont[rst]
    qimg = f"https://logoassetsgame.s3.us-east-2.amazonaws.com/wtp/pokemon/{rst}q.png"
    aimg = f"https://logoassetsgame.s3.us-east-2.amazonaws.com/wtp/pokemon/{rst}a.png"
    return JSONResponse(status_code=200, content={"question_image": qimg, "answer_image": aimg, "pokemon": mondict})


@router.get("/logogame")
async def logoguessgame(token: str = Header(None)):
    # r = await checktoken(token)
    # try:
    resp = await logGameClass.craftdata()
    return JSONResponse(status_code=200, content=resp)
    # except:
    #    return JSONResponse(status_code=500,content={'error':'Something went wrong! We will fix it'})


# @router.get("/pokemonimage')
# async def getmon(token: str = Header(None), search:str = Header(None)):
#     async with aiofiles.open('assets/pokemons.json',mode='r') as file:
#         st = await file.read()
#         js = json.loads(st)
#     try:
#         mon = js[search]
#     except:
#         try:
#             for key in js:
#                 if js[key]['name'].lower() == search.lower():
#                     mon = js[key]
#                 else:
#                     continue
#         except:
# raise

@router.post("/meme", response_model=Item, responses=rdict, include_in_schema=False)
async def meme(token: str = Header(None), url: str = Header(None), text: str = Header(None)):
    """Generate a meme by supplying the top joke and the template.Supports both gif and static images."""
    # r = await checktoken(token)
    byt = await get_img(url)
    fn = partial(memegen, byt, text)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )


@router.post("/retromeme", response_model=Item, responses=rdict, include_in_schema=False)
async def retromeme(token: str = Header(None), url: str = Header(None), text: str = Header(None)):
    """Generate a meme by supplying the top joke and the template.Supports both gif and static images."""
    # # r = await checktoken(token)
    byt = await get_img(url)
    meme = Meme(text)
    fn = partial(meme.make_meme, byt)
    img = await loop.run_in_executor(None, fn)
    if isinstance(img, str):
        return JSONResponse(
            status_code=200,
            content={"success": True, "url": f"http://dagpi.tk/{img}"},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "The Image manipulation had a small error"},
        )
