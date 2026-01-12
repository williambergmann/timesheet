# SSL/TLS Setup Guide

This guide covers enabling HTTPS for the Northstar Timesheet application in production.

---

## Overview

The production configuration uses **nginx as the TLS termination point**, supporting:

1. **Let's Encrypt** (recommended) — Free, automated certificate management
2. **Custom SSL Certificates** — Bring your own certificates (enterprise CAs, etc.)

---

## Prerequisites

Before starting, ensure you have:

- [ ] A **public domain name** pointing to your server (e.g., `timesheet.northstar.com`)
- [ ] **Ports 80 and 443** open on your firewall
- [ ] **Docker and Docker Compose** installed
- [ ] A valid **email address** for Let's Encrypt notifications

---

## Option 1: Let's Encrypt (Recommended)

### Step 1: Configure Environment Variables

Add these to your `.env` file:

```bash
# SSL Configuration
SSL_DOMAIN=timesheet.yourdomain.com

# Production Database (REQUIRED - change from defaults!)
POSTGRES_USER=timesheet
POSTGRES_PASSWORD=your-secure-password-here
POSTGRES_DB=timesheet

# Update Azure Redirect URI for HTTPS
AZURE_REDIRECT_URI=https://timesheet.yourdomain.com/auth/callback

# Update App URL for notifications
APP_URL=https://timesheet.yourdomain.com
```

### Step 2: Obtain Initial Certificate

First, start nginx to serve the ACME challenge:

```bash
cd /path/to/northstar/timesheet

# Create a temporary nginx config for initial cert issuance
docker compose -f docker/docker-compose.prod.yml up -d nginx
```

Then request the certificate:

```bash
docker compose -f docker/docker-compose.prod.yml run --rm certbot certonly \
  --webroot \
  -w /var/www/certbot \
  -d timesheet.yourdomain.com \
  --email admin@yourdomain.com \
  --agree-tos \
  --no-eff-email
```

**Expected output:**

```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/timesheet.yourdomain.com/fullchain.pem
Key is saved at: /etc/letsencrypt/live/timesheet.yourdomain.com/privkey.pem
```

### Step 3: Start the Full Stack

```bash
docker compose -f docker/docker-compose.prod.yml up -d
```

### Step 4: Verify HTTPS

1. Visit `https://timesheet.yourdomain.com` in your browser
2. Check for the padlock icon 🔒
3. Verify HTTP redirects to HTTPS: `http://timesheet.yourdomain.com` → `https://...`

### Step 5: Set Up Auto-Renewal

Let's Encrypt certificates expire after 90 days. Set up automatic renewal:

**Option A: Cron job (recommended)**

```bash
# Add to crontab (run 'crontab -e')
0 0 * * * cd /path/to/northstar/timesheet && docker compose -f docker/docker-compose.prod.yml run --rm certbot renew --quiet && docker compose -f docker/docker-compose.prod.yml exec nginx nginx -s reload
```

**Option B: Certbot renewal service**

```bash
# Start the certbot renewal container (runs every 12 hours)
docker compose -f docker/docker-compose.prod.yml --profile certbot-renew up -d certbot
```

---

## Option 2: Custom SSL Certificates

Use this option if you have certificates from an enterprise CA or purchased certificates.

### Step 1: Prepare Certificate Files

Place your certificate files in `docker/ssl/`:

```
docker/
├── ssl/
│   ├── server.crt      # Your SSL certificate (full chain)
│   └── server.key      # Private key
```

**Important:** The `server.crt` should include the full certificate chain (your cert + intermediate certs).

### Step 2: Modify nginx-ssl.conf

Edit `docker/nginx-ssl.conf` and uncomment the custom certificate lines:

```nginx
# Option 1: Let's Encrypt (comment out)
# ssl_certificate     /etc/letsencrypt/live/${SSL_DOMAIN}/fullchain.pem;
# ssl_certificate_key /etc/letsencrypt/live/${SSL_DOMAIN}/privkey.pem;

# Option 2: Custom certificates (uncomment)
ssl_certificate     /etc/nginx/ssl/server.crt;
ssl_certificate_key /etc/nginx/ssl/server.key;
```

