# import math
# import numpy as np


def estimateSpeed(dst, frame_num, fps):
	'''
		calculate the speed (distance/time) with constant distance (dst) which is known as a ROI from the place 
		we are going to estimate the vehicle speed, which is calculated here by Km/h
		km/h = m/s x 3600s/1000m
		time = Frame Per Second of the video/Number of frames for which the vehicle was inside ROI box
	'''
	speed = dst * (fps/frame_num) * 3.6 # 3600/1000
	return speed