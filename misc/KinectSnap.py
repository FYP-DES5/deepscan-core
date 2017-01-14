#!/usr/bin/python

import freenect
import sys

freenect.sync_get_depth()[0].dump(sys.argv[-1] + "_depth.p")
freenect.sync_get_video()[0].dump(sys.argv[-1] + "_video.p")
