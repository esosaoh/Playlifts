#!/bin/bash
set -e

source ./backend/.env  

echo ">>> Copying files to EC2..."
scp -i "$KEY_PATH" -r backend deployment Dockerfile.* docker-compose.yml scripts "$EC2_USER@$EC2_HOST:$REMOTE_DIR/playlifts"

echo ">>> Restarting backend Docker container..."

ssh -i "$KEY_PATH" "$EC2_USER@$EC2_HOST" << EOF
cd $REMOTE_DIR/playlifts

docker stop ec2-user-backend-1 || true
docker rm ec2-user-backend-1 || true
docker build -t playlifts-api -f Dockerfile.api .
docker run -d --name ec2-user-backend-1 -p 8889:8889 \
  -e REDIS_URL=$REDIS_URL \
  -e OAUTHLIB_INSECURE_TRANSPORT=1 \
  playlifts-api

docker stop ec2-user-celery-worker-1 || true
docker rm ec2-user-celery-worker-1 || true
docker build -t playlifts-celery -f Dockerfile.celery .
docker run -d --name ec2-user-celery-worker-1 \
  -e REDIS_URL=$REDIS_URL \
  -e OAUTHLIB_INSECURE_TRANSPORT=1 \
  playlifts-celery
EOF

echo ">>> Deployment complete!"