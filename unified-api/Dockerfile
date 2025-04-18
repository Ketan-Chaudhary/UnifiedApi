FROM python:3.10-slim

WORKDIR /app
COPY ./app /app

RUN pip install --ignore-installed  -r requirements.txt

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5300"]