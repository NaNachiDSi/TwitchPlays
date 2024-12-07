import asyncio
import json
from collections import Counter
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
from pathlib import Path
from twitchio.ext import commands
import time
import random

config_file = Path(__file__).parent / "TwitchPlays.json"
with open(config_file, "r") as f:
    config = json.load(f)

TWITCH_TOKEN = config["oauth"]
TWITCH_NICK = config["nickname"]
TWITCH_CHANNEL = config["channel"]
INTERVAL = config["interval"]
COMMAND_MAPPING = config["command_mapping"]

keyboard = KeyboardController()
mouse = MouseController()

KEY_MAPPING = {
    "shift": Key.shift,
    "ctrl": Key.ctrl,
    "alt": Key.alt,
    "tab": Key.tab,
    "enter": Key.enter,
    "space": Key.space,
    "backspace": Key.backspace,
    "esc": Key.esc,
    "caps_lock": Key.caps_lock,
    "pause": Key.pause,
    "insert": Key.insert,
    "home": Key.home,
    "page_up": Key.page_up,
    "page_down": Key.page_down,
    "delete": Key.delete,
    "end": Key.end,
    "left": Key.left,
    "right": Key.right,
    "up": Key.up,
    "down": Key.down,
    "f1": Key.f1,
    "f2": Key.f2,
    "f3": Key.f3,
    "f4": Key.f4,
    "f5": Key.f5,
    "f6": Key.f6,
    "f7": Key.f7,
    "f8": Key.f8,
    "f9": Key.f9,
    "f10": Key.f10,
    "f11": Key.f11,
    "f12": Key.f12
}

for char in "abcdefghijklmnopqrstuvwxyz0123456789":
    KEY_MAPPING[char] = char

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TWITCH_TOKEN,
            prefix="!",
            initial_channels=[TWITCH_CHANNEL]
        )
        self.chat_messages = []

    async def event_ready(self):
        print(f"Logged in as {self.nick}")

    async def event_message(self, message):
        self.chat_messages.append(message.content)

def move_mouse(x:int,y: int,steps: int,pause: float):
    for _ in range(steps*7):
        mouse.move(x, y)
        time.sleep(pause)

async def analyze_chat():
    bot = Bot()
    asyncio.create_task(bot.start())

    while True:
        await asyncio.sleep(INTERVAL)

        if bot.chat_messages:
            filtered_messages = [
                COMMAND_MAPPING.get(msg.lower())
                for msg in bot.chat_messages if msg.lower() in COMMAND_MAPPING
            ]

            filtered_messages = [msg for msg in filtered_messages if msg]
            counter = Counter(filtered_messages)

            if counter:
                most_common_command, count = counter.most_common(1)[0]
                print(f"Häufigste Nachricht: {most_common_command} ({count})")

                key = KEY_MAPPING.get(most_common_command)

                if key:
                    if isinstance(key, str):
                        keyboard.press(key)
                        time.sleep(random.uniform(1, 2))
                        keyboard.release(key)
                    else:
                        keyboard.press(key)
                        time.sleep(random.uniform(1, 2))
                        keyboard.release(key)

                if most_common_command == "left_click":
                    mouse.click(Button.left)
                elif most_common_command == "right_click":
                    mouse.click(Button.right)
                elif most_common_command in ["90", "180", "360"]:
                    move_mouse(1,0,int(most_common_command), 0.0001)
                elif most_common_command in ["up", "down", "left", "right"]:
                    if most_common_command == "up":
                        move_mouse(0,-1,800, 0.0002)
                    if most_common_command == "down":
                        move_mouse(0,1,800, 0.0002)
                    if most_common_command == "left":
                        move_mouse(-1,0,800, 0.0002)
                    if most_common_command == "right":
                        move_mouse(1,0,800, 0.0002)


            bot.chat_messages.clear()

if __name__ == "__main__":
    asyncio.run(analyze_chat())
