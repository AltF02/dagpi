import asyncio
import os
import random
import typing
import textwrap

from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import qrcode
import skimage

import wand.exceptions as we
import wand.image as wi

from async_timeout import timeout
from datetime import datetime

from skimage.color.adapt_rgb import adapt_rgb, each_channel
from skimage.exposure import rescale_intensity
from skimage import io
from skimage.feature import hog

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter, ImageSequence

from app.main import tkc
from app.utils.writetext import writetext
from app.utils.exceptions import *


async def delimage(source):
    await asyncio.sleep(60)
    os.remove(source)


async def get_img(url):
    import re
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    r = (re.match(regex, url) is not None)
    if not r:
        raise BadUrl('Your url is malformed')
    try:
        async with timeout(10):
            r = await session.get(url)
            if r.status == 200:
                # imgf = await aiofiles.open(f'avatar{name}.png', mode='wb')
                byt = await r.read()
                io = BytesIO(byt)
                bitsize = (len(io.getbuffer()) - io.tell())
                if bitsize > 10 * (2 ** 20):
                    raise FileLarge('File too large')
                else:
                    return byt
                # await imgf.close()
            else:
                return False
    except asyncio.TimeoutError:
        raise ServerTimeout('Image took too long to get')


def bytes_to_np(img_bytes):
    i_bytes = BytesIO(img_bytes)
    ret = io.imread(i_bytes)
    return ret


def getsobel(img):
    bt = bytes_to_np(img)

    @adapt_rgb(each_channel)
    def _sobel_each(image):
        return skimage.filters.sobel(image)

    resc = rescale_intensity(1 - _sobel_each(bt))
    y = tkc.randomword(10)
    plt.imsave(f'bin/{y}.png', resc)
    return f'bin/{y}.png'


def gethog(img):
    bt = bytes_to_np(img)
    fd, hog_image = hog(bt, orientations=8, pixels_per_cell=(16, 16),
                        cells_per_block=(1, 1), visualize=True, multichannel=True)
    y = tkc.randomword(10)
    plt.imsave(f'bin/{y}.png', hog_image, cmap=plt.cm.get_cmap("seismic"))
    return f'bin/{y}.png'


def pilimagereturn(image: bytes):
    try:
        io = BytesIO(image)
        io.seek(0)
        im = Image.open(io)
        return im
    except:
        raise BadImage('There was no image at your url')


def getsepia(image: typing.Union[BytesIO, bytes]):
    io = BytesIO(image)
    io.seek(0)

    with wi.Image() as dst_image:
        with wi.Image(blob=io.getvalue()) as src_image:
            for frame in src_image.sequence:
                frame.sepia_tone(threshold=0.8)
                dst_image.sequence.append(frame)
        y = tkc.randomword(10)
        dst_image.save(filename=f"bin/{y}.gif")
        return f"bin/{y}.gif"


def getwasted(image: typing.Union[BytesIO, bytes]):
    io = BytesIO(image)
    io.seek(0)
    try:
        with wi.Image() as dst_image:
            with wi.Image(blob=io.getvalue()) as src_image:
                for frame in src_image.sequence:
                    frame.transform_colorspace("gray")
                    dst_image.sequence.append(frame)
            bts = dst_image.make_blob()
            i = BytesIO(bts)
            i.seek(0)
    except we.TypeError:
        raise BadImage
    im = Image.open(i)
    fil = Image.open("assets/wasted.png")
    w, h = im.size
    filr = fil.resize((w, h), 5)
    flist = []
    for frame in ImageSequence.Iterator(im):
        ci = im.convert("RGBA")
        ci.paste(filr, mask=filr)
        flist.append(ci)
    y = tkc.randomword(10)
    flist[0].save(
        f"bin/{y}.gif", format="gif", save_all=True, append_images=flist, optimize=True
    )
    return f"bin/{y}.gif"


