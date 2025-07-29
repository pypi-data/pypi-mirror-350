/**
 * System Monitor Module
 * Handles system metrics, CPU visualization, and real-time monitoring
 */
class SystemMonitor {
    /**
     * Initialize the System Monitor
     */
    constructor() {
        // System metrics
        this.cpuCores = 4; // Will be updated from API
        this.cpuHistory = [];
        this.cpuCoreValues = [];
        
        // Update settings
        this.updateInterval = 3000; // Update every 3 seconds
        this.updateTimer = null;
        
        // Module references (will be set by Core)
        this.processManager = null;
        
        console.log('System Monitor initialized');
    }
    
    /**
     * Set reference to ProcessManager module
     * @param {ProcessManager} processManager - ProcessManager instance
     */
    setProcessManager(processManager) {
        this.processManager = processManager;
    }
    
    /**
     * Fetch initial system data from API to set up the application
     */
    fetchInitialData() {
        this._fetchSystemInfo()
            .then(data => {
                if (!data) {
                    this._initializeWithDefaultValues();
                    return;
                }
                
                // Initialize with real data from API
                this._initializeWithSystemData(data);
                
                // Start periodic updates
                this.startUpdating();
            })
            .catch(error => {
                console.error('Error in initial data fetch:', error);
                this._initializeWithDefaultValues();
            });
    }
    
    /**
     * Initialize system with default values (fallback)
     * @private
     */
    _initializeWithDefaultValues() {
        console.log('Initializing with default values');
        this.cpuCores = 4;
        this.cpuCoreValues = Array(this.cpuCores).fill(0);
        this.cpuHistory = Array(60).fill(0);
        this.initializeCpuVisualization();
        this.startUpdating();
    }
    
    /**
     * Initialize system with data from API
     * @private
     * @param {Object} data - System data from API
     */
    _initializeWithSystemData(data) {
        console.log('Initializing with system data:', data);
        // Update CPU cores count from API
        this.cpuCores = data.cpu.cores || 4;
        
        // Initialize CPU core values
        this.cpuCoreValues = Array(this.cpuCores).fill(0);
        
        // Initialize CPU history with zeros
        this.cpuHistory = Array(60).fill(0);
        
        // Initialize CPU visualization
        this.initializeCpuVisualization();
    }
    
