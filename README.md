# Vehicle Detection, Tracking, Plate Number Recognition and Speed Estimation


### Table of Contents
1. [Tasks.](#Tasks)  
2. [Video Source.](#VideoSource) 
3. [Run the project.](#Runproject )
4. [Results.](#Results)



<a name="Tasks"></a>
### 1. Tasks 
 * Vehicle Detection
	- pre-trained OpenCV models are use for detection purpose
    	- https://docs.openvinotoolkit.org/2019_R1/_vehicle_detection_adas_0002_description_vehicle_detection_adas_0002.html  		

 * Vehicle Attributes Recognition
	- pre-trained OpenCV models are use for detection purpose
		- https://docs.openvinotoolkit.org/2019_R1/_vehicle_attributes_recognition_barrier_0039_description_vehicle_attributes_recognition_barrier_0039.html 

 * Vehicle License Plate Detection
	- pre-trained OpenCV models are use for detection purpose
		- https://docs.openvinotoolkit.org/2019_R1/_vehicle_license_plate_detection_barrier_0106_description_vehicle_license_plate_detection_barrier_0106.html  

 * Vehicle License Plate Number Recognition
 	- extract each of the text ROIs and pass them into `Tesseract` (a highly popular OCR engine)

 * Vehicle Tracking
    - assigning IDs to generated tracking bounding boxes

 * Speed Calculation
    - the distance (length of ROI box) moved by the tracked vehicle in a second (Frame Per Second of the video/Number of frames for which the vehicle was inside ROI box)
    	- https://www.ijcseonline.org/pub_paper/124-IJCSE-06271.pdf 

* Store the results in SQlite database and Excel file


<a name="VideoSource"></a>
### 2. Video Source
- Get the sample video source
	- https://www.youtube.com/watch?v=xZMrRB36CVw&t=65s



<a name="Runproject"></a>
### 3. Run the project (Windows Users)

1. Clone repo :
`git clone https://github.com/https://github.com/msh8261/Vehicle-Detection-Classification-Speed.git`

2. cd (change directory) into Vehicle-Detection-Classification-Speed
`cd Vehicle-Detection-Classification-Speed`

3. Create virtual environment
`virtualenv .env`

4. Activate virtual environment
`./venv/Scripts/activate` 

5. Install requirements
`pip install  -r requirements.txt`

6. Install OpenVino (openvino_2020.3.194)
	https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_windows.html

7. Run the script
`python run.py`



<a name="Results"></a>
### 4. Results 

![GitHub Logo](/output/img.png)







