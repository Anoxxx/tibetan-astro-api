# Tibetan Astrological Calculator - Website Integration Guide

## Overview

This guide provides instructions for integrating the Tibetan Astrological Calculator into [zhengfei.info](https://zhengfei.info) as a new subpage under the "Miscellanies" section.

**System**: Nine Palaces Outer Calculation (九宫外算)  
**Purpose**: Calculate astrological profiles and identify potential obstacles based on Tibetan astrology  
**Target URL**: `https://zhengfei.info/tibetan-astrology`

---

## 1. Backend API Implementation

### 1.1 Python Flask API Setup

Create a Flask API service using the provided Python modules:

```bash
# Required files (already implemented):
- tibetan_astro_tables.py    # Reference tables and constants
- tibetan_astro_core.py      # Core calculation engine
- tibetan_astro_cli.py       # CLI interface (for testing)
```

### 1.2 API Endpoints

#### **Primary Endpoint**: `/api/astrology/calculate`

**Method**: `POST`  
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "birth_year": 1990,
  "current_year": 2025,
  "age": 35,
  "gender": "male",           // "male" or "female"
  "profession": "general"     // "general", "official", "monastic", "lay_practitioner", "sex_worker"
}
```

**Response Body (Success - 200 OK)**:
```json
{
  "success": true,
  "data": {
    "user_profile": {
      "gregorian_year": 1990,
      "rabjung_identifier_m": 7,
      "animal_sign": "马 (Horse)",
      "element": "金 (Metal)",
      "yin_yang": "阳 (Yang)",
      "sixty_cycle_name": "金阳马"
    },
    "user_mewas": {
      "life_mewa": {
        "number": 4,
        "color": "绿 (Green)",
        "element": "木 (Wood)"
      },
      "body_mewa": {
        "number": 7,
        "color": "红 (Red)",
        "element": "火 (Fire)"
      },
      "power_mewa": {
        "number": 1,
        "color": "白 (White)",
        "element": "金 (Metal)"
      }
    },
    "obstacle_analysis": {
      "current_year_profile": {
        "sixty_cycle_name": "木阴蛇",
        "gregorian_year": 2025
      },
      "current_year_mewas": {
        "body_mewa": {
          "number": 8,
          "color": "白 (White)",
          "element": "金 (Metal)"
        }
      },
      "obstacles_found": [
        {
          "type": "DO",
          "name": "Door Obstacle (门户障碍)",
          "interpretation": "人畜均衰、不兴旺 (Decline for people and livestock, not prosperous)",
          "details": {
            "element_clash": {
              "current_year_element": "金 (Metal)",
              "user_element": "火 (Fire)",
              "clash_direction": "user_destroys_current"
            }
          }
        }
      ],
      "total_obstacles": 1,
      "obstacle_types_present": ["DO"]
    },
    "analysis_timestamp": "2025-06-12T21:32:13.647712",
    "system_version": "1.0.0"
  }
}
```

**Response Body (Error - 400 Bad Request)**:
```json
{
  "success": false,
  "error": "Invalid input: birth_year must be between 1900 and 2100",
  "code": "VALIDATION_ERROR"
}
```

#### **Secondary Endpoint**: `/api/astrology/prosperity`

**Method**: `POST`  
**Purpose**: Assess prosperity of specific events

**Request Body**:
```json
{
  "event_type": "着衣 (Wearing new clothes)",
  "event_date": "2025-07-15",
  "event_hour": 14,
  "user_profile": {
    // Optional: user's profile from previous calculation
  }
}
```

### 1.3 Flask Implementation Template

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from tibetan_astro_core import TibetanAstroCalculator
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for your React frontend

calculator = TibetanAstroCalculator()

@app.route('/api/astrology/calculate', methods=['POST'])
def calculate_astrology():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['birth_year', 'current_year', 'age', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}',
                    'code': 'VALIDATION_ERROR'
                }), 400
        
        # Perform calculation
        result = calculator.full_analysis(
            birth_year=int(data['birth_year']),
            current_year=int(data['current_year']),
            user_age=int(data['age']),
            user_gender=data['gender'],
            user_profession=data.get('profession', 'general')
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 'VALIDATION_ERROR'
        }), 400
    except Exception as e:
        logging.error(f"Calculation error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'code': 'SERVER_ERROR'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 2. Frontend React Component Specification

### 2.1 Component Structure

```
TibetanAstrologyPage/
├── TibetanAstrologyCalculator.jsx    # Main component
├── components/
│   ├── InputForm.jsx                 # Step 1: User input
│   ├── ResultsDisplay.jsx            # Step 2: Results
│   ├── MewaCircle.jsx               # Mewa number visualization
│   └── ObstacleCard.jsx             # Obstacle display
├── styles/
│   └── TibetanAstrology.css         # Matching zhengfei.info aesthetic
└── utils/
    └── api.js                       # API call functions
