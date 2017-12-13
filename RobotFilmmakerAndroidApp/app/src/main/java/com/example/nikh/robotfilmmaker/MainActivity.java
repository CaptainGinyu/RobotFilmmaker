package com.example.nikh.robotfilmmaker;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private DatabaseReference root;
    private DatabaseReference status;

    private Button buttonTraining;
    private Button buttonTesting;
    private Button buttonResetCamera;
    private Button buttonResetTracking;
    private TextView statusText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        FirebaseDatabase firebaseDatabase = FirebaseDatabase.getInstance();

        root = firebaseDatabase.getReference();
        buttonTraining = (Button) findViewById(R.id.buttonTraining);
        buttonTesting = (Button) findViewById(R.id.buttonTesting);
        buttonResetCamera = (Button) findViewById(R.id.buttonResetCamera);
        buttonResetTracking = (Button) findViewById(R.id.buttonResetTracking);
        statusText = (TextView) findViewById(R.id.status);

        status = root.child("Status");
        status.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                if (dataSnapshot.getValue().equals("Tracking Completed")) {
                    buttonTesting.setText("Start Tracking");

                    buttonResetTracking.setVisibility(View.GONE);
                    buttonResetCamera.setVisibility(View.GONE);
                    buttonTesting.setVisibility(View.VISIBLE);
                    buttonTraining.setVisibility(View.VISIBLE);
                }
                if (dataSnapshot.getValue().equals("Training Started")) {
                    statusText.setText("Waiting for training to complete...");

                    buttonResetTracking.setVisibility(View.GONE);
                    buttonResetCamera.setVisibility(View.GONE);
                    buttonTesting.setVisibility(View.GONE);
                    buttonTraining.setVisibility(View.GONE);
                }
                if (dataSnapshot.getValue().equals("Tracking Started")) {
                    buttonTesting.setText("Stop Tracking");

                    buttonResetTracking.setVisibility(View.VISIBLE);
                    buttonResetCamera.setVisibility(View.VISIBLE);
                    buttonTesting.setVisibility(View.VISIBLE);
                    buttonTraining.setVisibility(View.GONE);
                }
                if (dataSnapshot.getValue().equals("Training Completed")) {
                    buttonResetTracking.setVisibility(View.GONE);
                    buttonResetCamera.setVisibility(View.GONE);
                    buttonTesting.setVisibility(View.VISIBLE);
                    buttonTraining.setVisibility(View.VISIBLE);
                }
                statusText.setText((String) dataSnapshot.getValue());
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {

            }
        });

        buttonTraining.setOnClickListener(this);
        buttonTesting.setOnClickListener(this);
        buttonResetCamera.setOnClickListener(this);
        buttonResetTracking.setOnClickListener(this);
    }
    @Override
    public void onClick(View view) {

        if (view == buttonTraining) {
            status.setValue("Training Started");
        }

        if (view == buttonTesting) {
            if (((Button) view).getText().equals("Start Tracking")) {
                status.setValue("Tracking Started");
            } else {
                status.setValue("Tracking Completed");
            }

        }

        if (view == buttonResetCamera) {
            status.setValue("Camera Reset");
        }

        if (view == buttonResetTracking) {
            status.setValue("Tracking Reset");
        }
    }

}
