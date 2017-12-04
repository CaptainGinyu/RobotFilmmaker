package ginyuforce.robotfilmmaker;

import org.opencv.core.Mat;
import org.opencv.core.Point;
import org.opencv.core.Rect2d;
import org.opencv.imgproc.Imgproc;
import org.opencv.tracking.Tracker;

/**
 * Created by Kevin on 12/3/2017.
 */

public class RobotFilmmakerTracker implements Runnable {
    private Mat frame;
    private Tracker tracker;
    private Point[] selectionRectPoints;
    private Rect2d selectionRect;
    private boolean trackerInitialized;

    public RobotFilmmakerTracker(Mat rgbaFrame, Tracker tracker, Point[] selectionRectPoints) {
        frame = rgbaFrame;
        this.tracker = tracker;
        this.selectionRectPoints = selectionRectPoints;
        trackerInitialized = false;
    }

    public synchronized Mat currFrame() {
        return frame;
    }

    @Override
    public void run() {
        if (Thread.interrupted()) {
            return;
        }
        Imgproc.cvtColor(frame, frame, Imgproc.COLOR_BGR2HSV);
        if (!trackerInitialized) {
            Point selectionRectTopLeftPoint = selectionRectPoints[0];
            Point selectionRectBottomRightPoint = selectionRectPoints[1];
            selectionRect = new Rect2d(selectionRectTopLeftPoint.x, selectionRectTopLeftPoint.y,
                    selectionRectBottomRightPoint.x - selectionRectTopLeftPoint.x,
                    selectionRectBottomRightPoint.y - selectionRectTopLeftPoint.y);
            tracker.init(frame, selectionRect);
            trackerInitialized = true;
        } else {
            tracker.update(frame, selectionRect);
        }

    }
}