def memegen(byt, text):
    tv = pilimagereturn(byt)
    wid = tv.size[0]
    hei = tv.size[0]

    sfm = [0, 0, 0, 0]
    mplier = 0
    hply = 0

    if 0 < wid < 200:
        sfm = [25, 15, 10, 5]
        mplier = 0.1
        hply = 0.1
    elif 400 > wid >= 200:
        sfm = [30, 20, 10, 5]
        mplier = 0.075
        hply = 0.2
    elif 400 <= wid < 600:
        sfm = [50, 30, 20, 10]
        mplier = 0.05
        hply = 0.3
    elif 800 > wid >= 600:
        sfm = [70, 50, 30, 20]
        mplier = 0.025
        hply = 0.4
    elif 1000 > wid >= 800:
        sfm = [80, 60, 40, 30]
        mplier = 0.01
        hply = 0.5
    elif 1500 > wid >= 1000:
        sfm = [100, 80, 60, 40]
        mplier = 0.01
        hply = 0.6
    elif 2000 > wid >= 1400:
        sfm = [120, 100, 80, 60]
        mplier = 0.01
        hply = 0.6
    elif 2000 <= wid < 3000:
        sfm = [140, 120, 100, 80]
        mplier = 0.01
        hply = 0.6
    elif wid >= 3000:
        sfm = [180, 160, 140, 120]
        mplier = 0.01
        hply = 0.6

    x_pos = int(mplier * wid)
    # y_pos = int(-1 * (mplier * hply * 10) * hei)
    size = sfm[0]

    if 50 > len(text) > 0:
        size = sfm[1]
    elif 100 > len(text) > 50:
        size = sfm[1]
    elif 100 < len(text) < 250:
        size = sfm[2]
    elif len(text) > 250 and len(text) > 500:
        size = sfm[3]
    elif 500 < len(text) < 1000:
        size = sfm[4]
    gg = None
    if str(tv.format) == "GIF":
        gg = tv
        tv.seek(0)
        form = "gif"
    else:
        form = "png"
    y = Image.new("RGBA", (tv.size[0], 800), (256, 256, 256))
    wra = writetext(y)
    f = wra.write_text_box(
        x_pos, -10, text, tv.size[0] - 40, "assets/whitney-medium.ttf", size, color=(0, 0, 0)
    )
    t = f
    bt = wra.retimg()
    im = Image.open(bt)
    ima = im.crop((0, 0, tv.size[0], t))
    if form == "gif":
        flist = []
        for frame in ImageSequence.Iterator(gg):
            bcan = Image.new("RGBA", (tv.size[0], tv.size[1] + t), (0, 0, 0, 0))
            bcan.paste(ima)
            bcan.paste(frame, (0, t))
            flist.append(bcan)
        y = tkc.randomword(10)
        flist[0].save(
            f"bin/{y}.gif",
            format="gif",
            save_all=True,
            append_images=flist,
            optimize=True,
            loop=0,
        )
        form = "gif"
    else:
        bcan = Image.new("RGBA", (tv.size[0], tv.size[1] + t), (0, 0, 0, 0))
        bcan.paste(ima)
        bcan.paste(tv, (0, t))
        form = "png"
        y = tkc.randomword(10)
        bcan.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.{form}"


def getjail(image):
    im = pilimagereturn(image)
    flist = []
    w, h = im.size
    fil = Image.open("assets/jail.png")
    filr = fil.resize((w, h), 5)
    for frame in ImageSequence.Iterator(im):
        ci = frame.convert("RGBA")
        ci.paste(filr, mask=filr)
        ci.show()
        flist.append(ci)
    y = tkc.randomword(10)
    flist[0].save(
        f"bin/{y}.gif",
        format="gif",
        save_all=True,
        append_images=flist,
        optimize=True,
    )
    return f"bin/{y}.gif"


def getgay(image):
    im = pilimagereturn(image)
    flist = []
    w, h = im.size
    fil = Image.open("assets/gayfilter.png")
    filr = fil.resize((w, h), 5)
    for frame in ImageSequence.Iterator(im):
        ci = frame.convert("RGBA")
        ci.paste(filr, mask=filr)
        ci.show()
        flist.append(ci)
    y = tkc.randomword(10)
    flist[0].save(
        f"bin/{y}.gif",
        format="gif",
        save_all=True,
        append_images=flist,
        optimize=True,
    )
    return f"bin/{y}.gif"


