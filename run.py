# import the necessary packages
import sys, os

f = os.path.dirname(__file__)


# print("="*20)
# print("==>>1: ", (os.path.dirname(sys.executable))+'/Library/bin')
# print("="*20)
# print("==>>2: ", os.listdir(sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))))
# print("="*20)



from tkinter import Tk
import xlsxwriter
from src.gui import videoGUI 
from src.api import Api

import matplotlib

# set matplotlib to not use the Xwindows backend
matplotlib.use('Agg')


if __name__ == '__main__':

	# which is the filename that we want to create. 
	Workbook = xlsxwriter.Workbook('./output/database.xlsx')
	# worksheet via the add_worksheet() method.
	worksheet = Workbook.add_worksheet() 
	# construct the class Api
	app = Api()

	# Create a window and pass it to videoGUI Class
	videoGUI(Tk(), "win", worksheet, app)

	# Finally, close the Excel file 
	Workbook.close()

