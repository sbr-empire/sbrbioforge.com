import axios from 'axios';
import offlineService from './offlineService';

// External API configurations
const NASA_API = 'https://api.nasa.gov';
const AIRNOW_API = 'https://api.airnowapi.org';
const OPENWEATHER_API = 'https://api.openweathermap.org';
const USGS_API = 'https://earthquake.usgs.gov';

const NASA_KEY = import.meta.env.REACT_APP_NASA_API_KEY;
const AIRNOW_KEY = import.meta.env.REACT_APP_AIRNOW_API_KEY;
const WEATHER_KEY = import.meta.env.REACT_APP_OPENWEATHER_API_KEY;

export const environmentalService = {
  // ========================================================================
  // AIR QUALITY - AirNow API
  // ========================================================================
  getAirQuality: async (latitude, longitude) => {
    const cacheKey = `air-quality-${latitude}-${longitude}`;
    
    try {
      // Try cache first
      const cached = await offlineService.getCacheData(cacheKey);
      if (cached) return cached;

      const response = await axios.get(`${AIRNOW_API}/observation/latLng`, {
        params: {
          latLng: `${latitude},${longitude}`,
          format: 'application/json',
          api_key: AIRNOW_KEY
        }
      });

      const data = response.data;

      // Cache for 6 hours
      await offlineService.saveCacheData(cacheKey, data, 21600000);

      return {
        success: true,
        data: {
          aqi: data[0]?.AQI || 0,
          category: data[0]?.Category?.Name || 'Unknown',
          pollutants: data,
          timestamp: new Date().toISOString()
        }
      };
    } catch (error) {
      console.error('Air quality error:', error);
      return { success: false, error: error.message };
    }
  },

  // ========================================================================
  // WEATHER FORECAST - OpenWeatherMap API
  // ========================================================================
  getWeatherForecast: async (latitude, longitude, days = 7) => {
    const cacheKey = `weather-forecast-${latitude}-${longitude}`;
    
    try {
      // Try cache first
      const cached = await offlineService.getCacheData(cacheKey);
      if (cached) return cached;

      const response = await axios.get(`${OPENWEATHER_API}/data/2.5/forecast`, {
        params: {
          lat: latitude,
          lon: longitude,
          appid: WEATHER_KEY,
          units: 'metric',
          cnt: days * 8 // 5-day forecast with 3-hour intervals
        }
      });

      const data = response.data;

      // Cache for 12 hours
      await offlineService.saveCacheData(cacheKey, data, 43200000);

      return {
        success: true,
        data: {
          location: data.city.name,
          forecast: data.list,
          timestamp: new Date().toISOString()
        }
      };
    } catch (error) {
      console.error('Weather forecast error:', error);
      return { success: false, error: error.message };
    }
  },

  // ========================================================================
  // CLIMATE DATA - NASA API
  // ========================================================================
  getClimateData: async (latitude, longitude) => {
    const cacheKey = `climate-data-${latitude}-${longitude}`;
    
    try {
      const cached = await offlineService.getCacheData(cacheKey);
      if (cached) return cached;

      const response = await axios.get(`${NASA_API}/planetary/earth/imagery`, {
        params: {
          lon: longitude,
          lat: latitude,
          dim: 0.15,
          api_key: NASA_KEY
        }
      });

      // Cache for 24 hours
      await offlineService.saveCacheData(cacheKey, response.data, 86400000);

      return {
        success: true,
        data: response.data,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Climate data error:', error);
      return { success: false, error: error.message };
    }
  },

  // ========================================================================
  // EARTHQUAKE DATA - USGS API
  // ========================================================================
  getEarthquakes: async (latitude, longitude, radiusKm = 100) => {
    const cacheKey = `earthquakes-${latitude}-${longitude}`;
    
    try {
      const cached = await offlineService.getCacheData(cacheKey);
      if (cached) return cached;

      const response = await axios.get(`${USGS_API}/fdsnws/event/1/query`, {
        params: {
          latitude,
          longitude,
          maxradius: radiusKm / 111, // Convert km to degrees
          limit: 20,
          format: 'geojson'
        }
      });

      // Cache for 1 hour
      await offlineService.saveCacheData(cacheKey, response.data, 3600000);

      return {
        success: true,
        data: response.data.features,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Earthquake data error:', error);
      return { success: false, error: error.message };
    }
  },

  // ========================================================================
  // HEALTH GUIDELINES BASED ON CONDITIONS
  // ========================================================================
  getHealthGuidelines: async (aqi, temperature, weatherCondition) => {
    const guidelines = {
      air: {},
      temperature: {},
      general: []
    };

    // Air Quality Guidelines
    if (aqi <= 50) {
      guidelines.air = {
        level: 'Good',
        color: 'green',
        recommendation: 'Air quality is satisfactory. Enjoy outdoor activities!'
      };
    } else if (aqi <= 100) {
      guidelines.air = {
        level: 'Moderate',
        color: 'yellow',
        recommendation: 'Unusually sensitive people should consider limiting outdoor exposure.'
      };
    } else if (aqi <= 150) {
      guidelines.air = {
        level: 'Unhealthy for Sensitive Groups',
        color: 'orange',
        recommendation: 'Sensitive groups should limit prolonged outdoor exposure.'
      };
    } else if (aqi <= 200) {
      guidelines.air = {
        level: 'Unhealthy',
        color: 'red',
        recommendation: 'Everyone may begin to experience health effects. Limit outdoor exposure.'
      };
    } else {
      guidelines.air = {
        level: 'Hazardous',
        color: 'purple',
        recommendation: 'Everyone should avoid outdoor exposure. Stay indoors.'
      };
    }

    // Temperature Guidelines
    if (temperature > 40) {
      guidelines.temperature = {
        level: 'Extreme Heat',
        recommendation: 'Drink plenty of water, stay in cool places, avoid outdoor work.'
      };
    } else if (temperature > 32) {
      guidelines.temperature = {
        level: 'Hot',
        recommendation: 'Stay hydrated, use sunscreen, limit outdoor activities.'
      };
    } else if (temperature < 0) {
      guidelines.temperature = {
        level: 'Freezing Cold',
        recommendation: 'Wear warm clothes, limit outdoor exposure, check on elderly.'
      };
    } else if (temperature < 10) {
      guidelines.temperature = {
        level: 'Cold',
        recommendation: 'Wear warm clothing, stay active to maintain body heat.'
      };
    } else {
      guidelines.temperature = {
        level: 'Comfortable',
        recommendation: 'Weather conditions are suitable for outdoor activities.'
      };
    }

    // General Guidelines
    guidelines.general = [
      'Drink water regularly throughout the day',
      'Use sunscreen if going outdoors',
      'Wear appropriate clothing for weather',
      'Check on elderly and vulnerable neighbors',
      'Keep emergency supplies at home',
      'Stay informed about local alerts'
    ];

    return guidelines;
  }
};

export default environmentalService;
