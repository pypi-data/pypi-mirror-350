def color_block_print(r, g, b):
    print(f"\033[48;2;{r};{g};{b}m   \033[0m RGB({r},{g},{b})")

def color_print(text, r, g, b, **kwargs):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", **kwargs)


def fading_print(text, start_rgb, end_rgb):
    """
    Print text with fading colors from start_rgb to end_rgb.

    Parameters:
    - text (str): The text to print
    - start_rgb (tuple): (r, g, b) start color
    - end_rgb (tuple): (r, g, b) end color
    """
    length = max(len(text) - 1, 1) 

    for i, char in enumerate(text):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / length)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / length)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / length)
        print(f"\033[38;2;{r};{g};{b}m{char}\033[0m", end='')

    print()  

import time
import os

import time
import sys

import threading
import time
import sys

# Globale lock gebruiken voor alle terminal output
print_lock = threading.Lock()

def moving_fade(text: str, start_rgb: tuple, end_rgb: tuple, delay=0.05, cycles=3):
    """
    Start a thread that prints a moving fade from start_rgb to end_rgb across the text.
    Andere prints worden beschermd met een globale print_lock.
    """

    def fade_worker():
        r1, g1, b1 = start_rgb
        r2, g2, b2 = end_rgb
        length = len(text)

        def lerp(a, b, t):
            return int(a + (b - a) * t)

        gradient = []
        for i in range(length):
            t = i / max(1, length - 1)
            r = lerp(r1, r2, t)
            g = lerp(g1, g2, t)
            b = lerp(b1, b2, t)
            gradient.append((r, g, b))

        for _ in range(cycles * length):
            out = ""
            for i, char in enumerate(text):
                r, g, b = gradient[i % length]
                out += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
            with print_lock:
                sys.stdout.write('\r' + out)
                sys.stdout.flush()
            gradient = [gradient[-1]] + gradient[:-1]
            time.sleep(delay)
        with print_lock:
            print()

    thread = threading.Thread(target=fade_worker, daemon=True)
    thread.start()
    return thread
