package com.example.americanredcross;

// Copyright by Hanlin Mok
// June 23, 2013
// hanlin.mok.36@gmail.com



import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.util.UUID;

import com.example.americanredcross.MyLocation.LocationResult;



import android.app.Activity;
import android.location.Location;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class FieldReport extends Activity{
	
	MyLocation myLocation = new MyLocation();
	
	TextView finished, uuid;
	EditText username, password, event;
	Button submit,clear;
	String[] results = new String[5];
	String[] titles = new String[5];
	UUID uniqueKey;
	/*
	 * results[0]=username
	 * 1=password
	 * 2=lat
	 * 3=long
	 * 4=description
	 * 
	 * 
	 */
	String latitude, longitude;
	
	@Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        findCurrentLocation();
        
        titles[0] = "username";
        titles[1] = "password";
        titles[2] = "latitude";
        titles[3] = "longitude";
        titles[4] = "description";
       
        
        username = (EditText)findViewById(R.id.username);
        password = (EditText)findViewById(R.id.password);
        event = (EditText)findViewById(R.id.event);
        finished = (TextView)findViewById(R.id.finished);
      
        clear = (Button)findViewById(R.id.clear);
        submit = (Button)findViewById(R.id.submit);
        
        uuid = (TextView)findViewById(R.id.uuid);
        
        uniqueKey = UUID.randomUUID();
        uuid.setText(uniqueKey.toString());
        
        
        
        for(int i =0; i<results.length ; i++){
        	results[i] = "";
        }
        
        
        hookupSubmit();
        hookupClear();
	}
	
	
	public void hookupClear() {
    	clear.setOnClickListener(new OnClickListener() {
    		@Override
    		public void onClick(View v) {
    			username.setText("");
    			password.setText("");
    			event.setText("\n \n \n");
    			finished.setText("");
    			
    		}});
    	
    }
	
	
	public void hookupSubmit() {
    	submit.setOnClickListener(new OnClickListener() {
    		@Override
    		public void onClick(View v) {
    			
    			
    		try{
                    
                    // CALL GetText method to make post method call
                   GetText();
            }
           catch(Exception ex)
            {
               submit.setText(" url exeption! " );
            }
    			
    		}});
    	
    }
	

	
	
	public  void  GetText()  throws  UnsupportedEncodingException
    {
        // Get user defined values
        
        results[0]=username.getText().toString();
		results[1]=password.getText().toString();
		results[2]=latitude;
		results[3]=longitude;
		results[4]=event.getText().toString();
        
        
        
         
         // Create data variable for sent values to server  
		
		String data = "";
		for(int i=0;i<results.length;i++){
			if (i==0){
				 data = URLEncoder.encode(titles[i], "UTF-8") 
	                       + "=" + URLEncoder.encode(results[i], "UTF-8");
			}
			else{
				data += "&" + URLEncoder.encode(titles[i], "UTF-8") + "="
                    + URLEncoder.encode(results[i], "UTF-8");
			}
		}
		
         
          
          String text = "";
          BufferedReader reader=null;

          // Send data 
        try
        { 
          
            // Defined URL  where to send data
            URL url = new URL("http://10.60.247.202:8001/fieldreport/create_api");
             
         // Send POST data request

          URLConnection conn = url.openConnection(); 
          conn.setDoOutput(true); 
          OutputStreamWriter wr = new OutputStreamWriter(conn.getOutputStream()); 
          wr.write( data ); 
          wr.flush(); 
      
          // Get the server response 
           
        reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        StringBuilder sb = new StringBuilder();
        String line = null;
        
        // Read Server Response
        while((line = reader.readLine()) != null)
            {
                   // Append server response in string
                   sb.append(line + "\n");
            }
            
            
            text = sb.toString();
        }
        catch(Exception ex)
        {
        }
        finally
        {
            try
            {
                finished.setText("Thank you for your submission!");
                reader.close();
            }

            catch(Exception ex) {
            }
        }
              
        // Show response on activity
    }
	
	
	
	
	private void findCurrentLocation() {
        myLocation.getLocation(this, locationResult);
    }

	public LocationResult locationResult = new LocationResult() {

        @Override
        public void gotLocation(Location location) {
            // TODO Auto-generated method stub
            if (location != null) {
            	
            	latitude = location.getLatitude() + " ";
            	longitude = location.getLongitude() + " ";
            	
            }
        }
    };
	
}

