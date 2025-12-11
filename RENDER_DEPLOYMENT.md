# Render Deployment Guide

## Backend Deployment on Render

### Step 1: Prepare Your Repository
1. Make sure all your code is committed and pushed to GitHub
2. Ensure `backend/requirements.txt` is up to date
3. Ensure `backend/Procfile` exists with: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 2: Create Render Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `persona-ai-backend` (or your preferred name)
   - **Environment**: `Python 3`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Set Environment Variables
In Render dashboard, go to "Environment" tab and add:
- `NVIDIA_API_KEY`: Your NVIDIA API key
- `CORS_ORIGINS`: Your Netlify frontend URL (e.g., `https://your-app.netlify.app`)

**Important**: After deploying frontend, update `CORS_ORIGINS` with the actual Netlify URL.

### Step 4: Deploy
1. Click "Create Web Service"
2. Render will automatically build and deploy
3. Wait for deployment to complete
4. Copy your backend URL (e.g., `https://persona-ai-backend.onrender.com`)

### Step 5: Update Frontend
Update your frontend `.env` or Netlify environment variables with:
```
REACT_APP_API_URL=https://your-backend-url.onrender.com
```

## Notes
- Render free tier may spin down after inactivity (takes ~30 seconds to wake up)
- For production, consider upgrading to paid tier for always-on service
- Backend URL will be something like: `https://persona-ai-backend.onrender.com`


