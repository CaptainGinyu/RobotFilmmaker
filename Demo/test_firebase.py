import pyrebase


config = {
  "apiKey": "AIzaSyBpFiIIpHEkuj7PgiQad8EcggMIqcGohWI",
  "authDomain": "https://fir-auth-6d6d8.firebaseapp.com",
  "databaseURL": "https://fir-auth-6d6d8.firebaseio.com",
  "storageBucket": "https://fir-auth-6d6d8.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

db.child("Mode").set("Testing")
db.child("Status").set("Train_Stop")


#tag_mode = db.child("Mode").get()
#tag_status = db.child("Status").get()

# while(1):
#   tag_mode = db.child("Mode").get()
#   tag_status = db.child("Status").get()
#
#   if(tag_mode.val() == "Training"):
#     print("Training")
#
#   if(tag_mode.val() == "Testing"):
#     print("Testing")
#
#   print("---------------------------")
#   time.sleep(1)

