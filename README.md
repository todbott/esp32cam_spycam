# esp32cam_spycam

So, I got an ESP32-CAM recently (early 2023), and eventually decided to set it up as a sort of security camera.  The outline of how the system works is below:

## Camera-to-Database
1. ESP32-CAM (using Micropython), takes a picture every 60 seconds (though that interval is adjustable)
2. After taking the picture, it sends it (as a bytes object which has been converted to a base64 text string) to a Google Cloud Function endpoint
3. The Google Cloud Function 'wakes up', then (because it's a POST request), writes the text string (as well as the date and time) to Google Cloud Datastore

## Database-to-Frontend
4. When wanting to view the camera images, I navigate to a page (written in Node.js) which I've deployed on Google App Engine.  The page is login-protected, so only certain people can access it.
5. Upon loading, the page sends a GET request to the same Google Cloud Function endpoint mentioned above.
6. Again, the Cloud Function wakes up, the (because it's a GET request), sends all the timestamps and associated base64 text strings (the images), to the front end
7. The images are loaded into a 'slider' on the frontend, where they can be scrolled through.
