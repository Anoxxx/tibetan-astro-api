# Tibetan Astrological Calculator API

🏔️ **Nine Palaces Outer Calculation (九宫外算) System**

This API provides Tibetan astrological calculations including:
- 60-cycle astrological profiles
- Mewa number calculations  
- Obstacle analysis
- Traditional interpretations

## API Endpoints

- `POST /api/astrology` - Main calculation endpoint
- `GET /health` - Health check

## Usage

Send POST request to `/api/astrology` with:
```json
{
  "birth_year": 1990,
  "current_year": 2025,
  "age": 35,
  "gender": "male",
  "profession": "general"
}
```

Deployed on Vercel for [zhengfei.info](https://zhengfei.info)