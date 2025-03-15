from PyQt6.QtCore import QTimer

class LoadingScreen:
    def __init__(self, parent):
        self.parent = parent

    def show(self, duration=2000, callback=None):
        self.parent.show_loading()
        QTimer.singleShot(duration, lambda: self.finish(callback))

    def finish(self, callback):
        self.parent.hide_loading()
        if callback:
            callback()