# Getting started

How to set up your computer, put these apps on a Tufty 2350, and iterate on them.

## What you need

- A Pimoroni Badger Tufty 2350 (or a Badgeware badge from the same family) and a USB cable.
- Current badge firmware. Pimoroni publishes update instructions at [Update your firmware](https://badgewa.re/docs/introduction/update-your-firmware.md). If an app misbehaves for no obvious reason, check your firmware first.
- Python 3 on your computer, for the tests and the art generators.
- Optional: [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html) for a serial connection (see [Testing and debugging](testing-and-debugging.md)).

Background on the hardware is in Pimoroni's [Meet your badge](https://github.com/pimoroni/badgeware-docs/blob/main/introduction/meet-your-badge.md).

## Set up your computer

```sh
git clone https://github.com/chaserx/raven.git
cd raven

# unit tests need nothing but Python 3
python3 -m unittest discover -s tests

# art and QR generation needs one small package. A virtual environment keeps it contained.
python3 -m venv .venv
.venv/bin/pip install -r tools/requirements.txt
```

`.venv/` is ignored by git.

## Install an app on the badge

An app is a folder inside `apps` on the badge. The menu finds any folder that has an `__init__.py`.

1. **Double-tap RESET** on the back of the badge. It appears on your computer as a drive named `TUFTY`.
2. **Copy the app folder** into the drive's `apps` folder:

   ```sh
   COPYFILE_DISABLE=1 cp -R raven_pet /Volumes/TUFTY/apps/raven_pet
   ```

3. **Eject** the drive (`diskutil eject /Volumes/TUFTY` on macOS), then press **RESET** once.
4. Press **HOME** to reach the menu and pick the app.

The menu name comes from the folder name: underscores become spaces and each word is capitalised, so `raven_pet` shows as **Raven Pet** ([Creating your first app](https://github.com/pimoroni/badgeware-docs/blob/main/introduction/your-first-app.md)).

### Path names: `/apps` versus `/system/apps`

On your computer the drive shows the folder as `/Volumes/TUFTY/apps/raven_pet`. The firmware sees the same folder as `/system/apps/raven_pet`. The apps in this repo hard-code the second form at the top of `__init__.py`:

```python
sys.path.insert(0, "/system/apps/raven_pet")
os.chdir("/system/apps/raven_pet")
```

This is the same bootstrap the sample apps use. It makes relative asset paths such as `assets/background.png` and imports of sibling files such as `from pet import Pet` work. **The folder name on the badge must match the name in that path.** If you rename a folder, update both lines.

### Updating an app

Copying over an existing folder does not delete files you removed locally. To get a clean copy, delete the old folder on the drive first:

```sh
rm -rf /Volumes/TUFTY/apps/raven_pet
COPYFILE_DISABLE=1 cp -R raven_pet /Volumes/TUFTY/apps/raven_pet
sync
```

### macOS copy gotchas

- `cp` and Finder add `._*` metadata files on this kind of drive. `COPYFILE_DISABLE=1` prevents them. If some slip in, remove them: `find /Volumes/TUFTY/apps/raven_pet -name '._*' -delete`.
- Don't copy `__pycache__` folders. Running the tests creates them next to the source; delete them first (`find raven_pet -name __pycache__ -prune -exec rm -rf {} +`).
- Always eject before resetting, or the badge may see a half-written file.

## Saved data

`raven_pet` stores its progress with Badgeware's `State` helper, which writes JSON to `/state/raven_pet.json` on the badge. To reset the pet, delete that file (or call `State.delete("raven_pet")` from the serial REPL). Details are in [Raven Pet app](raven-pet.md#saved-state).

## Next steps

- [App anatomy](app-anatomy.md): how a Badgeware app works, and which calls these apps use.
- [Testing and debugging](testing-and-debugging.md): tests, serial access, and a checklist for trying an app on the badge.
- [Art and QR codes](art-and-qr.md): regenerate the sprites or change the QR code's link.
