/**
 * Theme Manager
 * Handles dark/light mode toggle - always defaults to dark theme on page load
 */

class ThemeManager {
    constructor() {
        this.theme = this.getInitialTheme();
        this.toggleButton = null;
        this.init();
    }
    
    /**
     * Get initial theme - always dark on page load
     */
    getInitialTheme() {
        // Always default to dark theme on every page load
        return 'dark';
    }
    
    /**
     * Initialize theme manager
     */
    init() {
        // Apply initial theme
        this.applyTheme(this.theme);
        
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.attachListeners());
        } else {
            this.attachListeners();
        }
    }
    
    /**
     * Attach event listeners
     */
    attachListeners() {
        this.toggleButton = document.getElementById('theme-toggle');
        
        if (this.toggleButton) {
            this.toggleButton.addEventListener('click', () => this.toggle());
        }
    }
    
    /**
     * Apply theme to document
     */
    applyTheme(theme) {
        const html = document.documentElement;
        
        if (theme === 'dark') {
            html.classList.remove('light');
            html.classList.add('dark');
        } else {
            html.classList.remove('dark');
            html.classList.add('light');
        }
        
        // Update theme toggle icons
        const darkIcon = document.querySelector('.dark-icon');
        const lightIcon = document.querySelector('.light-icon');
        if (darkIcon && lightIcon) {
            if (theme === 'dark') {
                darkIcon.classList.remove('hidden');
                lightIcon.classList.add('hidden');
            } else {
                darkIcon.classList.add('hidden');
                lightIcon.classList.remove('hidden');
            }
        }
        
        // Update meta theme-color for mobile browsers
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.setAttribute('content', theme === 'dark' ? '#020617' : '#f6f7f8');
        } else {
            const meta = document.createElement('meta');
            meta.name = 'theme-color';
            meta.content = theme === 'dark' ? '#020617' : '#f6f7f8';
            document.head.appendChild(meta);
        }
    }
    
    /**
     * Toggle theme (temporary - resets to dark on page refresh)
     */
    toggle() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.theme);
        // Note: Theme preference is not persisted - always resets to dark on refresh
        
        // Dispatch custom event for other components
        window.dispatchEvent(new CustomEvent('themechange', { 
            detail: { theme: this.theme } 
        }));
    }
    
    /**
     * Get current theme
     */
    getTheme() {
        return this.theme;
    }
}

// Initialize theme manager immediately (before DOMContentLoaded)
const themeManager = new ThemeManager();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