```

### 2.2 Design Guidelines (Matching zhengfei.info Aesthetic)

Based on your website's clean, academic design:

**Color Palette**:
- Primary: Clean blacks and whites (matching your current design)
- Accent: Subtle grays for sections
- Mewa Colors: 
  - 白 (White): `#f8f9fa`
  - 黑 (Black): `#343a40` 
  - 蓝 (Blue): `#007bff`
  - 绿 (Green): `#28a745`
  - 黄 (Yellow): `#ffc107`
  - 红 (Red): `#dc3545`

**Typography**:
- Use your existing font family
- Clear hierarchy with h2, h3 headings
- Monospace for technical data (like your publications)

**Layout**:
- Single-column layout on mobile
- Two-column on desktop (form | results)
- Card-based sections
- Minimal, clean spacing

### 2.3 Component Props and State

```javascript
// Main component state
const [formData, setFormData] = useState({
  birthYear: '',
  currentYear: new Date().getFullYear(),
  age: '',
  gender: '',
  profession: 'general'
});

const [results, setResults] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState('');
const [step, setStep] = useState(1); // 1: form, 2: loading, 3: results
```

### 2.4 Key Features to Implement

1. **Progressive Form**: Step-by-step input collection
2. **Real-time Validation**: Immediate feedback on invalid inputs
3. **Loading States**: Beautiful loading animation during calculation
4. **Results Visualization**: 
   - Mewa numbers as colored circles
   - Obstacle cards with clear interpretations
   - Downloadable results (JSON/PDF)
5. **Responsive Design**: Works on all devices
6. **Error Handling**: Clear error messages
7. **Reset Functionality**: Easy to start over

---

## 3. Website Integration Steps

### 3.1 Add to Navigation

Update your website's navigation to include the new page under "Miscellanies":

```javascript
// In your navigation component
const miscellaneousItems = [
  // ... existing items
  {
    title: "Tibetan Astrology Calculator",
    path: "/tibetan-astrology",
    description: "Nine Palaces Outer Calculation (九宫外算)"
  }
];
```

### 3.2 Route Configuration

Add the route to your React Router setup:

```javascript
import TibetanAstrologyPage from './pages/TibetanAstrologyPage';

// In your App.js or router configuration
<Route 
  path="/tibetan-astrology" 
  element={<TibetanAstrologyPage />} 
/>
```

### 3.3 Page Metadata

```javascript
// SEO and metadata
const pageMetadata = {
  title: "Tibetan Astrological Calculator | Zhengfei Zhang",
  description: "Calculate your Tibetan astrological profile using the Nine Palaces Outer Calculation system. Analyze obstacles and prosperity based on traditional Tibetan astrology.",
  keywords: "tibetan astrology, nine palaces, mewa calculation, astrological calculator",
  canonicalUrl: "https://zhengfei.info/tibetan-astrology"
};
```

---

## 4. API Integration Code

