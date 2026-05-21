# 🚀 DevOps Project 25 — CI/CD Pipeline with Jenkins & Docker

<div align="center">

![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?style=for-the-badge&logo=jenkins&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-Flask%20App-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Source%20Control-181717?style=for-the-badge&logo=github&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)

**GitHub Push → Jenkins Pipeline → Docker Build → Container Deploy → Application Live!**

*Implemented by [@hmurafique](https://github.com/hmurafique)*

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Project Structure](#-project-structure)
- [Step-by-Step Implementation](#-step-by-step-implementation)
  - [Phase 1 — Server Setup](#phase-1--server-setup)
  - [Phase 2 — Jenkins Installation](#phase-2--jenkins-installation)
  - [Phase 3 — Jenkins Configuration](#phase-3--jenkins-configuration)
  - [Phase 4 — App & Pipeline Setup](#phase-4--app--pipeline-setup)
  - [Phase 5 — Jenkins Job Configure](#phase-5--jenkins-job-configure)
  - [Phase 6 — Deploy & Verify](#phase-6--deploy--verify)
- [Common Issues & Fixes](#-common-issues--fixes)
- [Cleanup](#-cleanup)
- [Lessons Learned](#-lessons-learned)

---

## 📌 Project Overview

This project demonstrates a complete **CI/CD Pipeline** using **Jenkins** and **Docker**. Every time code is pushed to GitHub, Jenkins automatically:
1. Clones the latest code
2. Builds a Docker image
3. Stops the old container
4. Deploys a new container
5. Verifies the deployment

### What We Built
- **Jenkins Server** installed via WAR file method (works on any Ubuntu version)
- **Jenkins systemctl service** for automatic startup
- **Python Flask App** containerized with Docker
- **Jenkinsfile** — Pipeline as Code
- **Automated CI/CD** — push code → auto deploy

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Developer                           │
│                  git push origin main                   │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                    GitHub Repository                    │
│            hmurafique/simple-python-app                 │
│                   Jenkinsfile here                      │
└─────────────────────────┬───────────────────────────────┘
                          │ Webhook / Manual Trigger
┌─────────────────────────▼───────────────────────────────┐
│                Jenkins CI/CD Server                     │
│                   Port 8080                             │
│                                                         │
│  Stage 1: Clone Repository                              │
│  Stage 2: Build Docker Image                            │
│  Stage 3: Stop Old Container                            │
│  Stage 4: Deploy New Container                          │
│  Stage 5: Verify Deployment                             │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│              Docker Container                           │
│         simple-python-app:latest                        │
│         Flask App — Port 9090                           │
│                                                         │
│    http://<EC2-IP>:9090  →  Hello from Jenkins!         │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| Jenkins | CI/CD Server | 2.555.2 |
| Docker | Containerization | 29.x |
| Python Flask | Web Application | 2.3.3 |
| GitHub | Source Code Management | — |
| Java | Jenkins Runtime | OpenJDK 21 |
| AWS EC2 | Cloud Server | Ubuntu 26.04 |

---

## ✅ Prerequisites

### AWS EC2 Instance
- **Instance Type:** t2.medium or higher (Jenkins needs 2GB+ RAM)
- **OS:** Ubuntu (any version)
- **Storage:** 20GB+
- **Security Group Ports:**

| Port | Purpose |
|------|---------|
| 22 | SSH |
| 8080 | Jenkins UI |
| 9090 | Flask App |

### Tools Required
```bash
java --version      # OpenJDK 21+
docker --version    # Docker 20+
git --version       # Git 2+
```

---

## 📁 Project Structure

```
simple-python-app/
├── app.py              # Flask web application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image definition
├── Jenkinsfile         # CI/CD Pipeline definition
└── README.md           # This file
```

### app.py
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Jenkins CI/CD Pipeline!</h1><p>DevOps Project 02</p>'

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
```

### Dockerfile
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 9090
CMD ["python", "app.py"]
```

### Jenkinsfile
```groovy
pipeline {
    agent any
    
    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t simple-python-app:latest .'
            }
        }
        
        stage('Stop Old Container') {
            steps {
                echo 'Stopping old container...'
                sh 'docker stop simple-python-app || true'
                sh 'docker rm simple-python-app || true'
            }
        }
        
        stage('Deploy Container') {
            steps {
                echo 'Deploying new container...'
                sh 'docker run -d -p 9090:9090 --name simple-python-app simple-python-app:latest'
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying deployment...'
                sh 'sleep 5 && curl http://localhost:9090/health'
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

---

## 📖 Step-by-Step Implementation

---

### Phase 1 — Server Setup

#### Step 1.1 — Launch EC2 Instance

- Instance Type: `t2.medium`
- OS: Ubuntu
- Security Group: Ports 22, 8080, 9090 open

#### Step 1.2 — SSH Connect

```bash
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

#### Step 1.3 — Install Java (Jenkins Requirement)

```bash
apt update && apt upgrade -y
apt install openjdk-21-jre -y

# Verify
java --version
# Expected: openjdk 21.x.x
```

#### Step 1.4 — Install Docker

```bash
apt install docker.io -y
systemctl start docker
systemctl enable docker

# Add root to docker group
usermod -aG docker root

# Verify
docker --version
```

#### Step 1.5 — Install Git

```bash
apt install git -y
git --version
```

---

### Phase 2 — Jenkins Installation

> ⚠️ **Note:** Jenkins official apt repo does not support Ubuntu 26.04 yet. WAR file method works on ALL Ubuntu versions.

#### Step 2.1 — Download Jenkins WAR File

```bash
cd /home/ubuntu
wget https://get.jenkins.io/war-stable/latest/jenkins.war

# Verify download
ls -lh jenkins.war
# Expected: ~95MB file
```

#### Step 2.2 — Create Jenkins Home Directory

```bash
mkdir -p /var/jenkins_home
```

#### Step 2.3 — Create Jenkins systemctl Service

```bash
cat > /etc/systemd/system/jenkins.service << 'EOF'
[Unit]
Description=Jenkins Server
After=network.target

[Service]
Environment="JENKINS_HOME=/var/jenkins_home"
ExecStart=/usr/bin/java -jar /home/ubuntu/jenkins.war --httpPort=8080
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF
```

#### Step 2.4 — Start Jenkins Service

```bash
systemctl daemon-reload
systemctl enable jenkins
systemctl start jenkins

# Verify
systemctl status jenkins
```

Expected output:
```
Active: active (running)
Jenkins is fully up and running
```

#### Step 2.5 — Get Initial Admin Password

```bash
cat /var/jenkins_home/secrets/initialAdminPassword
```

---

### Phase 3 — Jenkins Configuration

#### Step 3.1 — Open Jenkins UI

```
http://<EC2-PUBLIC-IP>:8080
```

Enter the initial admin password from Step 2.5.

#### Step 3.2 — Install Plugins

Go to: `Manage Jenkins → Plugins → Available plugins`

Search and install these plugins:

| Plugin | Purpose |
|--------|---------|
| Docker | Docker integration |
| Docker Commons | Shared Docker functionality |
| Docker Pipeline | Use Docker in pipelines |
| GitHub Integration Plugin | GitHub webhook support |

Check all → Click **Install** → Wait for completion.

#### Step 3.3 — Restart Jenkins After Plugin Install

```bash
systemctl restart jenkins
```

---

### Phase 4 — App & Pipeline Setup

#### Step 4.1 — Create GitHub Repository

1. Go to github.com → New Repository
2. Name: `simple-python-app`
3. Public ✅
4. Add README ✅
5. Create repository

#### Step 4.2 — Clone & Add Files

```bash
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/simple-python-app.git
cd simple-python-app
```

#### Step 4.3 — Create app.py

```bash
cat > app.py << 'EOF'
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Jenkins CI/CD Pipeline!</h1><p>DevOps Project 02</p>'

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
EOF
```

#### Step 4.4 — Create requirements.txt

```bash
cat > requirements.txt << 'EOF'
flask==2.3.3
EOF
```

#### Step 4.5 — Create Dockerfile

```bash
cat > Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 9090
CMD ["python", "app.py"]
EOF
```

#### Step 4.6 — Create Jenkinsfile

```bash
cat > Jenkinsfile << 'EOF'
pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t simple-python-app:latest .'
            }
        }
        stage('Stop Old Container') {
            steps {
                sh 'docker stop simple-python-app || true'
                sh 'docker rm simple-python-app || true'
            }
        }
        stage('Deploy Container') {
            steps {
                sh 'docker run -d -p 9090:9090 --name simple-python-app simple-python-app:latest'
            }
        }
        stage('Verify Deployment') {
            steps {
                sh 'sleep 5 && curl http://localhost:9090/health'
            }
        }
    }
}
EOF
```

#### Step 4.7 — Push to GitHub

```bash
git add .
git commit -m "Add Flask app, Dockerfile and Jenkinsfile"

# Set remote URL with token
git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/simple-python-app.git

git push origin main
```

---

### Phase 5 — Jenkins Job Configure

#### Step 5.1 — Create Pipeline Job

1. Jenkins Dashboard → **New Item**
2. Name: `simple-python-app-pipeline`
3. Select: **Pipeline**
4. Click **OK**

#### Step 5.2 — Configure General Settings

- Check **GitHub project** ✅
- Project URL: `https://github.com/YOUR_USERNAME/simple-python-app/`

#### Step 5.3 — Configure Pipeline

- Definition: `Pipeline script from SCM`
- SCM: `Git`
- Repository URL: `https://github.com/YOUR_USERNAME/simple-python-app.git`
- Branch: `*/main`
- Script Path: `Jenkinsfile`

Click **Save** ✅

---

### Phase 6 — Deploy & Verify

#### Step 6.1 — Run Pipeline

Click **"Build Now"** in Jenkins Dashboard.

#### Step 6.2 — Check Build Status

All stages should show green ✅:
```
✅ Clone Repository
✅ Build Docker Image
✅ Stop Old Container
✅ Deploy Container
✅ Verify Deployment
```

#### Step 6.3 — Verify Container Running

```bash
docker ps | grep simple-python-app
```

Expected:
```
simple-python-app   Up X minutes   0.0.0.0:9090->9090/tcp
```

#### Step 6.4 — Test Application

```bash
curl http://localhost:9090/
curl http://localhost:9090/health
```

Browser:
```
http://<EC2-PUBLIC-IP>:9090
```

Expected: **"Hello from Jenkins CI/CD Pipeline!"** ✅

---

## 🐛 Common Issues & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `apt install jenkins` fails | Ubuntu 26.04 not supported by Jenkins repo | Use WAR file method |
| Jenkins GPG key error | Jenkins key expired March 2026 | Use WAR file method |
| `docker: command not found` in Jenkins | Docker not in PATH | `usermod -aG docker root && systemctl restart jenkins` |
| Port 9090 not accessible | Security group not configured | Add inbound rule for port 9090 |
| Build fails at Clone stage | Wrong branch name | Change `*/master` to `*/main` |
| `Authentication failed` for git push | Token expired or wrong scope | Create new token with `repo` scope |

---

## 🛑 Cleanup

```bash
# Stop container
docker stop simple-python-app
docker rm simple-python-app

# Remove image
docker rmi simple-python-app:latest

# Stop Jenkins
systemctl stop jenkins

# Terminate EC2 instance from AWS Console
```

---

## 💡 Lessons Learned

1. **Jenkins WAR file** works on ANY Ubuntu version — better than apt install for newer OS
2. **systemctl service** for Jenkins — gives proper start/stop/restart/status control
3. **Jenkinsfile = Pipeline as Code** — version controlled, reproducible pipeline
4. **`|| true`** in shell commands — prevents pipeline failure when container doesn't exist
5. **Docker group permissions** — Jenkins must be in docker group to run docker commands
6. **Pipeline stages** — breaking pipeline into stages makes debugging easy
7. **Health check endpoint** — always add `/health` to verify deployment success

---

## 📊 Skills Gained

```
Jenkins CI/CD           ████████████████████  100%
Jenkins Pipeline        ████████████████████  100%
Jenkinsfile (Groovy)    ████████████████░░░░   80%
Docker                  ████████████████████  100%
GitHub Integration      ████████████████░░░░   80%
Linux systemctl         ████████████████████  100%
Flask App               ████████████░░░░░░░░   60%
```

---

## 🔗 References

- [Jenkins Official Documentation](https://www.jenkins.io/doc/)
- [Jenkins WAR Installation](https://www.jenkins.io/doc/book/installing/war-file/)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 🔜 What's Next

- [ ] Add GitHub Webhook for automatic trigger on push
- [ ] Push Docker image to AWS ECR
- [ ] Deploy to AWS ECS from Jenkins
- [ ] Add SonarQube for code quality check
- [ ] Multi-stage pipeline with Dev/Staging/Prod environments
- [ ] Email notifications on build success/failure

---

<div align="center">

**👨‍💻 Implemented by [@hmurafique](https://github.com/hmurafique)*

*Part of my 40 Real-World DevOps Projects Portfolio*

⭐ **If this helped you, give it a star!**

</div>
