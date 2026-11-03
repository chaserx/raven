# Raven Pet app

The second app: a virtual pet raven, in the style of a Tamagotchi. Feed it, train it, and have it send a QR code linking to https://engineeringmaester.com/r/next.

Folder: [`raven_pet/`](../raven_pet/). Menu name: **Raven Pet**.

## Behaviour

| Button | Action | What you see |
| --- | --- | --- |
| **A** | Feed | The raven pecks a berry. Its fullness returns to 100%. Toast: "Yum!" |
| **B** | Train | The raven flings a wing up. Toast: "Training 1/3", "Training 2/3", then "Level 2!". At the top level: "Fully trained!" |
| **C** | Show the QR code | A full-screen QR code, the same one every time. Any button closes it. |

The top-left of the screen shows the raven's level (`Lv 1`) and a fullness bar. The bar turns red when the raven is sad.

Design rules:

- **The raven never dies.** Neglect only makes it look sad (drooped head, a tear), and one feeding cures it.
- **The QR code can be shown at any time.** Neither the raven's mood nor its level gates it.
- **Training is quick.** Three presses per level and three levels, so six presses reach the top. A stranger can do it in one sitting.

## Files

| File | Purpose |
| --- | --- |
| `__init__.py` | The app: input, drawing, toasts, the QR screen, saving. |
| `pet.py` | Pure logic: the `Pet` class (fullness, training, levels, save/load). No badge APIs, so it is unit tested on a normal computer. |
| `assets/raven_pet.png` | The pet sprite sheet. |
| `assets/qr.png` | The pre-rendered QR code. |
| `assets/background.png` | The night-sky scene, shared with the first app. |

## Levels

| Level | Reached after |
| --- | --- |
| 1 | start |
| 2 | 3 training presses |
| 3 | 6 training presses |

Levels are cosmetic: they change the `Lv N` label and nothing else. Further training at level 3 does nothing and shows "Fully trained!". The constants are `TRAINS_PER_LEVEL = 3` and `MAX_LEVEL = 3` in [`pet.py`](../raven_pet/pet.py).

## Hunger

The raven has a `fullness` from 0 to 100. It starts at 100 and falls at a constant rate:

```
DECAY_PER_S = (FULL - SAD_BELOW) / SAD_AFTER_S = (100 - 40) / (90 * 60)
```

So a freshly fed raven looks **sad after 90 minutes**, and fullness would reach 0 after 150 minutes. It never goes below 0. The raven is sad whenever `fullness < SAD_BELOW` (40).

**Hunger only advances while the app is open.** The app measures time with `badge.ticks_delta`, which is milliseconds since the previous frame and not wall-clock time. If you close the app or power the badge off, the raven's hunger is frozen until the next time you open it. That suits a costume prop (a raven in your pocket doesn't starve), but it is a deliberate trade-off. Real elapsed time would need an RTC and Wi-Fi time sync (see the [rtc reference](https://github.com/pimoroni/badgeware-docs/blob/main/api/rtc.md)).

## Saved state

After every feed and train, and again in `on_exit()`, the app saves:

```json
{"fullness": 72, "trainings": 4}
```

to `/state/raven_pet.json` on the badge via `State.save("raven_pet", ...)`. At start-up `State.load()` restores it, and `Pet.load()` clamps both values to valid ranges so a corrupted file cannot break the app.

To reset the pet to a fresh level-1 raven, delete `/state/raven_pet.json` on the badge.

## Screen layout

Everything is positioned on the 160 x 120 screen:

| Element | Position |
| --- | --- |
| Scene | full screen background |
| Raven | 48 x 48 sprite at (56, 52), so its feet sit on the ground line at y = 100 |
| `Lv N` | top-left, (3, 0) |
| Fullness bar | (3, 12), 42 x 6 |
| Toast | centred, y = 28, shown for 1.2 s |
| Button labels | y = 106, centred at x = 31 (feed), 81 (train), 131 (send), over the three buttons |
| QR screen | solid dark background with the QR image centred |

## Sprite sheet

`raven_pet.png` is 240 x 48: **5 columns x 1 row** of 48 x 48 frames.

| Frame | Pose | Used for |
| --- | --- | --- |
| 0 | idle | resting; also the in-between frame during feed/train |
| 1 | idle, head slightly lower | the second frame of the idle bob (swaps every 600 ms) |
| 2 | sad | when `fullness < 40` |
| 3 | pecking a berry | feeding |
| 4 | wing flung up | training |

During a feed or train, the app alternates the pose with frame 0 every 150 ms for 1.2 seconds.

## The QR code screen

Pressing **C** loads `assets/qr.png` and shows it centred on a dark background. Scanning it with a phone camera offers to open https://engineeringmaester.com/r/next. See [Art and QR codes](art-and-qr.md#qr-code) for how the code is generated and why its size is limited.

## Tuning

| Constant | File | Default | Effect |
| --- | --- | --- | --- |
| `SAD_AFTER_S` | `pet.py` | 5400 | Seconds of running before a fed raven looks sad |
| `SAD_BELOW` | `pet.py` | 40 | The fullness at which the raven looks sad |
| `TRAINS_PER_LEVEL` | `pet.py` | 3 | Training presses per level |
| `MAX_LEVEL` | `pet.py` | 3 | Number of levels |
| `1200` (in `start_action`) | `__init__.py` | 1200 ms | How long the feed/train animation and toast last |

To try the sad state without waiting 90 minutes, temporarily set `SAD_AFTER_S` to something like `30` and reinstall the app.

## Changing the QR code's link

Edit `QR_URL` in [`tools/make_pet_assets.py`](../tools/make_pet_assets.py), then regenerate the QR image and copy the app to the badge. Full steps are in [Art and QR codes](art-and-qr.md#changing-the-link).
