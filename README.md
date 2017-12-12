# Robot Filmmaker
Philip Yuan, Harshil Prajapati, Kevin Chow, Nikhil Ranjan

## Product Description
For people who wish to film themselves in a non-selfie fashion, Robot Filmmaker is a robotic system that will track and record videos of a given person or object.  Unlike video drones, our product will reduce the need of human control during the filming process so that the person being filmed can focus on the task they want recorded and not the recording process itself!

## User Stories
**As a user I want the device to…**
  - Recognize me against other random people/objects
  - Follow me as I move so that I am always in view
  - Save my video to flash drive / cloud
  - Be portable and convenient to use
  
**As a user it would be nice if the device could...**
  - Film me in many different ways
  - Such as left frame only, fixed distance, etc.
  - Recognize and follow other objects like a ball or dog

## System Description
### Hardware and Software Requirements
  - Android Studio
  - Amazon Web Services
  - Arduino Mega 2560
  - Pan Tilt Kit and Servos
  - Logitech C270 Webcam
  - UniHobby 4WD Robot Chassis
  
### System Diagram
![alt tag](https://github.com/CaptainGinyu/RobotFilmmaker/blob/master/Readme%20Resources/System_Diagram.png)

## Repository Description
  - **Archives:** Archive of backups and unused code and pictures
  - **Demo:** Demo-ready code
    - /EC2: Folder containing python scripts that do face training on the cloud.
    - Demo_Main.py: Main function.  Forever loop that reads commands from the Android phone app.
    - Demo_Training.py: Training function called in Demo_Main.py when Android phone app sends command to start training.  Starts  mugshots to get face samples, then sends samples to S3 bucket and does training on cloud.  Leaves an XML model file on the cloud.
    - Demo_Tracking.py: Tracking function called in Demo_Main.py when Android phone app sends command to start tracking. Downloads xml model from S3 bucket.  Continually detects face, sends commands to Arduino, and listens for commands from phone app.
    - mosse.py and associated files: MOSSE tracking functions used in Demo_Training.py
    - Demo_Solo_Training.py, Demo_Solo_Tracking.py: Training and tracking scripts modified as solo runnable scripts that aren't callable functions.
    - haarcascade_frontalface_default.xml: OpenCV provided XML file used for face feature detection    
  - **Examples + Tutorials:** Example code and tutorials of how we wrote and set up cloud management
  - **ServosController:** Arduino code for robot control
  
 ## Poster
 ![alt tag](https://github.com/CaptainGinyu/RobotFilmmaker/blob/master/Readme%20Resources/Poster.png)
