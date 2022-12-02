from datetime import datetime
from threading import Thread
from time import sleep

from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Controller
from pynput.mouse import Listener as MouseListener
from screeninfo import get_monitors


def setup_listeners() -> tuple[Thread, 'KeyboardListener', 'MouseListener']:
    """Set up all listeners in their own threads.

    Returns:
        tuple[Thread, 'KeyboardListener', 'MouseListener']: all 3 listeners
    """

    idle_listener = Thread(target=idle_process)
    keyboard_listener = KeyboardListener(on_press=update_time, on_release=update_time)
    mouse_listener = MouseListener(on_move=update_time, on_click=update_time, on_scroll=update_time)

    return idle_listener, keyboard_listener, mouse_listener


def start_listeners(idle_listener: Thread, keyboard_listener: 'KeyboardListener', mouse_listener: 'MouseListener') -> None:
    """Make each listener begin detecting user actions.

    Args:
        idle_listener (Thread): _description_
        keyboard_listener (KeyboardListener): _description_
        mouse_listener (MouseListener): _description_
    """

    idle_listener.start()
    keyboard_listener.start()
    mouse_listener.start()


def join_listeners(idle_listener: Thread, keyboard_listener: 'KeyboardListener', mouse_listener: 'MouseListener') -> None:
    """Block the listeners so they don't exit.

    Args:
        idle_listener (Thread): _description_
        keyboard_listener (KeyboardListener): _description_
        mouse_listener (MouseListener): _description_
    """
    # idle_listener.join()
    keyboard_listener.join()
    mouse_listener.join()


def update_time(*args) -> None:
    """Update the time of the last user input."""

    global last_action_time
    last_action_time = datetime.now()


def get_screen_width() -> int:
    """Get the width of the primary monitor

    Returns:
        int: width of the primary monitor
    """
    monitor = get_monitors()[0]

    for monitor_elem in get_monitors()[1:]:
        if monitor_elem.is_primary:
            monitor = monitor_elem
    return monitor.width


def make_move(mouse: Controller, screen_width: int) -> None:
    """Move the mouse and return it to the starting position.

    Args:
        mouse (Controller): mouse controll object
        screen_width (int): width of primary monitor
        x (int): x position of mouse
        y (int): y position of mouse
    """

    x, y = mouse.position

    if x < screen_width:
        mouse.position = (x+1, y)
    else:
        mouse.position = (x-1, y)

    mouse.position = (x, y)


def idle_process() -> None:
    """Process that runs only when there is no user input."""

    global last_action_time
    mouse = Controller()
    screen_width = get_screen_width()

    while True:
        sleep(15)

        now = datetime.now()
        durration = now - last_action_time
        idle_seconds = 30.

        if durration.total_seconds() > idle_seconds:
            make_move(mouse, screen_width)


def main() -> None:
    idle_listener, keyboard_listener, mouse_listener = setup_listeners()
    start_listeners(idle_listener, keyboard_listener, mouse_listener)
    join_listeners(idle_listener, keyboard_listener, mouse_listener)


if __name__ == '__main__':
    last_action_time = datetime.now()
    main()
