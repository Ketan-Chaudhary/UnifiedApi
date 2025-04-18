FROM tensorflow/tensorflow:2.19.0

# 🧠 Install system packages for OpenCV and general compatibility
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./app /app

RUN pip install --ignore-installed  flask gunicorn opencv-python pillow numpy Werkzeug

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5200"]
