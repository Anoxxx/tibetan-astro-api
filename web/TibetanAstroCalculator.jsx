import React, { useState, useEffect } from 'react';
import './TibetanAstroCalculator.css';

const TibetanAstroCalculator = () => {
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
  const [step, setStep] = useState(1);

  const professionOptions = [
    { value: 'general', label: 'General' },
    { value: 'official', label: 'Official' },
    { value: 'monastic', label: 'Monastic' },
    { value: 'lay_practitioner', label: 'Lay Practitioner' },
    { value: 'sex_worker', label: 'Sex Worker' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError('');
  };

  const validateForm = () => {
    const { birthYear, age, gender } = formData;
    
    if (!birthYear || birthYear < 1900 || birthYear > 2100) {
      setError('Please enter a valid birth year between 1900 and 2100');
      return false;
    }
    
    if (!age || age < 0 || age > 150) {
      setError('Please enter a valid age between 0 and 150');
      return false;
    }
    
    if (!gender) {
      setError('Please select your gender');
      return false;
    }
    
    return true;
  };

  const calculateAstrology = async () => {
    if (!validateForm()) return;
    
    setLoading(true);
    setError('');
    
    try {
      // For now, we'll use a mock API call
      // In production, this would call your Flask API
      const response = await mockApiCall(formData);
      setResults(response);
      setStep(3);
    } catch (err) {
      setError('An error occurred during calculation. Please try again.');
      console.error('Calculation error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Mock API call - replace with actual API endpoint
  const mockApiCall = async (data) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          user_profile: {
            gregorian_year: data.birthYear,
            sixty_cycle_name: "金阳马",
            animal_sign: "马 (Horse)",
            element: "金 (Metal)",
            yin_yang: "阳 (Yang)",
            rabjung_identifier_m: 7
          },
          user_mewas: {
            life_mewa: { number: 4, color: "绿 (Green)", element: "木 (Wood)" },
            body_mewa: { number: 7, color: "红 (Red)", element: "火 (Fire)" },
            power_mewa: { number: 1, color: "白 (White)", element: "金 (Metal)" }
          },
          obstacle_analysis: {
            current_year_profile: {
              sixty_cycle_name: "木阴蛇",
              gregorian_year: data.currentYear
            },
            current_year_mewas: {
              body_mewa: { number: 8, color: "白 (White)", element: "金 (Metal)" }
            },
            obstacles_found: [
              {
                type: "DO",
                name: "Door Obstacle (门户障碍)",
                interpretation: "人畜均衰、不兴旺 (Decline for people and livestock, not prosperous)",
                details: {
                  element_clash: {
                    current_year_element: "金 (Metal)",
                    user_element: "火 (Fire)",
                    clash_direction: "user_destroys_current"
                  }
                }
              }
            ],
            total_obstacles: 1
          }
        });
      }, 1500);
    });
  };

  const resetCalculator = () => {
    setResults(null);
    setStep(1);
    setError('');
    setFormData({
      birthYear: '',
      currentYear: new Date().getFullYear(),
      age: '',
      gender: '',
      profession: 'general'
    });
  };

  const renderMewaCircle = (mewa) => {
    const colorMap = {
      '白 (White)': '#f8f9fa',
      '黑 (Black)': '#343a40',
      '蓝 (Blue)': '#007bff',
      '绿 (Green)': '#28a745',
      '黄 (Yellow)': '#ffc107',
      '红 (Red)': '#dc3545'
    };

    return (
      <div 
        className="mewa-circle"
        style={{ 
          backgroundColor: colorMap[mewa.color] || '#6c757d',
          color: mewa.color.includes('White') || mewa.color.includes('Yellow') ? '#000' : '#fff'
        }}
      >
        {mewa.number}
      </div>
    );
  };

  if (step === 1) {
    return (
      <div className="tibetan-astro-container">
        <div className="astro-header">
          <h2>🏔️ Tibetan Astrological Calculator</h2>
          <p>Nine Palaces Outer Calculation (九宫外算)</p>
        </div>

        <div className="astro-form">
          <div className="form-section">
            <h3>📅 Birth Information</h3>
            <div className="form-group">
              <label htmlFor="birthYear">Birth Year</label>
              <input
                type="number"
                id="birthYear"
                name="birthYear"
                value={formData.birthYear}
                onChange={handleInputChange}
                placeholder="e.g., 1990"
                min="1900"
                max="2100"
              />
            </div>

            <div className="form-group">
              <label htmlFor="age">Current Age</label>
              <input
                type="number"
                id="age"
                name="age"
                value={formData.age}
                onChange={handleInputChange}
                placeholder="e.g., 35"
                min="0"
                max="150"
              />
            </div>

            <div className="form-group">
              <label htmlFor="currentYear">Current Year</label>
              <input
                type="number"
                id="currentYear"
                name="currentYear"
                value={formData.currentYear}
                onChange={handleInputChange}
                min="1900"
                max="2100"
              />
            </div>
          </div>

          <div className="form-section">
            <h3>👤 Demographics</h3>
            <div className="form-group">
              <label>Gender</label>
              <div className="radio-group">
                <label className="radio-label">
                  <input
                    type="radio"
                    name="gender"
                    value="male"
                    checked={formData.gender === 'male'}
                    onChange={handleInputChange}
                  />
                  Male
                </label>
                <label className="radio-label">
                  <input
                    type="radio"
                    name="gender"
                    value="female"
                    checked={formData.gender === 'female'}
                    onChange={handleInputChange}
                  />
                  Female
                </label>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="profession">Profession/Status (Optional)</label>
              <select
                id="profession"
                name="profession"
                value={formData.profession}
                onChange={handleInputChange}
              >
                {professionOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button 
            className="calculate-btn"
            onClick={calculateAstrology}
            disabled={loading}
          >
            {loading ? '🔮 Calculating...' : '🔮 Calculate Astrological Profile'}
          </button>
        </div>
      </div>
    );
  }

  if (step === 3 && results) {
    return (
      <div className="tibetan-astro-container">
        <div className="astro-header">
          <h2>🏔️ Your Astrological Profile</h2>
        </div>

        <div className="results-container">
          {/* User Profile */}
          <div className="result-section">
            <h3>📊 Birth Profile</h3>
            <div className="profile-grid">
              <div className="profile-item">
                <strong>Birth Year:</strong> {results.user_profile.gregorian_year}
              </div>
              <div className="profile-item">
                <strong>Astrological Sign:</strong> {results.user_profile.sixty_cycle_name}
              </div>
              <div className="profile-item">
                <strong>Animal:</strong> {results.user_profile.animal_sign}
              </div>
              <div className="profile-item">
                <strong>Element:</strong> {results.user_profile.element}
              </div>
              <div className="profile-item">
                <strong>Yin/Yang:</strong> {results.user_profile.yin_yang}
              </div>
              <div className="profile-item">
                <strong>Rabjung:</strong> {results.user_profile.rabjung_identifier_m}
              </div>
            </div>
          </div>

          {/* Mewa Numbers */}
          <div className="result-section">
            <h3>🔢 Mewa Numbers</h3>
            <div className="mewa-grid">
              <div className="mewa-item">
                <div className="mewa-label">Life Mewa (命格)</div>
                {renderMewaCircle(results.user_mewas.life_mewa)}
                <div className="mewa-description">
                  {results.user_mewas.life_mewa.color}<br/>
                  {results.user_mewas.life_mewa.element}
                </div>
              </div>
              <div className="mewa-item">
                <div className="mewa-label">Body Mewa (体格)</div>
                {renderMewaCircle(results.user_mewas.body_mewa)}
                <div className="mewa-description">
                  {results.user_mewas.body_mewa.color}<br/>
                  {results.user_mewas.body_mewa.element}
                </div>
              </div>
              <div className="mewa-item">
                <div className="mewa-label">Power Mewa (权格)</div>
                {renderMewaCircle(results.user_mewas.power_mewa)}
                <div className="mewa-description">
                  {results.user_mewas.power_mewa.color}<br/>
                  {results.user_mewas.power_mewa.element}
                </div>
              </div>
            </div>
          </div>

          {/* Current Year Analysis */}
          <div className="result-section">
            <h3>📅 Current Year {results.obstacle_analysis.current_year_profile.gregorian_year}</h3>
            <div className="current-year-info">
              <div><strong>Current Year Sign:</strong> {results.obstacle_analysis.current_year_profile.sixty_cycle_name}</div>
              <div><strong>Current Year Body Mewa:</strong> {results.obstacle_analysis.current_year_mewas.body_mewa.number} {results.obstacle_analysis.current_year_mewas.body_mewa.color}</div>
            </div>
          </div>

          {/* Obstacles */}
          <div className="result-section">
            <h3>⚠️ Obstacle Analysis</h3>
            {results.obstacle_analysis.obstacles_found.length > 0 ? (
              <div className="obstacles-container">
                <div className="obstacles-summary">
                  {results.obstacle_analysis.total_obstacles} obstacle(s) detected
                </div>
                {results.obstacle_analysis.obstacles_found.map((obstacle, index) => (
                  <div key={index} className="obstacle-item">
                    <div className="obstacle-header">
                      <span className="obstacle-type">{obstacle.type}</span>
                      <span className="obstacle-name">{obstacle.name}</span>
                    </div>
                    <div className="obstacle-interpretation">
                      {obstacle.interpretation}
                    </div>
                    {obstacle.details && (
                      <div className="obstacle-details">
                        <small>Details: {JSON.stringify(obstacle.details, null, 2)}</small>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-obstacles">
                ✅ No obstacles detected. Current year conditions are favorable.
              </div>
            )}
          </div>

          <div className="action-buttons">
            <button className="secondary-btn" onClick={resetCalculator}>
              🔄 Calculate Another
            </button>
            <button 
              className="primary-btn" 
              onClick={() => {
                const dataStr = JSON.stringify(results, null, 2);
                const dataBlob = new Blob([dataStr], {type:'application/json'});
                const url = URL.createObjectURL(dataBlob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `tibetan_astro_${results.user_profile.gregorian_year}.json`;
                link.click();
              }}
            >
              💾 Download Results
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default TibetanAstroCalculator; 