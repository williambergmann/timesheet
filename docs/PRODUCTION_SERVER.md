# Production Server Credentials

## Timesheet Production Server

| Property       | Value                           |
| -------------- | ------------------------------- |
| **Hostname**   | timecardstx888.nst-training.com |
| **IP Address** | 172.17.2.27                     |
| **Username**   | nstadmin                        |
| **Password**   | 1Zumapuppy!                     |
| **OS**         | Ubuntu 24.04.3 LTS              |

## SSH Connection

```bash
ssh nstadmin@172.17.2.27
```

## Docker Containers

| Container              | Image              | Purpose             |
| ---------------------- | ------------------ | ------------------- |
| timesheet-prod-web-1   | timesheet-prod-web | Flask application   |
| timesheet-prod-db-1    | postgres:15-alpine | PostgreSQL database |
| timesheet-prod-redis-1 | redis:7-alpine     | Redis cache         |
| nginx-https            | nginx:alpine       | HTTPS reverse proxy |

## Database Access

```bash
# Connect to database
docker exec -it timesheet-prod-db-1 psql -U timesheet -d timesheet

# Database credentials
POSTGRES_USER=timesheet
POSTGRES_PASSWORD=ETeGPdPOZdt-1hyo0UsGsR9VtOcm-4cT
POSTGRES_DB=timesheet
```

## Deployment Commands

```bash
# SSH to server
ssh nstadmin@172.17.2.27

# Navigate to app
cd ~/timesheet

# Pull latest code (after git setup)
git pull origin main

# Rebuild and restart
docker compose --env-file .env -f docker/docker-compose.prod.yml build web
docker compose --env-file .env -f docker/docker-compose.prod.yml up -d --force-recreate web

# Check health
curl -sk https://localhost/health
```
