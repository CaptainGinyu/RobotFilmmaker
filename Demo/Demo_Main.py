###################################################################
# IMPORT
###################################################################
import pyrebase, time
from Demo_Training import training
from Demo_Tracking import tracking

###################################################################
# PARAMETERS
###################################################################
TIMER_MAIN = 3              # Pull tags from Firebase every x seconds

# Firebase parameters
config = {
  "apiKey": "AIzaSyBpFiIIpHEkuj7PgiQad8EcggMIqcGohWI",
  "authDomain": "https://fir-auth-6d6d8.firebaseapp.com",
  "databaseURL": "https://fir-auth-6d6d8.firebaseio.com",
  "storageBucket": "https://fir-auth-6d6d8.appspot.com"
}

###################################################################
# FIREBASE SETUP
###################################################################
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Set default tags
db.child("Mode").set("Idle")
db.child("Status").set("Idle")

# Start timer
main_t0 = time.time()

# Set default mode
mode = "Idle"

# Forever main loop
while 1:
    # Calculate time
    main_t1 = time.time()
    main_tdiff = main_t1 - main_t0

    # If main timer is up, retrieve command from firebase
    if main_tdiff > TIMER_MAIN:
        print("------RETRIEVING FIREBASE------")
        tag_status = db.child("Status").get()
        mode = tag_status.val()
        print(mode)
        main_t0 = time.time()

    # If mode is training, start training code
    if mode == "Training Started":
        print("------TRAINING STARTED------")
        training()
        db.child("Status").set("Training Completed")    # After completion, set tag in Firebase and local mode
        mode = "Idle"
        main_t0 = time.time()

    elif mode == "Tracking Started":
        print("------TRACKING STARTED------")
        tracking()
        db.child("Status").set("Tracking Completed")    # After completion, set tag in Firebase and local mode
        mode = "Idle"
        main_t0 = time.time()