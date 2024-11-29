import time
import os
import win32api
import win32con
import win32gui
from pynput import mouse, keyboard
from pynput.keyboard import Listener as KeyboardListener
# from pynput.keyboard import Key
#
# import pystray
# from pystray import MenuItem as item

import psutil

class Script:
    def __init__(self, hwnd):
        self.mouse_listener = self.mouse_listener()
        self.keyboard_listener = self.keyboard_listener()
        self.hwnd = hwnd
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()

        closeBtn = Mapping()
        closeBtn.x1, closeBtn.y1 = 1322, 293
        closeBtn.x2, closeBtn.y2 = 1340, 310
        closeBtn.x, closeBtn.y = 1329, 303

        Free = Mapping()
        Free.x1, Free.y1 = 0, 400
        Free.x2, Free.y2 = 1920, 1080
        Free.x, Free.y = None, None

        self.instaClose = False

        self.ench = []
        self.ench.append(closeBtn)
        self.ench.append(Free)

        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.keyboard_listener.join()
        self.mouse_listener.join()

    def silentClick(self, x, y):
        lParam = win32api.MAKELONG(x, y)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lParam)

    def mouse_listener(self):
        def on_click(x, y, button, pressed):
            if win32gui.GetForegroundWindow() == self.hwnd:
                if button == mouse.Button.left and pressed:
                    for ench in self.ench:
                        if ench.x1 <= x <= ench.x2 and ench.y1 <= y <= ench.y2:
                            self.silentClick(ench.x if ench.x else x, ench.y if ench.y else y)
                            if self.instaClose:
                                print('try')
                                self.silentClick(ench.x if ench.x else x, ench.y if ench.y else y)
                                self.silentClick(ench.x if ench.x else x, ench.y if ench.y else y)
                                self.silentClick(ench.x if ench.x else x, ench.y if ench.y else y)
                                self.silentClick(ench.x if ench.x else x, ench.y if ench.y else y)

                            self.mouse_listener._suppress = True
                else:
                    self.mouse_listener._suppress = False
            else:
                self.mouse_listener._suppress = False

        def win32_event_filter(msg, data):
            if msg == 513:
                self.mouse_listener._suppress = False
                return True
            else:
                self.mouse_listener._suppress = False
            return True

        return mouse.Listener(
            on_click=on_click,
            win32_event_filter=win32_event_filter,
            suppress=False
        )

    def keyboard_listener(self):
        def on_press(key):
            if win32gui.GetForegroundWindow() == self.hwnd:
                if key == keyboard.Key.caps_lock:
                    self.keyboard_controller.press(keyboard.Key.space)
                    self.keyboard_controller.release(keyboard.Key.space)
                    self.keyboard_controller.press(keyboard.Key.tab)
                    self.keyboard_controller.release(keyboard.Key.tab)
                    self.keyboard_controller.press(keyboard.Key.space)
                    self.keyboard_controller.release(keyboard.Key.space)
                elif key == keyboard.Key.ctrl_l:
                    print('down')
                    self.instaClose = True

        def on_release(key):
            if win32gui.GetForegroundWindow() == self.hwnd:
                if key == keyboard.Key.ctrl_l:
                    print('up')
                    self.instaClose = False


        return KeyboardListener(on_press=on_press, on_release=on_release)

    def start_listeners(self):
        self.mouse_listener.start()
        self.keyboard_listener.start()


class Mapping(dict):
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)


def on_quit(icon, item):
    icon.stop()

def get_window_titles():
    def _enum_windows_proc(hwnd, window_list):
        if win32gui.IsWindowVisible(hwnd):
            window_list.append((hwnd, win32gui.GetWindowText(hwnd)))

    window_list = []
    win32gui.EnumWindows(_enum_windows_proc, window_list)
    return window_list

from PIL import Image

def clear_recent_folder():
    recent_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Recent")
    for file in os.listdir(recent_folder):
        file_path = os.path.join(recent_folder, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def close_previous_instance():
    process_to_kill = 'pythonw.exe'
    my_pid = os.getpid()
    for p in psutil.process_iter():
        if p.name() == process_to_kill:
            if not p.pid == my_pid:
                p.terminate()

if __name__ == '__main__':
    close_previous_instance()
    clear_recent_folder()

    rageHwnd = None
    window_titles = get_window_titles()
    for hwnd, title in window_titles:
        if 'ult' in title:
            rageHwnd = hwnd
            break

    if rageHwnd:
        script = Script(rageHwnd)
    else:
        time.sleep(3)