def getcharc(image: typing.Union[BytesIO, bytes]):
    io = BytesIO(image)
    io.seek(0)
    with wi.Image() as dst_image:
        with wi.Image(blob=io.getvalue()) as src_image:
            for frame in src_image.sequence:
                frame.transform_colorspace("gray")
                frame.sketch(0.5, 0.0, 98.0)
                dst_image.sequence.append(frame)
        y = tkc.randomword(10)
        dst_image.save(filename=f"bin/{y}.gif")
        return f"bin/{y}.gif"


def getsolar(image: typing.Union[BytesIO, bytes]):
    io = BytesIO(image)
    io.seek(0)
    with wi.Image() as dst_image:
        with wi.Image(blob=io.getvalue()) as src_image:
            for frame in src_image.sequence:
                frame.solarize(threshold=0.5 * frame.quantum_range)
                dst_image.sequence.append(frame)
        y = tkc.randomword(10)
        dst_image.save(filename=f"bin/{y}.gif")
        return f"bin/{y}.gif"


def getpaint(image: typing.Union[BytesIO, bytes]):
    io = BytesIO(image)
    io.seek(0)
    with wi.Image() as dst_image:
        with wi.Image(blob=io.getvalue()) as src_image:
            for frame in src_image.sequence:
                frame.oil_paint(sigma=3)
                dst_image.sequence.append(frame)
        y = tkc.randomword(10)
        dst_image.save(filename=f"bin/{y}.gif")
        return f"bin/{y}.gif"


def getswirl(image: typing.Union[BytesIO, bytes]):
    io = BytesIO(image)
    io.seek(0)
    with wi.Image() as dst_image:
        with wi.Image(blob=io.getvalue()) as src_image:
            for frame in src_image.sequence:
                frame.swirl(degree=-90)
                dst_image.sequence.append(frame)
        y = tkc.randomword(10)
        dst_image.save(filename=f"bin/{y}.gif")
        return f"bin/{y}.gif"


def getpolaroid(image: typing.Union[BytesIO, bytes]):
    io = BytesIO(image)
    io.seek(0)
    with wi.Image() as dst_image:
        with wi.Image(blob=io.getvalue()) as src_image:
            for frame in src_image.sequence:
                frame.polaroid()
                dst_image.sequence.append(frame)
        y = tkc.randomword(10)
        dst_image.save(filename=f"bin/{y}.gif")
        return f"bin/{y}.gif"


def getedged(image: typing.Union[BytesIO, bytes]):
    io = BytesIO(image)
    io.seek(0)
    with wi.Image() as dst_image:
        with wi.Image(blob=io.getvalue()) as src_image:
            for frame in src_image.sequence:
                frame.alpha_channel = False
                frame.transform_colorspace('gray')
                frame.edge(2)
        y = tkc.randomword(10)
        dst_image.save(filename=f"bin/{y}.gif")
        return f"bin/{y}.gif"


def makeqr(text):
    qr = qrcode.make(text)
    y = tkc.randomword(10)
    qr.save(f"bin/{y}.png")
    return f"bin/{y}.png"


def getnight(image: typing.Union[BytesIO, bytes]):
    io = BytesIO(image)
    io.seek(0)
    with wi.Image() as dst_image:
        with wi.Image(blob=io.getvalue()) as src_image:
            for frame in src_image.sequence:
                frame.blue_shift(factor=1.25)
                dst_image.sequence.append(frame)
        y = tkc.randomword(10)
        dst_image.save(filename=f"bin/{y}.gif")
        return f"bin/{y}.gif"


def quotegen(user, text, img):
    today = datetime.today()
    y = Image.new("RGBA", (2400, 800), (0, 0, 0, 0))
    ft = pilimagereturn(img)
    topa = ft.resize((150, 150), 5)
    size = (150, 150)
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((20, 20) + size, fill=255)
    avatar = ImageOps.fit(topa, mask.size, centering=(0.5, 0.5))
    y.paste(avatar, (0, 10), mask=mask)
    stoday = datetime.today()
    h = today.hour
    if h > 12:
        su = "PM"
        h = h - 12
    else:
        su = "AM"
    tstring = f"Today at {h}:{today.minute} {su}"
    d = ImageDraw.Draw(y)
    fntd = ImageFont.truetype("assets/whitney-medium.ttf", 80)
    fntt = ImageFont.truetype("assets/whitney-medium.ttf", 40)
    if len(text) > 1000:
        print("text too long")
    else:
        d.text((190, 35), user, color=(256, 256, 256), font=fntd)
        wi = fntd.getsize(user)
        d.text((200 + wi[0], 70), tstring, color=(114, 118, 125), font=fntt)
        wrap = writetext(y)
        f = wrap.write_text_box(
            190, 70, text, 2120, "assets/whitney-medium.ttf", 60, color=(256, 256, 256)
        )
        print(f)
        bt = wrap.retimg()
        im = Image.open(bt)
        ima = im.crop((0, 0, 2400, (f + 90)))
        top = Image.new("RGBA", ima.size, (54, 57, 63))
        out = Image.alpha_composite(top, ima)
        y = tkc.randomword(10)
        out.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.png"


