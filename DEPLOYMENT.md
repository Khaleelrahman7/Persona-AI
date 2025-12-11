# Deployment Guide

This guide covers deploying the Persona AI application to various platforms.

## Backend Deployment

### Option 1: Railway

1. Create a new project on [Railway](https://railway.app)
2. Connect your GitHub repository
3. Add a new service and select "Deploy from GitHub repo"
4. Set the root directory to `backend`
5. Add environment variable:
   - `NVIDIA_API_KEY`: Your NVIDIA API key
6. Railway will automatically detect Python and install dependencies
7. The app will be available at the provided Railway URL

### Option 2: Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`
4. Add environment variables:
   - `NVIDIA_API_KEY`: Your NVIDIA API key
   - `CORS_ORIGINS`: Your frontend URL (e.g., `https://your-app.netlify.app`)
5. Deploy

**Note**: See `RENDER_DEPLOYMENT.md` for detailed step-by-step instructions.

### Option 3: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variable:
   ```bash
   heroku config:set NVIDIA_API_KEY=your_key_here
   ```
5. Deploy:
   ```bash
   cd backend
   git subtree push --prefix backend heroku main
   ```

### Option 4: PythonAnywhere

1. Upload backend files to PythonAnywhere
2. Create a web app
3. Set source code to your backend directory
4. Set WSGI file to point to `main:app`
5. Add environment variable in web app settings

## Frontend Deployment

### Option 1: Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Navigate to frontend directory: `cd frontend`
3. Build: `npm run build`
4. Deploy: `vercel`
5. Set environment variable:
   - `REACT_APP_API_URL`: Your backend URL (e.g., `https://your-backend.railway.app`)

### Option 2: Netlify

1. Connect GitHub repository to [Netlify](https://netlify.com)
2. Netlify will auto-detect settings from `netlify.toml`, but verify:
   - **Base directory**: `frontend`
   - **Build command**: `npm install && npm run build`
   - **Publish directory**: `frontend/build`
3. Add environment variable:
   - `REACT_APP_API_URL`: Your backend URL (e.g., `https://your-backend.onrender.com`)
4. Deploy

**Note**: See `NETLIFY_DEPLOYMENT.md` for detailed step-by-step instructions.

### Option 3: GitHub Pages

1. Install gh-pages: `npm install --save-dev gh-pages`
2. Add to `package.json`:
   ```json
   "homepage": "https://yourusername.github.io/persona-ai",
   "scripts": {
     "predeploy": "npm run build",
     "deploy": "gh-pages -d build"
   }
   ```
3. Deploy: `npm run deploy`
4. Update `REACT_APP_API_URL` to your backend URL

## Environment Variables

### Backend (Render)
- `NVIDIA_API_KEY`: Your NVIDIA API key
- `CORS_ORIGINS`: Your frontend URL (e.g., `https://your-app.netlify.app`) - **Required for CORS**

### Frontend (Netlify)
- `REACT_APP_API_URL`: Backend API URL (e.g., `https://your-backend.onrender.com`)

## Testing Deployment

1. Test backend health: `GET https://your-backend-url.com/`
2. Test memory extraction: `POST https://your-backend-url.com/api/extract-memory`
3. Test frontend: Open your frontend URL and verify it connects to backend

## Troubleshooting

### CORS Issues
- Ensure backend CORS settings include your frontend URL
- Update `allow_origins` in `backend/main.py`

### API Key Issues
- Verify environment variables are set correctly
- Check API key has proper permissions

### Build Failures
- Ensure all dependencies are in `requirements.txt` (backend) and `package.json` (frontend)
- Check Node.js and Python versions match deployment platform requirements

