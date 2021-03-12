if __name__=='__main__':
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import config
    import pyautogui
    import numpy as np
    from config import REGION

    import cv2 as cv


    screenshot = pyautogui.screenshot(region=REGION)
    left, top, right, bottom = REGION
    cv.imwrite(f'{left}_{top}_{right}_{bottom}.png',np.array(screenshot))