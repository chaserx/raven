# App anatomy

How a Badgeware app is structured, and the specific API calls these two apps depend on. Each section links to the official reference. Where this repo relies on something the API pages don't document, it says so.

## Folder layout

```
my_app/
  __init__.py   # the app: runs when the app is launched
  icon.png      # 24x24 PNG shown in the menu
  assets/       # optional images, fonts and other files
```

This matches Pimoroni's [Creating your first app](https://github.com/pimoroni/badgeware-docs/blob/main/introduction/your-first-app.md). The same layout is used by the apps in [badger/home](https://github.com/badger/home).

## The globals

Apps use `screen`, `color`, `shape`, `vec2`, `image`, `badge`, `run`, `rom_font`, `SpriteSheet` and the `BUTTON_*` constants without importing them. The firmware provides them before your code runs. The one thing the sample apps import explicitly is `State`:

```python
from badgeware import State
```

## Bootstrap

Every app here starts by pointing Python at its own folder so that relative paths work:

```python
import sys, os
sys.path.insert(0, "/system/apps/raven_pet")
os.chdir("/system/apps/raven_pet")
```

See [Getting started](getting-started.md#path-names-apps-versus-systemapps) for why the path says `/system/apps`.

## The main loop

Apps hand one function to `run()`, which calls it once per frame:

```python
def update():
    screen.blit(background, vec2(0, 0))
    ...

run(update)
```

From the [builtins reference](https://github.com/pimoroni/badgeware-docs/blob/main/api/builtins.md):

- Before each call, `run()` clears the screen to `badge.default_clear` and resets the pen. Draw the whole scene every frame.
- `run()` keeps calling `update` **until it returns something other than `None`**. Both apps here return `None` (or use a bare `return`) so they run forever.
- An unhandled exception is shown on the badge's screen, and the app waits for a button press and then resets. Details also go to the console. This is the quickest way to see a typo (see [Testing and debugging](testing-and-debugging.md)).

## Screen

The apps here treat the screen as **160 x 120 pixels**, as the sample apps do. The 2.8" display shows that image scaled up, which is why the art is chunky pixel art. Pixel positions in this repo, such as the moon at (124, 28), are in that 160 x 120 space.

## Buttons

The constants are `BUTTON_A`, `BUTTON_B`, `BUTTON_C`, `BUTTON_UP`, `BUTTON_DOWN` and `BUTTON_HOME` ([badge reference](https://github.com/pimoroni/badgeware-docs/blob/main/api/badge.md)). HOME returns to the menu and is handled by the system, so apps don't need to read it.

- `badge.pressed(BUTTON_A)` is true only on the **single frame** where the button goes from up to down. It is an event, not a state. Both apps use it for actions so that holding a button doesn't repeat the action.
- `badge.held(button)` is true for as long as the button is down.
- `badge.released(button)` is true on the frame the button comes back up.

## Time

- `badge.ticks` is milliseconds since power-on, sampled once per frame.
- `badge.ticks_delta` is milliseconds since the previous frame. It is the right value for timing that should not depend on a steady frame rate.

Both reset whenever the badge is powered off or reset. They are **not** a wall clock. This is why the pet's hunger only advances while the app is open (see [Raven Pet app](raven-pet.md#hunger)).

## Drawing

```python
screen.pen = color.rgb(255, 255, 255)          # set the colour (an optional 4th value is alpha)
screen.shape(shape.rectangle(x, y, w, h))      # filled rectangle
screen.font = rom_font.nope                    # built-in small font; rom_font.ziplock is the large one
screen.text("hello", x, y)
w, h = screen.measure_text("hello")            # used to centre text
screen.blit(image, vec2(x, y))                 # copy an image onto the screen
```

References: [color](https://github.com/pimoroni/badgeware-docs/blob/main/api/color.md), [shape](https://github.com/pimoroni/badgeware-docs/blob/main/api/shape.md), [text](https://github.com/pimoroni/badgeware-docs/blob/main/api/text.md), [font](https://github.com/pimoroni/badgeware-docs/blob/main/api/font.md), [vec2](https://github.com/pimoroni/badgeware-docs/blob/main/api/vec2.md).

### Images

`image.load(path)` loads a PNG, JPEG or GIF. The result has read-only `width` and `height`. `screen.blit(source, x, y)` and `screen.blit(source, vec2)` draw it 1:1. The [image reference](https://github.com/pimoroni/badgeware-docs/blob/main/api/image.md) also describes scaling and horizontal flipping by blitting into a rectangle with a negative width. This repo does not use that. Instead, [`raven.png`](raven-app.md#sprite-sheet) contains a pre-flipped copy of every frame, which avoids relying on flip behaviour that the docs themselves flag as ambiguous.

### Sprite sheets

```python
sprites = SpriteSheet("assets/raven.png", 4, 2)   # file, columns, rows
flap = sprites.animation(0, 0, 4)                 # start column, row, frame count
screen.blit(flap.frame(2), vec2(x, y))
```

The frame size is the image size divided by columns and rows, so a sheet must divide evenly. `frame()` is always given an integer here. `SpriteSheet` and `animation()` are used exactly as in the sample apps on the badge (such as `plucky_cluck`). The [spritesheet reference](https://github.com/pimoroni/badgeware-docs/blob/main/api/spritesheet.md) documents the related `image.spritesheet(cols, rows)` and `.sprite(x, y)` calls but not these names, so if one of them ever stops working after a firmware update, check that page first.

## Saved state

```python
from badgeware import State

state = {"fullness": 100, "trainings": 0}
if State.load("raven_pet", state):   # fills `state` in place; True if a saved file existed
    ...
State.save("raven_pet", {"fullness": 80, "trainings": 2})
```

`State` stores JSON at `/state/<name>.json`. Values must be JSON-serialisable (numbers, strings, booleans, lists, dicts) ([builtins reference](https://github.com/pimoroni/badgeware-docs/blob/main/api/builtins.md)).

## Exit hook

`raven_pet` defines `on_exit()` to save when the app closes, as the `snarky_sciuridae` sample does. The Badgeware API pages don't document that hook, so the pet **also saves immediately after every feed and train**. Nothing depends on `on_exit` running.

## Randomness

The firmware provides `rnd(n)` (an integer from 0 to n inclusive) as a builtin. `raven_pet` currently picks a message with `random.getrandbits` from MicroPython's `random` module instead (see [Raven Pet app](raven-pet.md#choosing-a-message)). If `import random` ever fails on the badge, switching to `rnd` is the fix.

## Icon

`icon.png` must be 24 x 24. The icons here are generated by the scripts in `tools/` (see [Art and QR codes](art-and-qr.md)).

## Hardware variants

Pimoroni's [Coding for the different badges](https://github.com/pimoroni/badgeware-docs/blob/main/guides/badge-differences.md) guide explains how Tufty, Badger and Blinky differ. These apps assume a Tufty (colour screen, buttons A/B/C). The [badger/home](https://github.com/badger/home) repo is for the GitHub Universe conference badge, a Tufty derivative with extra hardware, so check its README before copying code between the two.
