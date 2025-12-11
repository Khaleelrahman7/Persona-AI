# Deployment Checklist - Render + Netlify

Use this checklist to ensure everything is configured correctly before deploying.

## Pre-Deployment Checklist

### Backend (Render)
- [x] `backend/Procfile` exists with correct command
- [x] `backend/requirements.txt` has all dependencies
- [x] `backend/main.py` has CORS configured with environment variable support
- [x] `backend/runtime.txt` specifies Python version (optional but recommended)
- [ ] NVIDIA API key is ready
- [ ] GitHub repository is pushed and up to date

### Frontend (Netlify)
- [x] `netlify.toml` exists in root directory
- [x] `frontend/package.json` has build script
- [x] `frontend/src/App.js` uses `REACT_APP_API_URL` environment variable
- [ ] GitHub repository is pushed and up to date

## Deployment Steps

### Step 1: Deploy Backend on Render
1. [ ] Go to [Render Dashboard](https://dashboard.render.com)
2. [ ] Create new Web Service
3. [ ] Connect GitHub repository
4. [ ] Set Root Directory: `backend`
5. [ ] Set Build Command: `pip install -r requirements.txt`
6. [ ] Set Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. [ ] Add Environment Variable: `NVIDIA_API_KEY` = your key
8. [ ] Deploy and wait for completion
9. [ ] Copy backend URL (e.g., `https://persona-ai-backend.onrender.com`)
10. [ ] Test backend: Visit `https://your-backend-url.onrender.com/` - should see `{"message": "Persona AI API is running"}`

### Step 2: Deploy Frontend on Netlify
1. [ ] Go to [Netlify Dashboard](https://app.netlify.com)
2. [ ] Add new site from Git
3. [ ] Connect repository
4. [ ] Verify build settings (auto-detected from netlify.toml):
   - Base directory: `frontend`
   - Build command: `npm install && npm run build`
   - Publish directory: `frontend/build`
5. [ ] Add Environment Variable: `REACT_APP_API_URL` = your Render backend URL
6. [ ] Deploy and wait for completion
7. [ ] Copy frontend URL (e.g., `https://persona-ai.netlify.app`)

### Step 3: Update Backend CORS
1. [ ] Go back to Render dashboard
2. [ ] Add/Update Environment Variable: `CORS_ORIGINS` = your Netlify URL
3. [ ] Redeploy backend (or it will auto-redeploy)

### Step 4: Test Everything
1. [ ] Open your Netlify frontend URL
2. [ ] Check browser console for errors
3. [ ] Try sending a message
4. [ ] Verify memory extraction works
5. [ ] Test personality transformation
6. [ ] Check before/after comparison displays correctly

## Common Issues & Solutions

### CORS Errors
- **Symptom**: Browser console shows CORS errors
- **Solution**: 
  1. Verify `CORS_ORIGINS` in Render includes your Netlify URL
  2. Make sure URL has no trailing slash
  3. Redeploy backend after updating CORS_ORIGINS

### API Connection Errors
- **Symptom**: Frontend can't connect to backend
- **Solution**:
  1. Verify `REACT_APP_API_URL` in Netlify matches your Render URL
  2. Check backend is running (visit backend URL directly)
  3. Check browser console for exact error

### Build Failures
- **Backend**: Check `requirements.txt` has all dependencies
- **Frontend**: Check `package.json` and Node version (should be 18+)

### Environment Variables Not Working
- **Backend**: Variables must be set in Render dashboard, not in code
- **Frontend**: Variables must start with `REACT_APP_` prefix
- **Both**: Redeploy after adding/updating environment variables

## Post-Deployment

- [ ] Update README with live URLs
- [ ] Test all features in production
- [ ] Monitor Render and Netlify dashboards for errors
- [ ] Set up custom domain (optional)

## Quick Reference

### Backend Environment Variables (Render)
```
NVIDIA_API_KEY=your_nvidia_api_key
CORS_ORIGINS=https://your-app.netlify.app
```

### Frontend Environment Variables (Netlify)
```
REACT_APP_API_URL=https://your-backend.onrender.com
```

## Support

If you encounter issues:
1. Check deployment logs in Render/Netlify dashboards
2. Check browser console for frontend errors
3. Test backend endpoints directly using curl or Postman
4. Verify all environment variables are set correctly


