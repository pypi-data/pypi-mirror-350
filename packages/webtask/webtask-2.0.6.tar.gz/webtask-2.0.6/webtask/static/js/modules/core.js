/**
 * Core WebTask Module
 * Main entry point for the WebTask application
 * Coordinates all modules and initializes the application
 */
class WebTaskCore {
    /**
     * Initialize the WebTask application
     */
    constructor() {
        console.log('Initializing WebTask Core...');
        
        // Initialize modules
        this.processManager = new ProcessManager();
        this.systemMonitor = new SystemMonitor();
        this.fileSystemManager = new FileSystemManager();
        this.uiManager = new UIManager(this.processManager, this.systemMonitor, this.fileSystemManager);
        
        // Set up module references
        this.processManager.setSystemMonitor(this.systemMonitor);
        this.processManager.setUIManager(this.uiManager);
        
        // Initialize application
        this.init();
        
        console.log('WebTask Core initialized successfully');
    }
    
    /**
     * Initialize the application
     */
    init() {
        // Initialize file system first
        this.fileSystemManager.initializeFileSystem();
        
        // Fetch initial data from API
        this.systemMonitor.fetchInitialData();
        
        // Bind UI event handlers
        this.uiManager.bindEvents();
    }
    
    /**
     * Kill a process (proxy method for easy access from HTML)
     * @param {number} pid - Process ID
     * @param {string} signal - Signal to send (TERM, KILL, etc.)
     */
    killProcessWithSignal(pid, signal) {
        this.processManager.killProcess(pid, signal);
    }
}

// Initialize WebTask when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing WebTask...');
    window.webtask = new WebTaskCore();
});
