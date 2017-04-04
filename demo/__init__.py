import cv2
from tkFileDialog import askopenfilename
from ..util import denoise

def denoising():
    print("Select a file")
    img = cv2.imread(askopenfilename())
    dst = denoise.medianBlur(img)
    cv2.imshow("original", img)
    cv2.imshow("denoised", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
