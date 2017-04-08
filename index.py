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
                opcode = self.conn.recv(1)
                print 'data: %s' % opcode
                if not opcode:
                    break
                opcode = ord(opcode[0])
                print opcode is 1, opcode is 2, opcode is 3, opcode is 4, opcode is 5, opcode is 6
                print opcode == 1, opcode == 2, opcode == 3, opcode == 4, opcode == 5, opcode == 6
                if opcode is 1: # start
                    if not self.started:
                        core.start()
                        self.sendSuccess()
                    else:
                        self.sendFail()
                elif opcode is 2: # end
                    if self.started:
                        kinect.stop()
                    self.sendSuccess()
                elif opcode is 3: # zero
                    if not self.started:
                        self.sendFail()
                    else:
                        core.zero()
                        self.sendSuccess()
                elif opcode is 4: # scan
                    if not self.started:
                        self.sendFail()
                    else:
                        arr = core.scan()
                        arr = np.arange(3*15*10, dtype=np.uint8).reshape((10, 15, 3))
                        self.sendSuccess()
                        self.sendArr(arr)
                elif opcode is 5: # get image
                    if not self.started:
                        self.sendFail()
                    else:
                        arr = kinect.getVideo()
                        arr = np.arange(3*15*10, dtype=np.uint8).reshape((10, 15, 3))
                        self.sendSuccess()
                        self.sendArr(arr)
                elif opcode is 6: # start visualizer
                    self.sendSuccess()
                    mockVisualizer.start()
        finally:
            self.conn.close()
    def sendSuccess(self):
        self.conn.send(np.uint8(0).tobytes())
    def sendFail(self):
        self.conn.send(np.uint8(1).tobytes())
    def sendArr(self, arr):
        self.conn.send(np.array(arr.shape, dtype=np.uint32).tobytes('C'))
        self.conn.send(arr.tobytes('C'))

Server().start()
