#coding=utf-8

from pynput.keyboard import Listener, Key
from buildz import Base
import threading
class Keys(Base):
    def char(self, key):
        if hasattr(key, "char"):
            return key.char
        return None
    def stop(self):
        self.lst.stop()
    def init(self, fc=None):
        '''
            callback: fc(char, press=bool)
        '''
        self.th = None
        self.fc = fc
        self.keys= set()
    def press(self, key):
        c = self.char(key)
        if c is not None:
            if c in self.keys:
                return
            self.keys.add(c)
            self.fc(c, True)
    def release(self, key):
        c = self.char(key)
        if c is not None:
            if c in self.keys:
                self.keys.remove(c)
            self.fc(c, False)
    def start(self):
        if self.th:
            return
        self.th = threading.Thread(target=self.run, daemon=True)
        self.th.start()
    def run(self):
        with Listener(on_press=self.press, on_release=self.release) as lst:
            self.lst = lst
            lst.join()

pass