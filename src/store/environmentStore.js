import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import environmentalService from '../services/environmentalService';
import offlineService from '../services/offlineService';

export const useEnvironmentStore = create(
  persist(
    (set, get) => ({
      location: { latitude: null, longitude: null },
      airQuality: null,
      weather: null,
      climate: null,
      earthquakes: [],
      healthGuidelines: null,
      alerts: [],
      loading: false,
      error: null,
      lastUpdate: null,

      setLocation: (latitude, longitude) => {
        set({ location: { latitude, longitude } });
      },

      fetchAirQuality: async () => {
        const state = get();
        if (!state.location.latitude) return;

        set({ loading: true, error: null });
        try {
          const result = await environmentalService.getAirQuality(
            state.location.latitude,
            state.location.longitude
          );

          if (result.success) {
            set({ airQuality: result.data, lastUpdate: new Date().toISOString() });
          } else {
            set({ error: result.error });
          }
        } catch (error) {
          set({ error: error.message });
        } finally {
          set({ loading: false });
        }
      },

      fetchWeatherForecast: async (days = 7) => {
        const state = get();
        if (!state.location.latitude) return;

        set({ loading: true, error: null });
        try {
          const result = await environmentalService.getWeatherForecast(
            state.location.latitude,
            state.location.longitude,
            days
          );

          if (result.success) {
            set({ weather: result.data, lastUpdate: new Date().toISOString() });
          } else {
            set({ error: result.error });
          }
        } catch (error) {
          set({ error: error.message });
        } finally {
          set({ loading: false });
        }
      },

      fetchClimateData: async () => {
        const state = get();
        if (!state.location.latitude) return;

        set({ loading: true, error: null });
        try {
          const result = await environmentalService.getClimateData(
            state.location.latitude,
            state.location.longitude
          );

          if (result.success) {
            set({ climate: result.data, lastUpdate: new Date().toISOString() });
          } else {
            set({ error: result.error });
          }
        } catch (error) {
          set({ error: error.message });
        } finally {
          set({ loading: false });
        }
      },

      fetchEarthquakes: async (radiusKm = 100) => {
        const state = get();
        if (!state.location.latitude) return;

        set({ loading: true, error: null });
        try {
          const result = await environmentalService.getEarthquakes(
            state.location.latitude,
            state.location.longitude,
            radiusKm
          );

          if (result.success) {
            set({ earthquakes: result.data, lastUpdate: new Date().toISOString() });
          } else {
            set({ error: result.error });
          }
        } catch (error) {
          set({ error: error.message });
        } finally {
          set({ loading: false });
        }
      },

      generateHealthGuidelines: async () => {
        const state = get();
        const aqi = state.airQuality?.aqi || 0;
        const temp = state.weather?.forecast?.[0]?.main?.temp || 20;
        const condition = state.weather?.forecast?.[0]?.weather?.[0]?.main || 'Clear';

        const guidelines = await environmentalService.getHealthGuidelines(
          aqi,
          temp,
          condition
        );

        set({ healthGuidelines: guidelines });
        return guidelines;
      },

      fetchAllData: async () => {
        const state = get();
        set({ loading: true, error: null });

        try {
          await state.fetchAirQuality();
          await state.fetchWeatherForecast();
          await state.fetchClimateData();
          await state.fetchEarthquakes();
          await state.generateHealthGuidelines();

          // Clear expired cache
          await offlineService.clearExpiredData();
        } catch (error) {
          set({ error: error.message });
        } finally {
          set({ loading: false });
        }
      },

      addAlert: (alert) => {
        set((state) => ({
          alerts: [
            ...state.alerts,
            {
              id: Date.now(),
              ...alert,
              timestamp: new Date().toISOString()
            }
          ]
        }));
      },

      removeAlert: (alertId) => {
        set((state) => ({
          alerts: state.alerts.filter((a) => a.id !== alertId)
        }));
      }
    }),
    {
      name: 'environment-store',
      partialize: (state) => ({
        location: state.location,
        airQuality: state.airQuality,
        weather: state.weather,
        climate: state.climate,
        earthquakes: state.earthquakes,
        healthGuidelines: state.healthGuidelines,
        alerts: state.alerts,
        lastUpdate: state.lastUpdate
      })
    }
  )
);