### 4.1 API Service (utils/api.js)

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

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
        profession: formData.profession
      })
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Calculation failed');
    }
    
    return data.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const assessProsperity = async (eventData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/astrology/prosperity`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(eventData)
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Prosperity assessment failed');
    }
    
    return data.data;
  } catch (error) {
    console.error('Prosperity API Error:', error);
    throw error;
  }
};
```

### 4.2 React Hook for API Calls

```javascript
// Custom hook for astrology calculations
import { useState } from 'react';
import { calculateAstrology } from '../utils/api';

export const useAstrologyCalculation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  const calculate = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await calculateAstrology(formData);
      setResults(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResults(null);
    setError(null);
    setLoading(false);
  };

  return { calculate, loading, error, results, reset };
};
```

---

## 5. UI/UX Specifications

### 5.1 Input Form Layout

```
┌─────────────────────────────────────┐
│ 🏔️ Tibetan Astrological Calculator │
│ Nine Palaces Outer Calculation     │
├─────────────────────────────────────┤
│ 📅 Birth Information               │
│ ┌─────────────────────────────────┐ │
│ │ Birth Year: [____1990_____]     │ │
│ │ Current Age: [____35______]     │ │  
│ │ Current Year: [____2025____]    │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 👤 Demographics                    │
│ ┌─────────────────────────────────┐ │
│ │ Gender: ○ Male ● Female         │ │
│ │ Profession: [General ▼]         │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [🔮 Calculate Astrological Profile] │
└─────────────────────────────────────┘
```

### 5.2 Results Display Layout

```
┌─────────────────────────────────────┐
│ 🏔️ Your Astrological Profile      │
├─────────────────────────────────────┤
│ 📊 Birth Profile                   │
│ Birth Year: 1990                    │
│ Sign: 金阳马 | Animal: 马 (Horse)    │
│ Element: 金 (Metal) | Yin/Yang: 阳   │
├─────────────────────────────────────┤
│ 🔢 Mewa Numbers                    │
│ ┌─────┐ ┌─────┐ ┌─────┐           │
│ │  4  │ │  7  │ │  1  │           │
│ │Life │ │Body │ │Power│           │  
│ │ 绿  │ │ 红  │ │ 白  │           │
│ └─────┘ └─────┘ └─────┘           │
├─────────────────────────────────────┤
│ ⚠️ Obstacle Analysis               │
│ 1 obstacle(s) detected             │
│ ┌─────────────────────────────────┐ │
│ │ DO: Door Obstacle (门户障碍)     │ │
│ │ 人畜均衰、不兴旺                 │ │
│ └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│ [🔄 Calculate Another] [💾 Download] │
└─────────────────────────────────────┘
```

### 5.3 Mewa Circle Component

```css
.mewa-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  margin: 10px auto;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

---

## 6. Deployment Considerations

### 6.1 Environment Variables

```bash
# .env file
REACT_APP_API_URL=https://api.zhengfei.info
FLASK_APP=app.py
FLASK_ENV=production
```

### 6.2 Backend Deployment

1. **Option A**: Deploy Flask API as a separate service
2. **Option B**: Integrate with existing backend infrastructure
3. **Option C**: Use serverless functions (AWS Lambda, Vercel Functions)

### 6.3 Performance Optimization

- Cache reference tables in memory
- Add request rate limiting
- Implement result caching for common inputs
- Optimize bundle size for frontend

---

## 7. Testing Strategy

### 7.1 Test Cases

**Core Functionality**:
- Verify 1984 → 木阳鼠 (Life: 1, Body: 4, Power: 7)
- Verify 1990 → 金阳马 (Life: 4, Body: 7, Power: 1)
- Test obstacle detection logic
- Validate edge cases (age boundaries, special professions)

**UI Testing**:
- Form validation
- Error handling
- Responsive design
- Loading states

### 7.2 Test Data

```javascript
const testCases = [
  {
    name: "Document Example 1984",
    input: { birth_year: 1984, current_year: 2025, age: 41, gender: "male" },
    expected: { sixty_cycle_name: "木阳鼠", life_mewa: 1, body_mewa: 4, power_mewa: 7 }
  },
  {
    name: "Document Example 1990", 
    input: { birth_year: 1990, current_year: 2025, age: 35, gender: "male" },
    expected: { sixty_cycle_name: "金阳马", life_mewa: 4, body_mewa: 7, power_mewa: 1 }
  }
];
```

---

## 8. Documentation for Users

### 8.1 Page Introduction Text

```markdown
# Tibetan Astrological Calculator

This calculator implements the **Nine Palaces Outer Calculation** (九宫外算) system from Tibetan astrology. It calculates your astrological profile based on your birth year and analyzes potential obstacles in the current year.

## How to Use

1. **Enter your birth information** - Year, current age, and current year
2. **Provide demographics** - Gender and profession (affects obstacle calculations)  
3. **Get your profile** - View your animal sign, elements, and Mewa numbers
4. **Understand obstacles** - Learn about potential challenges and their meanings

## About the System

The Nine Palaces Outer Calculation is a traditional Tibetan astrological system that:
- Determines your 60-cycle astrological sign (animal + element + yin/yang)
- Calculates three Mewa numbers: Life (命格), Body (体格), and Power (权格)
- Identifies four types of obstacles: Regional (RO), Home (HO), Bedding (BO), and Door (DO)
- Provides interpretations and guidance based on ancient wisdom

*Note: This calculator is for educational and cultural interest purposes.*
```

### 8.2 Help/FAQ Section

Include explanations of:
- What each Mewa number represents
- How obstacles are calculated
- Meaning of different obstacle types
- Cultural context and traditional usage

---

## 9. File Structure Summary

```
zhengfei.info/
├── backend/
│   ├── api/
│   │   ├── tibetan_astro_tables.py
│   │   ├── tibetan_astro_core.py
│   │   └── app.py                    # Flask API
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   └── TibetanAstrologyPage.jsx
│   │   ├── components/
│   │   │   ├── InputForm.jsx
│   │   │   ├── ResultsDisplay.jsx
│   │   │   ├── MewaCircle.jsx
│   │   │   └── ObstacleCard.jsx
│   │   ├── utils/
│   │   │   └── api.js
│   │   └── styles/
│   │       └── TibetanAstrology.css
│   └── package.json
└── docs/
    └── WEBSITE_INTEGRATION_GUIDE.md  # This file
```

---

## 10. Next Steps

1. **Set up backend API** using the provided Python modules
2. **Create React components** following the specifications above
3. **Style components** to match zhengfei.info aesthetic
4. **Add route and navigation** links
5. **Test thoroughly** with the provided test cases
6. **Deploy and monitor** the new feature

This integration will add a unique, interactive element to your academic website that showcases both technical implementation skills and cultural interest in traditional knowledge systems.

**Contact**: For technical questions about the algorithm implementation, refer to the provided Python modules and CLI tool for testing. 