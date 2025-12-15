/**
 * Bulletin Loader
 * Handles fetching and parsing news bulletins from JSON files
 */

class BulletinLoader {
    constructor() {
        // Use relative path to work with GitHub Pages subdirectory
        this.baseURL = './data';
        this.cache = new Map();
    }
    
    /**
     * Load bulletin for a specific region, date, and period
     * @param {string} region - Region code (usa, india, world)
     * @param {string} date - Date in YYYY-MM-DD format
     * @param {string} period - Period (morning, evening)
     * @returns {Promise<Object>} Bulletin data
     */
    async loadBulletin(region, date, period) {
        const cacheKey = `${region}-${date}-${period}`;
        
        // Check cache first
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }
        
        const url = `${this.baseURL}/${region}/${date}-${period}.json`;
        
        try {
            const response = await fetch(url);
            
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error(`No bulletin available for ${region} on ${date} (${period})`);
                }
                throw new Error(`Failed to load bulletin: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Validate bulletin structure
            this.validateBulletin(data);
            
            // Cache the result
            this.cache.set(cacheKey, data);
            
            return data;
        } catch (error) {
            console.error('Error loading bulletin:', error);
            throw error;
        }
    }
    
    /**
     * Validate bulletin data structure
     * @param {Object} data - Bulletin data to validate
     * @throws {Error} If bulletin is invalid
     */
    validateBulletin(data) {
        // Check for bulletin wrapper
        if (!data.bulletin) {
            throw new Error('Invalid bulletin format: missing bulletin wrapper');
        }
        
        const bulletin = data.bulletin;
        
        // Required fields (only essential ones - id and version are optional for backwards compatibility)
        const requiredFields = ['region', 'date', 'period', 'generated_at', 'articles'];
        for (const field of requiredFields) {
            if (!(field in bulletin)) {
                throw new Error(`Invalid bulletin format: missing field "${field}"`);
            }
        }
        
        // Validate articles array
        if (!Array.isArray(bulletin.articles)) {
            throw new Error('Invalid bulletin format: articles must be an array');
        }
        
        if (bulletin.articles.length === 0) {
            throw new Error('Invalid bulletin format: no articles found');
        }
        
        // Validate each article (with lenient field checking)
        bulletin.articles.forEach((article, index) => {
            const requiredArticleFields = ['title', 'summary', 'category'];
            for (const field of requiredArticleFields) {
                if (!(field in article)) {
                    throw new Error(`Invalid article format at index ${index}: missing field "${field}"`);
                }
            }
        });
    }
    
    /**
     * Get available dates for a region
     * @param {string} region - Region code
     * @returns {Promise<Array<string>>} Array of available dates
     */
    async getAvailableDates(region) {
        try {
            const response = await fetch(`${this.baseURL}/index.json`);
            
            if (!response.ok) {
                throw new Error('Failed to load bulletin index');
            }
            
            const index = await response.json();
            
            // Extract dates for the given region
            const dates = new Set();
            
            if (index[region]) {
                Object.keys(index[region]).forEach(date => {
                    dates.add(date);
                });
            }
            
            // Sort dates in descending order (newest first)
            return Array.from(dates).sort().reverse();
        } catch (error) {
            console.error('Error loading bulletin index:', error);
            return [];
        }
    }
    
    /**
     * Check if a bulletin exists for a specific date/period
     * @param {string} region - Region code
     * @param {string} date - Date in YYYY-MM-DD format
     * @param {string} period - Period (morning, evening)
     * @returns {Promise<boolean>} True if bulletin exists
     */
    async bulletinExists(region, date, period) {
        const url = `${this.baseURL}/${region}/${date}-${period}.json`;
        
        try {
            const response = await fetch(url, { method: 'HEAD' });
            return response.ok;
        } catch {
            return false;
        }
    }
    
    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    }
    
    /**
     * Preload bulletins for faster navigation
     * @param {string} region - Region code
     * @param {string} date - Current date
     * @param {string} period - Current period
     */
    async preloadAdjacent(region, date, period) {
        // Preload yesterday and tomorrow's bulletins
        const currentDate = new Date(date);
        
        const yesterday = new Date(currentDate);
        yesterday.setDate(yesterday.getDate() - 1);
        const yesterdayStr = yesterday.toISOString().split('T')[0];
        
        const tomorrow = new Date(currentDate);
        tomorrow.setDate(tomorrow.getDate() + 1);
        const tomorrowStr = tomorrow.toISOString().split('T')[0];
        
        // Preload in background (don't await)
        [yesterdayStr, tomorrowStr].forEach(d => {
            this.loadBulletin(region, d, period).catch(() => {
                // Silently fail - bulletin might not exist yet
            });
        });
    }
}

// Export for use in app.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BulletinLoader;
}
