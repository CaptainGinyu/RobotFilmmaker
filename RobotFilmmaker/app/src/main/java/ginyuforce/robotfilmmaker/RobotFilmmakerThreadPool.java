package ginyuforce.robotfilmmaker;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * Created by Kevin on 12/2/2017.
 */

public class RobotFilmmakerThreadPool {
    private static RobotFilmmakerThreadPool pool;
    private ThreadPoolExecutor threadPoolExecutor;
    private static int MAX_POOL_SIZE;
    private static final int KEEP_ALIVE = 10;
    BlockingQueue<Runnable> workQueue = new LinkedBlockingQueue<Runnable>();

    public static synchronized void post(Runnable runnable) {
        if (pool == null) {
            pool = new RobotFilmmakerThreadPool();
        }
        pool.threadPoolExecutor.execute(runnable);
    }

    private RobotFilmmakerThreadPool() {
        int numOfCores = Runtime.getRuntime().availableProcessors();
        MAX_POOL_SIZE = numOfCores * 2;
        threadPoolExecutor = new ThreadPoolExecutor(numOfCores, MAX_POOL_SIZE,
                KEEP_ALIVE, TimeUnit.SECONDS, workQueue);
    }

    public static void finish() {
        pool.threadPoolExecutor.shutdown();
    }

}
