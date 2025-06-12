# Frontend Integration Guide: Tibetan Astrological Calculator API

This guide provides step-by-step instructions for integrating the Tibetan Astrological Calculator API into your React-based website, such as `zhengfei.info`.

**API URL:** `https://tibetan-astro-api.vercel.app`

---

## 1. API Endpoint Overview

### Main Calculation Endpoint

- **URL:** `/api/astrology`
- **Method:** `POST`
- **Description:** Performs the full astrological analysis.

**Request Body (JSON):**

```json
{
  "birth_year": 1990,       // integer
  "current_year": 2025,   // integer
  "age": 35,              // integer
  "gender": "male",         // "male" or "female"
  "profession": "general" // "general", "official", "monastic", "lay_practitioner", "sex_worker"
}
```

**Success Response (200 OK):**

The response is a JSON object containing the full analysis. See the `user_profile`, `user_mewas`, and `obstacle_analysis` keys for detailed results.

```json
{
  "success": true,
  "data": {
    "user_profile": { ... },
    "user_mewas": { ... },
    "obstacle_analysis": { ... },
    "analysis_timestamp": "...",
    "system_version": "1.0.0"
  }
}
```

### Health Check Endpoint

- **URL:** `/api/astrology`
- **Method:** `GET`
- **Description:** Confirms the API is online and returns its status.

---

## 2. React Component Example

Here is a complete, self-contained React component that you can drop into your project. It handles user input, API calls, loading states, errors, and displays the results in a user-friendly format.

### `TibetanAstroCalculator.js`

```javascript
import React, { useState } from 'react';

// You can create a separate CSS file or use styled-components/inline styles
import './TibetanAstroCalculator.css';

const TibetanAstroCalculator = () => {
    const [formData, setFormData] = useState({
        birth_year: '1990',
        gender: 'male',
        profession: 'general',
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        const currentYear = new Date().getFullYear();
        const age = currentYear - parseInt(formData.birth_year, 10);

        try {
            const response = await fetch('https://tibetan-astro-api.vercel.app/api/astrology', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    birth_year: parseInt(formData.birth_year, 10),
                    current_year: currentYear,
                    age: age,
                    gender: formData.gender,
                    profession: formData.profession,
                }),
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'An unknown error occurred.');
            }

            setResult(data.data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const renderObstacles = () => {
        const obstacles = result.obstacle_analysis.obstacles_found;
        if (obstacles.length === 0) {
            return <div className="tac-no-obstacles">✅ No Obstacles Detected for the Current Year.</div>;
        }
        return (
            <div className="tac-obstacles-list">
                <h4>⚠️ {obstacles.length} Obstacle(s) Detected:</h4>
                {obstacles.map((obs, index) => (
                    <div key={index} className="tac-obstacle-item">
                        <strong>{obs.name} ({obs.type})</strong>
                        <p>{obs.interpretation}</p>
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="tac-container">
            <h2>Tibetan Astrological Calculator (九宫外算)</h2>
            <form onSubmit={handleSubmit} className="tac-form">
                <div className="tac-form-group">
                    <label htmlFor="birth_year">Birth Year (年份):</label>
                    <input
                        type="number"
                        id="birth_year"
                        name="birth_year"
                        value={formData.birth_year}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="tac-form-group">
                    <label htmlFor="gender">Gender (性别):</label>
                    <select id="gender" name="gender" value={formData.gender} onChange={handleInputChange}>
                        <option value="male">Male (男)</option>
                        <option value="female">Female (女)</option>
                    </select>
                </div>
                <div className="tac-form-group">
                    <label htmlFor="profession">Status (身份):</label>
                    <select id="profession" name="profession" value={formData.profession} onChange={handleInputChange}>
                        <option value="general">General (普通)</option>
                        <option value="official">Official (官员)</option>
                        <option value="monastic">Monastic (出家人)</option>
                        <option value="lay_practitioner">Lay Practitioner (居家士)</option>
                        <option value="sex_worker">Sex Worker (性工作者)</option>
                    </select>
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Calculating...' : 'Calculate'}
                </button>
            </form>

            {error && <div className="tac-error">Error: {error}</div>}

            {result && (
                <div className="tac-results">
                    <h3>Analysis Results</h3>
                    <div className="tac-results-grid">
                        <div className="tac-result-card">
                            <h4>Astrological Sign (属相)</h4>
                            <p className="tac-prominent">{result.user_profile.sixty_cycle_name}</p>
                            <p>{result.user_profile.animal_sign}</p>
                            <p>{result.user_profile.element} • {result.user_profile.yin_yang}</p>
                        </div>
                        <div className="tac-result-card">
                            <h4>Mewa Numbers (九宫)</h4>
                            <p><strong>Life (命):</strong> {result.user_mewas.life_mewa.number} {result.user_mewas.life_mewa.color}</p>
                            <p><strong>Body (体):</strong> {result.user_mewas.body_mewa.number} {result.user_mewas.body_mewa.color}</p>
                            <p><strong>Power (权):</strong> {result.user_mewas.power_mewa.number} {result.user_mewas.power_mewa.color}</p>
                        </div>
                    </div>
                    <div className="tac-result-card">
                        <h4>Obstacle Analysis (障碍)</h4>
                        <p>For current year: {result.obstacle_analysis.current_year_profile.gregorian_year} ({result.obstacle_analysis.current_year_profile.sixty_cycle_name})</p>
                        {renderObstacles()}
                    </div>
                </div>
            )}
        </div>
    );
};

export default TibetanAstroCalculator;
```

