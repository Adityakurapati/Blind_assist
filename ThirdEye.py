from flask import Flask, jsonify
from flask_cors import CORS 
import pymongo

connection_url = "mongodb+srv://aavs:projectforus7@cluster0.claqrrh.mongodb.net/studygears_signup?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_url)
db = client['studygears_signup']
Modes = db['modes']
Languages = db['langs']
ThirdEyeData = db['thirdeyedatas']

app = Flask(__name__)
CORS(app)

current_mode = ""
current_lang = ""
last_processed_result = ""

def process_text_recognition():
    global last_processed_result
    # Placeholder logic to simulate text recognition
    # In a real application, implement the actual text recognition logic
    last_processed_result = "This is a sample text recognized from an image."

def translate_to_hindi(text):
    # Placeholder logic to simulate translation to Hindi
    # In a real application, implement the actual translation logic
    return "यह एक छवि से मान्यता प्राप्त करा गया टेक्स्ट है।"

def translate_to_marathi(text):
    # Placeholder logic to simulate translation to Marathi
    # In a real application, implement the actual translation logic
    return "ही एक छवीतून मान्यता मिळालेली मजकूर आहे।"

def convert_text_to_audio(text):
    # Placeholder logic to simulate text-to-speech conversion
    # In a real application, implement the actual text-to-speech conversion logic
    print(f"Playing audio: {text}")

@app.route('/')
def index():
    return "Welcome to ThirdEye!"

@app.route('/updateMode/<int:mode>')
def update_mode(mode):
    global current_mode
    current_mode = mode
    return jsonify({"message": f"Current mode updated to {mode}."}), 200

@app.route('/updateLang/<string:lang>')
def update_lang(lang):
    global current_lang
    current_lang = lang
    return jsonify({"message": f"Current language updated to {lang}."}), 200

@app.route('/processResult')
def process_result():
    global last_processed_result
    if current_mode == "obj_dect":
        # Placeholder logic to simulate fetching object_name from the database
        # In a real application, fetch object_name from the database
        object_name = "Sample Object Name"
        last_processed_result = object_name
        # Placeholder logic to simulate converting object_name to audio
        # In a real application, implement the actual audio conversion logic
        convert_text_to_audio(object_name)
    elif current_mode == "text_rec":
        process_text_recognition()
        if current_lang == "hi":
            translated_text = translate_to_hindi(last_processed_result)
            convert_text_to_audio(translated_text)
        elif current_lang == "ma":
            translated_text = translate_to_marathi(last_processed_result)
            convert_text_to_audio(translated_text)
    return jsonify({"message": "Result processed successfully."}), 200

if __name__ == "__main__":
    app.run(debug=True)
