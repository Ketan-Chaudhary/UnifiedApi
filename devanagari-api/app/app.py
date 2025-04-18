import os
import cv2
import io
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load the trained model
model = load_model('devanagari_digit_model.h5')

# Class labels
labels = [str(i) for i in range(10)]

# --- Utility Functions ---

def preprocess_and_segment(image):
    """
    Preprocess the image using adaptive thresholding and segment it into digits.
    Returns sorted contours and thresholded image.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by X coordinate (left to right)
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    return contours, thresh


def predict_digits_from_contours(image, contours):
    result_number = ""

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        digit = image[y:y+h, x:x+w]
        digit = cv2.resize(digit, (64, 64))
        digit = digit.astype(np.float32) / 255.0
        digit = np.expand_dims(digit, axis=0)  # batch
        digit = np.expand_dims(digit, axis=-1) if digit.shape[-1] != 3 else digit  # channel
        if digit.shape[-1] != 3:
            digit = np.repeat(digit, 3, axis=-1)  # convert to 3 channels if needed

        prediction = model.predict(digit)
        predicted_class = labels[np.argmax(prediction)]
        result_number += predicted_class

    return result_number

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        pil_image = Image.open(filepath).convert('RGB')
        image_np = np.array(pil_image)

        contours, _ = preprocess_and_segment(image_np)
        prediction = predict_digits_from_contours(image_np, contours)

        return render_template('result.html', filename=filename, label=prediction)

    except Exception as e:
        return f"Error processing image: {str(e)}", 500

@app.route('/uploads/<filename>')
def send_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    if 'image' not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files['image']
    try:
        pil_image = Image.open(file.stream).convert('RGB')
        image_np = np.array(pil_image)

        contours, _ = preprocess_and_segment(image_np)
        prediction = predict_digits_from_contours(image_np, contours)

        return {"prediction": prediction}, 200

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5200)
