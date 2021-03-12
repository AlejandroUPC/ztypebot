import cv2 as cv
import pyautogui
import numpy as np
import pytesseract
import time
from pynput.keyboard import Controller
import config
from processing import img_processing
import logging

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] - %(levelname)s [%(pathname)s at %(lineno)d]: %(message)s', datefmt='%d-%b-%y %H:%M:%S',level=logging.DEBUG)
    if not config.DEBUG_LOGGING:
        logging.getLogger().disabled = True 
    logging.debug(f'Starting ZtypeBot in {config.START_WAIT} seconds...')
    keyboard = Controller()
    time.sleep(config.START_WAIT)
    while (True):
        screenshot = pyautogui.screenshot(region=config.REGION)
        screenshot_array = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot_array, cv.COLOR_RGB2BGR)
        list_words = img_processing.extract_words(screenshot,screenshot_array)
        logging.debug(f'Words detected [{len(list_words)}]:,\n{list_words}')
        for word in list_words:
            for letter in word:
                time.sleep(config.ACTION_DELAY)
                keyboard.press(letter)
                
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            logging.debug('ZTypeBot has been killed.')
            break

