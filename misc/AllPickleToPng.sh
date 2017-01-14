#!/bin/sh

ls *.p | xargs -L 1 ./PickleToPng.py
