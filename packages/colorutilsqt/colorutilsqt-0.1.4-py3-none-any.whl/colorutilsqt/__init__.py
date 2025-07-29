#pycolortools - colorfunctions in python

from .converter import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsl,
    hsl_to_rgb,
    hex_to_hsl,
    hsl_to_hex,
)

from .terminal import (
    color_print,
    color_block_print,
    fading_print,
)

import builtins
import threading

print_lock = threading.Lock()

def safe_print(*args, **kwargs):
    """Thread-safe print"""
    with print_lock:
        builtins._original_print(*args, **kwargs)

def enable_safe_print():
    """Vervangt de globale print-functie door een thread-safe versie"""
    if not hasattr(builtins, "_original_print"):
        builtins._original_print = builtins.print
        builtins.print = safe_print

def disable_safe_print():
    """Herstelt de originele print-functie"""
    if hasattr(builtins, "_original_print"):
        builtins.print = builtins._original_print
        del builtins._original_print
