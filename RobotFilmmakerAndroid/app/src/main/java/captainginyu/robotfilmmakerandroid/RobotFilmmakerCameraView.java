package captainginyu.robotfilmmakerandroid;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.hardware.Camera;
import android.util.AttributeSet;

import org.opencv.android.JavaCameraView;

/**
 * Created by Kevin on 11/15/2017.
 */

@SuppressWarnings("deprecation")
public class RobotFilmmakerCameraView extends JavaCameraView {

    public RobotFilmmakerCameraView(Context context, AttributeSet attributeSet) {
        super(context, attributeSet);
    }

    public Bitmap takePictureToBitmap() {
        Bitmap pictureToReturn = null;

        Camera.PictureCallback pictureCallback = new Camera.PictureCallback() {
            Bitmap takenPicture;

            @Override
            public void onPictureTaken(byte[] bytes, Camera camera) {
                takenPicture = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
            }

            public Bitmap getTakenPicture() {
                return takenPicture;
            }
        };

        mCamera.takePicture(null, null, pictureCallback);
        return pictureToReturn;
    }

    public int getPreviewWidth() {
        return mCamera.getParameters().getPreviewSize().width;
    }

    public int getPreviewHeight() {
        return mCamera.getParameters().getPreviewSize().height;
    }
}
