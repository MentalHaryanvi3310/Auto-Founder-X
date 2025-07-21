# AutoFounder X Deployment Guide

This guide provides step-by-step instructions for deploying AutoFounder X in various environments.

## 🚀 Quick Start (Development)

### 1. Prerequisites
- Python 3.11 or higher
- Node.js 20 or higher
- pnpm (recommended) or npm
- Git

### 2. Clone and Setup

```bash
# Extract the AutoFounder X package
cd autofounder-x-final

# Setup Backend
cd autofounder-x-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/init_data.py
python src/main.py &

# Setup Frontend (in new terminal)
cd ../autofounder-x-frontend
pnpm install
pnpm run dev
```

Access the application at `http://localhost:5173`

## 🏭 Production Deployment

### Option 1: Traditional Server Deployment

#### Backend Deployment

1. **Prepare the server**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3.11 python3.11-venv python3-pip nginx -y
   ```

2. **Deploy backend**
   ```bash
   # Create application directory
   sudo mkdir -p /var/www/autofounder-x
   sudo chown $USER:$USER /var/www/autofounder-x
   
   # Copy backend files
   cp -r autofounder-x-backend /var/www/autofounder-x/
   cd /var/www/autofounder-x/autofounder-x-backend
   
   # Setup virtual environment
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   
   # Initialize database
   python src/init_data.py
   ```

3. **Create systemd service**
   ```bash
   sudo nano /etc/systemd/system/autofounder-backend.service
   ```
   
   Add the following content:
   ```ini
   [Unit]
   Description=AutoFounder X Backend
   After=network.target
   
   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/autofounder-x/autofounder-x-backend
   Environment=PATH=/var/www/autofounder-x/autofounder-x-backend/venv/bin
   ExecStart=/var/www/autofounder-x/autofounder-x-backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 src.main:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Start backend service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable autofounder-backend
   sudo systemctl start autofounder-backend
   ```

#### Frontend Deployment

1. **Build frontend**
   ```bash
   cd autofounder-x-frontend
   
   # Update API URL for production
   echo "VITE_API_BASE_URL=https://yourdomain.com/api" > .env
   
   # Build
   pnpm install
   pnpm run build
   
   # Copy to web directory
   sudo cp -r dist/* /var/www/autofounder-x/frontend/
   ```

2. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/autofounder-x
   ```
   
   Add the following configuration:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       
       # Frontend
       location / {
           root /var/www/autofounder-x/frontend;
           try_files $uri $uri/ /index.html;
       }
       
       # Backend API
       location /api/ {
           proxy_pass http://127.0.0.1:5000/api/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable site and restart Nginx**
   ```bash
   sudo ln -s /etc/nginx/sites-available/autofounder-x /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

4. **Setup SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

### Option 2: Docker Deployment

1. **Create Docker files**

   Backend Dockerfile (`autofounder-x-backend/Dockerfile`):
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   RUN python src/init_data.py
   
   EXPOSE 5000
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.main:app"]
   ```

   Frontend Dockerfile (`autofounder-x-frontend/Dockerfile`):
   ```dockerfile
   FROM node:20-alpine as build
   
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   
   COPY . .
   RUN npm run build
   
   FROM nginx:alpine
   COPY --from=build /app/dist /usr/share/nginx/html
   COPY nginx.conf /etc/nginx/nginx.conf
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

2. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   
   services:
     backend:
       build: ./autofounder-x-backend
       ports:
         - "5000:5000"
       environment:
         - FLASK_ENV=production
         - DATABASE_URL=sqlite:///autofounder.db
       volumes:
         - ./data:/app/data
   
     frontend:
       build: ./autofounder-x-frontend
       ports:
         - "80:80"
       depends_on:
         - backend
   ```

3. **Deploy with Docker**
   ```bash
   docker-compose up -d
   ```

### Option 3: Cloud Platform Deployment

#### Heroku Deployment

1. **Backend (Heroku)**
   ```bash
   cd autofounder-x-backend
   
   # Create Procfile
   echo "web: gunicorn src.main:app" > Procfile
   
   # Create runtime.txt
   echo "python-3.11.0" > runtime.txt
   
   # Deploy
   heroku create autofounder-x-backend
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

2. **Frontend (Netlify/Vercel)**
   ```bash
   cd autofounder-x-frontend
   
   # Update API URL
   echo "VITE_API_BASE_URL=https://autofounder-x-backend.herokuapp.com/api" > .env
   
   # Build and deploy
   pnpm run build
   # Upload dist folder to Netlify or connect to Vercel
   ```

#### AWS Deployment

1. **Backend (AWS EC2 + RDS)**
   - Launch EC2 instance with Ubuntu
   - Setup RDS PostgreSQL instance
   - Follow traditional server deployment steps
   - Update DATABASE_URL to PostgreSQL connection string

2. **Frontend (AWS S3 + CloudFront)**
   ```bash
   # Build frontend
   pnpm run build
   
   # Upload to S3
   aws s3 sync dist/ s3://your-bucket-name --delete
   
   # Setup CloudFront distribution
   # Point to S3 bucket with SPA configuration
   ```

## 🔧 Environment Configuration

### Production Environment Variables

#### Backend (.env)
```env
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
FLASK_ENV=production
PORT=5000
CORS_ORIGINS=https://yourdomain.com
```

#### Frontend (.env)
```env
VITE_API_BASE_URL=https://yourdomain.com/api
```

## 🔒 Security Considerations

1. **SSL/TLS**: Always use HTTPS in production
2. **Environment Variables**: Never commit secrets to version control
3. **Database**: Use PostgreSQL in production, not SQLite
4. **CORS**: Configure proper CORS origins
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Input Validation**: Ensure all inputs are properly validated
7. **Authentication**: Use strong JWT secrets and proper token expiration

## 📊 Monitoring and Logging

### Application Monitoring
```bash
# Check backend service status
sudo systemctl status autofounder-backend

# View backend logs
sudo journalctl -u autofounder-backend -f

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Performance Monitoring
- Use tools like New Relic, DataDog, or Prometheus
- Monitor database performance
- Set up alerts for downtime and errors

## 🔄 Backup and Recovery

### Database Backup
```bash
# SQLite backup
cp /path/to/autofounder.db /backup/location/

# PostgreSQL backup
pg_dump -h hostname -U username database_name > backup.sql
```

### Application Backup
```bash
# Backup entire application
tar -czf autofounder-x-backup-$(date +%Y%m%d).tar.gz /var/www/autofounder-x/
```

## 🚨 Troubleshooting

### Common Issues

1. **502 Bad Gateway**
   - Check if backend service is running
   - Verify Nginx proxy configuration
   - Check firewall settings

2. **Database Connection Errors**
   - Verify database credentials
   - Check database server status
   - Ensure proper network connectivity

3. **CORS Errors**
   - Update CORS_ORIGINS in backend
   - Verify frontend API URL configuration

4. **Build Failures**
   - Check Node.js and Python versions
   - Clear cache and reinstall dependencies
   - Verify environment variables

### Health Checks
```bash
# Backend health check
curl http://localhost:5000/api/health

# Frontend accessibility
curl http://localhost/

# Database connectivity
python -c "from src.models.user import db; print('DB OK' if db else 'DB Error')"
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancers (nginx, HAProxy, AWS ALB)
- Deploy multiple backend instances
- Use Redis for session storage
- Implement database read replicas

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Use caching (Redis, Memcached)
- Implement CDN for static assets

## 🔄 Updates and Maintenance

### Rolling Updates
```bash
# Backend update
sudo systemctl stop autofounder-backend
# Deploy new code
sudo systemctl start autofounder-backend

# Frontend update
pnpm run build
sudo cp -r dist/* /var/www/autofounder-x/frontend/
```

### Database Migrations
```bash
# Run database migrations
python src/migrate.py
```

---

For additional support, please refer to the main README.md or contact the development team.