### Step 3: Modify docker-compose.prod.yml

Uncomment the custom SSL volume mount:

```yaml
nginx:
  volumes:
    - ./nginx-ssl.conf:/etc/nginx/nginx.conf:ro
    # Custom certificates (uncomment)
    - ./ssl:/etc/nginx/ssl:ro
```

### Step 4: Start the Stack

```bash
docker compose -f docker/docker-compose.prod.yml up -d
```

---

## Configuration Reference

### Environment Variables

| Variable             | Required | Description                                      |
| -------------------- | -------- | ------------------------------------------------ |
| `SSL_DOMAIN`         | Yes      | Your domain name (e.g., `timesheet.example.com`) |
| `POSTGRES_PASSWORD`  | Yes      | Database password (production requires this)     |
| `AZURE_REDIRECT_URI` | Yes      | Must use `https://` in production                |
| `APP_URL`            | Yes      | Base URL for notification links                  |

### File Locations

| File                             | Purpose                            |
| -------------------------------- | ---------------------------------- |
| `docker/nginx-ssl.conf`          | Production nginx config with TLS   |
| `docker/docker-compose.prod.yml` | Production Docker Compose          |
| `docker/ssl/`                    | Custom SSL certificates (optional) |

### Ports

| Port | Protocol | Purpose                             |
| ---- | -------- | ----------------------------------- |
| 80   | HTTP     | ACME challenges + redirect to HTTPS |
| 443  | HTTPS    | Main application traffic            |

---

## Security Headers

The nginx configuration includes these security headers:

| Header                      | Value                                 | Purpose                   |
| --------------------------- | ------------------------------------- | ------------------------- |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Force HTTPS for 1 year    |
| `X-Frame-Options`           | `DENY`                                | Prevent clickjacking      |
| `X-Content-Type-Options`    | `nosniff`                             | Prevent MIME sniffing     |
| `X-XSS-Protection`          | `1; mode=block`                       | XSS protection (legacy)   |
| `Content-Security-Policy`   | (see config)                          | Restrict resource loading |
| `Referrer-Policy`           | `strict-origin-when-cross-origin`     | Control referrer info     |

---

## Troubleshooting

### Certificate issuance fails

**Error:** `Failed authorization procedure`

**Causes:**

- Domain DNS not pointing to server
- Port 80 blocked by firewall
- Another service using port 80

**Fix:**

```bash
# Check DNS
dig +short timesheet.yourdomain.com

# Check port 80 is open
curl -v http://timesheet.yourdomain.com/.well-known/acme-challenge/test
```

### nginx fails to start

**Error:** `cannot load certificate`

**Causes:**

- Certificate files don't exist yet
- Wrong path in nginx config
- Permissions issue

**Fix:**

```bash
# Check certificate exists
docker compose -f docker/docker-compose.prod.yml exec nginx ls -la /etc/letsencrypt/live/

# Check nginx config syntax
docker compose -f docker/docker-compose.prod.yml exec nginx nginx -t
```

### Mixed content warnings

**Error:** Browser shows mixed content warnings

**Causes:**

- `APP_URL` or `AZURE_REDIRECT_URI` still using `http://`
- Hardcoded `http://` URLs in JavaScript

**Fix:**

- Update `.env` with `https://` URLs
- Check `static/js/*.js` for hardcoded URLs

---

## Testing SSL Configuration

Use these tools to verify your SSL setup:

1. **SSL Labs:** https://www.ssllabs.com/ssltest/
2. **Security Headers:** https://securityheaders.com/

Expected grades:

- SSL Labs: **A** or **A+**
- Security Headers: **A**

---

## Reverting to HTTP (Development Only)

To switch back to HTTP-only for local development:

```bash
# Use the development compose file
docker compose -f docker/docker-compose.yml up -d
```

---

**Last Updated:** January 12, 2026