def getpixel(image):
    t = pilimagereturn(image)
    flist = []
    for frame in ImageSequence.Iterator(t):
        imgSmall = frame.resize((32, 32), resample=Image.BILINEAR)
        fim = imgSmall.resize(frame.size, Image.NEAREST)
        flist.append(fim)
    y = tkc.randomword(10)
    flist[0].save(
        f"bin/{y}.gif",
        format="gif",
        save_all=True,
        append_images=flist,
        optimize=True,
    )
    return f"bin/{y}.gif"


def getdeepfry(image):
    t = pilimagereturn(image)
    flist = []
    for frame in ImageSequence.Iterator(t):
        colours = ((254, 0, 2), (255, 255, 15))
        img = frame.convert("RGB")
        flare_positions = []
        width, height = img.width, img.height
        img = img.resize(
            (int(width ** 0.75), int(height ** 0.75)), resample=Image.LANCZOS
        )
        img = img.resize(
            (int(width ** 0.88), int(height ** 0.88)), resample=Image.BILINEAR
        )
        img = img.resize(
            (int(width ** 0.9), int(height ** 0.9)), resample=Image.BICUBIC
        )
        img = img.resize((width, height), resample=Image.BICUBIC)
        img = ImageOps.posterize(img, 4)
        r = img.split()[0]
        r = ImageEnhance.Contrast(r).enhance(2.0)
        r = ImageEnhance.Brightness(r).enhance(1.5)

        r = ImageOps.colorize(r, colours[0], colours[1])

        # Overlay red and yellow onto main image and sharpen the hell out of it
        img = Image.blend(img, r, 0.75)
        img = ImageEnhance.Sharpness(img).enhance(100.0)
        flist.append(img)
    y = tkc.randomword(10)
    flist[0].save(
        f"bin/{y}.gif",
        format="gif",
        save_all=True,
        append_images=flist,
        optimize=True,
    )
    return f"bin/{y}.gif"


def getinvert(image):
    t = pilimagereturn(image)
    flist = []
    for frame in ImageSequence.Iterator(t):
        frame = frame.convert("RGB")
        blurred_image = ImageOps.invert(frame)
        flist.append(blurred_image)
    y = tkc.randomword(10)
    flist[0].save(
        f"bin/{y}.gif",
        format="gif",
        save_all=True,
        append_images=flist,
        optimize=True,
    )
    return f"bin/{y}.gif"


def getblur(image):
    t = pilimagereturn(image)
    flist = []
    for frame in ImageSequence.Iterator(t):
        frame = frame.convert("RGBA")
        blurred_image = frame.filter(ImageFilter.BLUR)
        flist.append(blurred_image)
    y = tkc.randomword(10)
    flist[0].save(
        f"bin/{y}.gif",
        format="gif",
        save_all=True,
        append_images=flist,
        optimize=True,
    )
    return f"bin/{y}.gif"


def gethitler(image):
    t = pilimagereturn(image)
    im = Image.open("assets/hitler.jpg")
    wthf = t.resize((260, 300), 5)

    width = 800
    height = 600
    fim = im.resize((width, height), 4)
    area = (65, 40)
    fim.paste(wthf, area)
    y = tkc.randomword(10)
    fim.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.png"


# @app.get("/docs", include_in_schema=False)
# async def redoc_html():
#     return get_redoc_html(
#         openapi_url=app.openapi_url,
#         title=app.title + " - Docs",
#         redoc_js_url="/static/redoc.standalone.js",
#     )
#
def rgb_to_hex(rgb):
    return ('#%02x%02x%02x' % rgb).upper()


