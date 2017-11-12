package captainginyu.robotfilmmakerandroid;

import android.content.Context;
import android.view.SurfaceHolder;

import org.opencv.android.JavaCameraView;

/**
 * Created by Kevin on 11/12/2017.
 */

public class OpenCVCameraView extends JavaCameraView implements SurfaceHolder.Callback{
    public OpenCVCameraView(Context context, int cameraId) {
        super(context, cameraId);
    }

    @Override
    public void surfaceCreated(SurfaceHolder holder) {
        super.surfaceCreated(holder);
    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int frmt, int w, int h) {
        super.surfaceChanged(holder, frmt, w, h);
    }
}
