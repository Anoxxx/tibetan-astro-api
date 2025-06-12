# API Deployment Guide for GitHub Pages

## 🏆 Recommended: Vercel Functions (Perfect for GitHub Pages)

Since your website is hosted on GitHub Pages, Vercel Functions is the ideal solution!

### Prerequisites
- Heroku account (free signup)
- Git installed
- Our Flask API files

### Step 1: Prepare for Deployment

Create a `Procfile` (tells Heroku how to run your app):
```
web: gunicorn flask_api_example:app
```

Create a `runtime.txt` (specifies Python version):
```
python-3.11.0
```

Update `requirements.txt` to include gunicorn:
```
Flask>=3.0.0
Flask-CORS>=4.0.0
gunicorn>=21.0.0
```

### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-tibetan-astro-api

# Deploy
git add .
git commit -m "Deploy Tibetan Astrology API"
git push heroku main
```

### Step 3: Your API is Live!
Your API will be available at: `https://your-tibetan-astro-api.herokuapp.com`

### Step 4: Update Your React App
```javascript
const API_BASE_URL = 'https://your-tibetan-astro-api.herokuapp.com';
```

**Cost: $7/month** for basic dyno (can handle hundreds of users)

---

## Option 2: Deploy to Vercel Functions (Serverless)

### Benefits
- Free tier (100,000 requests/month)
- Automatic scaling
- Works great with React apps

### Requirements
Convert Flask to serverless format (I can help with this)

---

## Option 3: Deploy to DigitalOcean App Platform

### Benefits  
- $5/month for basic app
- Great performance
- Easy scaling

### Steps
1. Connect GitHub repository
2. Select Python/Flask template
3. Deploy automatically

---

## Which Option Do You Prefer?

Let me know your preference and I can provide detailed setup instructions! 