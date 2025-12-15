/**
 * Main Application
 * Handles UI state, bulletin rendering, and user interactions
 */

class NewsApp {
    constructor() {
        this.loader = new BulletinLoader();
        this.navigator = new DateNavigator();
        this.currentRegion = 'usa';
        this.currentPeriod = 'morning';
        this.currentBulletin = null;
        
        this.elements = {};
        this.init();
    }
    
    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.cacheElements();
            this.attachListeners();
            this.loadCurrentBulletin();
        });
    }
    
    cacheElements() {
        this.elements = {
            container: document.getElementById('bulletin-container'),
            loading: document.getElementById('loading-state'),
            error: document.getElementById('error-state'),
            errorMessage: document.getElementById('error-message'),
            retryBtn: document.getElementById('retry-btn'),
            info: document.getElementById('bulletin-info'),
            date: document.getElementById('bulletin-date'),
            count: document.getElementById('bulletin-count'),
            generated: document.getElementById('bulletin-generated'),
            currentDate: document.getElementById('current-date'),
            prevDate: document.getElementById('prev-date'),
            nextDate: document.getElementById('next-date'),
            regionBtns: document.querySelectorAll('.region-btn'),
            periodBtns: document.querySelectorAll('.period-btn')
        };
    }
    
    attachListeners() {
        // Region filter
        this.elements.regionBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const region = btn.dataset.region;
                if (region !== this.currentRegion) {
                    this.setRegion(region);
                }
            });
        });
        
        // Period toggle
        this.elements.periodBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const period = btn.dataset.period;
                if (period !== this.currentPeriod) {
                    this.setPeriod(period);
                }
            });
        });
        
        // Date navigation
        this.elements.prevDate.addEventListener('click', () => {
            if (this.navigator.goBack()) {
                this.loadCurrentBulletin();
            }
        });
        
        this.elements.nextDate.addEventListener('click', () => {
            if (this.navigator.goForward()) {
                this.loadCurrentBulletin();
            }
        });
        
        // Retry button
        this.elements.retryBtn.addEventListener('click', () => {
            this.loadCurrentBulletin();
        });
    }
    
    setRegion(region) {
        this.currentRegion = region;
        this.updateActiveButtons();
        this.loadCurrentBulletin();
    }
    
    setPeriod(period) {
        this.currentPeriod = period;
        this.updateActiveButtons();
        this.loadCurrentBulletin();
    }
    
    updateActiveButtons() {
        // Update region buttons
        this.elements.regionBtns.forEach(btn => {
            const isActive = btn.dataset.region === this.currentRegion;
            btn.classList.toggle('active', isActive);
            btn.setAttribute('aria-pressed', isActive);
        });
        
        // Update period buttons
        this.elements.periodBtns.forEach(btn => {
            const isActive = btn.dataset.period === this.currentPeriod;
            btn.classList.toggle('active', isActive);
            btn.setAttribute('aria-pressed', isActive);
        });
        
        // Update date navigation buttons
        this.elements.prevDate.disabled = !this.navigator.canGoBack();
        this.elements.nextDate.disabled = !this.navigator.canGoForward();
        this.elements.currentDate.textContent = this.navigator.getCurrentDisplay();
    }
    
    async loadCurrentBulletin() {
        this.showLoading();
        
        try {
            const date = this.navigator.getCurrentDate();
            const bulletin = await this.loader.loadBulletin(
                this.currentRegion,
                date,
                this.currentPeriod
            );
            
            this.currentBulletin = bulletin.bulletin;
            this.renderBulletin();
            this.updateActiveButtons();
            
            // Preload adjacent bulletins
            this.loader.preloadAdjacent(this.currentRegion, date, this.currentPeriod);
            
        } catch (error) {
            this.showError(error.message);
        }
    }
    
    renderBulletin() {
        const bulletin = this.currentBulletin;
        
        // Update info
        this.elements.date.textContent = new Date(bulletin.date).toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        this.elements.count.textContent = `${bulletin.articles.length} articles`;
        this.elements.generated.textContent = `Updated ${this.formatTime(bulletin.generated_at)}`;
        
        // Clear container
        this.elements.container.innerHTML = '';
        
        // Render cards
        bulletin.articles.forEach((article, index) => {
            const card = this.createCard(article, index);
            this.elements.container.appendChild(card);
        });
        
        // Show content
        this.hideLoading();
        this.hideError();
        this.elements.info.classList.remove('hidden');
    }
    
    createCard(article, index) {
        const card = document.createElement('article');
        card.className = 'bulletin-card';
        card.setAttribute('aria-label', `Article ${index + 1}: ${article.title}`);
        
        const categoryClass = `category-${article.category.toLowerCase()}`;
        
        card.innerHTML = `
            <div class="category-badge ${categoryClass}">
                <span>${article.category}</span>
            </div>
            
            <h2 class="card-title">${this.escapeHtml(article.title)}</h2>
            
            <p class="card-summary">${this.escapeHtml(article.summary)}</p>
            
            <div class="card-source">
                <span class="material-symbols-outlined" style="font-size: 1rem;">language</span>
                <a 
                    href="${article.source.url}" 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    class="card-source-link"
                >
                    ${this.escapeHtml(article.source.name)}
                </a>
                ${article.source.published_at ? `<span>• ${this.formatTime(article.source.published_at)}</span>` : ''}
            </div>
            
            ${article.citations.length > 0 ? `
                <div class="citations">
                    ${article.citations.map((citation, idx) => `
                        <a 
                            href="${citation.url}" 
                            target="_blank" 
                            rel="noopener noreferrer" 
                            class="citation-link"
                            aria-label="Citation ${idx + 1}: ${this.escapeHtml(citation.title)}"
                        >
                            <span class="material-symbols-outlined">link</span>
                            <span>${idx + 1}. ${this.escapeHtml(citation.publisher || citation.title.substring(0, 20))}</span>
                        </a>
                    `).join('')}
                </div>
            ` : ''}
        `;
        
        return card;
    }
    
    showLoading() {
        this.elements.loading.classList.remove('hidden');
        this.elements.container.classList.add('hidden');
        this.elements.error.classList.add('hidden');
        this.elements.info.classList.add('hidden');
    }
    
    hideLoading() {
        this.elements.loading.classList.add('hidden');
        this.elements.container.classList.remove('hidden');
    }
    
    showError(message) {
        this.elements.errorMessage.textContent = message;
        this.elements.error.classList.remove('hidden');
        this.elements.loading.classList.add('hidden');
        this.elements.container.classList.add('hidden');
        this.elements.info.classList.add('hidden');
    }
    
    hideError() {
        this.elements.error.classList.add('hidden');
    }
    
    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 60) {
            return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
        }
        
        const diffHours = Math.floor(diffMins / 60);
        if (diffHours < 24) {
            return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
        }
        
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize app
const app = new NewsApp();
