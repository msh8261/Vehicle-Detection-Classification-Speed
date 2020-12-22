import sys

import tkinter as tk
from tkinter import Tk, Frame, Canvas, Button 
from tkinter import TOP, BOTTOM, RIGHT, LEFT, NW, Entry, END, YES
from tkinter import messagebox
from tkinter import filedialog
import PIL.Image, PIL.ImageTk

import cv2

import numpy as np
import xlsxwriter 

from src.database import create_connection, insert_data
from src.config import database



class videoGUI:

	def __init__(self, window, window_title, worksheet, app):

		self.worksheet = worksheet
		self.row = 1

		self.app = app

		self.window = window
		self.window.title(window_title)

		top_frame = Frame(self.window)
		top_frame.pack(side=TOP, pady=5)

		left_frame = Frame(self.window)
		left_frame.pack(side=LEFT, pady=5)

		self.btm_frame1 = Frame(self.window)
		self.btm_frame1.place(height=20, x=130, y=680)
		self.btm_frame2 = Frame(self.window)
		self.btm_frame2.place(height=120, x=130, y=700)

		# pt = Table(btm_frame)
		# pt.show() 

		self.pause = False   # Parameter that controls pause button

		self.canvas = Canvas(left_frame)
		self.canvas.pack()

		# Select Button
		self.btn_select=Button(top_frame, text="Select", background = 'gray', fg = 'black', width=10, command=self.open_file)
		self.btn_select.grid(row=0, column=0)

		# Play Button
		self.btn_play=Button(top_frame, text="Play", background = 'gray', width=10, command=self.play_video)
		self.btn_play.grid(row=0, column=1)

		# Pause Button
		self.btn_pause=Button(top_frame, text="Pause", background = 'gray', width=10, command=self.pause_video)
		self.btn_pause.grid(row=0, column=2)

		# Resume Button
		self.btn_resume=Button(top_frame, text="resume", background = 'gray', width=10, command=self.resume_video)
		self.btn_resume.grid(row=0, column=3)

		self.delay = 15   # ms

		self.lst = []

		self.h_size = 400
		self.w_size = 600
		
		self.window.mainloop()




	def open_file(self):

		self.pause = False

		self.filename = filedialog.askopenfilename(title="Select file", filetypes=(("MP4 files", "*.mp4"),
																						 ("WMV files", "*.wmv"), ("AVI files", "*.avi")))
		print(self.filename)

		# Open the video file
		self.cap = cv2.VideoCapture(self.filename)

		self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


		self.canvas.config(width = self.width, height = self.height)


	def table_h(self, total_columns=5):
		header = ['id', 'color', 'type', 'speed', 'plate']
		for j in range(total_columns):        
			e = Entry(self.btm_frame1, width=20, background = 'blue', fg='black', 
							   font=('Arial',12,'bold'))				  
			e.grid(row=0, column=j)
			e.insert(END, header[j])      

	
	def table(self, lst):
		self.lst = lst
		total_rows = len(lst) 
		total_columns = len(lst[0])
		# create a database connection
		conn = create_connection(database)
		#with conn:

		for i in range(total_rows):
			insert_data(conn, lst[i]) 
			for j in range(total_columns):     
				e = Entry(self.btm_frame2, width=20, background = 'gray', fg='black', 
							   font=('Arial',12,'bold')) 				  
				e.grid(row=i, column=j)
				e.insert(END, lst[i][j]) 


	def table_del(self):
		lst = self.lst
		total_rows = len(lst) 
		total_columns = len(lst[0])
		for i in range(total_rows):
			for j in range(total_columns):     
				e = Entry(self.btm_frame2, width=20, background = 'gray', fg='black', 
							   font=('Arial',12,'bold')) 				  
				e.grid(row=i, column=j)
				e.delete(END, lst[i][j]) 


	def write_Exl_h(self):
		worksheet = self.worksheet
		worksheet.write('A1', 'ID') 
		worksheet.write('B1', 'Color') 
		worksheet.write('C1', 'Type') 
		worksheet.write('D1', 'Speed')
		worksheet.write('E1', 'Plate') 



	def write_Exl(self, lst):
		total_rows = len(lst) 
		worksheet = self.worksheet
		total_rows = len(lst)
		for i in range(total_rows):
			# iterating through content list 
			for j, item in enumerate(lst[i]): 
				#print(j, ",", item)
				if j == 0 or j == 3:  
					# write operation perform 
					worksheet.write(self.row, j, int(item)) 
				else:
					# write operation perform 
					worksheet.write(self.row, j, str(item)) 
			self.row += 1
			  
	
			  


	def get_frame(self):   # get only one frame
		try:
			if self.cap.isOpened():
				ret, frame = self.cap.read()
				return (ret, frame)
		except:
			messagebox.showerror(title='Video file not found', message='Please select a video file.')



	def play_video(self):
		# Get a frame from the video source, and go to the next frame automatically
		ret, frame0 = self.get_frame()

		if np.shape(frame0) == ():
			messagebox.showerror(title='Frame is NoneType', message='Please check the video file.')

		
		self.write_Exl_h()
		self.table_h(5)

		
		
		lst, frame = self.app.build_app(frame0)
		
		# if len(self.lst)>0:
		# 	self.table_del()

		if len(lst)>0:
			self.write_Exl(lst)
			# find total number of rows and 
			# columns in list 
			#print("===>>> size of detected: ", len(lst))
			self.table(lst) 

		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


		if ret:
			self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
			self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

		if not self.pause:
			self.window.after(self.delay, self.play_video)


	def pause_video(self):
		self.pause = True

#Addition
	def resume_video(self):
		self.pause=False
		self.play_video()



	# Release the video source when the object is destroyed
	def __del__(self):
		if self.cap.isOpened():
			self.cap.release()







