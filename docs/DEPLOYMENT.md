# Deployment Guide

This guide covers deploying the Poker API to Railway.app and hosting the frontend on GitHub Pages.

## Prerequisites

- GitHub account
- Railway.app account
- Firebase project (optional, for database features)

## Backend Deployment (Railway.app)

### 1. Connect Repository to Railway

1. Go to [Railway.app](https://railway.app/)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose the `putrtest` repository
5. Railway will automatically detect the configuration

### 2. Configure Environment Variables

In Railway dashboard, add these environment variables:

**Required:**
```
APP_NAME=Poker API
DEBUG=false
HOST=0.0.0.0
PORT=$PORT
```

**Optional (for Firebase):**
```
FIREBASE_PROJECT_ID=your-firebase-project-id
```

For Firebase credentials, you have two options:

#### Option A: Using Service Account Key File
1. Download service account key from Firebase Console
2. In Railway, go to Settings > Variables
3. Click "Raw Editor"
4. Add a multiline variable with the entire JSON content

#### Option B: Using Application Default Credentials
1. Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable
2. Railway can use built-in service account authentication

### 3. Deploy

Railway will automatically deploy your application when you push to the main branch.

- Build Command: Automatically detected (pip install)
- Start Command: From `Procfile` - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 4. Get Your Deployment URL

After deployment, Railway will provide a URL like:
```
https://your-app-name.railway.app
```

## Frontend Deployment (GitHub Pages)

### 1. Enable GitHub Pages

1. Go to repository Settings > Pages
2. Under "Source", select:
   - Branch: `main`
   - Folder: `/frontend`
3. Click "Save"

### 2. Update API URL

Edit `frontend/index.html` and update the API URL:

```javascript
// Change this line
const API_URL = 'http://localhost:8000';

// To your Railway URL
const API_URL = 'https://your-app-name.railway.app';
```

Commit and push the change.

### 3. Access Your Frontend

Your frontend will be available at:
```
https://samfeldman824.github.io/putrtest/
```

## Firebase Setup (Optional)

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Firestore Database

### 2. Create Service Account

1. Go to Project Settings > Service Accounts
2. Click "Generate New Private Key"
3. Download the JSON file

### 3. Configure Railway

Upload the service account JSON to Railway:

1. In Railway dashboard, go to Variables
2. Add `FIREBASE_CREDENTIALS_PATH` as a variable
3. Or add the entire JSON content as `GOOGLE_APPLICATION_CREDENTIALS`

## CORS Configuration

Update CORS origins in Railway environment variables:

```
CORS_ORIGINS=["https://samfeldman824.github.io", "https://your-custom-domain.com"]
```

## Custom Domain (Optional)

### Railway Custom Domain

1. In Railway dashboard, go to Settings > Domains
2. Click "Custom Domain"
3. Add your domain and configure DNS

### GitHub Pages Custom Domain

1. In repository Settings > Pages
2. Add your custom domain under "Custom domain"
3. Configure DNS with CNAME record

## Monitoring and Logs

### Railway Logs

View logs in Railway dashboard:
1. Go to your project
2. Click on "Deployments"
3. Select a deployment to view logs

The application uses structured JSON logging for easy parsing.

### Health Check

Monitor application health:
```bash
curl https://your-app-name.railway.app/health
```

## CI/CD

The repository includes GitHub Actions workflows in `.github/workflows/ci.yml`:

- **Linting**: Runs on every push/PR
- **Type Checking**: MyPy validation
- **Security Scanning**: Bandit security checks
- **Testing**: Pytest with coverage

## Troubleshooting

### Application Won't Start

1. Check Railway logs for errors
2. Verify environment variables are set correctly
3. Ensure `requirements.txt` is up to date

### Firebase Connection Issues

1. Verify service account credentials are correct
2. Check Firebase project ID matches
3. Ensure Firestore is enabled in Firebase Console

### CORS Errors

1. Add frontend URL to `CORS_ORIGINS` environment variable
2. Restart the Railway deployment

### Build Failures

1. Check `requirements.txt` for conflicting dependencies
2. Verify Python version compatibility (requires Python 3.11+)
3. Review build logs in Railway dashboard

## Performance Optimization

### Railway

- Use Railway's built-in metrics
- Consider upgrading plan for more resources
- Enable auto-scaling if needed

### Caching

Consider adding Redis for caching:
1. Add Redis plugin in Railway
2. Update application to use caching

## Security Best Practices

1. **Never commit secrets** to the repository
2. **Use environment variables** for all sensitive data
3. **Enable HTTPS** (automatic with Railway)
4. **Restrict CORS** to specific origins in production
5. **Add rate limiting** for production use
6. **Implement authentication** for sensitive endpoints

## Backup and Recovery

### Firebase Data

- Enable Firebase automatic backups
- Export Firestore data regularly
- Keep backups in separate location

### Application Code

- Always work in branches
- Tag releases for easy rollback
- Keep deployment documentation updated

## Cost Estimation

### Railway.app
- Free tier: Limited usage
- Starter: $5/month
- Pro: $20/month

### Firebase
- Spark (Free): Limited reads/writes
- Blaze (Pay-as-you-go): Based on usage

## Support

For issues or questions:
1. Check the [README.md](../README.md)
2. Review the [API documentation](API.md)
3. Open an issue on GitHub
