import sys
import os

sys.path.insert(0, "/system/apps/raven_pet")
os.chdir("/system/apps/raven_pet")

from badgeware import State
from pet import Pet, pick_message
from messages import MESSAGES

background = image.load("assets/background.png")
sprites = SpriteSheet("assets/raven_pet.png", 5, 1)
pet_frames = sprites.animation(0, 0, 5)
idle_frames = (0, 1)
SAD, EAT, TRAIN = 2, 3, 4

small_font = rom_font.nope

pet = Pet()

# a transient animation (eating, training) and the toast that goes with it
action = None
action_start = 0
action_until = 0
toast = ""

# the QR code currently on screen, or None while we're showing the raven
qr = None


def update():
    global qr

    if qr is not None:
        draw_qr()
        # any button closes the QR code
        if badge.pressed(BUTTON_A) or badge.pressed(BUTTON_B) or badge.pressed(BUTTON_C):
            qr = None
        return

    pet.tick(badge.ticks_delta / 1000)

    if badge.pressed(BUTTON_A):
        pet.feed()
        start_action("eat", "Yum!")
        save()

    if badge.pressed(BUTTON_B):
        result = pet.train()
        if result == "level_up":
            start_action("train", f"Level {pet.level}!")
        elif result == "maxed":
            start_action("train", "Fully trained!")
        else:
            start_action("train", f"Training {pet.progress}/3")
        save()

    if badge.pressed(BUTTON_C):
        # any raven can send a message, but only ones its level allows
        index = pick_message(MESSAGES, pet.level, lambda n: rnd(n - 1))
        qr = image.load(f"assets/qr/{index:02d}.png")
        return

    draw_scene()


def start_action(kind, text):
    global action, action_start, action_until, toast
    action = kind
    action_start = badge.ticks
    action_until = badge.ticks + 1200
    toast = text


def current_frame():
    now = badge.ticks
    if action and now < action_until:
        step = int((now - action_start) / 150) % 2
        flourish = EAT if action == "eat" else TRAIN
        return flourish if step == 0 else idle_frames[0]
    if pet.is_sad():
        return SAD
    return idle_frames[int(now / 600) % 2]


def draw_scene():
    screen.blit(background, vec2(0, 0))

    screen.blit(pet_frames.frame(current_frame()), vec2(56, 52))

    screen.font = small_font
    shadow_text(f"Lv {pet.level}", 3, 0)
    draw_bar(3, 12, pet.fullness)

    if action and badge.ticks < action_until:
        center_text(toast, 28, 80)

    # button labels sit on the dark ground, over each of the three buttons
    center_text("feed", 106, 31)
    center_text("train", 106, 81)
    center_text("send", 106, 131)


def draw_bar(x, y, fullness):
    screen.pen = color.rgb(10, 12, 30)
    screen.shape(shape.rectangle(x, y, 42, 6))
    screen.pen = color.rgb(242, 193, 78) if not pet.is_sad() else color.rgb(200, 70, 70)
    screen.shape(shape.rectangle(x + 1, y + 1, int(40 * fullness / 100), 4))


def draw_qr():
    screen.pen = color.rgb(10, 14, 36)
    screen.shape(shape.rectangle(0, 0, 160, 120))
    screen.blit(qr, vec2((160 - qr.width) // 2, (120 - qr.height) // 2))


def save():
    State.save("raven_pet", pet.save())


def shadow_text(text, x, y):
    screen.pen = color.rgb(20, 40, 60, 100)
    screen.text(text, x + 1, y + 1)
    screen.pen = color.rgb(255, 255, 255)
    screen.text(text, x, y)


def center_text(text, y, cx=80):
    w, _ = screen.measure_text(text)
    shadow_text(text, cx - (w / 2), y)


def init():
    state = {"fullness": 100, "trainings": 0}
    if State.load("raven_pet", state):
        pet.load(state)


def on_exit():
    save()


init()
run(update)
