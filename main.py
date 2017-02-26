import sys
import os
import re
import inquirer
from util import kinect, format, capture, android, screen

def initialize():
    screen.greeting()
    VERSION_QID = "VERSION_QID"
    DEBUG_QID = "DEBUG_QID"
    questions = []
    questions.append(inquirer.Confirm(DEBUG_QID,
      message="Enable Logging"))
    questions.append(inquirer.List(VERSION_QID,
      message="Please state your Kinect version",
      choices=['v1', 'v2']))
    answers = inquirer.prompt(questions)
    kinect.init(answers[VERSION_QID])

def enableDebuggingLog():
    questions = [
        inquirer.Confirm('debug', message="Enable Logging")
    ]
    answers = inquirer.prompt(questions)
    return answers['debug']

def deviceTypeDetection():
    questions = [
        inquirer.Text('deviceRevision',
                  message="Please state your Kinect version (v1 / v2)")
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


promptMainMenu()
