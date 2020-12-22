import cv2

import numpy as np
import pytesseract
from skimage.segmentation import clear_border




def build_tesseract_options(psm=7):
	# only OCR alphanumeric characters for tesseract function
	alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	options = "-c tessedit_char_whitelist={}".format(alphanumeric)
	# set the PSM mode
	options += " --psm {}".format(psm)
	# return the built options string
	return options


def build_tesseract_text(crop_plate):
	crop_plate = cv2.cvtColor(crop_plate, cv2.COLOR_BGR2GRAY)
	image = cv2.resize(crop_plate, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
	# adaptive filter
	thre = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
	cv2.THRESH_BINARY_INV,11,2) 
	# guassian filter
	blur = cv2.GaussianBlur(thre,(5,5),0)
	# Otsu's thresholding after Gaussian filtering
	retval, threshold = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	# clear any foreground pixels touching the border of the image
	threshold = clear_border(threshold)
	# options to configure the tesseract function
	options = build_tesseract_options(psm=7)
	# applying the tesseract function to recognize the text
	text = pytesseract.image_to_string(threshold , config=options)

	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()


