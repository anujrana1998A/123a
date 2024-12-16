import os
import cv2
from flask import Flask, render_template, Response, session

# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.6
THICKNESS = 1
# Colors.
BLACK  = (0,0,0)
BLUE   = (255,0,0)
YELLOW = (0,255,255)
GREEN = (0,255,0)
RED = (0,0,255)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'YOUR SECRET KEY'
app.config["DEBUG"] = True

def generate_frames():
    # Open the video capture object.
    cap = cv2.VideoCapture(0)  # Change the index to the appropriate camera input if necessary.
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Encode the frame as JPEG.
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        # Yield the frame as a response.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()

@app.route('/')
def home():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True, use_reloader=False)
