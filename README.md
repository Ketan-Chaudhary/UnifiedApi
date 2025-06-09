---

# 🧮 Unified Digit Recognition API (Flask + Docker + TensorFlow + AWS)

This project offers a unified interface to recognize handwritten digits in both:

* 🔢 **Western Decimal Digits** (0–9)
* 🕉️ **Devanagari Digits** (०–९)

It consists of three independent Flask APIs—each containerized with its own TensorFlow version—and a unified interface served via **Nginx reverse proxy**. All services are orchestrated using **Docker Swarm** and hosted on a single **AWS EC2** instance.

---

## 🚀 Features

* 🧠 Deep learning models using **TensorFlow**
* 🐳 Containerized per API with isolated environments
* ⚡ Unified Flask API interface for model selection
* 🔁 **Nginx** reverse proxy to unify routes
* 🔀 Supports both `curl` and Postman for requests
* 🛠️ Orchestrated with **Docker Swarm**
* ☁️ Production-ready deployment on **AWS EC2**

---

## 📂 Folder Structure

```
UnifiedApi/
├── decimal-api/
├── devanagari-api/
├── unified-api/
├── nginx/
├── docker-compose.yml
├── deployment.yml
└── README.md
```

---

## 🧪 Local Development

### 1. Clone the repository

```bash
git clone https://github.com/Ketan-Chaudhary/UnifiedApi.git
cd UnifiedApi
```

### 2. Build and run locally (development)

```bash
docker-compose up --build
```

### 3. Access APIs locally:

* **Unified UI:** [http://localhost:5300/](http://localhost:5300/)
* **Decimal API:** [http://localhost:5100/api/predict](http://localhost:5100/api/predict)
* **Devanagari API:** [http://localhost:5200/api/predict](http://localhost:5200/api/predict)

---

## 📮 Unified API Usage

**Endpoint:**
`POST http://localhost:5300/predict`

**Form-Data Fields:**

* `image`: (Upload digit image file)
* `model_type`: `decimal` or `devanagari`

**Example JSON Response:**

```json
{
  "prediction": "204"
}
```

---

## 🧠 Model Requirements

| API            | TensorFlow Version |
| -------------- | ------------------ |
| decimal-api    | 2.13.0             |
| devanagari-api | 2.19.0             |
| unified-api    | 2.13.0             |

---

## ☁️ Deployment on AWS EC2 (Docker Swarm + Nginx)

### 1. SSH into EC2

```bash
ssh -i your-key.pem ubuntu@<EC2_IP>
```

### 2. Install Docker, Docker Compose & Swarm

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
docker swarm init
```

### 3. Clone the project

```bash
git clone https://github.com/Bit-Nest/UnifiedApi.git
cd UnifiedApi
```

### 4. Deploy via Docker Swarm

```bash
docker stack deploy -c deployment.yml unifieddigitapi
```

### 5. Access APIs via Nginx

* **Unified API:** http\://\<EC2\_IP>/predict
* **Decimal API:** http\://\<EC2\_IP>/decimal/api/predict
* **Devanagari API:** http\://\<EC2\_IP>/devanagari/api/predict

Nginx reverse proxy handles all routing to the corresponding services via internal ports.

---

## 🔐 Optional: HTTPS for Production

Use [Let's Encrypt](https://letsencrypt.org/) + [Certbot](https://certbot.eff.org/) or Cloudflare Proxy for SSL.

---

## 📤 Pushing Docker Images (CI/CD Optional)

### 1. Build and test locally

```bash
docker-compose build
```

### 2. Tag and push to Docker Hub

```bash
docker tag decimal-api youruser/decimal-api:latest
docker push youruser/decimal-api:latest
```

### 3. Update EC2 `docker-compose.yml` to use remote images

```yaml
image: youruser/decimal-api:latest
```

### 4. Pull and run

```bash
docker-compose pull
docker-compose up -d
```

---

## 🤝 Contributing

Pull requests are welcome! Feel free to submit improvements on:

* 📈 Model Accuracy
* 🎨 UI Enhancements
* 🐳 Docker & DevOps Optimization

---
