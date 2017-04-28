import socket
import numpy as np
import core
from util import format
from experimental import mockVisualizer

class Server:
    def __init__(self, hostname='0.0.0.0', port=1080):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((hostname, port))
        self.s.listen(1)
        self.kinectStarted = False
        self.tempFolder = format.TempFolder()
    def start(self):
        print 'waiting for connection...'
        self.conn, self.addr = self.s.accept()
        try:
            while 1:
                print 'waiting for data...'
                self.opcode = self.recvUint8()
                print 'data: %d' % self.opcode
                if not self.opcode:
                    break
                self.opcode = self.opcode
                if self.opcode is 1: # start
                    if not self.kinectStarted:
                        core.start()
                        self.kinectStarted = True
                        self.sendSuccess()
                    else:
                        self.sendFail()
                elif self.opcode is 2: # end
                    if self.kinectStarted:
                        kinect.stop()
                    self.sendSuccess()
                elif self.opcode is 3: # zero
                    if not self.kinectStarted:
                        self.sendFail()
                    else:
                        core.zero()
                        self.sendSuccess()
                elif self.opcode is 4: # scan
                    if not self.kinectStarted:
                        self.sendFail()
                    else:
                        flags = self.recvUint8()
                        gridsize = self.recvFloat64()
                        ext = self.recvStr(self.recvInt32())
                        rawData = flags & 1
                        showIntemediate = flags & 2
                        if rawData:
                            img, raw = core.scan(rawData=rawData, showIntemediate=showIntemediate,
                                gridsize=gridsize,
                                tempFolder=self.tempFolder.folder)
                        else:
                            img = core.scan(rawData=rawData, showIntemediate=showIntemediate,
                                gridsize=gridsize,
                                tempFolder=self.tempFolder.folder)
                        # arr = np.arange(3*15*10, dtype=np.uint8).reshape((10, 15, 3))
                        if not img:
                            self.sendFail()
                            continue
                        self.sendSuccess()
                        # self.sendImage(arr)
                        self.sendImage(img, ext)
                        if rawData:
                            self.sendRawBuffer(raw)
                elif self.opcode is 5: # get image
                    if not self.kinectStarted:
                        self.sendFail()
                    else:
                        arr = kinect.getVideo()
                        self.sendSuccess()
                        self.sendImage(arr)
                elif self.opcode is 6: # start visualizer
                    self.sendSuccess()
                    mockVisualizer.start()
                elif self.opcode is 7: # cleanup temp folder
                    del self.tempFolder
                    self.tempFolder = format.TempFolder()
                    self.sendSuccess()
                elif self.opcode is 8: # depth image
                    if not self.kinectStarted:
                        self.sendFail()
                    else:
                        arr = kinect.getDepth()
                        self.sendSuccess()
                        self.sendImage(arr)
                elif self.opcode is 9: # mesh only
                    if not self.kinectStarted:
                        self.sendFail()
                    else:
                        core.scan(showMeshOnly=True, tempFolder=self.tempFolder.folder)
                        self.sendSuccess()
        finally:
            self.conn.close()
    def sendSuccess(self):
        self.conn.send(np.uint8(0).tobytes())
        self.conn.send(np.uint8(self.opcode).tobytes())
    def sendFail(self):
        self.conn.send(np.uint8(1).tobytes())
        self.conn.send(np.uint8(self.opcode).tobytes())
    def sendImage(self, arr, ext='.png'):
        self.conn.send(self.tempFolder.saveTempImage(arr, ext))
    def sendRawBuffer(self, obj):
        self.conn.send(self.tempFolder.savePickle(obj))
    def recvUint8(self):
        print 'recv uint8'
        r = ord(self.conn.recv(1))
        print r
        return r
    def recvInt32(self):
        print 'recv int32'
        r = np.frombuffer(self.conn.recv(4), dtype=np.int32)[0]
        print r
        return r
    def recvFloat64(self):
        print 'recv float64'
        r = np.frombuffer(self.conn.recv(8), dtype=np.float64)[0]
        print r
        return r
    def recvStr(self, size):
        print 'recv char[%d]' % size
        r = self.conn.recv(size)
        print r
        return r
Server().start()
