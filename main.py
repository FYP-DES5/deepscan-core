from __future__ import print_function
import inquirer, cv2
from Tkinter import Tk
from tkFileDialog import askopenfilename
from collections import OrderedDict
from util import kinect, format, capture, android, screen, denoise

def initialize():
    Tk().withdraw()
    screen.greeting()
    VERSION_QID = "VERSION_QID"
    DEBUG_QID = "DEBUG_QID"
    questions = []
    questions.append(inquirer.Confirm(DEBUG_QID,
        message="Enable Logging"))
    questions.append(inquirer.List(VERSION_QID,
        message="Please state your Kinect version",
        choices=["v1", "v2", "dryrun"]))
    answers = inquirer.prompt(questions)
    kinect.init(answers[VERSION_QID])

def denoiseDemo():
    print("Select a file")
    img = cv2.imread(askopenfilename())
    dst = denoise.medianBlur(img)
    cv2.imshow("original", img)
    cv2.imshow("denoised", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True

class Menu:
    def __init__(self, name="Main", root=True, layers=[]):
        self.name = name
        self.layers = layers + [name]
        self.__backName = "Quit" if root else "Back"
        self.__message = " > ".join(self.layers)
        self.__operations = OrderedDict([(self.__backName, lambda: False)])

    def appendOperation(self, name, operation):
        self.__operations[name] = operation
        del self.__operations[self.__backName]
        self.__operations[self.__backName] = lambda: False

    def appendMenu(self, name):
        menu = Menu(name, False, self.layers)
        self.appendOperation(name + " [+]", menu.show)
        return menu

    def show(self):
        while True:
            answers = inquirer.prompt([inquirer.List(None,
                message = self.__message,
                choices = list(self.__operations)
            )])
            if not self.__operations[answers[iter(answers).next()]]():
                return True

initialize()
main = Menu()
main.appendMenu("Calibration")
main.appendOperation("Denoising", denoiseDemo)
main.appendMenu("Segmentation")
main.appendMenu("Triangulation")
main.appendMenu("ConformalMapping")
main.appendMenu("Debug")
main.show()
