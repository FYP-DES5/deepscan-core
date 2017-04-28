import sys
import cv2
import pickle
import os
import numpy as np
import tempfile, shutil

class TempFolder:
    def __init__(self):
        self.folder = tempfile.mkdtemp()
    def __del__(self):
        if self.folder:
            shutil.rmtree(self.folder)
            self.folder = None
    def saveTempImage(self, img, ext='.png', verbose=False):
        preprocessImage(img, verbose)
        print 'ext: %s' % ext
        temp = tempfile.NamedTemporaryFile(delete=False, dir=self.folder, suffix=ext)
        if verbose:
            print 'Saving %s...' % temp.name
        _, buf = cv2.imencode(ext, img)
        temp.write(buf)
        temp.close()
        if verbose:
            print 'Saved %s.' % temp.name
        return temp.name
    def savePickle(self, obj, verbose=True):
        temp = tempfile.NamedTemporaryFile(delete=False, dir=self.folder, suffix='.p')
        if verbose:
            print 'Saving %s...' % temp.name
        pickle.dump(obj, temp)
        temp.close()
        if verbose:
            print 'Saved %s.' % temp.name
        return temp.name

def saveImage(name, img, bgr=False, verbose=False):
    name = os.path.abspath(name)
    if verbose:
        print 'Saving %s...' % name
    img = preprocessImage(img, bgr, verbose)
    if verbose:
        print '  imwrite call'
        print img
        print 'result: ' + str(cv2.imwrite(name, img))
    else:
        cv2.imwrite(name, img)
    if verbose:
        print 'Saved %s.' % name

def bgrToRgb(img):
    if img.shape[2] is 3:
        return img[:, :, [2, 1, 0]]
    else:
        return np.dsplit(img[:, :, [2, 1, 0, 3]], (3, 1))[0]

def preprocessImage(img, bgr=True, verbose=False):
    if len(img.shape) == 2:
        if verbose:
            print '  BW image detected'
            print '  dtype: ' + str(img.dtype)
        if img.dtype == 'uint16':
            img = np.vectorize(lambda x: x / 8)(img) # downgrade if it is the 11bit format
        img = np.dstack((img, img, img)) # K -> KKK
    elif bgr:
        if verbose:
            print '  changing bgr to rgb'
        img = bgrToRgb(img)
    return img
