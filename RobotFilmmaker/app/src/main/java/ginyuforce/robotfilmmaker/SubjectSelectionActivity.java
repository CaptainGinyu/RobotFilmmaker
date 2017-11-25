package ginyuforce.robotfilmmaker;

import android.content.Intent;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.MotionEvent;
import android.view.SurfaceView;
import android.view.View;
import android.view.WindowManager;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.Mat;
import org.opencv.core.Point;
import org.opencv.core.Rect2d;
import org.opencv.core.Scalar;
import org.opencv.imgproc.Imgproc;
import org.opencv.tracking.Tracker;

import java.io.InputStream;

/**
 * Created by Kevin on 11/17/2017.
 */

public class SubjectSelectionActivity extends AppCompatActivity
        implements CameraBridgeViewBase.CvCameraViewListener2 {

    private static final String TAG = "Subject Selection";
    private static final Scalar SELECTION_RECT_COLOR = new Scalar(255, 0, 0);

    private int widthPixels;
    private int heightPixels;

    private RobotFilmmakerCameraView mOpenCvCameraView;
    private Point[] selectionRectPoints;

    private FloatingActionButton cameraFlipButton;
    private int cameraIndex;

    private FloatingActionButton startSubjectSelectButton;

    private Mat takenPic;

    private Tracker tracker;
    private boolean trackerInitialized;
    private Rect2d selectionRect;

    private Mat hsv;

    static {
        System.loadLibrary("opencv_java3");
    }

    private BaseLoaderCallback mLoaderCallback = new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(int status) {
            switch (status) {
                case LoaderCallbackInterface.SUCCESS:
                    Log.i(TAG, "OpenCV loaded successfully");
                    mOpenCvCameraView.enableView();
                    break;
                default:
                    super.onManagerConnected(status);
                    break;
            }
        }
    };

    public SubjectSelectionActivity() {
        Log.i(TAG, "Instantiated new " + this.getClass());
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        Log.i(TAG, "called onCreate");
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        setContentView(R.layout.subject_selection);

        Intent intent = getIntent();
        Bundle extras = intent.getExtras();
        if (extras != null) {
            if (extras.containsKey(MainActivity.CAMERA_INDEX_MESSAGE)) {
                cameraIndex = extras.getInt(MainActivity.CAMERA_INDEX_MESSAGE);
            }
        } else {
            cameraIndex = 0;
        }

        DisplayMetrics displayMetrics = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(displayMetrics);
        widthPixels = displayMetrics.widthPixels;
        heightPixels = displayMetrics.heightPixels;

        mOpenCvCameraView = (RobotFilmmakerCameraView) findViewById(
                R.id.camera_view_subject_select);
        mOpenCvCameraView.setVisibility(SurfaceView.VISIBLE);
        mOpenCvCameraView.setCvCameraViewListener(this);
        mOpenCvCameraView.setCameraIndex(cameraIndex);
        mOpenCvCameraView.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                double[] eventPoints = new double[]{
                        (double) ((motionEvent.getX() * mOpenCvCameraView.getPreviewWidth())
                                / widthPixels),
                        (double) ((motionEvent.getY() * mOpenCvCameraView.getPreviewHeight())
                                / heightPixels)};
                switch (motionEvent.getAction() & MotionEvent.ACTION_MASK) {
                    case MotionEvent.ACTION_DOWN:
                        selectionRectPoints = new Point[2];
                        selectionRectPoints[0] = new Point(eventPoints);
                        selectionRectPoints[1] = new Point(eventPoints);
                        return true;
                    case MotionEvent.ACTION_MOVE:
                        selectionRectPoints[1].set(eventPoints);
                        return true;
                    case MotionEvent.ACTION_UP:
                        selectionRectPoints[1].set(eventPoints);
                        return true;
                    default:
                        break;
                }
                return false;
            }
        });

        cameraFlipButton = (FloatingActionButton) findViewById(
                R.id.camera_flip_button_subject_select);
        cameraFlipButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                selectionRectPoints = null;
                cameraIndex ^= 1;
                mOpenCvCameraView.disableView();
                mOpenCvCameraView.setCameraIndex(cameraIndex);
                mOpenCvCameraView.enableView();
            }
        });

        takenPic = null;

        startSubjectSelectButton
                = (FloatingActionButton) findViewById(R.id.start_selection_button_subject_select);
        startSubjectSelectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startSubjectSelectButton.setEnabled(false);
                cameraFlipButton.setEnabled(false);
                startSubjectSelectButton.setVisibility(View.GONE);
                cameraFlipButton.setVisibility(View.GONE);
            }
        });


        tracker = Tracker.create("KCF");
        trackerInitialized = false;
        selectionRect = null;

        hsv = new Mat();
    }


    @Override
    public void onPause() {
        super.onPause();
        if (mOpenCvCameraView != null) {
            mOpenCvCameraView.disableView();
        }
    }

    @Override
    public void onResume() {
        super.onResume();
        if (!OpenCVLoader.initDebug()) {
            Log.d(TAG,
                    "Internal OpenCV library not found. Using OpenCV Manager for initialization");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION_3_0_0, this, mLoaderCallback);
        } else {
            Log.d(TAG, "OpenCV library found inside package. Using it!");
            mLoaderCallback.onManagerConnected(LoaderCallbackInterface.SUCCESS);
        }
    }

    public void onDestroy() {
        super.onDestroy();
        if (mOpenCvCameraView != null) {
            mOpenCvCameraView.disableView();
        }
    }

    public void onCameraViewStarted(int width, int height) {
    }

    public void onCameraViewStopped() {
    }

    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
        Mat rgbaFrame = inputFrame.rgba();
        /*if ((selectionRectPoints != null) && (rgbaFrame != null)) {
            Imgproc.rectangle(rgbaFrame, selectionRectPoints[0],
                    selectionRectPoints[1], SELECTION_RECT_COLOR);
        }*/

        Imgproc.cvtColor(rgbaFrame, hsv, Imgproc.COLOR_BGR2HSV);
        if (rgbaFrame != null) {
            if (!trackerInitialized) {
                selectionRect = new Rect2d(100.0, 100.0, 200.0, 200.0);
                tracker.init(hsv, selectionRect);
                trackerInitialized = true;
                Log.i("tracker", "initialized");

            } else {
                tracker.update(hsv, selectionRect);
                Log.i("tracker", "update");
            }

            Log.i("tracker coords", Double.toString(selectionRect.x)
                    + ", " + Double.toString(selectionRect.y));

            Imgproc.rectangle(rgbaFrame, new Point(selectionRect.x, selectionRect.y),
                    new Point(selectionRect.x + selectionRect.width, selectionRect.y + selectionRect.height), SELECTION_RECT_COLOR);
        }


        return rgbaFrame;
    }

    private void takePictureForSelection() {
        Bitmap takenPic = mOpenCvCameraView.takePictureToBitmap();
        mOpenCvCameraView.pauseCamera();
    }
}