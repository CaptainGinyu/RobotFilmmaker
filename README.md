# ![alt tag](https://github.com/CaptainGinyu/RobotFilmmaker/blob/master/Readme%20Resources/icon_small.png)  Robot Filmmaker 
Philip Yuan, Harshil Prajapati, Kevin Chow, Nikhil Ranjan

## Product Description
Robot Filmmaker is a system that will automatically track and record videos of the user to reduce the need of human control during the filming process so users can focus on content rather than the recording process.

## User Stories
**As a user I want the device to…**
  - Recognize the user against other random people or objects.
  - Follow the user to always keep the user in frame.
  - Save the user’s video.
  - Be portable and convenient to use.
  
**As a user it would be nice if the device could...**
  - Film user in many different ways (Such as left frame only, fixed distance, etc.)
  - Recognize and follow other objects like a ball or dog

## System Description
### Hardware Requirements
  - Arduino Mega 2560 (https://www.arduino.cc/en/Main/arduinoBoardMega2560/)
  - Pan Tilt Kit and Servos (https://www.servocity.com/spt100#324=38)
  - Logitech C270 Webcam (https://www.logitech.com/en-us/product/hd-webcam-c270)
  - UniHobby 4WD Robot Chassis (http://www.unihobbytech.com/arduino-robot-parts/arduino-robot-chassis-c)

### Software Requirements
  - Python 3.6.2 (https://www.python.org/download/releases/3.0/)
    - boto3 (pip3 install boto3)
    - botocore (https://pypi.python.org/pypi/botocore)
    - serial (pip3 install pyserial)
    - pyrebase (pip3 install pyrebase)
  - OpenCV 3.0 (https://opencv.org/opencv-3-3.html)
  - OpenCV contrib (https://github.com/opencv/opencv_contrib)
  - Arduino (https://www.arduino.cc/en/Main/Software)
    - RBD_Timer (https://github.com/alextaujenis/RBD_SerialManager)
  - Android Studio (https://developer.android.com/studio/index.html)
  - Amazon Web Services (https://aws.amazon.com)
  
  There should also be an adminuser.txt file with two lines: first line is access key, seconds line is secret key in order to run the training code on the cloud Linux servers.
  
### System Diagram
![alt tag](https://github.com/CaptainGinyu/RobotFilmmaker/blob/master/Readme%20Resources/System_Diagram.png)

### Android Application
 The Robot Filmmaker Android application provides a simple UI for users to wirelessly start the different modes of Training and Tracking as well as provide useful information such as current status and other functions like resetting the camera or resetting the face detection.
 
 ![alt tag](https://github.com/CaptainGinyu/RobotFilmmaker/blob/master/Readme%20Resources/app_small.png)
 
## Repository Description
  - **Archives:** Archive of backups and unused code and pictures
  - **Demo:** Demo-ready code
    - /EC2: Folder containing python scripts that do face training on the cloud.
    - Demo_Main.py: Main function.  Forever loop that reads commands from the Android phone app.
    - Demo_Training.py: Training function called in Demo_Main.py when Android phone app sends command to start training.  Starts  mugshots to get face samples, then sends samples to S3 bucket and does training on cloud.  Leaves an XML model file on the cloud.
    - Demo_Tracking.py: Tracking function called in Demo_Main.py when Android phone app sends command to start tracking. Downloads xml model from S3 bucket.  Continually detects face, sends commands to Arduino, and listens for commands from phone app.
    - mosse.py and associated files: MOSSE tracking functions used in Demo_Training.py (Taken from the examples of OpenCV   contrib)
    - Demo_Solo_Training.py, Demo_Solo_Tracking.py: Training and tracking scripts modified as solo runnable scripts that aren't callable functions.
    - haarcascade_frontalface_default.xml: OpenCV provided XML file used for face feature detection    
  - **Readme Resources:** Pictures for Github readme
  - **Examples + Tutorials:** Example code and tutorials of how we wrote and set up cloud management
  - **RobotFilmmakerAndroidApp:** Android application code
  - **ServosController:** Arduino code for robot control
  - **Test Report.pdf:** Report on unit testing scenarios and their results
  
 ## Poster
 ![alt tag](https://github.com/CaptainGinyu/RobotFilmmaker/blob/master/Readme%20Resources/Poster.png)
 

