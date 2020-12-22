'''get idea:
https://github.com/Neoanarika/object-tracking-detection/blob/master/centroidtracker.py
'''
import numpy as np
from scipy.spatial import distance as dist
from collections import OrderedDict



class Tracker():
	def __init__(self, maxDisappeared=20):
		# initialize the next unique object ID along with two ordered
		# dictionaries used to keep track of mapping a given object
		self.nextObjectID = 0
		self.objects = OrderedDict()
		self.disappeared = OrderedDict()

		# store the number of maximum consecutive frames a given
		# object is allowed to be marked as "disappeared" until we
		# need to remove the object from tracking
		self.maxDisappeared = maxDisappeared


	def addObject(self, rect):
		# when adding an object we use the next available object
		# ID to store the box
		self.objects[self.nextObjectID] = rect
		self.disappeared[self.nextObjectID] = 0
		self.nextObjectID += 1


	def removeObject(self, objectID):
		# to remove an object ID we delete the object ID from
		# both of our respective dictionaries
		del self.objects[objectID]
		del self.disappeared[objectID]


	def update(self, rects):
		# check to see if the list of input bounding box rectangles
		# is empty
		if len(rects) == 0:
			# loop over any existing tracked objects and mark them
			# as disappeared

			for objectID in list(self.disappeared.keys()).copy():
				self.disappeared[objectID] += 1

				# if we have reached a maximum number of consecutive
				# frames where a given object has been marked as
				# missing, remove it
				if self.disappeared[objectID] > self.maxDisappeared:
					self.removeObject(objectID)

			# return early as there are no boxes or tracking info
			# to update
			return self.objects


		# if we are currently not tracking any objects take the input
		# boxes and add each of them
		if len(self.objects) == 0:
			for i in range(0, len(rects)):
				self.addObject(rects[i])


		# otherwise, are are currently tracking objects so we need to
		# try to match the input boxes to existing object
		# boxes
		else:
			# grab the set of object IDs and corresponding boxes
			objectIDs = list(self.objects.keys())
			objectRects = list(self.objects.values())

			# compute the distance between each pair of boxes, respectively
			# to check if they are match 
			D = dist.cdist(np.array(objectRects), rects)

			# in order to perform this matching we must (1) find the
			# smallest value in each row and then (2) sort the row
			# indexes based on their minimum values so that the row
			# with the smallest value as at the *front* of the index
			# list
			rows = D.min(axis=1).argsort()

			# next, we perform a similar process on the columns by
			# finding the smallest value in each column and then
			# sorting using the previously computed row index list
			cols = D.argmin(axis=1)[rows]

			# in order to determine if we need to update, add,
			# or remove an object we need to keep track of which
			# of the rows and column indexes we have already examined
			usedRows = set()
			usedCols = set()

			# loop over the combination of the (row, column) index
			# tuples
			for (row, col) in zip(rows, cols):
				# if we have already examined either the row or
				# column value before, ignore it
				# val
				if row in usedRows or col in usedCols:
					continue

				# otherwise, grab the object ID for the current row,
				# set its new box, and reset the disappeared
				# counter
				objectID = objectIDs[row]
				self.objects[objectID] = rects[col]
				self.disappeared[objectID] = 0

				# indicate that we have examined each of the row and
				# column indexes, respectively
				usedRows.add(row)
				usedCols.add(col)

			# compute both the row and column index we have NOT yet
			# examined
			unusedRows = set(range(0, D.shape[0])).difference(usedRows)
			unusedCols = set(range(0, D.shape[1])).difference(usedCols)

			# in the event that the number of object boxes is
			# equal or greater than the number of input boxes
			# we need to check and see if some of these objects have
			# potentially disappeared
			if D.shape[0] >= D.shape[1]:
				# loop over the unused row indexes
				for row in unusedRows:
					# grab the object ID for the corresponding row
					# index and increment the disappeared counter
					objectID = objectIDs[row]
					self.disappeared[objectID] += 1

					# check to see if the number of consecutive
					# frames the object has been marked "disappeared"
					# for warrants remove the object
					if self.disappeared[objectID] > self.maxDisappeared:
						self.removeObject(objectID)

			# otherwise, if the number of input boxes is greater
			# than the number of existing object boxes we need to
			# add each new input box as a trackable object
			else:
				for col in unusedCols:
					self.addObject(rects[col])

		# return the set of trackable objects
		return self.objects



