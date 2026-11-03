# Raven

Two Game of Thrones themed apps for the [Pimoroni Badger Tufty 2350](https://badgewa.re/) smart badge (a 2.8" colour screen, RP2350, MicroPython). They were built as props for an Engineering Maester Halloween costume, and the goal is simply to get a smile from whoever is standing next to you.

| App | Folder | What it does | Buttons |
| --- | --- | --- | --- |
| **Raven** | [`raven/`](raven/) | A pixel-art raven flies across a moonlit castle skyline, leaves the screen, and flies back in from the same edge a few seconds later. | **A** sends the raven |
| **Raven Pet** | [`raven_pet/`](raven_pet/) | A virtual pet raven. Feed it, train it, or have it send a QR code linking to https://engineeringmaester.com/next. | **A** feed, **B** train, **C** show QR code |

Both apps use the same night-sky scene and are written in MicroPython against Pimoroni's [Badgeware](https://github.com/pimoroni/badgeware-docs) API.

## Quick start

You need a Tufty 2350 and a computer. Nothing has to be installed on the badge beyond copying a folder.

1. Double-tap the **RESET** button on the back of the badge. It mounts as a USB drive named `TUFTY`.
2. Copy the app folders into the drive's `apps` folder. On macOS, `COPYFILE_DISABLE=1` stops Finder-style `._*` junk files being copied too:

   ```sh
   COPYFILE_DISABLE=1 cp -R raven     /Volumes/TUFTY/apps/raven
   COPYFILE_DISABLE=1 cp -R raven_pet /Volumes/TUFTY/apps/raven_pet
   ```

3. Eject the drive, then reset the badge.
4. Press **HOME** to open the menu. The apps appear as **Raven** and **Raven Pet**.

The full walkthrough, including firmware and serial access, is in [docs/getting-started.md](docs/getting-started.md).

## Developing

```sh
python3 -m unittest discover -s tests          # logic tests, no badge needed

python3 -m venv .venv && .venv/bin/pip install -r tools/requirements.txt
python3 tools/make_assets.py                   # raven/ art
.venv/bin/python tools/make_pet_assets.py      # raven_pet/ art and QR codes
```

Only the pure logic (`flight.py`, `pet.py`) can run on a normal computer. Anything that touches the screen, buttons or saved state needs a badge, or the Badgeware simulator. See [docs/testing-and-debugging.md](docs/testing-and-debugging.md).

## Repository layout

```
raven/            App 1: the flying raven (this folder is what gets copied to the badge)
  __init__.py       app entry point: draws the scene and runs the flight
  flight.py         pure timing/position maths for the round trip
  assets/           background.png, raven.png (flap frames, both directions)
  icon.png          24x24 menu icon
raven_pet/        App 2: the virtual pet raven
  __init__.py       app entry point: input, drawing, QR screen, saving
  pet.py            pure pet logic: hunger, levels
  assets/           background.png, raven_pet.png, qr.png
  icon.png
tools/            Pixel-art and QR generators (run on your computer, not the badge)
tests/            Unit tests for the pure logic
docs/             Developer documentation
```

## Documentation

| Doc | Read it when you want to... |
| --- | --- |
| [Getting started](docs/getting-started.md) | set up your computer, install apps on the badge, and update them |
| [App anatomy](docs/app-anatomy.md) | understand how a Badgeware app is put together and which API calls these apps use |
| [Raven app](docs/raven-app.md) | change the flight timing or art of the first app |
| [Raven Pet app](docs/raven-pet.md) | change the pet's behaviour, levels or UI |
| [Art and QR codes](docs/art-and-qr.md) | regenerate sprites, or change the QR code's link |
| [Testing and debugging](docs/testing-and-debugging.md) | run the tests, check an app on the badge, and find out why it crashed |
| [References](docs/references.md) | find the official Pimoroni, GitHub and MicroPython documentation |

## Status

- **Raven Pet** has been installed and run on a Tufty 2350 and works.
- **Raven** has not yet been confirmed on a badge.
- The pure logic is covered by unit tests. The rendering and input code has no automated tests, so check changes on a badge. [docs/testing-and-debugging.md](docs/testing-and-debugging.md) lists the things still worth confirming on hardware.
