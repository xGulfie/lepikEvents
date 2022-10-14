import mouse
import keyboard
import sys
from threading import Lock, Thread
import time
import signal

print_lock = Lock()

def safe_print(*a, **b):
    with print_lock:
        print(*a, **b)
        sys.stdout.flush()


def handle_key_hook(e: tuple) -> None:
    if e.event_type == "down":
        safe_print("keyPress:", e.name)
    else :
        safe_print("keyRelease:", e.name)

def handle_mouse_hook(e: tuple) -> None:
    if type(e) == mouse.MoveEvent:
        safe_print("mouseMove:[",e.x,",",e.y,",",e.time,"]")

keyboard.hook(handle_key_hook)
mouse.hook(handle_mouse_hook)

def mousePress(button: int) -> None:
    finalTuple = mouse.get_position() + (button,)
    safe_print("mouseClick:", list(finalTuple))

def mouseDoubleClick(button: int) -> None:
    finalTuple = mouse.get_position() + (button,)
    safe_print("mouseDoubleClick:", list(finalTuple))

mouse.on_click(lambda: mousePress(1))
mouse.on_right_click(lambda: mousePress(2))
mouse.on_middle_click(lambda: mousePress(3))
mouse.on_double_click(lambda: mouseDoubleClick(1))

running = True

# handle kill
def exit_graceful(*args):
    global running
    keyboard.unhook_all()
    mouse.unhook_all()
    running=False
    
signal.signal(signal.SIGINT, exit_graceful)
signal.signal(signal.SIGTERM, exit_graceful)

while running:
    time.sleep(1)
