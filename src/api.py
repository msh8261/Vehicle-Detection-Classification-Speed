# import the necessary packages
import os, sys


os.environ["OMP_NUM_THREADS"]= '1'
os.environ["OMP_THREAD_LIMIT"] = '1'
os.environ["MKL_NUM_THREADS"] = '1'
os.environ["NUMEXPR_NUM_THREADS"] = '1'
os.environ["OMP_NUM_THREADS"] = '1'
os.environ["PAPERLESS_AVX2_AVAILABLE"]="false"
os.environ["OCR_THREADS"] = '1'

from src.config import color_classes, type_classes, fpath_vid, save_path, df
from src.config import fps, scale1, scale2, position1, position2 , carBoxWidht, carWidht
from src.config import car_detection_bin_model, car_detection_xml_model, car_classification_bin_model, car_classification_xml_model, plate_detecttion_bin_model, plate_detection_xml_model
from src.config import scale1, scale2, horizontal, dst, thr_box, thr_plate
from src.utils import VideoRW, resizeImg, rect_point_center, bbg_b, bbg_p, ybg_b


import cv2

# print("=====>>>>> cv2: ",cv2.__version__)
# print("=====>>>>> cv2: ",cv2.__file__)

import numpy as np
from src.speed import estimateSpeed
from src.typeClassify import type_color
from src.tracker import Tracker
from src.plateNumRecog import build_tesseract_options, build_tesseract_text
import time
import math


