package ginyuforce.robotfilmmaker;

import android.os.HandlerThread;

import java.util.logging.Handler;

/**
 * Created by Kevin on 12/2/2017.
 */

public class RobotFilmmakerHandlerThread extends HandlerThread {
    private static String TAG = "RobotFilmmakerHandlerThread";

    private Handler handler;

    public RobotFilmmakerHandlerThread() {
        super(TAG);
        start();
    }
}
