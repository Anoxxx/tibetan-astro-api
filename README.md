# Tibetan Astrological Calculator

An interactive web application for the "Nine Palaces Outer Calculation" (九宫外算), a system of Tibetan Astrology. This project provides on-demand astrological analysis based on a user's birth year and other demographic data.

**Live Showcase:** [**https://tibetan-astro-api.vercel.app/**](https://tibetan-astro-api.vercel.app/)

---

## Features

- **Interactive UI:** A minimalist, North-European style interface for easy calculation.
- **Astrological Profile:** Calculates the 60-cycle sign (Animal, Element, Yin/Yang).
- **Mewa Numbers:** Determines the Life, Body, and Power Mewa numbers.
- **Obstacle Analysis:** Identifies four types of potential obstacles for the current year.
- **Serverless API:** Powered by a Python backend deployed on Vercel.

---

## API Usage

While the primary use is through the interactive web interface, the backend can be called directly.

### Main Calculation Endpoint
- **URL:** `https://tibetan-astro-api.vercel.app/api/astrology`
- **Method:** `POST`
- **Description:** Performs the full astrological analysis.

**Request Body (JSON):**

```json
{
  "birth_year": 1990,       // integer
  "gender": "male",         // "male" or "female"
  "profession": "general"   // "general", "official", "monastic", etc.
}
```
*Note: `current_year` and `age` are now calculated automatically on the backend.*

**Success Response (200 OK):**

The response is a JSON object containing the full analysis.

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

- **URL:** `https://tibetan-astro-api.vercel.app/api/astrology`
- **Method:** `GET`
- **Description:** Confirms the API is online and returns its status.