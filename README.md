# Unified Digit Recognition API (Flask + Docker + TensorFlow)

This project provides a unified interface to recognize handwritten digits in both:

- 🔢 Western Decimal Digits (0–9)
- 🕉️ Devanagari Digits (०–९)

It uses three separate Flask APIs, each with its own environment (due to TensorFlow version differences), containerized via Docker and served via Nginx reverse proxy.

✨ Fully dockerized & deployable on a single EC2 instance.

---

## 🚀 Features

- 🧠 Deep learning models using TensorFlow
- 🐳 Containerized per-API to isolate dependencies
- ⚡ Unified UI to access both models from one endpoint
- 🔀 Nginx reverse proxy for clean routing
- ✅ REST API compatible with Postman & curl

---

## 🧪 Local Development

1. Clone the repo:

```bash
git clone https://github.com/Ketan-Chaudhary/UnifiedApi.git
cd UnifiedApi
```

2. Build & run all containers:

```bash
docker-compose up --build
```

3. Access locally:

- Unified Frontend: http://localhost:5300/
- Decimal API: http://localhost:5100/api/predict
- Devanagari API: http://localhost:5200/api/predict

---

## 📮 Unified API Usage (via Postman or curl)

Endpoint: POST http://localhost:5300/predict

Form-Data Fields:

- image: (upload a digit image file)
- model_type: decimal or devanagari

Example JSON response:

```json
{
  "prediction": "204"
}
```

---

## 🧠 Model Requirements

- decimal-api:
  - TensorFlow 2.13.0
- devanagari-api:
  - TensorFlow 2.19.0
- unified-api:
  - Communicates with both via HTTP

---

## ☁️ Deploying to AWS EC2

1. SSH into EC2:

```bash
ssh -i your-key.pem ubuntu@<EC2_IP>
```

2. Install Docker & Compose:

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
```

3. Clone this repo or transfer project files:

```bash
git clone https://github.com/Ketan-Chaudhary/UnifiedApi.git
cd UnifiedApi
```

4. Run the containers:

```bash
docker-compose up -d
```

5. Access:

- http://<EC2-IP>/ (Unified UI)
- http://<EC2-IP>/decimal/api/predict
- http://<EC2-IP>/devanagari/api/predict

---

## 📤 Pushing Images to Docker Hub (Optional for CI/CD)

1. Build and test images locally:

```bash
docker-compose build
```

2. Tag and push to Docker Hub:

```bash
docker tag decimal-api youruser/decimal-api:latest
docker push youruser/decimal-api:latest
```

3. In docker-compose.yml on EC2, replace build with image:

```yaml
image: youruser/decimal-api:latest
```

4. Then just:

```bash
docker-compose pull
docker-compose up -d
```

---

## 🛡️ Optional: Enable HTTPS (Recommended for Production)

Use Let's Encrypt + Certbot with Nginx or a Cloudflare proxy to secure your EC2 deployment.

---

## 🤝 Contributing

Pull requests welcome! Feel free to fork and submit improvements to:

- Model performance
- UI design
- Docker deployment flow

---
