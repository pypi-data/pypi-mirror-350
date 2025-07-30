import multiprocessing as mp
import subprocess
import struct
import random
import atexit
import os

class CAVA:
    def __init__(self, bars=10, callback=print,config=""):
        self.id = random.randint(11111,99999)
        os.system(f"""
        echo "
        [general]
        bars = {bars}
        {config}

        [output]
        method = raw
        raw_target = /tmp/cava_{self.id}.fifo
        " > /tmp/cava_{self.id}
        """)
        self._process = subprocess.Popen(args=[f"cava -p /tmp/cava_{self.id} > /dev/null 2>&1"],shell=True,start_new_session=True)
        while not os.path.exists(f"/tmp/cava_{self.id}.fifo"):pass
        self._process2 = None
        self._fifo = open(f"/tmp/cava_{self.id}.fifo", "rb")
        self._chunk = bars
        self._callback = callback
        self.samples = []
        
        atexit.register(self.close)
        
    def close(self):
        atexit.unregister(self.close)
        self._fifo.close()
        if self._process2:
            self._process2.kill()
        self._process.kill()
        os.remove(f"/tmp/cava_{self.id}")
        os.remove(f"/tmp/cava_{self.id}.fifo")
    
    def _run(self):
        while True:
            data = self._fifo.read(self._chunk)
            if len(data) < self._chunk:
                break
            sample = [i / 255 for i in struct.unpack("B" * self._chunk,data)]
            self.samples.append(sample)
            self._callback(tuple(sample))

    def start(self):
        self._process2 = mp.Process(target=self._run)
        self._process2.start()

