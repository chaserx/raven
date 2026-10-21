# Raven app

The first app. A raven flies across a night sky and castle skyline when you press **A**, leaves the screen, and comes back from the same edge a few seconds later.

Folder: [`raven/`](../raven/). Menu name: **Raven**.

## Behaviour

| Time since press | What you see |
| --- | --- |
| 0 - 3 s | The raven flies in from the **left** edge, facing right, and exits the **right** edge. |
| 3 - 7 s | Nothing. The sky is empty. |
| 7 - 10 s | The raven returns from the **right** edge, facing left, and exits the left edge. |
| 10 s on | The scene is idle again and **A** can send another raven. |

While a raven is on its way, presses of **A** are ignored, so ravens never stack. The stars at the top of the sky blink slowly the whole time.

## Files

| File | Purpose |
| --- | --- |
| `__init__.py` | The app. Loads art, reads **A**, calls `flight()` each frame, and draws. |
| `flight.py` | Pure maths: given milliseconds since the press, returns where the raven is, which way it faces and which wing frame to show. No badge APIs, so it runs and is tested on a normal computer. |
| `assets/background.png` | 160 x 120 night sky, moon and castle. |
| `assets/raven.png` | The raven sprite sheet. |
| `icon.png` | 24 x 24 menu icon. |

## How it works

`update()` runs every frame ([run loop](app-anatomy.md#the-main-loop)):

1. If **A** was just pressed and no raven is in flight, remember `sent_at = badge.ticks`.
2. Draw the background, then the blinking stars.
3. If a raven is in flight, call `flight(badge.ticks - sent_at)`. A result of `None` means "not visible right now". Otherwise it is `(x, y, flipped, frame)`, and the app blits that frame from the correct row of the sheet.
4. When the elapsed time passes `TOTAL_MS`, clear `sent_at` so the next press starts a new trip.

There is no per-frame state. The whole round trip is a function of elapsed time, which keeps it simple and makes `flight.py` easy to test.

## Sprite sheet

`raven.png` is 128 x 48: **4 columns x 2 rows** of 32 x 24 frames.

| Row | Direction |
| --- | --- |
| 0 | facing right (the outbound flight) |
| 1 | facing left (the return flight), a mirrored copy of row 0 |

Columns 0-3 are the wing positions: up, mid, level, down. `FLAP_FRAMES = (0, 1, 2, 3, 2, 1)` plays them as a flap cycle, advancing every `FLAP_MS` (90 ms).

## Tuning

All the numbers live at the top of [`raven/flight.py`](../raven/flight.py):

| Constant | Default | Effect |
| --- | --- | --- |
| `CROSS_MS` | 3000 | How long each crossing takes. Smaller is a faster raven. |
| `AWAY_MS` | 4000 | How long the screen stays empty before the raven returns. |
| `FLAP_MS` | 90 | Time per wing frame. Smaller is a faster flap. |
| `FLAP_FRAMES` | `(0, 1, 2, 3, 2, 1)` | The order the four wing frames play. |

The outbound raven's height is `40 + 5 * sin(t / 200)` and the return's is `30 + 5 * sin(t / 200)`, which gives a gentle bob at slightly different altitudes. Both are in `flight()`.

After changing `flight.py`, run the tests (`python3 -m unittest discover -s tests`) to confirm the raven still starts at the left edge, returns from the right, and stays on screen.

## Changing the art

The background, sprite sheet and icon are generated, not hand-drawn. Edit [`tools/make_assets.py`](../tools/make_assets.py) and run it. See [Art and QR codes](art-and-qr.md).