def top5colors(path):
    im = pilimagereturn(path)
    w, h = im.size
    font = ImageFont.truetype('assets/Helvetica Neu Bold.ttf', size=30)
    print(int(w * (h // 256)))
    im = im.resize((int(w * (256 / h)), 256), 1)
    print(w, h)
    q = im.quantize(colors=5, method=2)
    pal = (q.getpalette())
    back = Image.new('RGBA', (int(w * (256 / h)) + 200, 256), color=(0, 0, 0, 0))
    d = ImageDraw.Draw(back)
    d.rectangle([10, 10, 40, 40], fill=(pal[0], pal[1], pal[2]))
    d.text((50, 10), rgb_to_hex((pal[0], pal[1], pal[2])), font=font)
    d.rectangle([10, 60, 40, 90], fill=(pal[3], pal[4], pal[5]))
    d.text((50, 60), rgb_to_hex((pal[3], pal[4], pal[5])), font=font)
    d.rectangle([10, 110, 40, 140], fill=(pal[6], pal[7], pal[8]))
    d.text((50, 110), rgb_to_hex((pal[6], pal[7], pal[8])), font=font)
    d.rectangle([10, 160, 40, 190], fill=(pal[9], pal[10], pal[11]))
    d.text((50, 160), rgb_to_hex((pal[9], pal[10], pal[11])), font=font)
    d.rectangle([10, 210, 40, 240], fill=(pal[12], pal[13], pal[14]))
    d.text((50, 210), rgb_to_hex((pal[12], pal[13], pal[14])), font=font)
    back.paste(im, (200, 0))
    y = tkc.randomword(10)
    back.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.png"


def getrgbgraph(img):
    def getr(R):
        return '#%02x%02x%02x' % (R, 0, 0)

    def getg(G):
        return '#%02x%02x%02x' % (0, G, 0)

    def getb(B):
        return '#%02x%02x%02x' % (0, 0, B)

    im = pilimagereturn(img)
    im = im.convert('RGB')
    dat = (im.histogram())
    rvals = dat[0:256]
    gvals = dat[256:512]
    plt.figure()
    bvals = dat[512:768]
    axa = plt.subplot(2, 2, 1)
    axa.imshow(bytes_to_np(img))
    axa.set_title('Image')
    axb = plt.subplot(2, 2, 2)
    for i in range(0, 256):
        axb.bar(i, rvals[i], color=getr(i), alpha=0.3)
    axb.set_title('Red Values')
    axb.set_xlabel('Position')
    axb.set_ylabel('Red Intensity')
    axc = plt.subplot(2, 2, 3)
    for i in range(0, 256):
        axc.bar(i, gvals[i], color=getg(i), alpha=0.3)
    axc.set_xlabel('Position')
    axc.set_ylabel('Green Intensity')
    axd = plt.subplot(2, 2, 4)
    for i in range(0, 256):
        axd.bar(i, bvals[i], color=getb(i), alpha=0.3)
    axd.set_xlabel('Position')
    axd.set_ylabel('Blue Intensity')
    plt.tight_layout()
    # plt.show()
    y = tkc.randomword(10)
    plt.savefig(f'bin/{y}.png')
    return f'bin/{y}.png'


def asciiart(in_b, SC=0.1, GCF=2, bgcolor=(13, 2, 8)):
    chars = np.asarray(list(" .'`^\,:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"))
    font = ImageFont.load_default()
    letter_width = font.getsize("x")[0]
    letter_height = font.getsize("x")[1]
    WCF = letter_height / letter_width
    img = pilimagereturn(in_b)
    img = img.convert('RGB')
    widthByLetter = round(img.size[0] * SC * WCF)
    heightByLetter = round(img.size[1] * SC)
    S = (widthByLetter, heightByLetter)
    img = img.resize(S)
    img = np.sum(np.asarray(img), axis=2)
    img -= img.min()
    img = (1.0 - img / img.max()) ** GCF * (chars.size - 1)
    lines = ("\n".join(("".join(r) for r in chars[img.astype(int)]))).split("\n")
    nbins = len(lines)
    newImg_width = letter_width * widthByLetter
    newImg_height = letter_height * heightByLetter
    newImg = Image.new("RGBA", (newImg_width, newImg_height), bgcolor)
    draw = ImageDraw.Draw(newImg)
    leftpadding = 0
    y = 0
    lineIdx = 0
    for line in lines:
        lineIdx += 1
        draw.text((leftpadding, y), line, (0, 255, 65), font=font)
        y += letter_height
    y = tkc.randomword(10)
    newImg.save(f'bin/{y}.png')
    return f'bin/{y}.png'


def tweetgen(username, image, tezt):
    today = datetime.today()
    mlist = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "October",
        "November",
        "December",
    ]
    m = today.month
    mo = mlist[int(m - 1)]

    h = today.hour
    if h > 12:
        su = "PM"
        h = h - 12
    else:
        su = "AM"
    y = str(today.day).strip("0")
    tstring = f"{h}:{today.minute} {su} - {y} {mo} {today.year}"
    print(tstring)
    tweet = Image.open("assets/tweet.png")
    st = username
    lst = st.lower()
    ft = pilimagereturn(image)
    topa = ft.resize((150, 150), 5)
    size = (100, 100)
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((20, 20) + size, fill=255)
    avatar = ImageOps.fit(topa, mask.size, centering=(0.5, 0.5))
    tweet.paste(avatar, mask=mask)
    d = ImageDraw.Draw(tweet)
    fntna = ImageFont.truetype("assets/HelveticaNeue Medium.ttf", 22)
    fnth = ImageFont.truetype("assets/HelveticaNeue Light.ttf", 18)
    fntt = ImageFont.truetype("assets/HelveticaNeue Light.ttf", 18)
    d.multiline_text((110, 35), st, font=fntna, fill=(0, 0, 0, 0))
    d.multiline_text((110, 60), f"@{lst}", font=fnth, fill=(101, 119, 134, 178))
    d.multiline_text((20, 310), tstring, font=fntt, fill=(101, 119, 134, 178))
    margin = 20
    offset = 120
    text = tezt
    print(len(text))
    imgwrap = writetext(tweet)
    imgwrap.write_text_box(
        20, 100, text, 630, "assets/HelveticaNeue Medium.ttf", 26, (0, 0, 0, 0)
    )
    t = imgwrap.retimg()
    y = tkc.randomword(10)
    with open(f"bin/{y}.png", "wb") as out:
        out.write(t.read())
    return f"bin/{y}.png"


def getsatan(image):
    t = pilimagereturn(image)
    im = Image.open("assets/satan.jpg")
    wthf = t.resize((400, 225), 5)
    width = 800
    height = 600
    fim = im.resize((width, height), 4)
    area = (250, 100)
    fim.paste(wthf, area)
    y = tkc.randomword(10)
    fim.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.png"


def getwanted(image):
    av = pilimagereturn(image)
    im = Image.open("assets/wanted.png")
    tp = av.resize((800, 800), 0)
    im.paste(tp, (200, 450))
    y = tkc.randomword(10)
    im.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.png"


def gettriggered(image):
    im = pilimagereturn(image)
    im = im.resize((500, 500), 1)
    overlay = Image.open('assets/triggered.png')
    ml = []
    for i in range(0, 30):
        blank = Image.new('RGBA', (400, 400))
        x = -1 * (random.randint(50, 100))
        y = -1 * (random.randint(50, 100))
        blank.paste(im, (x, y))
        rm = Image.new('RGBA', (400, 400), color=(255, 0, 0, 80))
        blank.paste(rm, mask=rm)
        blank.paste(overlay, mask=overlay)
        ml.append(blank)
    y = tkc.randomword(10)
    ml[0].save(f"bin/{y}.gif", format='gif', save_all=True, duration=1, append_images=ml, loop=0)
    return f"bin/{y}.gif"


def getobama(image):
    im = pilimagereturn(image)
    obam = Image.open('assets/obama.png')
    y = im.resize((300, 300), 1)
    obam.paste(y, (250, 100))
    obam.paste(y, (650, 0))
    y = tkc.randomword(10)
    obam.save(f'bin/{y}.png')
    return f'bin/{y}.png'


def getsithorld(image):
    ft = pilimagereturn(image)
    im = Image.open("assets/sithlord.jpg")

    topa = ft.resize((250, 275), 5)
    size = (225, 225)
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((50, 10) + size, fill=255)
    topt = ImageOps.fit(topa, mask.size, centering=(0.5, 0.5))
    im.paste(topt, (225, 180), mask=mask)
    y = tkc.randomword(10)
    im.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.png"


def get5g1g(img1, img2):
    im = pilimagereturn(img1)
    im2 = pilimagereturn(img2)
    back = Image.open('assets/5g1g.png')
    im = im.resize((150, 150), 1)
    back.paste(im, (80, 100))
    back.paste(im, (320, 10))
    back.paste(im, (575, 60))
    back.paste(im, (830, 60))
    back.paste(im, (1050, 0))
    im2 = im2.resize((150, 150), 1)
    back.paste(im2, (650, 320))
    y = tkc.randomword(10)
    back.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.png"


def getwhyareyougay(img1, img2):
    gay = pilimagereturn(img1)
    av = pilimagereturn(img2)
    im = Image.open('assets/whyareyougay.png')
    mp = av.resize((150, 150), 0)
    op = gay.resize((150, 150), 0)
    im.paste(op, (550, 100))
    im.paste(mp, (100, 125))
    y = tkc.randomword(10)
    im.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.png"


def gettrash(image):
    t = pilimagereturn(image)
    im = Image.open("assets/trash.jpg")
    wthf = t.resize((200, 150), 5)
    width = 800
    height = 600
    fim = im.resize((width, height), 4)
    area = (500, 250)
    fim.paste(wthf, area)
    y = tkc.randomword(10)
    fim.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.png"


def getthoughtimg(image, text):
    ft = pilimagereturn(image)
    im = Image.open("assets/speech.jpg")

    file = str(text)
    if len(file) > 200:
        return f"Your text is too long {len(file)} is greater than 200"
    else:
        if len(file) > 151:
            fo = file[:50] + "\n" + file[50:]
            ft = fo[:100] + "\n" + fo[100:]
            ff = ft[:150] + "\n" + ft[150:]
            size = 10
        elif len(file) > 101:
            fo = file[:50] + "\n" + file[50:]
            ff = fo[:100] + "\n" + fo[100:]
            size = 12
        elif 51 < len(file) < 100:
            ff = file[:50] + "\n" + file[50:]
            size = 14
        elif 20 < len(file) <= 50:
            ff = file
            size = 18
        else:
            ff = file
            size = 25
        wthf = ft.resize((200, 225), 5)

        width = 800
        height = 600
        fim = im.resize((width, height), 4)
        area = (125, 50)
        fim.paste(wthf, area)
        base = fim.convert("RGBA")
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        fnt = ImageFont.truetype("Helvetica-Bold-Font.ttf", size)
        d = ImageDraw.Draw(txt)
        d.text((400, 150), f"{ff}", font=fnt, fill=(0, 0, 0, 255))
        out = Image.alpha_composite(base, txt)
        y = tkc.randomword(10)
        out.save(f"bin/{y}.png", format="PNG", optimize=True)
        return f"bin/{y}.png"


def badimg(image):
    im = pilimagereturn(image)
    back = Image.open("assets/bad.png")
    t = im.resize((200, 200), 5)
    back.paste(t, (20, 150))
    y = tkc.randomword(10)
    back.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.png"


def getangel(image):
    t = pilimagereturn(image)
    im = Image.open("assets/angel.jpg")
    wthf = t.resize((300, 175), 5)
    width = 800
    height = 600
    fim = im.resize((width, height), 4)
    area = (250, 130)
    fim.paste(wthf, area)
    y = tkc.randomword(10)
    fim.save(f"bin/{y}.png", format="PNG", optimize=True)
    return f"bin/{y}.png"


class Meme:
    def __init__(self, text):
        self.draw = None
        self.image = None
        self.meme_path = None
        self.tmp_path = None
        self.text = text
        self.filetype = "png"
        self.font_path = "assets/impact.ttf"

    def store_image(self):
        y = tkc.randomword(10)
        self.image.save(f"bin/{y}.png", format="PNG", optimize=True)
        return f"bin/{y}.png"

    def get_image(self, image):
        self.image = Image.open(BytesIO(image)).convert("RGB")
        return True

    def find_longest_line(self, text):
        longest_width = 0
        longest_line = ""
        for line in text:
            width = self.draw.textsize(
                line, font=ImageFont.truetype(self.font_path, 20)
            )[0]
            if width > longest_width:
                longest_width = width
                longest_line = line

        return longest_line

    def get_font_measures(self, text, font_size, ratio):
        measures = {"font": ImageFont.truetype(self.font_path, size=font_size)}
        measures["width"] = self.draw.textsize(text, font=measures["font"])[0]
        measures["ratio"] = measures["width"] / float(self.image.width)
        measures["ratio_diff"] = abs(ratio - measures["ratio"])

        return measures

    def optimize_font(self, text):
        """Fuckin' magnets how do they work"""
        font_min_size = 12
        font_max_size = 70
        font_size_range = range(font_min_size, font_max_size + 1)

        longest_text_line = self.find_longest_line(text)

        # set min/max ratio of font width to image width
        min_ratio = 0.7
        max_ratio = 0.9
        perfect_ratio = min_ratio + (max_ratio - min_ratio) / 2
        ratio = 0

        font = 0
        while (ratio < min_ratio or ratio > max_ratio) and len(font_size_range) > 2:
            measures = {
                "top": self.get_font_measures(
                    text=longest_text_line,
                    font_size=font_size_range[-1],
                    ratio=perfect_ratio,
                ),
                "low": self.get_font_measures(
                    text=longest_text_line,
                    font_size=font_size_range[0],
                    ratio=perfect_ratio,
                ),
            }

            half_index = len(font_size_range) // 2
            if measures["top"]["ratio_diff"] < measures["low"]["ratio_diff"]:
                closer = "top"
                font_size_range = font_size_range[int(half_index): -1]
            else:
                closer = "low"
                font_size_range = font_size_range[0:half_index]

            ratio = measures[closer]["ratio"]
            # witdh = measures[closer]["width"]
            font = measures[closer]["font"]

        width = self.draw.textsize(longest_text_line, font=font)[0]

        return font, width

    @staticmethod
    def set_text_wrapping(text_length):
        wrapping = 0
        if text_length <= 32:
            wrapping = 32
        elif text_length > 100:
            wrapping = 10 + text_length // 3
        elif text_length > 32:
            wrapping = 5 + text_length // 2
        return int(wrapping)

    def prepare_text(self, text):
        if not text:
            return "", 0
        if type(text) == list:
            text = text[0]
        wrapping = self.set_text_wrapping(len(text))
        text = text.strip().upper()
        text = textwrap.wrap(text, wrapping)
        font, text_width = self.optimize_font(text)

        text = "\n".join(text)

        return text, text_width, font

    def draw_text(self, xy, text, font):
        x = xy[0]
        y = xy[1]

        o = 1

        xys = (
            (x + o, y),
            (x - o, y),
            (x + o, y + o),
            (x - o, y - o),
            (x - o, y + o),
            (x, y - o),
            (x, y + o),
        )

        for xy in xys:
            self.draw.multiline_text(xy, text, fill="black", font=font, align="center")

        self.draw.multiline_text((x, y), text, fill="white", font=font, align="center")

    def draw_meme(self):
        self.draw = ImageDraw.Draw(self.image)

        margin_xy = (0, self.image.height / 18)

        text_top = self.text.split("|")[0]
        if text_top:
            text_top, text_top_width, top_font = self.prepare_text(text_top)
            top_xy = (((self.image.width - text_top_width) / 2), (margin_xy[1]))
            self.draw_text(top_xy, text_top, top_font)

        text_bottom = self.text.split("|")[1:]
        if text_bottom:
            text_bottom, text_bottom_width, bottom_font = self.prepare_text(text_bottom)
            bottom_xy = [
                ((self.image.width - text_bottom_width) / 2),
                (
                        self.image.height
                        - bottom_font.getsize(text_bottom)[1] * len(text_bottom.split("\n"))
                        - margin_xy[1]
                ),
            ]
            self.draw_text(bottom_xy, text_bottom, bottom_font)

    def make_meme(self, path):

        ret = self.get_image(path)
        if ret:
            self.draw_meme()
            im = self.store_image()
            return im
        else:
            return False
