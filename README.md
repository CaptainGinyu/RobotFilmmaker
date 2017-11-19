# Robot Filmmaker
Kevin Chow, Harshil Prajapati, Nikhil Ranjan, Philip Yuan

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
  - Raspberry Pi
  - Arduino
  - Servos, Linear Actuator, Cart
  
### System Diagram
![alt tag](https://github.com/CaptainGinyu/RobotFilmmaker/blob/master/Readme%20Resources/SystemDiagram.PNG)

## Repository Description
  - **Archives:** Archive of backups and unused code and pictures
  - **Demo:** Demo-ready code
    - COMBINED-Train1-Mugshots.py:
      1/2 of Training. Takes streaming video and saves mugshots of target's face
    - COMBINED-Train2-UploadTrain.py: 2/2 of Training. Uploads mugshots of target to S3 buckets, executes training to generate xml file of model in another S3 bucket.  AWS credentials needed to run this.
    - COMBINED-Track.py: 1/1 of Tracking. Downloads xml model from S3 bucket. Does tracking
  - **Examples + Tutorials:** Example code and tutorials of how we wrote and set up cloud management
  
