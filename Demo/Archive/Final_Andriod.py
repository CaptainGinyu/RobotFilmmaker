import pyrebase, time
import Final_Mugshots
import Final_UploadTrain
import Final_ZArduino
from cv2 import face

config = {
  "apiKey": "AIzaSyBpFiIIpHEkuj7PgiQad8EcggMIqcGohWI",
  "authDomain": "https://fir-auth-6d6d8.firebaseapp.com",
  "databaseURL": "https://fir-auth-6d6d8.firebaseio.com",
  "storageBucket": "https://fir-auth-6d6d8.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

while(1):
    tag_mode = db.child("Mode").get()
    tag_status = db.child("Status").get()
    print(tag_mode.val())
    print(tag_status.val())
    
    if(tag_status.val() == "Started"):
        Final_Mugshots.Mugshots()
        Final_UploadTrain.Upload()
        break
        
    if(tag_status.val() == "Started1"):
        Final_ZArduino.Download_Track()
        break

    print("---------------------------")
    time.sleep(5)