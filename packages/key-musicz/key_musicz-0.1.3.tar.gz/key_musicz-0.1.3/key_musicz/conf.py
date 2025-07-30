#
from buildz import xf, fz, pyz, dz, Args, Base
import os
from . import playz, keyz
def fetch(keys, as_list = False):
    if type(keys) not in (list,tuple):
        #print(f"return not list", keys, as_list)
        if as_list:
            return [keys]
        return keys
    if as_list:
        rst = []
        for it in keys:
            rst+=fetch(it, as_list)
        #print("return list:", rst)
        return rst
    if len(keys)==2:
        if type(keys[0]) not in (list, tuple, dict) and keys[0]!='vals':
            rst = {}
            rst[keys[0]] = keys[1]
            return rst
        elif keys[0]=='vals' or (keys[0][0]=='vals' and len(keys[0])==1):
            rst = []
            for it in keys[1]:
                rst+= fetch(it, as_list)
            return rst
        elif keys[0][0] == 'vals':
            rst = [fetch(it, True) for it in keys[1]]
            ks = keys[0][1:]
            out = []
            for it in rst:
                tmp = {}
                for k,v in zip(ks, it):
                    tmp[k] = v
                out.append(tmp)
            return out
    temp = {}
    arr = []
    for it in keys:
        tmp = fetch(it, as_list)
        if type(tmp) == dict:
            temp.update(tmp)
        else:
            arr += tmp
    if len(arr)==0:
        return temp
    out = []
    for it in arr:
        dt = dict(temp)
        dt.update(it)
        out.append(dt)
    return out

def init(fp):
    conf = xf.loadxf(fp, as_args=True,spc=False)
    if isinstance(conf, Args):
        conf = conf.dicts
    ks, vs, inits= dz.g(conf, keys=[], vars={}, init={})
    if isinstance(ks, Args):
        ks = ks.as_list(cmb=0, item_args = False, deep=True)
    if isinstance(vs, Args):
        vs = vs.as_dict(True)
    if isinstance(inits, Args):
        inits = inits.as_dict(True)
    cmds = []
    for it in ks:
        cs = fetch(it)
        if type(cs) == dict:
            cs = [cs]
        cmds+=cs
    # print("orders:", cmds)
    # print("vars:", vs)
    # print("init:", inits)
    return cmds, vs, inits

pass
class Orders(Base):
    def init(self):
        self.orders = {}
    def set(self, key, fc):
        self.orders[key] = fc
    def call(self, maps, *args):
        maps = dict(maps)
        key = maps['action']
        del maps['action']
        return self.orders[key](*args, **maps)

pass
dp = os.path.dirname(__file__)
fp = os.path.join(dp, 'conf', 'play.js')
default_src = os.path.join(dp, 'res/FluidR3Mono_GM.sf2')
class Conf(Base):
    def init(self, fp, sys_sfile):
        self.to_stops = set()
        #self.play = play
        self.fp = fp
        cmds, vs, inits = init(fp)
        sfile, fps, select, sample_rate = dz.g(inits, sfile = default_src, fps=30, select={}, sample_rate=44100)
        sfile = sfile or default_src
        sfile = sys_sfile or sfile
        if not os.path.isfile(sfile):
            print(f"ERROR: sf2文件'{sfile}'不存在 / sf2 file '{sfile}' not exists")
            exit()
        play = playz.Play(sfile,fps=fps, sample_rate=sample_rate)
        play.select(**select)
        channel = dz.g(select, channel= 0)
        self.channel= channel
        self.play = play
        self.ks = keyz.Keys(self.press_callback)
        self.vars = vs
        self.baks = {}
        rst = {}
        for cmd in cmds:
            key = str(cmd['key'])
            rst[key] = cmd
        self.keys = rst
        #print(f"keys:", list(self.keys.keys()))
        self.build_fc()
        self.running = True
    def start(self):
        self.running = True
        self.play.start()
        self.ks.start()
    def close(self):
        self.ks.stop()
        self.play.stop()
        self.play.close()
    def quit(self, *a, **b):
        self.running = False
        input("press enter to quit:\n")
    def wait(self):
        import time
        while self.running:
            time.sleep(0.1)
    def press(self, do_press, label, var, val, **maps):
        if do_press:
            bak = self.vars[label][var]
            dz.dset(self.baks, [label, var], bak)
            self.vars[label][var] = val
        else:
            bak = self.baks[label][var]
            self.vars[label][var] = bak
    def change(self, do_press, label, var, val, **_):
        if not do_press:
            return
        self.vars[label][var] = val
    def mode(self, do_press, mode, **_):
        self.vars['mode'] = mode
    def sound(self, do_preess, label, sound, power=None, **_):
        vs = self.vars[label]
        n = vs['base']+sound
        if not do_preess:
            if self.vars['mode']==0:
                self.play.unpress(n, self.channel)
                self.to_stops.remove(n)
            return
        if power is None:
            power = vs['power']
        #print(f"play.press({n}, {power})")
        if n in self.to_stops:
            self.play.unpress(n, self.channel)
            self.to_stops.remove(n)
        self.play.press(n, power, self.channel)
        self.to_stops.add(n)
    def press_callback(self, char, press):
        #print(f"press:", char, press)
        if char not in self.keys:
            return
        maps = self.keys[char]
        self.orders(maps, press)
    def build_fc(self):
        self.orders = Orders()
        self.orders.set('press', self.press)
        self.orders.set('mode', self.mode)
        self.orders.set('quit', self.quit)
        self.orders.set('change', self.change)
        self.orders.set('sound', self.sound)



def test():
    dp = os.path.dirname(__file__)
    fp = os.path.join(dp, 'conf', 'play.js')
    import time,sys
    argv = sys.argv[1:]
    sfile = None
    if len(argv)>0:
        sfile = argv[0]
    conf = Conf(fp, sfile)
    conf.start()
    print("run success, enter '~' to quit")
    print("运行中,按下'~'键来退出")
    conf.wait()
    print("release")
    conf.close()

pass

pyz.lc(locals(), test)
