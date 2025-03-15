import time
import psutil
from pynput import mouse, keyboard
from threading import Thread


class UserMonitor:
    def __init__(self):
        self.running = False
        self.processes = set()
        self.mouse_listener = None
        self.keyboard_listener = None

    def log_action(self, message):
        print(f"{time.ctime()}: {message}")

    def monitor_processes(self):
        while self.running:
            current_processes = {p.info["name"] for p in psutil.process_iter(['name'])}
            new_processes = current_processes - self.processes

            for proc in new_processes:
                if proc:
                    self.log_action(f"Starting program: {proc}")

            closed_processes = self.processes - current_processes
            for proc in closed_processes:
                if proc:
                    self.log_action(f"Closed program: {proc}")

            self.processes = current_processes
            time.sleep(1)
    
    def on_click(self, x, y, button, pressed):
        if pressed:
            self.log_action(f"Клик мыши: {button} на позиции ({x}, {y})")

    def on_scroll(self, x, y, dx, dy):
        self.log_action(f"Прокрутка мыши: ({dx}, {dy}) на позиции ({x}, {y})")

    def on_press(self, key):
        try:
            self.log_action(f"Нажата клавиша: {key.char}")
        except AttributeError:
            self.log_action(f"Нажата специальная клавиша: {key}")

    def on_release(self, key):
        pass

    def start(self):
        if not self.running:
            self.running = True
            self.processes = {p.info["name"] for p in psutil.process_iter(['name'])}

            process_thread = Thread(target=self.monitor_processes)
            process_thread.daemon = True
            process_thread.start()

            self.mouse_listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll)
            self.mouse_listener.start()

            self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.keyboard_listener.start()

            self.log_action("Start")

    def stop(self):
        if self.running:
            self.running = False
            if self.mouse_listener:
                self.mouse_listener.stop()
            if self.keyboard_listener:
                self.keyboard_listener.stop()
            self.log_action("Stop")

    