# 🚀 COMPLETE DEPLOYMENT GUIDE - Ahmedabad Property API

**For VPS Hosting with Full Control Panel Setup**

---

## 📋 TABLE OF CONTENTS

1. [Prerequisites](#prerequisites)
2. [VPS Initial Setup](#vps-initial-setup)
3. [Docker Installation](#docker-installation)
4. [Application Configuration](#application-configuration)
5. [Database Setup](#database-setup)
6. [SSL Certificate](#ssl-certificate)
7. [Nginx Setup](#nginx-setup)
8. [Deployment](#deployment)
9. [Monitoring](#monitoring)
10. [Troubleshooting](#troubleshooting)

---

## ✅ PREREQUISITES

### Required
- VPS with Ubuntu 22.04 LTS (minimum 2GB RAM, 20GB storage)
- SSH access to your VPS
- Domain name (for SSL certificate)
- Basic Linux knowledge

### Recommended
- 4GB+ RAM for optimal performance
- MongoDB Atlas account or self-hosted MongoDB
- Redis for caching
- CloudFlare account for DDoS protection

---

## 🔧 VPS INITIAL SETUP

### Step 1: SSH into Your VPS
```bash
ssh root@your-vps-ip
# Enter your VPS password
```

### Step 2: Update System
```bash
apt update && apt upgrade -y
apt install -y curl wget git vim htop

# Create non-root user (recommended for security)
adduser propertyapi
usermod -aG sudo propertyapi
su - propertyapi
```

### Step 3: Configure Firewall
```bash
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 8000/tcp    # API (internal only)
sudo ufw status
```

### Step 4: Set Timezone
```bash
sudo timedatectl set-timezone Asia/Kolkata
timedatectl
```

---

## 🐳 DOCKER INSTALLATION

### Step 1: Install Docker
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
```

### Step 2: Install Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

### Step 3: Create Application Directory
```bash
mkdir -p ~/ahmedabadproperty
cd ~/ahmedabadproperty
```

---

## ⚙️ APPLICATION CONFIGURATION

### Step 1: Clone Repository
```bash
git clone https://github.com/Piyushbgandhi/ahmedabadproperty.git .
ls -la
```

### Step 2: Create .env File
```bash
# Copy example file
cp .env.example .env

# Edit with your values
nano .env
```

### Step 3: Configure Environment Variables

Add these to your `.env` file:

```dotenv
# ==================== CORE ====================
ENVIRONMENT=production
DEBUG_MODE=false
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,admin.yourdomain.com

# ==================== DATABASE ====================
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=ahmedabad_property
REDIS_URL=redis://redis:6379/0

# ==================== SECURITY ====================
SECRET_KEY=YOUR_SECRET_KEY_MIN_32_CHARS_RANDOM
ADMIN_SECRET_KEY=YOUR_ADMIN_SECRET_MIN_32_CHARS_RANDOM
ADMIN_IP_WHITELIST=0.0.0.0/0

# ==================== AWS S3 ====================
AWS_ACCESS_KEY_ID=your_aws_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your-bucket-name

# ==================== PAYMENT ====================
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret

# ==================== EMAIL ====================
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# ==================== CORS ====================
CORS_ORIGINS=https://yourdomain.com,https://admin.yourdomain.com
```

### Step 4: Generate Secure Keys
```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ADMIN_SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 💾 DATABASE SETUP

### Option A: MongoDB Atlas (Recommended for Beginners)

1. **Create Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create free account
   - Create new project

2. **Create Cluster**
   - Click "Build a Cluster"
   - Select M0 (Free) tier
   - Choose AWS + ap-south-1 region
   - Wait for cluster creation

3. **Get Connection String**
   - Go to "Clusters" → "Connect"
   - Choose "Drivers"
   - Copy connection string
   - Add to `.env` as `MONGO_URL`

4. **Create Database User**
   ```
   Username: your_db_user
   Password: strong_password_here
   ```

5. **Whitelist IP**
   - In MongoDB Atlas: Security → Network Access
   - Add your VPS IP address
   - Or allow all (0.0.0.0/0) for development

### Option B: Self-Hosted MongoDB

```bash
# Add MongoDB repository
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Check status
sudo systemctl status mongod

# Connect to MongoDB shell
mongosh

# Create database
use ahmedabad_property

# Create user
db.createUser({
  user: "propertyapi",
  pwd: "StrongPassword123!",
  roles: ["readWrite"]
})

# Update docker-compose.yml with local MongoDB
```

---

## 🔒 SSL CERTIFICATE

### Step 1: Install Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Step 2: Get Certificate
```bash
# For single domain
sudo certbot certonly --standalone \
  -d yourdomain.com \
  --email your-email@gmail.com \
  --agree-tos

# For multiple domains
sudo certbot certonly --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com \
  -d admin.yourdomain.com \
  --email your-email@gmail.com \
  --agree-tos
```

### Step 3: Copy Certificates to Application
```bash
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ~/ahmedabadproperty/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ~/ahmedabadproperty/ssl/key.pem
sudo chown propertyapi:propertyapi ~/ahmedabadproperty/ssl/*
```

### Step 4: Auto-Renewal
```bash
# Test renewal
sudo certbot renew --dry-run

# Set up cron
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## 🌐 NGINX SETUP

### Step 1: Install Nginx
```bash
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### Step 2: Create Nginx Configuration

**File: `/etc/nginx/sites-available/ahmedabadproperty`**

```nginx
# HTTP redirect to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com admin.yourdomain.com;
    
    # Let's Encrypt challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    # Redirect to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com admin.yourdomain.com;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Gzip compression
    gzip on;
    gzip_types text/plain text/css text/javascript application/json;
    gzip_min_length 1000;
    
    # Proxy to API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Proxy to docs
    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
    
    location /openapi.json {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

### Step 3: Enable Configuration
```bash
sudo ln -s /etc/nginx/sites-available/ahmedabadproperty /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🚀 DEPLOYMENT

### Step 1: Update docker-compose.yml

**File: `docker-compose.yml`**

```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: property-api
    restart: always
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - MONGO_URL=${MONGO_URL}
      - DB_NAME=${DB_NAME}
      - SECRET_KEY=${SECRET_KEY}
      - ADMIN_SECRET_KEY=${ADMIN_SECRET_KEY}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - S3_BUCKET_NAME=${S3_BUCKET_NAME}
      - RAZORPAY_KEY_ID=${RAZORPAY_KEY_ID}
      - SMTP_USER=${SMTP_USER}
    volumes:
      - ./logs:/app/logs
      - ./ssl:/app/ssl
    networks:
      - property-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    container_name: property-redis
    restart: always
    ports:
      - "6379:6379"
    networks:
      - property-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  property-network:
    driver: bridge

volumes:
  redis_data:
```

### Step 2: Deploy Application
```bash
cd ~/ahmedabadproperty

# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f

# Verify services
docker-compose ps
```

### Step 3: Create Admin User
```bash
# Connect to API container
docker-compose exec api bash

# Create admin
python3 << 'EOF'
from models import hash_password
from dependencies import db
import asyncio
from datetime import datetime

async def create_admin():
    admin_data = {
        'username': 'admin',
        'email': 'admin@yourdomain.com',
        'password': hash_password('AdminPass@123'),
        'role': 'superadmin',
        'permissions': ['all'],
        'created_at': datetime.utcnow(),
        'last_login': None
    }
    result = await db.admins.insert_one(admin_data)
    print(f"✅ Admin created: {result.inserted_id}")

asyncio.run(create_admin())
EOF

exit
```

### Step 4: Test Application
```bash
# Test API health
curl https://yourdomain.com/api/health

# Test admin docs
curl https://yourdomain.com/api/docs

# Check logs
docker-compose logs api
```

---

## 📊 MONITORING

### Step 1: View Logs
```bash
# Real-time logs
docker-compose logs -f api

# Specific service
docker-compose logs -f redis

# Last 100 lines
docker-compose logs --tail 100 api
```

### Step 2: Monitor Resources
```bash
# Inside VPS
htop

# Docker stats
docker stats

# Check disk space
df -h
```

### Step 3: Database Backup
```bash
# Create backup script
mkdir -p ~/backups

cat > ~/backups/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/propertyapi/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/ahmedabad_property_$TIMESTAMP.tar.gz"

# Backup MongoDB (if self-hosted)
# mongodump --uri "mongodb://user:pass@localhost" --out $BACKUP_DIR/dump

# Backup volumes
docker-compose exec -T api tar czf - /app/uploads > $BACKUP_FILE

echo "✅ Backup created: $BACKUP_FILE"

# Keep only last 7 backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x ~/backups/backup.sh

# Schedule daily backup
crontab -e
# Add: 0 2 * * * /home/propertyapi/backups/backup.sh
```

---

## 🐛 TROUBLESHOOTING

### Issue: Container Won't Start
```bash
# Check logs
docker-compose logs api

# Rebuild
docker-compose build --no-cache

# Restart
docker-compose down
docker-compose up -d
```

### Issue: Database Connection Error
```bash
# Check MongoDB connection
docker-compose logs api | grep -i mongo

# Verify MONGO_URL in .env
cat .env | grep MONGO_URL

# Test connection from container
docker-compose exec api python3 -c "
from dependencies import db
import asyncio
asyncio.run(db.admin.command('ping'))
print('✅ Connected')
"
```

### Issue: SSL Certificate Error
```bash
# Check certificate
sudo certbot certificates

# Renew manually
sudo certbot renew --force-renewal

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Issue: High Memory Usage
```bash
# Check container memory
docker stats

# Increase limit in docker-compose.yml
# mem_limit: 2g

# Clear old logs
docker system prune -a
```

### Issue: Slow API Response
```bash
# Check Redis
docker-compose exec redis redis-cli info

# Check MongoDB performance
# In MongoDB Atlas: Performance Advisor

# Check Nginx
sudo tail -f /var/log/nginx/access.log
```

---

## ✅ FINAL CHECKLIST

### Before Going to Production
- [ ] SSL certificate installed and working
- [ ] Admin user created with strong password
- [ ] Database backups configured
- [ ] Firewall rules set up
- [ ] Nginx reverse proxy working
- [ ] All environment variables configured
- [ ] Email service working
- [ ] S3 bucket configured
- [ ] DNS pointing to VPS IP
- [ ] Monitoring setup
- [ ] Alert notifications enabled

### After Deployment
- [ ] Test admin login
- [ ] Create test property
- [ ] Verify payment processing
- [ ] Check email notifications
- [ ] Monitor logs for errors
- [ ] Test admin analytics
- [ ] Verify visitor tracking

---

## 🎯 NEXT STEPS

1. Follow each step sequentially
2. Test after each major step
3. Keep backups of configuration files
4. Monitor application logs regularly
5. Update system and Docker regularly
6. Review security settings monthly
7. Optimize performance based on metrics

---

**For Support or Issues**: 
- Check logs: `docker-compose logs api`
- Restart service: `docker-compose restart api`
- Full rebuild: `docker-compose down && docker-compose up -d`

**Deployment Ready!** ✅🚀
