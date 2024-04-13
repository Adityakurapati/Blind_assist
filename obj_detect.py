import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import urllib.request
import numpy as np
from cvlib.object_detection import draw_bbox
import threading

url='http://192.168.46.15/1600x1200.jpg'
im=None

def run1():
    print("Run1 started")
    cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
    while True:
        try:
            print("Fetching image...")
            img_resp = urllib.request.urlopen(url)
            img_data = img_resp.read()
            print("Image fetched successfully")
            imgnp = np.array(bytearray(img_data), dtype=np.uint8)
            im = cv2.imdecode(imgnp, -1)

            cv2.imshow('live transmission',im)
            key = cv2.waitKey(5)
            if key == ord('q'):
                break
        except Exception as e:
            print("Error fetching image:", e)
            # You can add more detailed error handling here

    cv2.destroyAllWindows()

def run2():
    print("Run2 started")
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)
    while True:
        try:
            print("Fetching image...")
            img_resp = urllib.request.urlopen(url)
            img_data = img_resp.read()
            print("Image fetched successfully")
            imgnp = np.array(bytearray(img_data), dtype=np.uint8)
            im = cv2.imdecode(imgnp, -1)

            print("Performing object detection...")
            bbox, label, conf = cv.detect_common_objects(im)
            im = draw_bbox(im, bbox, label, conf)

            cv2.imshow('detection',im)
            key = cv2.waitKey(5)
            if key == ord('q'):
                break
        except Exception as e:
            print("Error performing object detection:", e)
            # You can add more detailed error handling here

    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("Main started")
    # Check if the URL is correct and accessible
    try:
        print("Checking URL accessibility...")
        urllib.request.urlopen(url)
        print("URL is accessible")
    except Exception as e:
        print("Error accessing URL:", e)
        exit()

    # Create and start threads
    thread1 = threading.Thread(target=run1)
    thread2 = threading.Thread(target=run2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
