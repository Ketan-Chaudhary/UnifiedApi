from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

DECIMAL_API_URL = "http://decimal:5100/api/predict"
DEVANAGARI_API_URL = "http://devanagari:5200/api/predict"


def is_api_request():
    """
    Determines if the request is coming from Postman, curl, or an API client (not a browser).
    """
    accept = request.headers.get('Accept', '')
    return 'application/json' in accept or request.path.startswith('/api')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def unified_predict():
    image = request.files.get('image') or request.files.get('file')
    model_type = request.form.get('model_type') or request.args.get('model_type')

    if not image or not model_type:
        error_msg = "Both 'image' and 'model_type' are required."
        return jsonify({"error": error_msg}) if is_api_request() else render_template('index.html', error=error_msg)

    if model_type not in ['decimal', 'devanagari']:
        error_msg = "model_type must be 'decimal' or 'devanagari'."
        return jsonify({"error": error_msg}) if is_api_request() else render_template('index.html', error=error_msg)

    try:
        endpoint = DECIMAL_API_URL if model_type == 'decimal' else DEVANAGARI_API_URL
        field_name = 'file' if model_type == 'decimal' else 'image'

        # Forward the image to the respective backend
        response = requests.post(endpoint, files={field_name: image})
        data = response.json()

        if response.status_code == 200:
            return jsonify(data) if is_api_request() else render_template('index.html', prediction=data['prediction'])
        else:
            return jsonify(data) if is_api_request() else render_template('index.html', error=data.get('error', 'Unknown error'))

    except Exception as e:
        return jsonify({"error": str(e)}) if is_api_request() else render_template('index.html', error=str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5300, debug=True)
