# Deployment Guide

This document explains how to deploy Playlifts.  
For local setup details, see [backend/README.md](./backend/README.md).

---

## Overview
- **Frontend**: Deployed on Vercel.
- **Backend**: Runs on an EC2 instance using Docker containers for:
  - API (Flask + Gunicorn)
  - Celery Worker (background tasks)

Deployment is managed via:
- `scripts/deploy.sh` (deployment automation)
- `Dockerfile.api` (API image)
- `Dockerfile.celery` (Celery worker image)
- `docker-compose.yml` (optional, for local or remote orchestration)

---

## File Locations
- **Deployment Script**: `scripts/deploy.sh`
- **Dockerfiles**:
  - API: `Dockerfile.api`
  - Celery Worker: `Dockerfile.celery`
- **Env Variables**: `backend/.env`
- **Compose File**: `docker-compose.yml` (root)

---

## How Deployment Works
1. `scripts/deploy.sh`:
   - Reads environment variables from `backend/.env`.
   - Copies backend, Dockerfiles, and configs to the EC2 instance.
   - Builds Docker images on EC2.
   - Stops and removes old containers.
   - Runs new containers with environment variables.

2. Containers:
   - **API container** runs Flask app via Gunicorn on port `8889`.
   - **Celery worker** processes async tasks (Spotify ↔ YouTube transfers).

---

## How to Deploy
1. Make sure your EC2 instance is running and accessible.
2. Update `backend/.env` with all required variables:

```bash 
FRONTEND_URL=https://playlifts.com  
REDIS_URL=redis://<host>:6379/0  
KEY_PATH=/path/to/your-ssh-key.pem  
EC2_USER=ec2-user  
EC2_HOST=<your-ec2-ip-or-dns>  
REMOTE_DIR=/home/ec2-user  
```

---

### Run:
```bash
bash scripts/deploy.sh
```

---

### Verify:
```bash
curl -I https://api.playlifts.com/healthz
```

**Should return:**
```json
{ "status": "ok" }
```

---

### Logs and Management

**Check API logs:**
```bash
docker logs ec2-user-backend-1
```

**Check Celery logs:**
```bash
docker logs ec2-user-celery-worker-1
```

**Restart containers:**
```bash
docker restart ec2-user-backend-1
docker restart ec2-user-celery-worker-1
```

---

### Notes
- `docker-compose.yml` can be used for local testing or remote orchestration if needed.  
- All code updates require re-running `scripts/deploy.sh` to rebuild and restart containers.
