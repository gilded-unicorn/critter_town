"""Draw 32x32 pixel-art sprite sheets for Soot (crow), Seed (pigeon) and Fluffy (opossum).

Sheet layout matches AI Town's f1 spritesheet: 3 columns (stand, step A, step B),
rows: 0 = down (facing viewer), 1 = left, 2 = right, 3 = up (facing away).
"""
import sys
from PIL import Image, ImageDraw, ImageOps

S = 32
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
OUTLINE = (20, 20, 24, 255)


def canvas():
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def px(d, pts, c):
    for p in pts:
        d.point(p, fill=c)


def outline(im, color=OUTLINE):
    a = im.split()[3]
    w, h = im.size
    src = a.load()
    out = im.copy()
    o = out.load()
    for y in range(h):
        for x in range(w):
            if src[x, y] >= 100:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and src[nx, ny] >= 100:
                    o[x, y] = color
                    break
    return out


def shadow(d, cx, y, rx):
    d.ellipse((cx - rx, y - 1, cx + rx, y + 1), fill=(0, 0, 0, 70))


def legs(d, xs, top, bottom, c, step, side):
    """Two legs; step 0 = standing, 1/2 = alternate strides."""
    for i, x in enumerate(xs):
        dx = 0
        lift = 0
        if step:
            if side:
                dx = (1 if (i == 0) == (step == 1) else -1)
            else:
                lift = 1 if (i == 0) == (step == 1) else 0
        d.line((x, top, x + dx, bottom - lift), fill=c)
        d.point((x + dx + (1 if side else 0), bottom - lift), fill=c)


# ---------------------------------------------------------------- crow
CROW = dict(body=(28, 35, 42, 255), wing=(44, 58, 70, 255), hi=(70, 92, 110, 255),
            beak=(80, 80, 84, 255), leg=(60, 60, 60, 255), eye=(255, 255, 255, 255), pup=(10, 10, 10, 255))


def crow(view, step):
    im, d = canvas()
    c = CROW
    bob = 1 if step else 0
    if view == "side":
        shadow(d, 15, 29, 7)
        legs(d, (14, 17), 24, 28, c["leg"], step, True)
        d.polygon([(10, 17 - bob), (2, 20 - bob), (3, 23 - bob), (11, 22 - bob)], fill=c["body"])  # tail
        d.ellipse((7, 13 - bob, 22, 25 - bob), fill=c["body"])
        d.ellipse((10, 15 - bob, 19, 21 - bob), fill=c["wing"])
        d.line((11, 16 - bob, 17, 16 - bob), fill=c["hi"])
        d.ellipse((17, 7 - bob, 26, 16 - bob), fill=c["body"])
        d.polygon([(25, 10 - bob), (30, 12 - bob), (25, 14 - bob)], fill=c["beak"])
        px(d, [(22, 10 - bob)], c["eye"])
        px(d, [(23, 10 - bob)], c["pup"])
        px(d, [(20, 8 - bob), (21, 8 - bob)], c["hi"])
    elif view == "down":
        shadow(d, 16, 29, 7)
        legs(d, (13, 18), 24, 28, c["leg"], step, False)
        d.ellipse((9, 12 - bob, 22, 26 - bob), fill=c["body"])
        d.ellipse((8, 15 - bob, 12, 23 - bob), fill=c["wing"])
        d.ellipse((19, 15 - bob, 23, 23 - bob), fill=c["wing"])
        d.ellipse((10, 5 - bob, 21, 15 - bob), fill=c["body"])
        px(d, [(13, 9 - bob), (18, 9 - bob)], c["eye"])
        px(d, [(13, 10 - bob), (18, 10 - bob)], c["pup"])
        d.polygon([(14, 11 - bob), (17, 11 - bob), (15, 15 - bob)], fill=c["beak"])
        px(d, [(13, 6 - bob), (14, 6 - bob)], c["hi"])
    else:  # up
        shadow(d, 16, 29, 7)
        legs(d, (13, 18), 24, 28, c["leg"], step, False)
        d.polygon([(13, 22 - bob), (19, 22 - bob), (20, 28 - bob), (12, 28 - bob)], fill=c["body"])  # tail
        d.ellipse((9, 12 - bob, 22, 25 - bob), fill=c["body"])
        d.ellipse((10, 13 - bob, 15, 23 - bob), fill=c["wing"])
        d.ellipse((16, 13 - bob, 21, 23 - bob), fill=c["wing"])
        d.ellipse((10, 5 - bob, 21, 15 - bob), fill=c["body"])
        d.line((12, 7 - bob, 15, 6 - bob), fill=c["hi"])
    return outline(im)


