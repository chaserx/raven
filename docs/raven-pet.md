# Raven Pet app

The second app: a virtual pet raven, in the style of a Tamagotchi. Feed it, train it, and have it send a Game of Thrones style message as a QR code.

Folder: [`raven_pet/`](../raven_pet/). Menu name: **Raven Pet**.

## Behaviour

| Button | Action | What you see |
| --- | --- | --- |
| **A** | Feed | The raven pecks a berry. Its fullness returns to 100%. Toast: "Yum!" |
| **B** | Train | The raven flings a wing up. Toast: "Training 1/3", "Training 2/3", then "Level 2!". At the top level: "Fully trained!" |
| **C** | Send a message | A full-screen QR code. Any button closes it. |

The top-left of the screen shows the raven's level (`Lv 1`) and a fullness bar. The bar turns red when the raven is sad.

Design rules:

- **The raven never dies.** Neglect only makes it look sad (drooped head, a tear), and one feeding cures it.
- **A message can be sent at any time.** The raven's mood doesn't gate it. Only its **level** does, because training unlocks longer messages.
- **Training is quick.** Three presses per level and three levels, so six presses reach the top. A stranger can do it in one sitting.

## Files

| File | Purpose |
| --- | --- |
| `__init__.py` | The app: input, drawing, toasts, the QR screen, saving. |
| `pet.py` | Pure logic: the `Pet` class (fullness, training, levels, save/load) and `pick_message()`. No badge APIs, so it is unit tested on a normal computer. |
| `messages.py` | The list of `(tier, text)` messages. |
| `assets/raven_pet.png` | The pet sprite sheet. |
| `assets/qr/NN.png` | One pre-rendered QR code per message, numbered by position in `MESSAGES`. |
| `assets/background.png` | The night-sky scene, shared with the first app. |

## Levels

| Level | Reached after | Messages it can send |
| --- | --- | --- |
| 1 | start | tier 1 (up to 30 characters) |
| 2 | 3 training presses | tiers 1 and 2 (up to 45 characters) |
| 3 | 6 training presses | tiers 1, 2 and 3 (up to 70 characters) |

Further training at level 3 does nothing and shows "Fully trained!". The constants are `TRAINS_PER_LEVEL = 3` and `MAX_LEVEL = 3` in [`pet.py`](../raven_pet/pet.py).

## Hunger

The raven has a `fullness` from 0 to 100. It starts at 100 and falls at a constant rate:

```
DECAY_PER_S = (FULL - SAD_BELOW) / SAD_AFTER_S = (100 - 40) / (90 * 60)
```

So a freshly fed raven looks **sad after 90 minutes**, and fullness would reach 0 after 150 minutes. It never goes below 0. The raven is sad whenever `fullness < SAD_BELOW` (40).

**Hunger only advances while the app is open.** The app measures time with `badge.ticks_delta`, which is milliseconds since the previous frame and not wall-clock time. If you close the app or power the badge off, the raven's hunger is frozen until the next time you open it. That suits a costume prop (a raven in your pocket doesn't starve), but it is a deliberate trade-off. Real elapsed time would need an RTC and Wi-Fi time sync (see the [rtc reference](https://github.com/pimoroni/badgeware-docs/blob/main/api/rtc.md)).

## Choosing a message

`pick_message(messages, level, rand)` builds a pool of every message whose tier is at most the raven's level, then picks one at random. It returns an **index**, which is also the number in the QR file name (`assets/qr/07.png` belongs to `MESSAGES[7]`).

`rand(n)` must return an integer in `range(n)`. The app passes `lambda n: rnd(n - 1)`, because the firmware's builtin `rnd(n)` returns an integer from 0 to n **inclusive**. Tests pass a deterministic function. See [App anatomy](app-anatomy.md#randomness).

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

Pressing **C** loads `assets/qr/NN.png` and shows it centred on a dark background. It is plain text inside the QR code, so any phone camera shows the message straight away. See [Art and QR codes](art-and-qr.md#qr-codes) for how the codes are generated and why they are limited in size.

## Tuning

| Constant | File | Default | Effect |
| --- | --- | --- | --- |
| `SAD_AFTER_S` | `pet.py` | 5400 | Seconds of running before a fed raven looks sad |
| `SAD_BELOW` | `pet.py` | 40 | The fullness at which the raven looks sad |
| `TRAINS_PER_LEVEL` | `pet.py` | 3 | Training presses per level |
| `MAX_LEVEL` | `pet.py` | 3 | Number of levels |
| `1200` (in `start_action`) | `__init__.py` | 1200 ms | How long the feed/train animation and toast last |

To try the sad state without waiting 90 minutes, temporarily set `SAD_AFTER_S` to something like `30` and reinstall the app.

## Adding or changing messages

Edit [`raven_pet/messages.py`](../raven_pet/messages.py), then regenerate the QR images and copy the app to the badge. The tier length limits are enforced by `tests/test_pet.py` and by the generator. Full steps are in [Art and QR codes](art-and-qr.md#adding-or-changing-a-message).
