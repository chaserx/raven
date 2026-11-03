# Testing and debugging

What can be tested on your computer, what needs the badge, and how to work out what went wrong.

## Unit tests

```sh
python3 -m unittest discover -s tests
```

They need only Python 3. They cover the logic that doesn't touch the badge:

| File | Covers |
| --- | --- |
| `tests/test_flight.py` | The raven enters from the left, leaves by the right, is invisible while away, returns from the right facing left, finishes, only uses frames that exist, and stays on screen |
| `tests/test_pet.py` | Hunger timing (sad just after 90 minutes, never below zero), feeding, three trainings per level, reaching and holding the top level, and save/load and clamping bad data |

Why the logic is split into `flight.py` and `pet.py`: those files import nothing from the badge, so they run anywhere. Keep new logic there, and keep `__init__.py` thin.

### What the tests don't cover

Drawing, button handling, sprite frames, QR display, saving through `State`, and timing against the real clock. Those need a badge or the simulator.

## Trying an app on the badge

After [installing](getting-started.md#install-an-app-on-the-badge), run through the checklist for the app you changed.

### Raven

- [ ] The menu shows **Raven** with its icon.
- [ ] The night sky, moon, castle and twinkling stars draw correctly.
- [ ] **A** starts a raven from the left, flapping, facing right.
- [ ] It leaves the right edge, the screen is empty for about 4 seconds, and it returns from the right facing **left**.
- [ ] Pressing **A** during the trip does nothing; pressing it afterwards sends another raven.

### Raven Pet

- [ ] The menu shows **Raven Pet** with its icon, and the raven sits on the ground line.
- [ ] **A** shows the berry animation and "Yum!".
- [ ] **B** shows "Training 1/3", "Training 2/3", then "Level 2!". The level in the corner changes.
- [ ] **C** shows the same QR code every time, at every level.
- [ ] **A phone camera scans the QR code** and offers to open https://engineeringmaester.com/next.
- [ ] Any button closes the QR code.
- [ ] Quit and reopen the app: the level and fullness are restored.
- [ ] Temporarily set `SAD_AFTER_S` to `30` in `pet.py`, reinstall, and wait. The raven should droop and the bar should turn red, and feeding should fix both.

## Things still worth confirming on a badge

Raven Pet has been installed and run on a Tufty 2350 and works. That covers sprite sheets (`SpriteSheet` / `animation()`, which the API pages don't document by those names), button handling, and `State`. The **Raven** (first) app has not been confirmed on a badge yet, though it uses the same sprite and button calls.

Still unconfirmed, because nothing in this repo checks them automatically:

- **QR scan reliability.** The code uses 3 pixels per module and a 2-module border. Scanning it on the badge with a phone is the one check not yet recorded.
- **`on_exit()`** is used in the sample apps but is not in the API pages. The pet doesn't depend on it, since it saves after every feed and train.

## When an app crashes

An unhandled exception is drawn on the badge's screen, and details also go to the console ([`run()` reference](https://github.com/pimoroni/badgeware-docs/blob/main/api/builtins.md)). Press a button to reset. Read the message first, as it usually names the file and line.

Common causes in this repo:

| Symptom | Likely cause |
| --- | --- |
| `ImportError` for `flight` or `pet` | The folder on the badge doesn't match the path in the app's `sys.path.insert(...)` line, or a file didn't get copied |
| `OSError` when loading an image | A file is missing from `assets/`, or the `os.chdir` path is wrong |
| The app is missing from the menu | The folder has no `__init__.py`, or it was copied to the wrong place |
| The menu entry looks right but the icon is blank | `icon.png` is missing or not 24 x 24 |
| An odd name in the menu | The menu title-cases the folder name, replacing underscores with spaces |

## Serial access with mpremote

[`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html) gives you the MicroPython REPL and file access over USB. The badge team documents the workflow in [`hardware/USB_SERIAL.md`](https://github.com/badger/home/blob/main/hardware/USB_SERIAL.md).

```sh
python3 -m pip install mpremote
mpremote devs                                   # find the badge (USB ID 2e8a:1101)
mpremote connect /dev/cu.usbmodemXXXX repl      # live REPL; Ctrl-] to leave
mpremote connect /dev/cu.usbmodemXXXX fs ls :/system/apps/raven_pet
mpremote connect /dev/cu.usbmodemXXXX reset
```

Things to know, from that guide:

- Port names change between connections, so run `mpremote devs` each time, and only one program can use the port at once.
- Connecting usually soft-resets the badge, which stops the running app.
- `/system` is **read-only** over serial. Install and update apps through USB mass-storage mode instead.
- `mpremote mount` can mount a local folder for quick tests, but streaming PNGs through it is unreliable, and these apps hard-code `/system/apps/<name>` paths, so they are not a good fit. Copy the app to the badge for real testing.

Handy REPL checks:

```python
import os
os.listdir("/system/apps/raven_pet")            # confirm the files arrived
open("/state/raven_pet.json").read()            # see the saved pet
```

Where `print()` output from a running app appears is not spelled out in the guide, so test it with a trivial `print` before relying on it for debugging.

## The Badgeware simulator

Pimoroni publishes a [Badgeware simulator](https://github.com/pimoroni/badgeware-simulator) (and a [web version](https://github.com/pimoroni/badgeware-web-simulator)) that can run apps on a computer. Its README describes a Linux build, keyboard controls (**A** = Left arrow, **B** = Space, **C** = Right arrow, Escape = hot reload, `h` = screenshot), and screenshot and recording support. These apps have not been run in it. If you try, note that they hard-code `/system/apps/<name>` and may need that path to exist.

## Debugging approach

1. Reproduce on the badge and read the on-screen error.
2. If it's logic (timing, levels), write a failing test in `tests/` first. Those files run in milliseconds.
3. If it's visual, change one thing, reinstall, and look. For pet poses, `.preview/pets.png` shows the result without touching the badge.
4. Keep `__init__.py` small, so that most bugs land in testable files.