# ---------------------------------------------------------------- pigeon
PIG = dict(body=(160, 167, 176, 255), wing=(118, 125, 136, 255), bar=(52, 56, 64, 255),
           neck=(79, 138, 120, 255), neck2=(122, 90, 140, 255), head=(150, 157, 167, 255),
           beak=(90, 74, 68, 255), cere=(240, 240, 240, 255), eye=(255, 140, 42, 255),
           pup=(10, 10, 10, 255), leg=(217, 114, 127, 255), tail=(70, 74, 84, 255))


def pigeon(view, step):
    im, d = canvas()
    c = PIG
    bob = 1 if step else 0
    if view == "side":
        shadow(d, 15, 29, 7)
        legs(d, (14, 17), 24, 28, c["leg"], step, True)
        d.polygon([(9, 18 - bob), (3, 20 - bob), (4, 23 - bob), (10, 22 - bob)], fill=c["tail"])
        d.ellipse((6, 13 - bob, 23, 26 - bob), fill=c["body"])
        d.ellipse((9, 15 - bob, 19, 22 - bob), fill=c["wing"])
        d.line((11, 18 - bob, 16, 18 - bob), fill=c["bar"])
        d.line((11, 20 - bob, 16, 20 - bob), fill=c["bar"])
        d.ellipse((17, 11 - bob, 24, 18 - bob), fill=c["neck"])
        px(d, [(18, 15 - bob), (19, 16 - bob), (20, 16 - bob)], c["neck2"])
        d.ellipse((18, 6 - bob, 25, 13 - bob), fill=c["head"])
        d.polygon([(25, 9 - bob), (28, 10 - bob), (25, 11 - bob)], fill=c["beak"])
        px(d, [(25, 9 - bob)], c["cere"])
        px(d, [(22, 9 - bob)], c["eye"])
        px(d, [(23, 9 - bob)], c["pup"])
    elif view == "down":
        shadow(d, 16, 29, 7)
        legs(d, (13, 18), 24, 28, c["leg"], step, False)
        d.ellipse((8, 13 - bob, 23, 26 - bob), fill=c["body"])
        d.ellipse((7, 15 - bob, 11, 23 - bob), fill=c["wing"])
        d.ellipse((20, 15 - bob, 24, 23 - bob), fill=c["wing"])
        d.ellipse((11, 10 - bob, 20, 17 - bob), fill=c["neck"])
        px(d, [(12, 15 - bob), (19, 15 - bob), (13, 16 - bob), (18, 16 - bob)], c["neck2"])
        d.ellipse((11, 4 - bob, 20, 12 - bob), fill=c["head"])
        px(d, [(13, 7 - bob), (18, 7 - bob)], c["eye"])
        px(d, [(13, 8 - bob), (18, 8 - bob)], c["pup"])
        d.polygon([(15, 9 - bob), (16, 9 - bob), (16, 12 - bob), (15, 12 - bob)], fill=c["beak"])
        px(d, [(15, 9 - bob), (16, 9 - bob)], c["cere"])
    else:
        shadow(d, 16, 29, 7)
        legs(d, (13, 18), 24, 28, c["leg"], step, False)
        d.polygon([(13, 22 - bob), (19, 22 - bob), (20, 28 - bob), (12, 28 - bob)], fill=c["tail"])
        d.ellipse((8, 12 - bob, 23, 25 - bob), fill=c["body"])
        d.ellipse((9, 13 - bob, 15, 23 - bob), fill=c["wing"])
        d.ellipse((16, 13 - bob, 22, 23 - bob), fill=c["wing"])
        for y in (17, 20):
            d.line((10, y - bob, 14, y - bob), fill=c["bar"])
            d.line((17, y - bob, 21, y - bob), fill=c["bar"])
        d.ellipse((11, 9 - bob, 20, 16 - bob), fill=c["neck"])
        d.ellipse((11, 4 - bob, 20, 12 - bob), fill=c["head"])
    return outline(im)