class Api():
	def __init__(self):

		# load the serialized model from disk
		self.net = cv2.dnn.readNet(car_detection_bin_model, car_detection_xml_model)
		self.net2 = cv2.dnn.readNet(car_classification_bin_model, car_classification_xml_model)
		self.net3 = cv2.dnn.readNet(plate_detecttion_bin_model, plate_detection_xml_model)


		# initialize the tracker and frame dimensions
		self.tr = Tracker(df)

		self.last_ids = []
		self.last_positions = []
		self.dt = 0
		self.frame_num = 1
		self.start = 0
		self.ppm = 0
		self.fn = 1
		self.ids = []
		self.fns = []
		self.ids2 = []
		self.sp = []
		self.cnt = 0





	def build_app(self, frame):

		# initiliaze the parameters
		fps0 = 25	

		xmin = 0
		ymin = 0
		xmax = 0
		ymax = 0

		w_size = 600
		h_size = 400

		speed = 0
		sp = []
		idsp = []


		# border for padding the croped image
		topBorderWidth = 300 
		bottomBorderWidth = 300 
		leftBorderWidth = 300 
		rightBorderWidth = 300 


		# resize the image to be same size for different input size
		frame = resizeImg(frame, h_size, w_size)
		# copy of frame
		frame_copy = frame.copy()

		# this CNN requires fixed spatial dimensions for the input image(s)
		# so we need to ensure it is resized to (672, 384) 
		blob = cv2.dnn.blobFromImage(frame, size=(672, 384))
		# set the blob as input to the network and perform a forward-pass to
		# obtain our output classification
		self.net.setInput(blob)
		out = self.net.forward()

		rects = []

		# make a ROI to estimate the speed
		pts = [(0,240), (420,240), (0,320), (440,320)]
		cv2.line(frame, pts[0],pts[1], (250,0,0), 2)
		cv2.line(frame, pts[2],pts[3], (250,0,0), 2)


		# loop over the predictions and display them
		for detection in out.reshape(-1, 7):
			confidence = float(detection[2])
			# the confidence above threshold can be proceed
			if confidence > thr_box:
				xmin = int(detection[3] * frame.shape[1])
				ymin = int(detection[4] * frame.shape[0])
				xmax = int(detection[5] * frame.shape[1])
				ymax = int(detection[6] * frame.shape[0])

				# check if boundig boxes are out of the frame size
				if (xmin < 0 or ymin < 0 or xmax >= frame.shape[1] or ymax >= frame.shape[0]):
				 continue
				
				# collect the high confidence detection boxes
				object_box = (xmin, ymin, (xmax), (ymax))
				rects.append(object_box)


		# update our centroid tracker using the computed set of bounding
		# box rectangles
		objects = self.tr.update(rects)

		list1 = []
		ids = []
		positions = []

		frame_cnt = 1


		# loop over the tracked objects
		for (trackID, rect) in objects.items():	
			

			if (rect[0] < 0 or rect[1] < 0 or rect[2] >= frame.shape[1] or rect[3] >= frame.shape[0]):
				continue


			if (rect[2] - rect[0]) < 100 or (rect[3] - rect[1]) < 100:
				continue
				
			
			carBoxWidth = (rect[2] - rect[0])
			carBoxHeight = (rect[3] - rect[1])

			croped = frame_copy[rect[1]:rect[3], rect[0]:rect[2]] 


			if np.shape(croped) == ():
				continue

          
			# resize the image to make it proper for calssification 
			resized_c = resizeImg(croped, h_size, w_size)

			# apply this function to get type and color of the vehicles
			# ["car", "bus", "truck", "van"] and ["white", "gray", "yellow", "red", "green", "blue", "black"]
			type_index, color_index = type_color(resized_c, self.net2)
			
			# find the centroid point of boxes for speed estimation 
			centroid = rect_point_center(rect)

			# check if vehicles pass the firt line of ROI
			if (centroid[1] <= pts[2][1] and centroid[1] > pts[0][1] and centroid[0] < pts[1][0]):
				# check the id if is not in the list
				if trackID not in self.ids:
					# collect ids and their frame number recorded 
					self.ids.append(trackID)
					self.fns.append(self.frame_num)

			# chekc if vehicles pass the second line of ROI
			if (centroid[1] <= pts[0][1] and centroid[0] < pts[1][0]):				
				# check if the id is in the list
				if trackID in self.ids:
					fps = fps0
					# find the index of the porposed id 
					ind = self.ids.index(trackID)
					# find the number of frame which take by proposed vehicle by passing the ROI
					frame_cnt = np.abs(self.fns[ind] - self.frame_num)
					# this function estimate the speed of the proposed vehicle
					speed0 = estimateSpeed(dst, frame_cnt, fps)
					speed = int(speed0)
					# collect the speed and its id
					self.sp.append(speed)
					self.ids2.append(trackID)
					# delete the index and id that already estimated
					self.ids.pop(ind)
					self.fns.pop(ind)
					
			
			
			speed_ = 0
			
			# show the speed of the vehicle that already estimated
			if trackID in self.ids2:
				ind = self.ids2.index(trackID)
				speed_ = self.sp[ind]
				sc = ybg_b(frame, rect)
				cv2.putText(frame, str(self.sp[ind]), (rect[2]+5, rect[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 2*sc, (0, 0, 0), 1)
				cv2.putText(frame, "Km/h", (rect[2]+5, rect[1]+40), cv2.FONT_HERSHEY_SIMPLEX, 2*sc, (0, 0, 0), 1)
				if self.cnt == 200:
					self.ids2.clear()
					self.sp.clear()
					self.cnt = 0 
				
			
			id_ = "{}".format(trackID)

			# show the parameters that already provided 
			cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0, 250, 0), 2)
			# make a black backgraound to see parameters clearly
			sc = bbg_b(frame, rect)
			cv2.putText(frame, (id_)+", "+(color_classes[color_index])+", "+(type_classes[type_index]), (rect[0], rect[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 2*sc, (0, 0, 250), 1)
			# show the center of the boxes
			cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 250), -1)


			# make a copy boorder to be proper for licence plate detection
			resized = cv2.copyMakeBorder(croped, 
										topBorderWidth, 
										bottomBorderWidth, 
										leftBorderWidth, 
										rightBorderWidth, 
										cv2.BORDER_CONSTANT, 
										value=(0,0,0)
										)

		
			# this CNN requires fixed spatial dimensions for the input image(s)
			# so we need to ensure it is resized to (300, 300) 
			blob3 = cv2.dnn.blobFromImage(resized, size=(300, 300))
			# set the blob as input to the network and perform a forward-pass to
			# obtain our output classification
			self.net3.setInput(blob3)
			out3 = self.net3.forward() 

			for detection in out3.reshape(-1, 7):
				confidence = float(detection[2])
				xmin_ = int(detection[3] * resized.shape[1])
				ymin_ = int(detection[4] * resized.shape[0])
				xmax_ = int(detection[5] * resized.shape[1])
				ymax_ = int(detection[6] * resized.shape[0])                                

				# suitable threshold and a max range for detected plate box
				if confidence > thr_plate and (ymax_ - ymin_) < 50:
					x1 = rect[0] + xmin_ - leftBorderWidth
					y1 = rect[1] + ymin_ - topBorderWidth
					x2 = rect[0] + xmax_ - rightBorderWidth
					y2 = rect[1] + ymax_ - bottomBorderWidth

					rect_ = (x1, y1, x2, y2)

					cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 250, 0), 2)

					
					croped_plate = resized[ymin_:ymax_, xmin_:xmax_]
					# the plate number can be read by this function
					text = build_tesseract_text(croped_plate)


					if text:
						sc = bbg_p(frame, rect_)
						cv2.putText(frame, text, (x1, y1-4), cv2.FONT_HERSHEY_SIMPLEX, 4*sc, (0, 0, 250), 1)
					else:
						text = "Not Recognized"

					# collect all parameters to save in database
					list1.append((trackID, color_classes[color_index], type_classes[type_index], (speed_), text))

			

		self.frame_num += 1
		self.cnt += 1



		return list1, frame



