import re
from typing import List, Tuple
import numpy as np
import cv2 as cv
import pytesseract
import logging
logger = logging.getLogger(__name__)
Words = str
BANNED_WORDS = [r'\x0c']


def extract_words(image_frame_ori, original_img) -> List[Words]:

    image_frame = np.array(image_frame_ori)
    image_frame = cv.cvtColor(image_frame, cv.COLOR_RGB2BGR)
    image_frame_hsv = cv.cvtColor(image_frame, cv.COLOR_BGR2HSV)
    orange_frame = _hsv_filter(
        image_frame_hsv, original_img, (60,35,140),(180,255,255))
    orange_words = pytesseract.image_to_string(orange_frame)
    normal_words = pytesseract.image_to_string(image_frame_ori)
    orange_words = _clear_list(orange_words)
    normal_words = _clear_list(normal_words)
    if orange_words:
        logger.debug(f'Orange words detected:\n{orange_words}')
    return orange_words+normal_words


def _hsv_filter(image_hsv, original_img, lower_filter: Tuple, higher_filter: Tuple):
    mask = cv.inRange(image_hsv, lower_filter, higher_filter)
    imask = mask > 0
    filtered_img = np.zeros_like(image_hsv, np.uint8)
    filtered_img[imask] = original_img[imask]
    (_, filtered_frame) = cv.threshold(filtered_img, 127, 255, cv.THRESH_BINARY)
    cv.imwrite('remove_me.png',filtered_frame)
    return filtered_frame


def _clear_list(raw_list: str) -> List[Words]:
    raw_list = raw_list.split('\n')
    list_sentences = []
    for word in raw_list:
        if word.strip() and word not in BANNED_WORDS and re.match('[a-z]+', word):
            list_sentences.append(re.match('[a-z]+', word).group(0))
    list_sentences = sorted(list_sentences, key=len)
    return list_sentences

