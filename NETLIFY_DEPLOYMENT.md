# Netlify Deployment Guide

## Frontend Deployment on Netlify

### Step 1: Prepare Your Repository
1. Make sure all your code is committed and pushed to GitHub
2. Ensure `netlify.toml` exists in the root directory
3. Ensure `frontend/package.json` has build script

### Step 2: Create Netlify Site
1. Go to [Netlify Dashboard](https://app.netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect to your Git provider (GitHub/GitLab/Bitbucket)
4. Select your repository

### Step 3: Configure Build Settings
Netlify should auto-detect from `netlify.toml`, but verify:
- **Base directory**: `frontend`
- **Build command**: `npm install && npm run build`
- **Publish directory**: `frontend/build`

### Step 4: Set Environment Variables
In Netlify dashboard, go to "Site settings" → "Environment variables" and add:
- `REACT_APP_API_URL`: Your Render backend URL (e.g., `https://persona-ai-backend.onrender.com`)

**Important**: 
- Use your actual Render backend URL
- Netlify will rebuild when you add environment variables
- Variable names must start with `REACT_APP_` to be accessible in React

### Step 5: Deploy
1. Click "Deploy site"
2. Wait for build to complete
3. Your site will be available at: `https://random-name-12345.netlify.app`
4. You can customize the domain name in site settings

### Step 6: Update Backend CORS
After getting your Netlify URL, update Render backend environment variable:
- Go to Render dashboard → Your service → Environment
- Update `CORS_ORIGINS` to: `https://your-netlify-app.netlify.app`
- Redeploy backend if needed

## Custom Domain (Optional)
1. Go to "Domain settings" in Netlify
2. Add your custom domain
3. Follow DNS configuration instructions

## Notes
- Netlify automatically deploys on every push to main branch
- Preview deployments are created for pull requests
- Build logs are available in the deploy log


