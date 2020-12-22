import cv2

import numpy as np

def type_color(crop, net):
	# this CNN requires fixed spatial dimensions for the input image(s)
	# so we need to ensure it is resized to (72, 72) 	           
	blob = cv2.dnn.blobFromImage(crop, 1.0,size=(72, 72))
	# set the blob as input to the network and perform a forward-pass to
	# obtain our output classification
	net.setInput(blob)
	layers = []
	layers.append("color")
	layers.append("type")

	out = net.forward(layers)
	# find the maximum classified value as a best score 
	color_index = np.argmax(out[0])
	type_index = np.argmax(out[1])

	return type_index, color_index