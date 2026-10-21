"""Generate the raven app's pixel art. Standard library only.

Run from the repo root:  python3 tools/make_assets.py
"""
import math
import os
import struct
import zlib

OUT = os.path.join(os.path.dirname(__file__), "..", "raven")

CLEAR = (0, 0, 0, 0)


def write_png(path, pixels):
    h, w = len(pixels), len(pixels[0])
    raw = b"".join(b"\x00" + b"".join(bytes(p) for p in row) for row in pixels)

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def canvas(w, h, fill=CLEAR):
    return [[fill] * w for _ in range(h)]


def in_polygon(x, y, pts):
    inside = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def fill_shape(img, test, color):
    for y, row in enumerate(img):
        for x in range(len(row)):
            if test(x + 0.5, y + 0.5):
                row[x] = color


def ellipse(cx, cy, rx, ry):
    return lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def polygon(*pts):
    return lambda x, y: in_polygon(x, y, pts)


# ---------------------------------------------------------------- raven

BODY = (16, 17, 28, 255)
WING = (38, 42, 74, 255)
RIM = (96, 106, 168, 255)
EYE = (240, 220, 140, 255)

RAVEN_W, RAVEN_H = 32, 24

# wing tip for each flap frame: up, mid, level, down
WING_TIPS = ((7, 1), (4, 6), (2, 13), (7, 22))


def raven_frame(wing_tip):
    img = canvas(RAVEN_W, RAVEN_H)
    fill_shape(img, polygon((9, 12), (2, 12), (2, 18), (9, 15)), BODY)    # tail
    fill_shape(img, ellipse(15, 13, 7.5, 4), BODY)                         # body
    fill_shape(img, ellipse(23, 10, 3.6, 3.4), BODY)                       # head
    fill_shape(img, polygon((26, 8.5), (31.5, 11), (26, 12.5)), BODY)      # beak
    tx, ty = wing_tip
    fill_shape(img, polygon((11, 11), (21, 11), (tx, ty)), WING)           # wing
    img[9][24] = EYE

    # a lighter rim on every edge pixel so the black bird reads against a dark sky
    rimmed = [row[:] for row in img]
    for y in range(RAVEN_H):
        for x in range(RAVEN_W):
            if img[y][x] == CLEAR:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < RAVEN_W and 0 <= ny < RAVEN_H) or img[ny][nx] == CLEAR:
                    rimmed[y][x] = RIM if img[y][x] != EYE else EYE
                    break
    return rimmed


def make_sprites():
    frames = [raven_frame(tip) for tip in WING_TIPS]
    flipped = [[row[::-1] for row in frame] for frame in frames]
    sheet = canvas(RAVEN_W * len(frames), RAVEN_H * 2)
    for i, (right, left) in enumerate(zip(frames, flipped)):
        for y in range(RAVEN_H):
            for x in range(RAVEN_W):
                sheet[y][i * RAVEN_W + x] = right[y][x]
                sheet[RAVEN_H + y][i * RAVEN_W + x] = left[y][x]
    write_png(os.path.join(OUT, "assets", "raven.png"), sheet)


# ----------------------------------------------------------- background

W, H = 160, 120
SKY_TOP = (6, 8, 28, 255)
SKY_LOW = (20, 26, 62, 255)
STARS = ((12, 14), (40, 8), (70, 20), (104, 10), (22, 44), (146, 54),
         (58, 36), (90, 48), (138, 12), (6, 62), (82, 6), (116, 56))
MOON = (124, 28)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(4))


def make_background():
    img = canvas(W, H)
    for y in range(H):
        for x in range(W):
            img[y][x] = lerp(SKY_TOP, SKY_LOW, y / H)

    for x, y in STARS:
        img[y][x] = (255, 255, 255, 255)

    mx, my = MOON
    glow = ellipse(mx, my, 20, 20)
    for y in range(H):
        for x in range(W):
            if glow(x + 0.5, y + 0.5) and img[y][x][2] < 140:
                img[y][x] = lerp(img[y][x], (60, 70, 120, 255), 0.45)
    fill_shape(img, ellipse(mx, my, 14, 14), (244, 239, 208, 255))
    fill_shape(img, ellipse(mx - 5, my - 4, 3, 3), (220, 213, 172, 255))
    fill_shape(img, ellipse(mx + 5, my + 6, 2, 2), (220, 213, 172, 255))
    fill_shape(img, ellipse(mx + 2, my - 8, 1.5, 1.5), (220, 213, 172, 255))

    ink = (4, 5, 14, 255)

    def rect(x0, y0, x1, y1, color=ink):
        for y in range(y0, y1):
            for x in range(x0, x1):
                img[y][x] = color

    rect(0, 100, W, H)                                       # ground
    rect(8, 80, 22, 104); rect(6, 76, 24, 81)                # left tower
    for x in range(6, 24, 4):
        rect(x, 73, x + 2, 76)                               # battlements
    rect(30, 88, 40, 104)                                    # wall
    rect(44, 88, 60, 104)                                    # keep
    fill_shape(img, polygon((44, 88), (52, 70), (60, 88)), ink)   # spire
    rect(66, 84, 78, 104)                                    # gatehouse
    rect(82, 94, 96, 104)                                    # low wall
    rect(100, 86, 112, 104); rect(98, 82, 114, 87)           # tower
    rect(120, 76, 136, 104); rect(118, 72, 138, 77)          # great tower
    for x in range(118, 138, 4):
        rect(x, 69, x + 2, 72)
    rect(144, 90, 156, 104)

    lit = (242, 193, 78, 255)
    for x, y in ((13, 88), (50, 94), (126, 84), (70, 92), (104, 92), (130, 90), (150, 96)):
        rect(x, y, x + 2, y + 3, lit)

    write_png(os.path.join(OUT, "assets", "background.png"), img)


# ----------------------------------------------------------------- icon

def make_icon():
    img = canvas(24, 24)
    fill_shape(img, ellipse(12, 12, 11, 11), (244, 239, 208, 255))
    fill_shape(img, ellipse(8, 9, 2, 2), (220, 213, 172, 255))
    fill_shape(img, ellipse(16, 16, 2.5, 2.5), (220, 213, 172, 255))
    ink = (10, 11, 22, 255)
    fill_shape(img, polygon((3, 13), (8, 13), (8, 16), (3, 17)), ink)       # tail
    fill_shape(img, ellipse(12, 14, 5, 3), ink)                              # body
    fill_shape(img, ellipse(17, 11.5, 2.6, 2.4), ink)                        # head
    fill_shape(img, polygon((19, 10.5), (23, 12), (19, 13.5)), ink)          # beak
    fill_shape(img, polygon((8, 13), (15, 13), (6, 5)), ink)                 # wing
    write_png(os.path.join(OUT, "icon.png"), img)


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    make_sprites()
    make_background()
    make_icon()
    print("wrote assets to", os.path.abspath(OUT))
