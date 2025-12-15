/**
 * Date Navigator
 * Handles date navigation and formatting
 */

class DateNavigator {
    constructor() {
        this.currentDate = new Date();
        this.minDate = this.getMinDate(); // 7 days ago
        this.maxDate = new Date(); // Today
    }
    
    getMinDate() {
        const date = new Date();
        date.setDate(date.getDate() - 7);
        return date;
    }
    
    formatDate(date) {
        return date.toISOString().split('T')[0];
    }
    
    formatDisplay(date) {
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        
        if (date.toDateString() === today.toDateString()) {
            return 'Today';
        } else if (date.toDateString() === yesterday.toDateString()) {
            return 'Yesterday';
        } else {
            return date.toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric',
                year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined
            });
        }
    }
    
    canGoBack() {
        return this.currentDate > this.minDate;
    }
    
    canGoForward() {
        return this.currentDate < this.maxDate;
    }
    
    goBack() {
        if (this.canGoBack()) {
            this.currentDate.setDate(this.currentDate.getDate() - 1);
            return true;
        }
        return false;
    }
    
    goForward() {
        if (this.canGoForward()) {
            this.currentDate.setDate(this.currentDate.getDate() + 1);
            return true;
        }
        return false;
    }
    
    getCurrentDate() {
        return this.formatDate(this.currentDate);
    }
    
    getCurrentDisplay() {
        return this.formatDisplay(this.currentDate);
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = DateNavigator;
}
