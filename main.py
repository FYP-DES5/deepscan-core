import sys
import os
import re
import inquirer
import util.screen

util.screen.greeting()

def enableDebuggingLog():
	questions = [
		inquirer.Confirm('debug', message="Enable Logging")
	]
	answers = inquirer.prompt(questions)
	return answers['debug']

def deviceTypeDetection():
	questions = [
		inquirer.Text('deviceRevision',
                  message="Please state your Kinect version (v1 / v2)"),
	]
	answers = inquirer.prompt(questions)
	return answers['deviceRevision']

def promptMainMenu():
	questions = [
	inquirer.List('action', message="Which operations do you want to perform?", 
		choices=['Calibration', 'Denoising', 'Segmentation', 'ConformalMapping', 'Debug'],
		)
	]
	answers = inquirer.prompt(questions)
	return answers['action']

enableDebuggingLog()
device = deviceTypeDetection()

if device == 'v1':
	import freenect
elif device == 'v2':
	from pylibfreenect2 import Freenect2, SyncMultiFrameListener

promptMainMenu()
