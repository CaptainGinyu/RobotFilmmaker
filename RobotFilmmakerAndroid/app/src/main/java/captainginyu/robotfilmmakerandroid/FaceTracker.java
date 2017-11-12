package captainginyu.robotfilmmakerandroid;

import android.util.Log;
import com.google.android.gms.vision.Tracker;
import com.google.android.gms.vision.face.Face;
import com.google.android.gms.vision.face.FaceDetector;

/**
 * Created by Kevin on 11/12/2017.
 */

public class FaceTracker extends Tracker<Face> {

    public FaceTracker() {

    }

    @Override
    public void onNewItem(int faceId, Face item) {
        Log.i("New face", Integer.toString(faceId));
    }

    @Override
    public void onUpdate(FaceDetector.Detections<Face> detectionResults, Face face) {

    }

    @Override
    public void onMissing(FaceDetector.Detections<Face> detectionResults) {

    }

    @Override
    public void onDone() {

    }
}