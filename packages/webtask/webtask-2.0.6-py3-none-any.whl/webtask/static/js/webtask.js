/**
 * WebTask - DevOps Terminal Application
 * Main entry point for the WebTask application
 */

// Note: Modules are loaded via script tags in the HTML file

/**
 * WebTask Core Class
 * Initializes and coordinates all modules
 */
class WebTaskCore {
    constructor() {
        console.log('Initializing WebTask...');
        
        // Initialize modules
        this.processManager = new ProcessManager();
        this.systemMonitor = new SystemMonitor();
        this.fileSystemManager = new FileSystemManager();
        this.uiManager = new UIManager(this.processManager, this.systemMonitor, this.fileSystemManager);
        
        // Set up module references
        this.processManager.setSystemMonitor(this.systemMonitor);
        this.processManager.setUIManager(this.uiManager);
        this.systemMonitor.setProcessManager(this.processManager);
        
        // Initialize application
        this.init();
        
        console.log('WebTask initialized successfully');
    }
    
    /**
     * Initialize the application
     */
    init() {
        // Initialize file system
        this.fileSystemManager.initializeFileSystem();
        
        // Fetch initial system data
        this.systemMonitor.fetchInitialData();
        
        // Fetch initial processes
        this.processManager.updateProcesses();
        
        // Bind UI event handlers
        this.uiManager.bindEvents();
        
        console.log('WebTask initialized successfully');
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
    window.webtask = new WebTaskCore();
});
