import PouchDB from 'pouchdb';

// Initialize offline database for 30-day cache
const offlineDB = new PouchDB('sbrbioforge-cache');

export const offlineService = {
  // Save environmental data
  saveCacheData: async (key, data, ttl = 2592000000) => { // 30 days default
    try {
      const doc = {
        _id: key,
        data,
        timestamp: new Date().getTime(),
        expiresAt: new Date().getTime() + ttl
      };
      await offlineDB.put(doc);
      return { success: true };
    } catch (error) {
      console.error('Cache save error:', error);
      return { success: false, error: error.message };
    }
  },

  // Retrieve cached data
  getCacheData: async (key) => {
    try {
      const doc = await offlineDB.get(key);
      
      // Check if data is expired
      if (doc.expiresAt && new Date().getTime() > doc.expiresAt) {
        await offlineDB.remove(doc);
        return null;
      }
      
      return doc.data;
    } catch (error) {
      if (error.name === 'not_found') return null;
      console.error('Cache retrieve error:', error);
      return null;
    }
  },

  // Clear old cache
  clearExpiredData: async () => {
    try {
      const allDocs = await offlineDB.allDocs({ include_docs: true });
      const now = new Date().getTime();
      
      const toDelete = allDocs.rows
        .map(row => row.doc)
        .filter(doc => doc.expiresAt && now > doc.expiresAt);

      for (const doc of toDelete) {
        await offlineDB.remove(doc);
      }
      
      return { success: true, removed: toDelete.length };
    } catch (error) {
      console.error('Clear cache error:', error);
      return { success: false, error: error.message };
    }
  },

  // Get all cached data
  getAllCacheData: async () => {
    try {
      const allDocs = await offlineDB.allDocs({ include_docs: true });
      return allDocs.rows.map(row => row.doc);
    } catch (error) {
      console.error('Get all cache error:', error);
      return [];
    }
  }
};

export default offlineService;
