
# path of input video to test
fpath_vid = "./samples/test6.mp4";
# path of output video that will be save 
save_path = "./output/save.avi"

# colors that can be detected by opencv model
color_classes = ["white", "gray", "yellow", "red", "green", "blue", "black"]
# types of car can be detected by opencv model
type_classes = ["car", "bus", "truck", "van"]


# path of database
database = "./output/database.db"



# initiliaze the speed parameters
# frame per second
fps = 1
# scales for black backgraound to show values on the detected boxes
scale1 = 1
scale2 = 1
# last position
position1 = (0, 0)
# current position
position2 = (0, 0) 
# width of the detected box by pixel
carBoxWidht = 1
# width of the real car by meter 
carWidht = 1
# number of dissapear frames
df = 5
# distance between two line in the street as a roi 
dst =10
# threshold for detection
thr_box = 0.5
thr_plate = 0.3

horizontal = False


# path of the models
car_detection_bin_model = './models/vehicle-detection-adas-0002.bin'
car_detection_xml_model = './models/vehicle-detection-adas-0002.xml'

car_classification_bin_model = './models/vehicle-attributes-recognition-barrier-0039.bin'
car_classification_xml_model = './models/vehicle-attributes-recognition-barrier-0039.xml'

plate_detecttion_bin_model = './models/vehicle-license-plate-detection-barrier-0106.bin'
plate_detection_xml_model = './models/vehicle-license-plate-detection-barrier-0106.xml'


