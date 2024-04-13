import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import numpy as np
from flask import Flask, render_template, Response
import urllib.request

app = Flask(__name__)

# url = 'http://192.168.46.15/1600x1200.jpg'

url='https://imgs.search.brave.com/iDas1dDk291tPfoWKGJY9JU6a6HD41krNICmcDzRQEU/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9wZXRh/cGl4ZWwuY29tL2Fz/c2V0cy91cGxvYWRz/LzIwMjMvMDEvTTIt/TWF4LU1hY0Jvb2st/UHJvLVJldmlldy0x/LTgwMHg1MzQuanBl/Zw'
def process_image():
    while True:
        try:
            img_resp = urllib.request.urlopen(url)
            img_data = img_resp.read()
            imgnp = np.array(bytearray(img_data), dtype=np.uint8)
            im = cv2.imdecode(imgnp, -1)

            bbox, label, conf = cv.detect_common_objects(im)
            im = draw_bbox(im, bbox, label, conf)

            ret, jpeg = cv2.imencode('.jpg', im)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print("Error processing image:", e)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(process_image(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
