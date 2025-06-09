
---

# 🧮 Unified Digit Recognition API (Flask + Docker + TensorFlow + AWS)

This project offers a unified interface to recognize handwritten digits in both:

* 🔢 **Western Decimal Digits** (0–9)
* 🕉️ **Devanagari Digits** (०–९)

It consists of three independent Flask APIs—each containerized with its own TensorFlow version—and a unified interface served via **Nginx reverse proxy**. All services are orchestrated using **Docker Swarm** and hosted on a single **AWS EC2** instance.

> 🧪 **Note:** Local development uses **Docker Compose**, while deployment on EC2 uses **Docker Swarm**.

---

## 🚀 Features

* 🧠 Deep learning models using **TensorFlow**
* 🐳 Each API containerized with isolated environments
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
git clone https://github.com/Bit-Nest/UnifiedApi.git
cd UnifiedApi
```

### 2. Build and run locally (development)

```bash
docker-compose up --build
```

### 3. Access APIs locally

* **Unified UI:** [http://localhost:5300/](http://localhost:5300/)
* **Decimal API:** [http://localhost:5100/api/predict](http://localhost:5100/api/predict)
* **Devanagari API:** [http://localhost:5200/api/predict](http://localhost:5200/api/predict)

### 🔌 Port Mappings (Local Only)

| Service        | Port |
| -------------- | ---- |
| Unified UI     | 5300 |
| Decimal API    | 5100 |
| Devanagari API | 5200 |

---

## 📮 Unified API Usage

**Endpoint:**

```
POST http://localhost:5300/predict
```

**Form-Data Fields:**

| Field        | Type   | Description               |
| ------------ | ------ | ------------------------- |
| `image`      | File   | Upload a digit image      |
| `model_type` | String | `decimal` or `devanagari` |

**Example JSON Response:**

```json
{
  "prediction": "204"
}
```

---

## 🧠 Model Requirements

| API            | TensorFlow Version     |
| -------------- | ---------------------- |
| decimal-api    | 2.13.0                 |
| devanagari-api | 2.19.0                 |
| unified-api    | N/A (acts as a router) |

---

## ☁️ Deployment on AWS EC2 (Docker Swarm + Nginx)

### 1. SSH into your EC2 instance

```bash
ssh -i your-key.pem ubuntu@<EC2_IP>
```

### 2. Install Docker, Compose & Swarm

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

### 4. Deploy with Docker Swarm

```bash
docker stack deploy -c deployment.yml unifieddigitapi
```

### 5. Access Services via Nginx (on EC2)

* **Unified UI:** http\://\<EC2\_IP>/
* **Unified Prediction Endpoint:** http\://\<EC2\_IP>/predict
* **Decimal API:** http\://\<EC2\_IP>/decimal/api/predict
* **Devanagari API:** http\://\<EC2\_IP>/devanagari/api/predict

> Nginx handles internal routing and load balancing between services.

---

## 🔐 Optional: Enable HTTPS for Production

Use [Let's Encrypt](https://letsencrypt.org/) with [Certbot](https://certbot.eff.org/) or a Cloudflare proxy to secure your deployment with SSL certificates.

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

### 3. Update image source in production YAML

```yaml
# In deployment.yml
image: youruser/decimal-api:latest
```

### 4. Pull and deploy on EC2

```bash
docker-compose pull
docker-compose up -d
```

---

## 🤝 Contributing

Pull requests are welcome! Feel free to contribute to:

* 📈 Improving model accuracy
* 🎨 Enhancing UI/UX
* 🐳 Optimizing Docker & deployment flow

---
