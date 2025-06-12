# 🏔️ GitHub Pages + Vercel API Deployment Guide

Since **zhengfei.info** is hosted on GitHub Pages, here's the **perfect solution**:

## 🎯 **Architecture**
```
zhengfei.info (GitHub Pages)  →  API calls  →  Vercel Functions (Python API)
     Static React Site         →   HTTPS     →  Serverless Python
         FREE                  →              →      FREE*
```

**Cost: FREE** for up to 100,000 API calls/month!

---

## 🚀 **Step-by-Step Setup**

### **Step 1: Create Vercel Account**
1. Go to [vercel.com](https://vercel.com)
2. Sign up with your GitHub account
3. ✅ Done in 30 seconds!

### **Step 2: Prepare API Files**
Create a new repository (or use existing) with these files:

```
your-tibetan-api-repo/
├── api/
│   └── astrology.py          # ✅ Already created
├── tibetan_astro_tables.py   # ✅ Copy from our project  
├── tibetan_astro_core.py     # ✅ Copy from our project
├── vercel.json               # ✅ Already created
└── requirements.txt          # ✅ Already created
```

### **Step 3: Deploy to Vercel**

**Option A: GitHub Integration (Recommended)**
1. Push files to a GitHub repository
2. Connect repository to Vercel
3. Vercel automatically deploys on every push

**Option B: Vercel CLI**
```bash
npm i -g vercel
vercel login
vercel --prod
```

### **Step 4: Your API is Live! 🎉**
Your API will be available at:
```
https://your-project-name.vercel.app/api/astrology/calculate
```

### **Step 5: Update zhengfei.info**
In your React code, update the API URL:
```javascript
const API_BASE_URL = 'https://your-project-name.vercel.app';

// Make API calls
fetch(`${API_BASE_URL}/api/astrology/calculate`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    birth_year: 1990,
    current_year: 2025,
    age: 35,
    gender: 'male'
  })
})
```

---

## 🔧 **Detailed Integration**

### **For Your React Components:**

```javascript
// utils/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-tibetan-api.vercel.app';

export const calculateAstrology = async (formData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/astrology/calculate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        birth_year: parseInt(formData.birthYear),
        current_year: parseInt(formData.currentYear),
        age: parseInt(formData.age),
        gender: formData.gender,
        profession: formData.profession || 'general'
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Calculation failed');
    }
    
    return result.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
```

### **Environment Variables:**
Add to your React app's `.env` file:
```bash
REACT_APP_API_URL=https://your-tibetan-api.vercel.app
```

---

## ✅ **Benefits of This Setup**

### **💰 Cost**
- **GitHub Pages**: FREE (your site stays where it is)
- **Vercel Functions**: FREE up to 100,000 calls/month
- **Total Monthly Cost**: $0

### **🚀 Performance**
- **Global CDN**: Your API runs on Vercel's edge network
- **Fast Cold Starts**: Python functions start quickly
- **Auto-scaling**: Handles traffic spikes automatically

### **🛠️ Maintenance**
- **Zero Server Management**: No servers to maintain
- **Automatic Updates**: Deploy by pushing to GitHub
- **Built-in Monitoring**: Vercel provides analytics

### **🔒 Security**
- **HTTPS by Default**: All API calls are encrypted
- **CORS Configured**: Works seamlessly with your React app
- **No API Keys Needed**: Simple, secure setup

---

## 🧪 **Testing Your Setup**

### **Test the API Directly:**
```bash
curl -X POST https://your-tibetan-api.vercel.app/api/astrology/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "birth_year": 1990,
    "current_year": 2025,
    "age": 35,
    "gender": "male",
    "profession": "general"
  }'
```

### **Expected Response:**
```json
{
  "success": true,
  "data": {
    "user_profile": {
      "sixty_cycle_name": "金阳马",
      "animal_sign": "马 (Horse)",
      "element": "金 (Metal)",
      "yin_yang": "阳 (Yang)"
    },
    "user_mewas": {
      "life_mewa": {"number": 4, "color": "绿 (Green)"},
      "body_mewa": {"number": 7, "color": "红 (Red)"},
      "power_mewa": {"number": 1, "color": "白 (White)"}
    }
  }
}
```

---

## 🚢 **Alternative: Keep It Even Simpler**

If you want to avoid any API setup, we could also:

### **Option: Client-Side Only**
- Convert Python logic to JavaScript
- Run entirely in the browser
- No API needed, but larger bundle size

### **Would you prefer:**
1. ✅ **Vercel API** (recommended) - Professional, scalable
2. 🔄 **Client-side JS** - Simpler, but larger download

---

## 🎯 **Summary**

**Perfect Solution for GitHub Pages:**
- ✅ Keep zhengfei.info on GitHub Pages (FREE)
- ✅ Add Vercel API (FREE up to 100k calls/month)
- ✅ Professional setup with zero maintenance
- ✅ Easy deployment and updates

**Your users get:**
- Fast, reliable API responses
- Seamless user experience
- Traditional Tibetan calculations with modern UX

**Ready to set this up?** I can help you through each step! 