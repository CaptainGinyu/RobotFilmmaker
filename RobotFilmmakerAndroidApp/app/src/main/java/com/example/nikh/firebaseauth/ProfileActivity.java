package com.example.nikh.firebaseauth;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.security.PrivateKey;

public class ProfileActivity extends AppCompatActivity implements View.OnClickListener{

    private FirebaseAuth firebaseAuth;

    private TextView textViewUserEmail;
    private Button buttonLogout;

    private DatabaseReference Mydatabase;
    private DatabaseReference Tag_Mode;
    private DatabaseReference Tag_Status;



    private EditText editTextName, editTextAddress;
    private Button buttonsave;

    private Button buttonTraining;
    private Button buttonTesting;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        //initializing firebase authentication object
        firebaseAuth =FirebaseAuth.getInstance();

        //if the user is not logged in
        //that means current user will return null
        if (firebaseAuth.getCurrentUser() ==null){
            //closing this activity
            finish();
            //starting new activity
                startActivity(new Intent(getApplicationContext(),ProfileActivity.class));
            }

        Mydatabase = FirebaseDatabase.getInstance().getReference();
        editTextName = (EditText) findViewById(R.id.editTextName);
        editTextAddress =(EditText) findViewById(R.id.editTextAddress);
        buttonsave =(Button) findViewById(R.id.buttonSave);
       buttonTraining = (Button) findViewById( R.id.buttonTraining);
        buttonTesting = (Button) findViewById( R.id.buttonTesting);



        FirebaseUser user = firebaseAuth.getCurrentUser();

        //initializing views
        textViewUserEmail = (TextView) findViewById(R.id.textViewUserEmail);
        buttonLogout = (Button) findViewById(R.id.buttonLogout);



        //displaying logged in user name
        textViewUserEmail.setText("Welcome"+user.getEmail());

       Tag_Mode = Mydatabase.child( "Mode" );
        Tag_Status = Mydatabase.child("Status" );







        //adding listner to button
        buttonLogout.setOnClickListener(this);
        buttonsave.setOnClickListener(this);
        buttonTraining.setOnClickListener( this );
        buttonTesting.setOnClickListener( this );

    }

    private void saveUserInformation(){
        String name = editTextName.getText().toString().trim();
        String address = editTextAddress.getText().toString().trim();

        UserInformation userInformation =new UserInformation(name, address);

        FirebaseUser user = firebaseAuth.getCurrentUser();

        Mydatabase.child(user.getUid()).setValue(userInformation);


        Toast.makeText(this,"Information saved...", Toast.LENGTH_LONG).show();

    }
    /**
     * Called when a view has been clicked.
     *
     * @param view The view that was clicked.*/

    @Override
    public void onClick(View view) {

       if (view == buttonTraining){

            Tag_Mode.setValue( "Training" );

        }

        if  (view == buttonTesting) {

            Tag_Mode.setValue( "Testing" );
        }

        if (view ==buttonLogout){
            firebaseAuth.signOut();
            finish();
            startActivity(new Intent(this, UserLogin.class));
        }

        if (view ==buttonsave){
            saveUserInformation();
        }
    }
}
