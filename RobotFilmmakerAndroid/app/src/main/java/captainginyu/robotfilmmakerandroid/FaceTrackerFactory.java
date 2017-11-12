package captainginyu.robotfilmmakerandroid;

import com.google.android.gms.vision.MultiProcessor;
import com.google.android.gms.vision.Tracker;
import com.google.android.gms.vision.face.Face;

/**
 * Created by Kevin on 11/12/2017.
 */

public class FaceTrackerFactory implements MultiProcessor.Factory<Face> {
    @Override
    public Tracker<Face> create(Face face) {
        return new FaceTracker();
    }
}
