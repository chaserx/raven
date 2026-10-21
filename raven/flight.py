import math

SCREEN_W = 160
SPRITE_W = 32

CROSS_MS = 3000   # time to fly from one edge of the screen to the other
AWAY_MS = 4000    # time the raven spends off screen before it returns
TOTAL_MS = CROSS_MS + AWAY_MS + CROSS_MS

# flap cycle: wings up, mid, level, down, then back up through level and mid
FLAP_FRAMES = (0, 1, 2, 3, 2, 1)
FLAP_MS = 90


def flight(elapsed):
    # work out where the raven is, which way it faces, and which flap frame to
    # show, given the milliseconds since the button was pressed. returns None
    # once the round trip is over or while the raven is out of sight.
    if elapsed < 0 or elapsed >= TOTAL_MS:
        return None

    frame = FLAP_FRAMES[(elapsed // FLAP_MS) % len(FLAP_FRAMES)]

    if elapsed < CROSS_MS:
        # out: enter from the left edge, fly off the right edge
        progress = elapsed / CROSS_MS
        x = -SPRITE_W + (SCREEN_W + SPRITE_W) * progress
        y = 40 + 5 * math.sin(elapsed / 200)
        return x, y, False, frame

    if elapsed < CROSS_MS + AWAY_MS:
        return None

    # back: return from the right edge, fly off the left edge
    t = elapsed - CROSS_MS - AWAY_MS
    progress = t / CROSS_MS
    x = SCREEN_W - (SCREEN_W + SPRITE_W) * progress
    y = 30 + 5 * math.sin(t / 200)
    return x, y, True, frame
