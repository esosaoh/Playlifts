#!/bin/bash
set -e

source ./backend/.env  

echo ">>> Copying files to EC2..."
scp -i "$KEY_PATH" -r backend "$EC2_USER@$EC2_HOST:$REMOTE_DIR"

echo ">>> Restarting backend Docker container..."

ssh -i "$KEY_PATH" "$EC2_USER@$EC2_HOST" << EOF
docker stop ec2-user-backend-1 || true
docker rm ec2-user-backend-1 || true
docker build -t playlifts-api -f $REMOTE_DIR/Dockerfile.api $REMOTE_DIR
docker run -d --name ec2-user-backend-1 -p 8889:8889 -e REDIS_URL=$REDIS_URL playlifts-api

docker stop ec2-user-celery-worker-1 || true
docker rm ec2-user-celery-worker-1 || true
docker build -t playlifts-celery -f $REMOTE_DIR/Dockerfile.celery $REMOTE_DIR
docker run -d --name ec2-user-celery-worker-1 -e REDIS_URL=$REDIS_URL playlifts-celery
EOF

echo ">>> Deployment complete!"
