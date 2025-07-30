#
import fluidsynth
import numpy as np
from buildz import Base
class Source(Base):
    def init(self, source, sample_rate = 44100):
        #print(f"sample_rate:", sample_rate)
        self.fs = fluidsynth.Synth()
        self.source = source
        self.sfid=self.fs.sfload(source)
        self.sample_rate = sample_rate
        self.do_select=False
    def get(self, sz=None):
        sz = sz or self.sample_rate
        return self.fs.get_samples(sz)
    def read(self, sec=1.0):
        sz = int(self.sample_rate*sec)
        return self.get(sz)
    def check_select(self):
        if not self.do_select:
            self.select()
    def select(self, channel=0, bank=0, preset=0):
        # 选择钢琴音色(通道0, 音色库0, 音色0)
        self.do_select = True
        self.fs.program_select(channel, self.sfid, bank, preset)
    def press(self, key, power=90, channel=0):
        self.check_select()
        self.fs.noteon(channel, key, power)
    def unpress(self, key, channel=0):
        self.check_select()
        self.fs.noteoff(channel, key)
    def close(self):
        self.fs.delete()
        self.fs = None

pass
