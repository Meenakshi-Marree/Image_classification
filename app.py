# -*- coding: utf-8 -*-



from __future__ import division, print_function
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

# Define a Flask app
app = Flask(__name__)

# Load your trained model
MODEL_PATH = 'model_inception.h5'
model = load_model(MODEL_PATH)


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    x = x / 255.0  # Normalize the image
    x = np.expand_dims(x, axis=0)

    # Predict
    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)

    # Define diseases, symptoms, and remedies
    disease_info = [
        {
            "disease": "Bacterial Spot",
            "symptoms": "Small, dark, water-soaked spots on leaves and fruits.",
            "remedies": "Use copper-based fungicides and avoid overhead watering."
        },
        {
            "disease": "Early Blight",
            "symptoms": "Yellowing of lower leaves with dark concentric spots.",
            "remedies": "Apply fungicides containing chlorothalonil or mancozeb."
        },
        {
            "disease": "Late Blight",
            "symptoms": "Dark, water-soaked lesions on leaves and fruits.",
            "remedies": "Destroy infected plants and apply fungicides like metalaxyl."
        },
        {
            "disease": "Leaf Mold",
            "symptoms": "Yellow spots on leaves with a velvety mold on the underside.",
            "remedies": "Improve air circulation and use fungicides."
        },
        {
            "disease": "Septoria Leaf Spot",
            "symptoms": "Circular spots with dark margins and gray centers.",
            "remedies": "Use resistant varieties and fungicides."
        },
        {
            "disease": "Spider Mites",
            "symptoms": "Tiny yellow spots and fine webbing on leaves.",
            "remedies": "Use insecticidal soaps or neem oil."
        },
        {
            "disease": "Target Spot",
            "symptoms": "Brown, circular spots on leaves and stems.",
            "remedies": "Apply appropriate fungicides and maintain crop hygiene."
        },
        {
            "disease": "Tomato Yellow Leaf Curl Virus",
            "symptoms": "Yellowing and curling of leaves with stunted growth.",
            "remedies": "Control whiteflies and use resistant varieties."
        },
        {
            "disease": "Tomato Mosaic Virus",
            "symptoms": "Mottling and mosaic-like patterns on leaves.",
            "remedies": "Destroy infected plants and disinfect tools."
        },
        {
            "disease": "Healthy",
            "symptoms": "No visible symptoms. The plant is healthy.",
            "remedies": "Maintain good cultural practices."
        }
    ]

    return disease_info[preds[0]]


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files or request.files['file'].filename == '':
        return "No file uploaded", 400

    # Get the file from the post request
    f = request.files['file']

    # Save the file to ./uploads
    basepath = os.path.dirname(__file__)
    upload_folder = os.path.join(basepath, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, secure_filename(f.filename))
    f.save(file_path)

    # Make prediction
    result = model_predict(file_path, model)

    # Return prediction as JSON
    return jsonify(result)


if __name__ == '__main__':
    print("Starting Flask app on http://127.0.0.1:5001")
    app.run(port=5001, debug=True)
