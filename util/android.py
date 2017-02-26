"""
Simple wrappers to adb commands
"""

import subprocess
import os
import tempfile
import os
import numpy as np
from os.path import isfile, join
import shutil
import cv2

__dir = '/'.join(__file__.split('/')[0:-1])

# LG V10
androidDir = '/storage/self/primary/DCIM/SimpleCamera'

# Lenovo A7000 Plus
# androidDir = '/storage/sdcard0/DCIM'

def capture():
  """Presses shutter button. An image should appear in the DCIM folder of the phone."""
  __call(__dir + '/adb shell "input keyevent KEYCODE_CAMERA"')

def fetchImage(rot90=0):
  """
  fetchImage(rot90=0) -> image (3D NumPy array, size (w, h, 3))

  Fetches the first image from the DCIM folder inside the phone and pulls it into a temporary directory. After reading the pulled image, deletes the content of both the phone's DCIM folder and the temporary folder.

  Optional parameter specifies how many times rotation is needed.
  """
  path = tempfile.mkdtemp() # make temp folder
  __copy(path) # pull image from phone to computer
  clean() # delete all images on the phone
  files = [f for f in os.listdir(path) if isfile(join(path, f))]
  if len(files) < 1:
    shutil.rmtree(path) # remove temp folder
    return None
  img = cv2.imread(join(path, files[0]))
  shutil.rmtree(path) # remove temp folder
  return np.rot90(img, k=rot90)

def focus():
  """Presses focus button"""
  __call(__dir + '/adb shell "input keyevent KEYCODE_FOCUS"')

def startCamera():
  """Sends a IMAGE_CAPTURE intent, thus opening the camera app"""
  __call(__dir + '/adb shell "am start -a android.media.action.IMAGE_CAPTURE"')

def __call(command):
  subprocess.call(command, shell=True)

def clean():
  """Cleans (deletes content of) DCIM directory."""
  __call(__dir + '/adb shell "rm ' + androidDir + '/*"')

def __copy(path):
  __call(__dir + '/adb pull ' + androidDir + ' ' + path)
