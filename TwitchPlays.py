import asyncio
from collections import Counter
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
from twitchio.ext import commands
import time
import random
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
BOTNICK = os.getenv("BOTNICK")
CHANNEL = os.getenv("CHANNEL")
INTERVAL = 1

KEY_MAPPING = {
# A - Z
    "a": "a", 
    "b": "b", 
    "c": "c", 
    "d": "d", 
    "e": "e", 
    "f": "f", 
    "g": "g",
    "h": "h", 
    "i": "i", 
    "j": "j", 
    "k": "k", 
    "l": "l", 
    "m": "m", 
    "n": "n",
    "o": "o", 
    "p": "p", 
    "q": "q", 
    "r": "r", 
    "s": "s", 
    "t": "t", 
    "u": "u",
    "v": "v", 
    "w": "w", 
    "x": "x", 
    "y": "y", 
    "z": "z", 
# 0 - 9
    "0": "0", 
    "1": "1",
    "2": "2", 
    "3": "3", 
    "4": "4", 
    "5": "5", 
    "6": "6", 
    "7": "7", 
    "8": "8",
    "9": "9", 
# F1 - F12
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
    "f12": Key.f12,
# Special Keys
    "shift": Key.shift,
    "ctrl": Key.ctrl, 
    "alt": Key.alt, 
    "tab": Key.tab,
    "space": Key.space, 
    "esc": Key.esc, 
# Mouse Controls
    "Linksklick": "left_click", 
    "Rechtsklick": "right_click", 
    "90": "90", 
    "180": "180",
    "360": "360", 
    "oben": "up", 
    "unten": "down", 
    "links": "left", 
    "rechts": "right",
}

keyboard = KeyboardController()
mouse = MouseController()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=OAUTH_TOKEN, prefix="!",initial_channels=[CHANNEL])
        self.chat_messages = []
    
    async def event_message(self, message):
        self.chat_messages.append(message.content)

def mouse_mover(x,y,steps,pause):
    for _ in range(steps*7):
        mouse.move(x, y)
        time.sleep(pause)

async def read_chat():
    bot = Bot()
    asyncio.create_task(bot.start())

    while True:
        await asyncio.sleep(INTERVAL)

        if bot.chat_messages:
            filtered_messages = [KEY_MAPPING.get(msg.lower()) for msg in bot.chat_messages]
            counter = Counter(filtered_messages)

            if counter:
                most_common_command,count = counter.most_common(1)[0]
                print(most_common_command,count)
                if most_common_command:
                    if most_common_command in ["90", "180", "360"]:
                        mouse_mover(1,0,int(most_common_command), 0.0001)
                    elif most_common_command in ["up", "down", "left", "right"]:
                        if most_common_command == "up":
                            mouse_mover(0,-1,800, 0.0002)
                        if most_common_command == "down":
                            mouse_mover(0,1,800, 0.0002)
                        if most_common_command == "left":
                            mouse_mover(-1,0,800, 0.0002)
                        if most_common_command == "right":
                            mouse_mover(1,0,800, 0.0002)
                    elif most_common_command == "left_click":
                        mouse.press(Button.left)
                        time.sleep(random.uniform(1, 2))
                        mouse.release(Button.left)
                    elif most_common_command == "right_click":
                        mouse.press(Button.right)
                        time.sleep(random.uniform(1, 2))
                        mouse.release(Button.right)
                    else:
                        keyboard.press(most_common_command)
                        time.sleep(random.uniform(1, 2))
                        keyboard.release(most_common_command)
            bot.chat_messages.clear()

if __name__ == "__main__":
    asyncio.run(read_chat())