import numpy as np
import math

import cv2


def resizeImg(image, height=None, width=None):
	(w, h) = image.shape[:2]
	dim = None
	# if both the width and height are None, then return the
	# original image
	if width is None and height is None:
		return image

	# check to see if the width is None
	if width is None:
		# calculate the ratio of the height and construct the
		# dimensions
		r = height / float(h)
		dim = (int(w * r), height)

	# otherwise, the height is None
	else:
		# calculate the ratio of the width and construct the
		# dimensions
		r = width / float(w)
		dim = (int(h * r), width)

		# resize image
	resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
	return resized



class VideoRW():
	'''
		to read and write video by opencv functions
	'''
	def __init__(self, vid_path, save_path, height =None, width= None, cam=False):
		if cam:
			self.cap = cv2.VideoCapture(0)
		else:
			self.cap = cv2.VideoCapture(vid_path)


		self.frame_width = int( self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		self.frame_height =int( self.cap.get( cv2.CAP_PROP_FRAME_HEIGHT))
		self.fourcc = cv2.VideoWriter_fourcc(*'X264')

		if width is None:
			width = self.frame_width
		if height is None:
			height = self.frame_height

		self.out = cv2.VideoWriter(save_path, self.fourcc, 30.0, (width, height))



	def read(self):
		ret, frame = self.cap.read()
		return ret, frame


	def write(self, frame):
		self.out.write(frame)


	def __del__(self):
		self.cap.release()
		cv2.destroyAllWindows()


	

def rect_point_center(rect):
	'''
		to find the center of the point
	'''
	x1 = rect[0];
	y1 = rect[1];
	x2 = rect[2];
	y2 = rect[3];
	w = x2 - x1
	h = y2 - y1

	cx = int(x1 + (w+1)/2);
	cy = int(y1 + (h+1)/2);

	return (cx, cy);



def bbg_b(frame, rect):
	'''
		to make a black region to see the parameters clearly
	'''
	scale = (((rect[2] - rect[0])/frame.shape[0]))
	sc = (rect[3]-rect[1])/4
	frame[int(rect[1]-sc):rect[1], rect[0]:rect[2]] = [0, 0, 0]
	return scale


def bbg_p(frame, rect):
	scale = (((rect[2] - rect[0])/frame.shape[0]))
	sc = (rect[3]-rect[1])
	frame[int(rect[1]-sc):rect[1], rect[0]:rect[2]] = [0, 0, 0]
	return scale

def ybg_b(frame, rect):
	scale = (((rect[2] - rect[0])/frame.shape[0]))
	sc1 = (rect[2]-rect[0])/3
	sc2 = (rect[3]-rect[1])/2
	frame[rect[1]:int(rect[1]+sc2), rect[2]:int(rect[2]+sc1)] = [0, 250, 250]
	return scale

