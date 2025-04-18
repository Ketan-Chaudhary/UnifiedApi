from flask import Flask, request, render_template
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import model_from_json
from PIL import Image
import io
import cv2

app = Flask(__name__)

# Load the model architecture from model.json
with open('model.json', 'r') as json_file:
    model_json = json_file.read()

model = model_from_json(model_json)

# Load the model weights from model.h5
model.load_weights('model.h5')


def preprocess_image(image):
    """
    Preprocess the image to make it suitable for digit detection and prediction.
    Converts the image to grayscale, applies thresholding, and finds contours.
    """
    # Convert to grayscale and apply thresholding
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding for better digit isolation
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours (individual digits)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from left to right based on the x-coordinate (for sequential digits)
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    return contours, thresh


def recognize_digits_from_contours(image, contours):
    """
    Recognizes digits from detected contours.
    Crops each detected digit, resizes it, and predicts using the model.
    """
    predicted_number = ""

    for contour in contours:
        # Get bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Crop the region containing the digit
        digit_image = image[y:y + h, x:x + w]

        # Resize to 28x28 pixels, the size expected by the model
        digit_image_resized = cv2.resize(digit_image, (28, 28))

        # Convert to grayscale and normalize
        digit_image_resized = cv2.cvtColor(digit_image_resized, cv2.COLOR_BGR2GRAY)
        digit_image_resized = digit_image_resized / 255.0

        # Add channel dimension and batch dimension
        digit_image_resized = np.expand_dims(digit_image_resized, axis=-1)  # Add channel dimension
        digit_image_resized = np.expand_dims(digit_image_resized, axis=0)  # Add batch dimension

        # Predict the digit
        predictions = model.predict(digit_image_resized)
        predicted_digit = np.argmax(predictions)

        # Append the predicted digit to the result
        predicted_number += str(predicted_digit)

    return predicted_number


# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file provided"), 400

        file = request.files['file']

        try:
            # Load the image from file
            image = Image.open(io.BytesIO(file.read()))
            image = np.array(image)

            # Preprocess the image to detect digits
            contours, thresh = preprocess_image(image)

            # Debugging output to check contours detected
            print(f"Detected {len(contours)} contours.")

            # Recognize digits from the contours
            predicted_number = recognize_digits_from_contours(image, contours)

            # Render the result in the template
            return render_template('index.html', prediction=predicted_number)

        except Exception as e:
            return render_template('index.html', error=str(e)), 500

    # Render the page for GET requests (i.e., when visiting the page)
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def api_predict():
    if 'file' not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files['file']

    try:
        image = Image.open(io.BytesIO(file.read()))
        image = np.array(image)

        contours, thresh = preprocess_image(image)
        prediction = recognize_digits_from_contours(image, contours)

        return {"prediction": prediction}, 200

    except Exception as e:
        return {"error": str(e)}, 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)
