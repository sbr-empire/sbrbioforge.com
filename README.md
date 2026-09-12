# 🌍 SBR BIOFORGE - Climate Resilience & Survival Intelligence Platform

**Real-time environmental monitoring, health guidance, and community resilience for the next 300 years.**

---

## 🌟 Features

### 🌫️ Air Quality Monitoring
- Real-time AQI tracking (AirNow API)
- Pollutant breakdown (PM2.5, O3, NO2, SO2)
- Health recommendations
- Trend analysis
- Alert system

### 🌤️ Weather Forecasting
- 30-day weather forecast
- Severe weather alerts
- Temperature & precipitation tracking
- Wind speed & direction
- UV index monitoring

### 🏥 Health Guidelines
- Personalized health recommendations
- Disease prevention tips
- Nutrition guidance
- Vaccination schedules
- Emergency preparedness

### 📍 Location Intelligence
- GPS-based data tracking
- Interactive maps (Leaflet)
- Earthquake monitoring (USGS)
- Climate data (NASA)
- Disaster zones identification

### 📱 Offline Capabilities
- 30-day data cache (PouchDB)
- Works without internet
- Auto-sync when online
- Battery-efficient mode
- Progressive Web App (PWA)

### 🔔 Real-time Alerts
- Push notifications
- SMS alerts
- Email notifications
- Community alerts
- Emergency broadcasting

---

## 🚀 Tech Stack

- **Frontend**: React 18 + Vite
- **Styling**: TailwindCSS
- **State**: Zustand
- **Offline DB**: PouchDB (30-day cache)
- **Maps**: Leaflet + React-Leaflet
- **Charts**: Chart.js
- **Auth**: Firebase
- **Database**: Firestore
- **External APIs**:
  - NASA Earth Imagery
  - AirNow Air Quality
  - OpenWeatherMap Weather
  - USGS Earthquake Data
  - Google Maps
- **i18n**: i18next (100+ languages)
- **Deployment**: Firebase Hosting + Cloud Run

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/sbr-empire/sbrbioforge.com.git
cd sbrbioforge.com
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Setup
```bash
cp .env.example .env.local
# Edit .env.local with your API keys
```

### 4. Start Development
```bash
npm run dev
```

App runs on: `http://localhost:5173`

---

## 🔑 Environment Variables

```
REACT_APP_SBCORE_API=https://sbr-core-api.run.app
REACT_APP_NASA_API_KEY=your_nasa_key
REACT_APP_AIRNOW_API_KEY=your_airnow_key
REACT_APP_OPENWEATHER_API_KEY=your_weather_key
REACT_APP_FIREBASE_PROJECT_ID=your_project
```

---

## 📚 API Integration

### Air Quality (AirNow)
```javascript
const airQuality = await environmentalService.getAirQuality(lat, lng);
```

### Weather Forecast
```javascript
const weather = await environmentalService.getWeatherForecast(lat, lng, days);
```

### Earthquakes (USGS)
```javascript
const quakes = await environmentalService.getEarthquakes(lat, lng, radius);
```

### Climate Data (NASA)
```javascript
const climate = await environmentalService.getClimateData(lat, lng);
```

---

## 🏗️ Project Structure

```
src/
├── components/        # Reusable React components
├── pages/            # Page components
├── services/         # External APIs & services
├── store/            # Zustand state management
├── config/           # Firebase & API config
├── styles/           # TailwindCSS styles
└── App.jsx          # Main app component
```

---

## 💾 Offline Database (30-Day Cache)

Data automatically cached for 30 days using PouchDB:
- Air quality (6-hour refresh)
- Weather forecast (12-hour refresh)
- Climate data (24-hour refresh)
- Earthquake data (1-hour refresh)

Works completely offline with cached data!

---

## 🌍 Supported Languages (100+ Global)

✅ **Major Languages**: English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Hindi, Bengali, Turkish, Vietnamese, Thai, Indonesian, Polish, Dutch, Swedish, Norwegian, Danish, Finnish, Greek, Czech, Hungarian, Romanian, Hebrew, Urdu

✅ **Regional Languages**: Punjabi, Marathi, Gujarati, Tamil, Telugu, Kannada, Malayalam, Odia, Assamese, Maithili, Sindhi, Kashmiri, Dogri, Manipuri, Nepali, Sinhala, Burmese, Khmer, Lao, Cambodian, Filipino, Vietnamese, Mongolian, Kazakh, Uzbek, Turkmen, Tajik, Kyrgyz, Uyghur, Persian, Kurdish, Pashto, Balochi, Sindhi, Amharic, Tigrinya, Somali, Swahili, Hausa, Igbo, Yoruba, Zulu, Afrikaans, Shona

✅ **Plus 50+ more regional and minority languages**

---

## 🎯 Key Features

### Real-time Monitoring
- Live air quality index
- Current weather conditions
- Active earthquake alerts
- Health warnings

### Predictive Analytics
- 30-day weather forecast
- Air quality trends
- Climate patterns
- Health recommendations

### Community Features
- Share experiences
- Local mutual aid
- Emergency contacts
- Resource sharing

### Accessibility
- WCAG 2.1 AAA compliant
- Screen reader support
- Keyboard navigation
- High contrast mode
- 100+ language support

---

## 🔒 Security & Privacy

- ✅ End-to-end encryption
- ✅ Firebase security rules
- ✅ GDPR compliant
- ✅ CCPA compliant
- ✅ No tracking cookies
- ✅ Secure data transmission
- ✅ Regular security audits

---

## 📱 Progressive Web App (PWA)

- Works offline
- Installable on home screen
- Push notifications
- Fast loading (< 2s)
- Works on all devices

---

## 🚀 Deployment

### Firebase Hosting
```bash
npm run build
firebase deploy
```

---

## 📊 Performance Targets

- Page Load: < 2 seconds
- API Response: < 100ms
- Offline Mode: Instant (cached data)
- 30-day data cache: Full functionality
- 99.99% uptime SLA

---

## 🤝 Contributing

Contributions welcome! Please follow the contributing guidelines.

---

## 📄 License

Copyright 2024 SBR Empire. All rights reserved.

---

**Built for humanity's resilience for the next 300 years.**