# ---------------------------------------------------------------- opossum
OPO = dict(fur=(196, 192, 188, 255), dark=(150, 146, 144, 255), face=(246, 242, 236, 255),
           nose=(240, 150, 168, 255), ear=(40, 40, 44, 255), eye=(15, 15, 15, 255),
           leg=(55, 55, 60, 255), tail=(236, 160, 176, 255))


def opossum(view, step):
    im, d = canvas()
    c = OPO
    bob = 1 if step else 0
    if view == "side":
        shadow(d, 15, 29, 9)
        # four short legs, front & back pairs alternate
        for i, x in enumerate((8, 11, 18, 21)):
            lift = 1 if step and ((i % 2 == 0) == (step == 1)) else 0
            d.line((x, 25, x, 28 - lift), fill=c["leg"])
        d.line((6, 21 - bob, 3, 20 - bob), fill=c["tail"])
        d.line((3, 20 - bob, 1, 17 - bob), fill=c["tail"])
        d.line((1, 17 - bob, 2, 14 - bob), fill=c["tail"])
        d.ellipse((5, 15 - bob, 23, 27 - bob), fill=c["fur"])
        d.ellipse((7, 16 - bob, 19, 20 - bob), fill=c["dark"])
        d.ellipse((18, 13 - bob, 27, 22 - bob), fill=c["face"])
        d.polygon([(25, 15 - bob), (30, 18 - bob), (25, 20 - bob)], fill=c["face"])
        d.rectangle((29, 17 - bob, 30, 18 - bob), fill=c["nose"])
        d.ellipse((19, 10 - bob, 22, 14 - bob), fill=c["ear"])
        px(d, [(23, 16 - bob)], c["eye"])
    elif view == "down":
        shadow(d, 16, 29, 8)
        legs(d, (12, 19), 25, 28, c["leg"], step, False)
        d.ellipse((8, 15 - bob, 23, 27 - bob), fill=c["fur"])
        d.ellipse((8, 6 - bob, 13, 11 - bob), fill=c["ear"])
        d.ellipse((18, 6 - bob, 23, 11 - bob), fill=c["ear"])
        d.ellipse((10, 8 - bob, 21, 19 - bob), fill=c["face"])
        d.polygon([(13, 17 - bob), (18, 17 - bob), (16, 22 - bob), (15, 22 - bob)], fill=c["face"])
        d.rectangle((15, 21 - bob, 16, 22 - bob), fill=c["nose"])
        px(d, [(13, 13 - bob), (18, 13 - bob)], c["eye"])
        px(d, [(15, 10 - bob), (16, 10 - bob)], c["dark"])
    else:
        shadow(d, 16, 29, 8)
        legs(d, (12, 19), 25, 28, c["leg"], step, False)
        d.line((16, 26 - bob, 16, 30), fill=c["tail"])
        d.line((16, 30, 19, 31), fill=c["tail"])
        d.ellipse((8, 13 - bob, 23, 27 - bob), fill=c["fur"])
        d.ellipse((10, 14 - bob, 21, 22 - bob), fill=c["dark"])
        d.ellipse((8, 5 - bob, 13, 10 - bob), fill=c["ear"])
        d.ellipse((18, 5 - bob, 23, 10 - bob), fill=c["ear"])
        d.ellipse((10, 7 - bob, 21, 17 - bob), fill=c["fur"])
    return outline(im)


def sheet(fn):
    sh = Image.new("RGBA", (S * 3, S * 4), (0, 0, 0, 0))
    for col in range(3):
        side = fn("side", col)
        sh.paste(fn("down", col), (col * S, 0))
        sh.paste(ImageOps.mirror(side), (col * S, S))  # left
        sh.paste(side, (col * S, 2 * S))               # right
        sh.paste(fn("up", col), (col * S, 3 * S))
    return sh


for name, fn in (("soot", crow), ("seed", pigeon), ("fluffy", opossum)):
    sheet(fn).save(f"{OUT}/{name}.png")
print("ok")
