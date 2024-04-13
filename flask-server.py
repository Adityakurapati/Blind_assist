from flask import Flask, render_template, Response, jsonify, request, send_file
import cv2
import numpy as np
import urllib.request
import easyocr
from threading import Thread
from gtts import gTTS
import os


app = Flask(__name__)


# Object Detection Using MobileNEt
config_file = 'content/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'content/frozen_inference_graph.pb'
url_ ='http://192.168.33.15/1600x1200.jpg'
file_name = 'content/labels.txt'

model = cv2.dnn_DetectionModel(frozen_model, config_file)
model.setInputSize(320, 320)
model.setInputScale(1.0 / 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

classLabels = []
with open(file_name, 'rt') as fpt:
    classLabels = fpt.read().rstrip('\n').split('\n')

# Global variable to store the last processed result
last_processed_result = None

# Global variable to indicate the current mode (0 for object detection, 1 for text recognition)
current_mode = 0
current_lang = 'en';

def object_detection():
    global last_processed_result
    while True:
        try:
            img_response = urllib.request.urlopen(url_)
            img_array = np.array(bytearray(img_response.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, -1)

            ClassIndex, confidence, bbox = model.detect(img, confThreshold=0.5)

            font_scale = 3
            font = cv2.FONT_HERSHEY_PLAIN

            for i in range(len(ClassIndex)):
                classInd = int(ClassIndex[i])
                conf = confidence[i]
                box = bbox[i]

                cv2.rectangle(img, box, (255, 0, 0), 2)
                cv2.putText(img, classLabels[classInd - 1], (box[0] + 10, box[1] + 40),
                            font, fontScale=font_scale, color=(0, 255, 0), thickness=3)

            _, jpeg = cv2.imencode('.jpg', img)
            frame = jpeg.tobytes()

            # Update last_processed_result
            last_processed_result = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except Exception as e:
            print(f"Error in object_detection: {str(e)}")
            break

# Load text recognition model.
reader = easyocr.Reader([current_lang], gpu=False)


def text_recognition():
    global last_processed_result
    while True:
        try:
            img_response = urllib.request.urlopen(url_)
            img_array = np.array(bytearray(img_response.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, -1)

            # Resize image for faster processing
            img = cv2.resize(img, None, fx=0.5, fy=0.5)

            text_data = reader.readtext(img)

            for t in text_data:
                bbox, text, score = t
                pt1 = (int(bbox[0][0]), int(bbox[0][1]))
                pt2 = (int(bbox[2][0]), int(bbox[2][1]))

                cv2.rectangle(img, pt1, pt2, (255, 255, 0), 5)
                cv2.putText(img, text, pt1, cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 0, 0), 1)

            _, jpeg = cv2.imencode('.jpg', img)
            frame = jpeg.tobytes()

            # Update last_processed_result
            last_processed_result = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except Exception as e:
            print(f"Error in text_recognition: {str(e)}")
            break

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/object_detection')
def object_detection_route():
    global current_mode
    current_mode = 0  # Set current mode to object detection
    return Response(object_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/text_recognition')
def text_recognition_route():
    global current_mode
    current_mode = 1  # Set current mode to text recognition
    return Response(text_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/getresult')
def get_result():
    global last_processed_result
    return Response(last_processed_result, mimetype='image/jpeg')

@app.route('/switchmode/<int:mode>')
def switch_mode(mode):
    global current_mode
    current_mode = mode
    print("Type of current_mode:", type(current_mode))  # Print the type of current_mode
    print("Current Mode: " + str(current_mode))  # Convert current_mode to a string
    return jsonify({"message": "Mode switched successfully."})



@app.route('/switchLang/<string:lang>')
def switch_lang(lang):
    global current_lang
    current_lang = lang
    print("Current Lang"+current_lang)
    return jsonify({"message": "Lang switched successfully."})

# Test To Speech
def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

@app.route('/tts')
def generate_speech():
    text = "This Is Python Audio player Output?"
    filename = "output.wav"
    text_to_speech(text, filename)
    return send_file(filename, as_attachment=True)



if __name__ == '__main__':
    # Multithreading for both object detection and text recognition
    Thread(target=app.run).start()
    Thread(target=object_detection).start()
    Thread(target=text_recognition).start()
