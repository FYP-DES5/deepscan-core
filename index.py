import socket
import numpy as np
import core
from experimental import mockVisualizer

class Server:
    def __init__(self, hostname='0.0.0.0', port=1080):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((hostname, port))
        self.s.listen(1)
        self.kinectStarted = False
    def start(self):
        print 'waiting for connection...'
        self.conn, self.addr = self.s.accept()
        try:
            while 1:
                print 'waiting for data...'
                self.opcode = self.conn.recv(1)
                print 'data: %s' % self.opcode
                if not self.opcode:
                    break
                self.opcode = ord(self.opcode[0])
                print self.opcode is 1, self.opcode is 2, self.opcode is 3, self.opcode is 4, self.opcode is 5, self.opcode is 6
                print self.opcode == 1, self.opcode == 2, self.opcode == 3, self.opcode == 4, self.opcode == 5, self.opcode == 6
                if self.opcode is 1: # start
                    if not self.started:
                        core.start()
                        self.sendSuccess()
                    else:
                        self.sendFail()
                elif self.opcode is 2: # end
                    if self.started:
                        kinect.stop()
                    self.sendSuccess()
                elif self.opcode is 3: # zero
                    if not self.started:
                        self.sendFail()
                    else:
                        core.zero()
                        self.sendSuccess()
                elif self.opcode is 4: # scan
                    if not self.started:
                        self.sendFail()
                    else:
                        arr = core.scan()
                        arr = np.arange(3*15*10, dtype=np.uint8).reshape((10, 15, 3))
                        self.sendSuccess()
                        self.sendArr(arr)
                elif self.opcode is 5: # get image
                    if not self.started:
                        self.sendFail()
                    else:
                        arr = kinect.getVideo()
                        arr = np.arange(3*15*10, dtype=np.uint8).reshape((10, 15, 3))
                        self.sendSuccess()
                        self.sendArr(arr)
                elif self.opcode is 6: # start visualizer
                    self.sendSuccess()
                    mockVisualizer.start()
        finally:
            self.conn.close()
    def sendSuccess(self):
        self.conn.send(np.uint8(0).tobytes())
        self.conn.send(np.uint8(self.opcode).tobytes())
    def sendFail(self):
        self.conn.send(np.uint8(1).tobytes())
        self.conn.send(np.uint8(self.opcode).tobytes())
    def sendArr(self, arr):
        self.conn.send(np.array(arr.shape, dtype=np.uint32).tobytes('C'))
        self.conn.send(arr.tobytes('C'))

Server().start()
