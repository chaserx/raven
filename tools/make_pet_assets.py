"""Generate the raven_pet app's art and QR codes.

Needs segno (see tools/requirements.txt). From the repo root:
    .venv/bin/python tools/make_pet_assets.py
"""
import os
import shutil
import sys

import segno

sys.path.insert(0, os.path.dirname(__file__))
from make_assets import (BODY, CLEAR, EYE, RIM, WING, canvas, ellipse,
                         fill_shape, polygon, write_png)

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "raven_pet")

QR_URL = "https://engineeringmaester.com/next"

TEAR = (110, 170, 255, 255)
BERRY = (210, 50, 60, 255)

UNITS = 32          # the raven is drawn on a 32x32 grid...
FRAME = 48          # ...and rendered 1.5x bigger into 48x48 frames
POSES = ("idle", "idle_bob", "sad", "eat", "train")


def scaled(test, k):
    return lambda x, y: test(x / k, y / k)


def dot(img, x, y, color, k, size=2):
    for dy in range(size):
        for dx in range(size):
            px, py = int(x * k) + dx, int(y * k) + dy
            if 0 <= py < len(img) and 0 <= px < len(img[0]):
                img[py][px] = color


def rim(img):
    h, w = len(img), len(img[0])
    out = [row[:] for row in img]
    for y in range(h):
        for x in range(w):
            if img[y][x] == CLEAR:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < w and 0 <= ny < h) or img[ny][nx] == CLEAR:
                    out[y][x] = RIM
                    break
    return out


def pet_frame(pose, k=FRAME / UNITS):
    size = int(UNITS * k)
    img = canvas(size, size)

    def draw(test, color):
        fill_shape(img, scaled(test, k), color)

    draw(polygon((12, 20), (6, 31), (15, 29)), BODY)                     # tail
    draw(polygon((13.2, 26), (14.6, 26), (14.6, 31.5), (13.2, 31.5)), BODY)   # legs
    draw(polygon((17.4, 26), (18.8, 26), (18.8, 31.5), (17.4, 31.5)), BODY)

    if pose == "sad":
        draw(ellipse(16, 21, 6.5, 8), BODY)
        draw(ellipse(14, 22, 4, 6), WING)
        draw(ellipse(18, 14, 4, 4), BODY)                                # head, drooped
        draw(polygon((20.5, 13), (25.5, 19), (21.5, 17.5)), BODY)        # beak points down
    elif pose == "eat":
        draw(ellipse(15, 19, 6.5, 8), BODY)
        draw(ellipse(13, 20, 4, 6), WING)
        draw(ellipse(20, 19, 4, 4), BODY)                                # head, pecking
        draw(polygon((22, 20), (27.5, 27), (22.5, 24.5)), BODY)
    else:
        dy = 1.2 if pose == "idle_bob" else 0
        draw(ellipse(16, 19, 6.5, 8.5), BODY)
        draw(ellipse(18, 9 + dy, 4, 4), BODY)
        draw(polygon((21, 7.5 + dy), (28, 10 + dy), (21, 11.5 + dy)), BODY)
        if pose == "train":
            draw(polygon((11, 17), (21, 17), (6, 1)), WING)              # wing flung up
        else:
            draw(ellipse(14, 20, 4, 6.5), WING)                          # wing folded

    img = rim(img)

    if pose == "sad":
        dot(img, 19.2, 13, RIM, k, 2)                                    # closed eye
        dot(img, 20, 16, TEAR, k, 1)
        dot(img, 20, 18, TEAR, k, 1)
    elif pose == "eat":
        dot(img, 21, 18.5, EYE, k, 2)
        fill_shape(img, scaled(ellipse(27.5, 29.5, 2, 2), k), BERRY)
    else:
        dy = 1.2 if pose == "idle_bob" else 0
        dot(img, 19.2, 8 + dy, EYE, k, 2)
    return img


def make_sheet():
    frames = [pet_frame(p) for p in POSES]
    sheet = canvas(FRAME * len(frames), FRAME)
    for i, frame in enumerate(frames):
        for y in range(FRAME):
            for x in range(FRAME):
                sheet[y][i * FRAME + x] = frame[y][x]
    write_png(os.path.join(OUT, "assets", "raven_pet.png"), sheet)
    return frames


def paste(dst, src, ox, oy):
    for y, row in enumerate(src):
        for x, px in enumerate(row):
            if px[3] and 0 <= oy + y < len(dst) and 0 <= ox + x < len(dst[0]):
                dst[oy + y][ox + x] = px


def make_icon():
    img = canvas(24, 24)
    fill_shape(img, ellipse(12, 12, 12, 12), (14, 18, 48, 255))
    fill_shape(img, ellipse(17, 7, 3.5, 3.5), (244, 239, 208, 255))
    paste(img, pet_frame("idle", k=0.75), 0, 1)
    write_png(os.path.join(OUT, "icon.png"), img)


def make_qr_code():
    quiet = 2  # modules of white around the code; phones cope with this fine
    qr = segno.make(QR_URL, error="l", micro=False, boost_error=False)
    matrix = [list(row) for row in qr.matrix]
    n = len(matrix)
    scale = 116 // (n + 2 * quiet)
    assert scale >= 3, f"QR_URL needs a QR too big to scan ({n} modules)"
    side = (n + 2 * quiet) * scale
    white, black = (255, 255, 255, 255), (0, 0, 0, 255)
    img = canvas(side, side, white)
    for my in range(n):
        for mx in range(n):
            if matrix[my][mx]:
                for sy in range(scale):
                    for sx in range(scale):
                        img[(my + quiet) * scale + sy][(mx + quiet) * scale + sx] = black
    write_png(os.path.join(OUT, "assets", "qr.png"), img)
    print(f"qr: {n}x{n} modules at {scale}px -> {side}px  {QR_URL!r}")


def make_preview(frames):
    # not shipped: the scene with the raven in a few poses, enlarged 3x
    import zlib  # noqa: F401  (write_png handles compression)
    bg = os.path.join(OUT, "assets", "background.png")
    scene = read_png_rgba(bg)
    panels = []
    for idx in (0, 2, 3, 4):
        panel = [row[:] for row in scene]
        paste(panel, frames[idx], 56, 52)
        panels.append(panel)
    strip = [sum((p[y] for p in panels), []) for y in range(120)]
    big = [[px for px in row for _ in range(3)] for row in strip for _ in range(3)]
    os.makedirs(os.path.join(ROOT, ".preview"), exist_ok=True)
    write_png(os.path.join(ROOT, ".preview", "pets.png"), big)


def read_png_rgba(path):
    import struct
    import zlib
    data = open(path, "rb").read()
    pos, idat, w, h = 8, b"", 0, 0
    while pos < len(data):
        length, tag = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        if tag == b"IHDR":
            w, h = struct.unpack(">II", body[:8])
        elif tag == b"IDAT":
            idat += body
        pos += 12 + length
    raw = zlib.decompress(idat)
    stride = w * 4 + 1
    return [[tuple(raw[y * stride + 1 + x * 4: y * stride + 5 + x * 4]) for x in range(w)]
            for y in range(h)]


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    # the scene is shared with the first app, so it stays in one place
    shutil.copy(os.path.join(ROOT, "raven", "assets", "background.png"),
                os.path.join(OUT, "assets", "background.png"))
    frames = make_sheet()
    make_icon()
    make_qr_code()
    make_preview(frames)
    print("wrote assets to", os.path.abspath(OUT))
