from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

DECIMAL_API_URL = "http://localhost:5100/api/predict"
DEVANAGARI_API_URL = "http://localhost:5200/api/predict"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def unified_predict():
    image = request.files.get('image') or request.files.get('file')
    model_type = request.form.get('model_type') or request.args.get('model_type')

    if not image or not model_type:
        return (
            jsonify({"error": "Both 'image' and 'model_type' are required."})
            if request.is_json or 'application/json' in request.content_type
            else render_template('index.html', error="Image and model type are required.")
        )

    if model_type not in ['decimal', 'devanagari']:
        return (
            jsonify({"error": "model_type must be 'decimal' or 'devanagari'."})
            if request.is_json or 'application/json' in request.content_type
            else render_template('index.html', error="Invalid model type selected.")
        )

    try:
        endpoint = DECIMAL_API_URL if model_type == 'decimal' else DEVANAGARI_API_URL
        field_name = 'file' if model_type == 'decimal' else 'image'

        response = requests.post(endpoint, files={field_name: image})
        data = response.json()

        if response.status_code == 200:
            return (
                jsonify(data) if request.is_json or 'application/json' in request.content_type
                else render_template('index.html', prediction=data['prediction'])
            )
        else:
            return (
                jsonify(data) if request.is_json or 'application/json' in request.content_type
                else render_template('index.html', error=data.get('error', 'Unknown error.'))
            )

    except Exception as e:
        return (
            jsonify({"error": str(e)})
            if request.is_json or 'application/json' in request.content_type
            else render_template('index.html', error=str(e))
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5300, debug=True)
