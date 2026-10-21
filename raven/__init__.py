import sys
import os

sys.path.insert(0, "/system/apps/raven")
os.chdir("/system/apps/raven")

from flight import flight, TOTAL_MS

background = image.load("assets/background.png")
sprites = SpriteSheet("assets/raven.png", 4, 2)
facing_right = sprites.animation(0, 0, 4)
facing_left = sprites.animation(0, 1, 4)

# a few extra stars that blink so the sky isn't completely still
TWINKLES = ((30, 24), (96, 32), (148, 78), (64, 60))

sent_at = None


def update():
    global sent_at

    # press A to send a raven. ignore the button while one is already on its way
    if badge.pressed(BUTTON_A) and sent_at is None:
        sent_at = badge.ticks

    screen.blit(background, vec2(0, 0))
    draw_twinkles()

    if sent_at is not None:
        elapsed = badge.ticks - sent_at

        pos = flight(elapsed)
        if pos:
            x, y, flipped, frame = pos
            sprite = (facing_left if flipped else facing_right).frame(frame)
            screen.blit(sprite, vec2(int(x), int(y)))

        # the round trip is over, so the next press can send another raven
        if elapsed >= TOTAL_MS:
            sent_at = None


def draw_twinkles():
    screen.pen = color.rgb(255, 255, 255)
    for i, (x, y) in enumerate(TWINKLES):
        if int(badge.ticks / 700 + i * 1.7) % 3:
            screen.shape(shape.rectangle(x, y, 1, 1))


run(update)
