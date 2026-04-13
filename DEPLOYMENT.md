# Deployment Guide

This guide will help you deploy the BrowserStack Report Generator to free hosting platforms.

## 🚀 Recommended: Deploy to Render

### Prerequisites
- GitHub account
- Render account (free, no credit card required)

### Step 1: Push to GitHub

Your code is already on GitHub at: https://github.com/EwibTech/Browserstack-Report-generator.git

### Step 2: Deploy Backend (Flask API)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `browserstack-report-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: `Free`

5. Click **"Create Web Service"**
6. Wait for deployment to complete
7. Copy your backend URL (e.g., `https://browserstack-report-backend.onrender.com`)

### Step 3: Deploy Frontend (React App)

1. In Render Dashboard, click **"New +"** → **"Static Site"**
2. Connect the same GitHub repository
3. Configure the site:
   - **Name**: `browserstack-report-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`

4. Add Environment Variable:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://browserstack-report-backend.onrender.com/api` (your backend URL from Step 2)

5. Click **"Create Static Site"**
6. Wait for deployment to complete

### Step 4: Update CORS (Important!)

After deployment, update the backend CORS settings:

1. Go to your backend service on Render
2. Add environment variable:
   - **Key**: `FRONTEND_URL`
   - **Value**: `https://browserstack-report-frontend.onrender.com` (your frontend URL)

3. The backend is already configured to use this variable

### Step 5: Test Your Deployment

1. Visit your frontend URL
2. Enter BrowserStack credentials
3. Generate a report
4. Download CSV to verify everything works

---

## 🔄 Automatic Deployments

Both services will automatically redeploy when you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

---

## 🌐 Alternative: Deploy to Vercel (Frontend) + Render (Backend)

### Backend on Render (same as above)

### Frontend on Vercel

1. Go to [Vercel](https://vercel.com)
2. Import your GitHub repository
3. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: `Create React App`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. Add Environment Variable:
   - **REACT_APP_API_URL**: `https://your-backend-url.onrender.com/api`

5. Deploy!

---

## 📝 Environment Variables Summary

### Backend (Render)
- `FRONTEND_URL` - Your frontend URL (for CORS)
- `SMTP_SERVER` - (Optional) For email functionality
- `SMTP_PORT` - (Optional) For email functionality
- `SMTP_USERNAME` - (Optional) For email functionality
- `SMTP_PASSWORD` - (Optional) For email functionality

### Frontend (Render/Vercel)
- `REACT_APP_API_URL` - Your backend API URL

---

## ⚠️ Important Notes

### Free Tier Limitations
- **Render Free Tier**: Services sleep after 15 minutes of inactivity
- **First request after sleep**: May take 30-60 seconds to wake up
- **Build minutes**: 500 minutes/month (plenty for this project)

### Security
- Never commit `.env` files with real credentials
- Use environment variables on hosting platforms
- Keep your BrowserStack credentials secure

### CORS Issues
If you encounter CORS errors:
1. Ensure `FRONTEND_URL` is set correctly in backend
2. Check that backend CORS is configured properly
3. Verify API URL in frontend matches backend URL

---

## 🔧 Troubleshooting

### Backend won't start
- Check logs in Render dashboard
- Verify `requirements.txt` is correct
- Ensure `gunicorn` is installed

### Frontend can't connect to backend
- Verify `REACT_APP_API_URL` is set correctly
- Check browser console for CORS errors
- Ensure backend is running (visit backend URL directly)

### Build fails
- Check build logs in Render/Vercel dashboard
- Verify all dependencies are in `package.json`
- Ensure Node version compatibility

---

## 📊 Monitoring

### Render Dashboard
- View deployment logs
- Monitor service health
- Check resource usage

### Custom Domain (Optional)
Both Render and Vercel support custom domains on free tier:
1. Purchase a domain (or use a free subdomain)
2. Add domain in platform settings
3. Update DNS records as instructed

---

## 🎉 You're Live!

Once deployed, share your app:
- Frontend: `https://browserstack-report-frontend.onrender.com`
- Backend API: `https://browserstack-report-backend.onrender.com`

Happy testing! 🚀
