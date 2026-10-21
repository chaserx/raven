# References

External documentation and articles relevant to building apps like these.

## Badgeware and the Tufty 2350

**Start here**

- [Badgeware](https://badgewa.re/): Pimoroni's home for the Badger, Tufty and Blinky badges.
- [Badgeware documentation](https://badgewa.re/docs): the hosted docs.
- [Meet your badge](https://github.com/pimoroni/badgeware-docs/blob/main/introduction/meet-your-badge.md): the hardware tour.
- [Creating your first app](https://github.com/pimoroni/badgeware-docs/blob/main/introduction/your-first-app.md): the app folder layout, installing over USB, button handling.
- [Update your firmware](https://badgewa.re/docs/introduction/update-your-firmware.md): keep the badge current.
- [Tufty 2350 in the Pimoroni shop](https://shop.pimoroni.com/products/tufty-2350).

**API reference** (in the [badgeware-docs](https://github.com/pimoroni/badgeware-docs) repo, under `api/`)

| Page | Use it for |
| --- | --- |
| [badge](https://github.com/pimoroni/badgeware-docs/blob/main/api/badge.md) | `ticks`, `ticks_delta`, buttons (`pressed`, `held`, `released`) |
| [builtins](https://github.com/pimoroni/badgeware-docs/blob/main/api/builtins.md) | `run()`, `State`, `rnd()`, `free()`, `file_exists()` |
| [image](https://github.com/pimoroni/badgeware-docs/blob/main/api/image.md) | `image.load`, `screen.blit`, scaling and flipping, antialiasing |
| [spritesheet](https://github.com/pimoroni/badgeware-docs/blob/main/api/spritesheet.md) | sprite sheets |
| [shape](https://github.com/pimoroni/badgeware-docs/blob/main/api/shape.md) | drawing shapes |
| [color](https://github.com/pimoroni/badgeware-docs/blob/main/api/color.md) | colours and pens |
| [text](https://github.com/pimoroni/badgeware-docs/blob/main/api/text.md) and [font](https://github.com/pimoroni/badgeware-docs/blob/main/api/font.md) | drawing text and the built-in fonts |
| [vec2](https://github.com/pimoroni/badgeware-docs/blob/main/api/vec2.md) and [rect](https://github.com/pimoroni/badgeware-docs/blob/main/api/rect.md) | positions and rectangles |
| [tween](https://github.com/pimoroni/badgeware-docs/blob/main/api/tween.md) | easing for smoother motion |
| [rtc](https://github.com/pimoroni/badgeware-docs/blob/main/api/rtc.md) and [wifi](https://github.com/pimoroni/badgeware-docs/blob/main/api/wifi.md) | real-time clock and Wi-Fi, for a pet that tracks real elapsed time |

**Guides**

- [Coding for the different badges](https://github.com/pimoroni/badgeware-docs/blob/main/guides/badge-differences.md): Tufty versus Badger versus Blinky.
- The [guides](https://github.com/pimoroni/badgeware-docs/tree/main/guides), [tutorials](https://github.com/pimoroni/badgeware-docs/tree/main/tutorials), [examples](https://github.com/pimoroni/badgeware-docs/tree/main/examples) and [patterns](https://github.com/pimoroni/badgeware-docs/tree/main/patterns) folders in the same repo.

**Source and tools**

- [pimoroni/tufty2350](https://github.com/pimoroni/tufty2350): firmware source.
- [pimoroni/badgeware-simulator](https://github.com/pimoroni/badgeware-simulator) and [badgeware-web-simulator](https://github.com/pimoroni/badgeware-web-simulator): run apps on a computer.
- [Pimoroni Learn](https://learn.pimoroni.com/tag/MicroPython): tutorials tagged MicroPython.

## Sample apps

- [badger/home](https://github.com/badger/home): the GitHub Universe badge repo, with many example apps in `badge/apps/`. The apps on the badge that this repo was modelled on (`plucky_cluck`, `snarky_sciuridae` and others) come from this family.
- [Its README](https://github.com/badger/home/blob/main/README.md), [CONTRIBUTING](https://github.com/badger/home/blob/main/CONTRIBUTING.md) and [hardware notes](https://github.com/badger/home/blob/main/hardware/README.md).
- [USB serial and REPL workflow](https://github.com/badger/home/blob/main/hardware/USB_SERIAL.md): `mpremote`, mass-storage mode, and testing without copying files.

## Articles

- [Simon Willison: GitHub Universe badge](https://simonwillison.net/2025/Oct/28/github-universe-badge/): a hands-on first look at the previous-year badge, including mass-storage mode and Wi-Fi setup.

## MicroPython and tooling

- [MicroPython documentation](https://docs.micropython.org/en/latest/): the language the badge runs.
- [`mpremote` reference](https://docs.micropython.org/en/latest/reference/mpremote.html): REPL and file access over USB.
- [`segno`](https://segno.readthedocs.io/): the pure-Python QR code library used by the generator, and its [PyPI page](https://pypi.org/project/segno/).
- [QR code (Wikipedia)](https://en.wikipedia.org/wiki/QR_code): versions, error correction and capacity.