    /**
     * Fetch system information from API
     * @private
     * @returns {Promise} Promise that resolves with system data
     */
    _fetchSystemInfo() {
        return fetch('/api/system')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`API error: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('System info fetched:', data);
                return data;
            })
            .catch(error => {
                console.error('Error fetching system info:', error);
                return null;
            });
    }
    
    /**
     * Start periodic updates of system data
     */
    startUpdating() {
        // Perform initial updates
        this._performDataUpdates();
        
        // Set interval for periodic updates
        this.updateTimer = setInterval(() => {
            this._performDataUpdates();
        }, this.updateInterval);
        
        console.log(`Started periodic updates every ${this.updateInterval}ms`);
    }
    
    /**
     * Perform all data updates (system info and processes)
     * @private
     */
    _performDataUpdates() {
        // Update timestamp
        this._updateTimestamp();
        
        // Fetch system information
        this._fetchSystemInfo()
            .then(data => {
                if (data) {
                    this._updateSystemDisplay(data);
                } else {
                    this._simulateSystemData();
                }
            })
            .catch(() => {
                this._simulateSystemData();
            });
        
        // Update processes
        if (this.processManager) {
            this.processManager.updateProcesses();
        }
    }
    
    /**
     * Update the last update timestamp
     * @private
     */
    _updateTimestamp() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        const lastUpdateElement = document.getElementById('last-update');
        if (lastUpdateElement) {
            lastUpdateElement.textContent = timeString;
        }
    }
    
    /**
     * Update system display with real data
     * @private
     * @param {Object} data - System data from API
     */
    _updateSystemDisplay(data) {
        // Update CPU usage
        const cpuUsage = data.cpu.percent || 0;
        
        // Update CPU cores visualization
        this.updateCpuCores(cpuUsage);
        
        // Update CPU history
        this.cpuHistory.push(cpuUsage);
        if (this.cpuHistory.length > 60) {
            this.cpuHistory.shift();
        }
        
        // Update CPU history chart
        this.updateCpuHistoryChart(cpuUsage);
    }
    
    /**
     * Simulate system data when API is unavailable
     * @private
     */
    _simulateSystemData() {
        // Simulate memory usage
        const memPercent = 30 + Math.random() * 40;
        const memFill = document.getElementById('mem-fill');
        const memText = document.getElementById('mem-percent');
        
        if (memFill) {
            memFill.style.width = `${memPercent}%`;
        }
        
        if (memText) {
            memText.textContent = `${memPercent.toFixed(1)}%`;
        }
        
        // Simulate load average
        const loadAvg = (1 + Math.random() * 2).toFixed(2);
        const loadAvgElement = document.getElementById('load-avg');
        if (loadAvgElement) {
            loadAvgElement.textContent = loadAvg;
        }
        
        // Simulate CPU usage
        const cpuUsage = 10 + Math.random() * 70;
        
        // Update CPU cores visualization
        this.updateCpuCores(cpuUsage);
        
        // Update CPU history
        this.updateCpuHistory(cpuUsage);
    }
    
    /**
     * Update CPU history with latest usage data
     * @param {number} cpuUsage - Current CPU usage percentage
     */
    updateCpuHistory(cpuUsage) {
        // Add new value to history
        this.cpuHistory.push(cpuUsage);
        
        // Keep only the last 60 values (1 minute at 1 second intervals)
        if (this.cpuHistory.length > 60) {
            this.cpuHistory.shift();
        }
        
        // Update the CPU history chart
        this.updateCpuHistoryChart(cpuUsage);
    }
    
    /**
     * Initialize CPU visualization
     */
    initializeCpuVisualization() {
        const container = document.getElementById('cpu-cores-container');
        if (!container) return;
        
        // Clear existing content
        container.innerHTML = '';
        
        // Create CPU core elements
        for (let i = 0; i < this.cpuCores; i++) {
            const coreElement = document.createElement('div');
            coreElement.className = 'cpu-core';
            coreElement.innerHTML = `
<!--                <div class="core-label">${i + 1}</div>-->
                <div class="core-bar">
                    <div class="core-fill" id="core-fill-${i}" style="width: 0%"></div>
                </div>
                <div class="core-value" id="core-value-${i}">0%</div>
            `;
            container.appendChild(coreElement);
        }
        
        // Initialize CPU history chart
        this.initializeCpuHistoryChart();
    }
    
    /**
     * Initialize CPU history chart
     */
    initializeCpuHistoryChart() {
        const canvas = document.getElementById('cpu-history-chart');
        if (!canvas) return;
        
        // Set canvas size
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;
        
        // Draw empty chart
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = '#00ffff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        // Draw baseline
        ctx.moveTo(0, canvas.height);
        ctx.lineTo(canvas.width, canvas.height);
        ctx.stroke();
    }
    
    /**
     * Update CPU cores with real or simulated activity
     * @param {number} overallCpuUsage - Overall CPU usage percentage
     */
    updateCpuCores(overallCpuUsage) {
        // Base load affects all cores
        const baseLoad = overallCpuUsage * 0.4;
        
        for (let i = 0; i < this.cpuCores; i++) {
            // Each core gets the base load plus individual variation
            let coreLoad = baseLoad;
            
            // Add some random variation to each core
            coreLoad += Math.random() * (overallCpuUsage * 0.6);
            
            // Ensure the core load is within bounds
            coreLoad = Math.max(0, Math.min(100, coreLoad));
            
            // Store the core value
            this.cpuCoreValues[i] = coreLoad;
            
            // Update the UI
            const fillElement = document.getElementById(`core-fill-${i}`);
            const valueElement = document.getElementById(`core-value-${i}`);
            
            if (fillElement && valueElement) {
                fillElement.style.width = `${coreLoad}%`;
                valueElement.textContent = `${coreLoad.toFixed(0)}%`;
                // valueElement.textContent = `${coreLoad.toFixed(1)}%`;

                // Update color based on load
                if (coreLoad < 50) {
                    fillElement.style.backgroundColor = '#00ffff';
                } else if (coreLoad < 80) {
                    fillElement.style.backgroundColor = '#ffff00';
                } else {
                    fillElement.style.backgroundColor = '#ff3333';
                }
            }
        }
        
        // Update the overall CPU usage display
        const cpuUsageElement = document.getElementById('cpu-percent');
        if (cpuUsageElement) {
            cpuUsageElement.textContent = `${overallCpuUsage.toFixed(1)}%`;
        }
    }
    
    /**
     * Update CPU history chart
     * @param {number} cpuUsage - Current CPU usage percentage
     */
    updateCpuHistoryChart(cpuUsage) {
        const canvas = document.getElementById('cpu-history-chart');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw the CPU history line
        ctx.strokeStyle = '#00ffff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        const step = canvas.width / (this.cpuHistory.length - 1);
        
        for (let i = 0; i < this.cpuHistory.length; i++) {
            const x = i * step;
            const y = canvas.height - (this.cpuHistory[i] / 100 * canvas.height);
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        
        ctx.stroke();
        
        // Fill area under the line
        ctx.lineTo(canvas.width, canvas.height);
        ctx.lineTo(0, canvas.height);
        ctx.closePath();
        ctx.fillStyle = 'rgba(0, 255, 255, 0.1)';
        ctx.fill();
    }
}