---

### `TibetanAstroCalculator.css`

Create this corresponding CSS file to style the component.

```css
.tac-container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    background-color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.tac-container h2 {
    text-align: center;
    color: #333;
    margin-bottom: 1.5rem;
}

.tac-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.tac-form-group {
    display: flex;
    flex-direction: column;
}

.tac-form-group label {
    margin-bottom: 0.5rem;
    color: #555;
    font-weight: bold;
}

.tac-form-group input,
.tac-form-group select {
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
}

.tac-form button {
    padding: 0.8rem 1.5rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.tac-form button:disabled {
    background-color: #aaa;
    cursor: not-allowed;
}

.tac-form button:hover:not(:disabled) {
    background-color: #0056b3;
}

.tac-error {
    margin-top: 1rem;
    padding: 0.75rem;
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
    text-align: center;
}

.tac-results {
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid #eee;
}

.tac-results h3 {
    text-align: center;
    margin-bottom: 1.5rem;
}

.tac-results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.tac-result-card {
    background-color: #f9f9f9;
    padding: 1.5rem;
    border-radius: 8px;
    border: 1px solid #eee;
}

.tac-result-card h4 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: #007bff;
    border-bottom: 2px solid #eef;
    padding-bottom: 0.5rem;
}

.tac-result-card p {
    margin: 0.5rem 0;
    line-height: 1.5;
}

.tac-result-card .tac-prominent {
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
}

.tac-no-obstacles {
    color: #155724;
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    padding: 1rem;
    border-radius: 4px;
    text-align: center;
    margin-top: 1rem;
}

.tac-obstacles-list {
    margin-top: 1rem;
}

.tac-obstacle-item {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #eee;
}
.tac-obstacle-item:last-child {
    border-bottom: none;
    padding-bottom: 0;
}
.tac-obstacle-item strong {
    color: #dc3545;
}

```

---

## 3. How to Use

1.  **Save the Files:** Save the code above as `TibetanAstroCalculator.js` and `TibetanAstroCalculator.css` in your React project's components directory (e.g., `src/components/`).
2.  **Import the Component:** In the page where you want to display the calculator (e.g., in a "Miscellanies" section on `zhengfei.info`), import the component:

    ```javascript
    import TibetanAstroCalculator from './components/TibetanAstroCalculator';
    ```
3.  **Use the Component:** Add the component to your JSX:

    ```javascript
    function MiscellaniesPage() {
      return (
        <div>
          <h1>Miscellanies</h1>
          <p>Here are some interesting tools and calculations.</p>
          
          <hr />
          
          <TibetanAstroCalculator />
          
          {/* Other content... */}
        </div>
      );
    }
    ```

This provides a complete, working, and styled solution for integrating the calculator into your website. 