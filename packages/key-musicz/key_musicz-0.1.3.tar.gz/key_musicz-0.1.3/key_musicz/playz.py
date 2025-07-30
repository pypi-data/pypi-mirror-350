#
from buildz import Base
from . import soundz, sourcez
import time,threading
class Play(Base):
    def init(self, source, sound=None, fps=10, sample_rate = 44100):
        if sound is None:
            sound = soundz.Sound(rate=sample_rate)
        if type(source)==str:
            source = sourcez.Source(source, sample_rate)
        self.source = source
        self.sound = sound
        self.fps = fps
        self.running = True
        self.done_run = False
        self.select = self.source.select
        self.press=self.source.press
        self.unpress = self.source.unpress
        self.th = None
    def start(self):
        if self.th is not None:
            return
        self.th = threading.Thread(target=self.loop, daemon=True)
        self.th.start()
    def stop(self):
        self.running = False
    def close(self):
        self.stop()
        while not self.done_run and self.th is not None:
            time.sleep(0.1)
        self.source.close()
        self.sound.close()
    def loop(self):
        self.running = True
        self.done_run = False
        try:
            while self.running:
                dt = self.source.read(1.0/self.fps)
                self.sound.add(dt)
        finally:
            self.done_run = True

pass