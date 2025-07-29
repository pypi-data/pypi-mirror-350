/**
 * Process Manager Module
 * Handles all process-related functionality including fetching, sorting, filtering,
 * and managing processes.
 */
class ProcessManager {
    /**
     * Initialize the Process Manager
     */
    constructor() {
        // Process data
        this.processes = [];
        this.filteredProcesses = [];
        this.selectedPid = null;
        this.processCounter = 1000;
        
        // UI state
        this.filterText = '';
        this.sortConfig = {
            column: 'cpu',
            direction: 'desc'
        };
        
        // Module references (will be set by Core)
        this.systemMonitor = null;
        this.uiManager = null;
        
        console.log('Process Manager initialized');
    }
    
    /**
     * Set reference to SystemMonitor module
     * @param {SystemMonitor} systemMonitor - SystemMonitor instance
     */
    setSystemMonitor(systemMonitor) {
        this.systemMonitor = systemMonitor;
    }
    
    /**
     * Set reference to UIManager module
     * @param {UIManager} uiManager - UIManager instance
     */
    setUIManager(uiManager) {
        this.uiManager = uiManager;
    }
    
    /**
     * Update processes with real data from API
     */
    updateProcesses() {
        this._fetchProcesses()
            .then(data => {
                if (!data || data.length === 0) {
                    this._simulateProcesses();
                    return;
                }
                
                // Transform and update process data
                this._updateProcessData(data);
            })
            .catch(error => {
                console.error('Error in process update:', error);
                this._simulateProcesses();
            });
    }
    
    /**
     * Fetch processes from API
     * @private
     * @returns {Promise} Promise that resolves with process data
     */
    _fetchProcesses() {
        return fetch('/api/processes')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`API error: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Processes fetched:', data.length);
                return data;
            })
            .catch(error => {
                console.error('Error fetching processes:', error);
                return null;
            });
    }
    
    /**
     * Update process data with API results
     * @private
     * @param {Array} data - Process data from API
     */
    _updateProcessData(data) {
        // Transform API data to match our expected format
        this.processes = data.map(proc => this._transformProcessData(proc));

        // Process the data
        this._processAndRenderData();
    }
    
    /**
     * Transform raw process data to application format
     * @private
     * @param {Object} proc - Raw process data
     * @returns {Object} Transformed process object
     */
    _transformProcessData(proc) {
        return {
            pid: proc.pid,
            user: proc.user || 'system',
            cpu: proc.cpu || 0,
            memory: proc.memory || 0,
            time: this.generateTime(),
            port: null, // API doesn't provide port info
            command: proc.name || 'unknown',
            file: null,
            service: proc.name ? proc.name.split(' ')[0] : 'unknown',
            parent: null,
            children: [],
            transparency: this.calculateTransparency(proc.name ? proc.name.split(' ')[0] : 'unknown'),
            startTime: Date.now() - (Math.random() * 3600000) // Random start time within the last hour
        };
    }
    
    /**
     * Process and render the current data
     * @private
     */
    _processAndRenderData() {
        // Build process hierarchy
        this.buildProcessHierarchy();
        
        // Sort processes according to current sort configuration
        this.sortProcesses();
        
        // Apply current filter
        this.applyFilter();
        
        // Render the process list
        if (this.uiManager) {
            this.uiManager.renderProcesses(this.filteredProcesses);
        }
        
        // Update process count
        this._updateProcessCount();
    }
    
    /**
     * Update the process count display
     * @private
     */
    _updateProcessCount() {
        const processCountElement = document.getElementById('process-count');
        const filteredCountElement = document.getElementById('filtered-count');
        
        if (processCountElement) {
            processCountElement.textContent = this.processes.length;
        }
        
        if (filteredCountElement) {
            filteredCountElement.textContent = this.filteredProcesses.length;
        }
    }
    
    /**
     * Simulate processes (fallback if API fails)
     * @private
     */
    _simulateProcesses() {
        console.log('Using simulated process data');
        
        // Create initial processes if none exist
        if (this.processes.length === 0) {
            this._createInitialSimulatedProcesses();
        } else {
            this._updateSimulatedProcesses();
        }

        // Process and render the data
        this._processAndRenderData();
    }
    
    /**
     * Create initial simulated processes
     * @private
     */
    _createInitialSimulatedProcesses() {
        const baseProcesses = [
            { command: 'systemd', user: 'root', cpu: 0.5, memory: 1.2 },
            { command: 'nginx', user: 'www-data', cpu: 1.5, memory: 3.2 },
            { command: 'node app.js', user: 'nodejs', cpu: 5.2, memory: 8.7 },
            { command: 'python3 server.py', user: 'python', cpu: 3.7, memory: 6.5 },
            { command: 'java -jar app.jar', user: 'java', cpu: 4.1, memory: 12.3 },
            { command: 'mysql', user: 'mysql', cpu: 2.8, memory: 15.6 }
        ];
        
        this.processes = baseProcesses.map((proc, index) => ({
            pid: this.processCounter++,
            user: proc.user,
            cpu: proc.cpu,
            memory: proc.memory,
            time: this.generateTime(),
            port: index % 2 === 0 ? 8000 + index * 100 : null,
            command: proc.command,
            file: proc.command.includes('node') ? '/var/www/html/app.js' : null,
            service: proc.command.split(' ')[0],
            parent: null,
            children: [],
            transparency: this.calculateTransparency(proc.command.split(' ')[0]),
            startTime: Date.now() - (Math.random() * 3600000)
        }));
    }
    
    /**
     * Update existing simulated processes
     * @private
     */
    _updateSimulatedProcesses() {
        // Update existing processes
        this.processes.forEach(process => {
            // Random CPU fluctuation
            process.cpu += (Math.random() - 0.5) * 2;
            process.cpu = Math.max(0, Math.min(100, process.cpu));

            // Random memory fluctuation
            process.memory += (Math.random() - 0.5) * 1;
            process.memory = Math.max(0, Math.min(100, process.memory));
        });

        // Occasionally add new processes (10% chance if under 50 processes)
        if (Math.random() < 0.1 && this.processes.length < 50) {
            this._addRandomProcess();
        }
    }
    
    /**
     * Add a random process to the simulation
     * @private
     */
    _addRandomProcess() {
        const commands = ['node app.js', 'python3 server.py', 'java -jar app.jar', 'go run main.go'];
        const users = ['user', 'www-data', 'nodejs', 'python', 'java', 'root'];
        
        const command = commands[Math.floor(Math.random() * commands.length)];
        const user = users[Math.floor(Math.random() * users.length)];
        const port = Math.random() < 0.3 ? Math.floor(Math.random() * 9000) + 1000 : null;

        this.processes.push({
            pid: this.processCounter++,
            user: user,
            cpu: Math.random() * 5,
            memory: Math.random() * 10,
            time: this.generateTime(),
            port: port,
            command: command,
            file: command.includes('node') ? '/var/www/html/app.js' : null,
            service: command.split(' ')[0],
            parent: null,
            children: [],
            transparency: this.calculateTransparency(command.split(' ')[0]),
            startTime: Date.now()
        });
    }
    
    /**
     * Sort processes according to current sort configuration
     */
    sortProcesses() {
        const { column, direction } = this.sortConfig;
        const multiplier = direction === 'asc' ? 1 : -1;
        
        this.processes.sort((a, b) => {
            return this._compareProcesses(a, b, column, multiplier);
        });
    }
    
    /**
     * Compare two processes for sorting
     * @private
     * @param {Object} a - First process
     * @param {Object} b - Second process
     * @param {string} column - Column to sort by
     * @param {number} multiplier - Sort direction multiplier (1 for asc, -1 for desc)
     * @returns {number} Comparison result
     */
    _compareProcesses(a, b, column, multiplier) {
        switch (column) {
            case 'pid':
                return (a.pid - b.pid) * multiplier;
            case 'user':
                return a.user.localeCompare(b.user) * multiplier;
            case 'cpu':
                return (a.cpu - b.cpu) * multiplier;
            case 'mem':
                return (a.memory - b.memory) * multiplier;
            case 'time':
                // Convert time strings to seconds for comparison
                const aTime = this.timeToSeconds(a.time);
                const bTime = this.timeToSeconds(b.time);
                return (aTime - bTime) * multiplier;
            case 'port':
                // Handle null ports
                if (!a.port && !b.port) return 0;
                if (!a.port) return 1 * multiplier;
                if (!b.port) return -1 * multiplier;
                return (a.port - b.port) * multiplier;
            case 'command':
                return a.command.localeCompare(b.command) * multiplier;
            default:
                return (a.cpu - b.cpu) * multiplier; // Default to CPU sorting
        }
    }
    
    /**
     * Apply filter to processes based on filterText
     */
    applyFilter() {
        if (!this.filterText) {
            this.filteredProcesses = [...this.processes];
            return;
        }
        
        const filter = this.filterText.toLowerCase();
        this.filteredProcesses = this.processes.filter(process => this._processMatchesFilter(process, filter));
    }
    
    /**
     * Check if a process matches the filter
     * @private
     * @param {Object} process - Process to check
     * @param {string} filter - Filter text (lowercase)
     * @returns {boolean} True if process matches filter
     */
    _processMatchesFilter(process, filter) {
        return (
            process.pid.toString().includes(filter) ||
            process.user.toLowerCase().includes(filter) ||
            process.command.toLowerCase().includes(filter) ||
            (process.port && process.port.toString().includes(filter))
        );
    }
    
    /**
     * Set filter text
     * @param {string} text - Filter text
     */
    setFilterText(text) {
        this.filterText = text;
        this.applyFilter();
        if (this.uiManager) {
            this.uiManager.renderProcesses(this.filteredProcesses);
        }
    }
    
    /**
     * Set sort configuration
     * @param {string} column - Column to sort by
     * @param {string} direction - Sort direction ('asc' or 'desc')
     */
    setSortConfig(column, direction) {
        this.sortConfig = { column, direction };
        this.sortProcesses();
        this.applyFilter();
        if (this.uiManager) {
            this.uiManager.renderProcesses(this.filteredProcesses);
        }
    }

    /**
     * Fetch processes from the API
     * @returns {Promise} Promise that resolves with process data
     */
    fetchProcesses() {
        return fetch('/api/processes')
            .then(response => response.json())
            .then(data => {
                // Transform API data to match our expected format
                this.processes = data.map(proc => this.transformProcessData(proc));
                
                // Build process hierarchy
                this.buildProcessHierarchy();
                
                // Sort processes according to current sort configuration
                this.sortProcesses();
                
                // Apply current filter
                this.applyFilter();
                
                return this.processes;
            })
            .catch(error => {
                console.error('Error fetching processes:', error);
                // Fallback to simulated data if API fails
                this.simulateProcesses();
                return this.processes;
            });
    }
    
    /**
     * Transform raw API process data into application format
     * @param {Object} proc - Raw process data from API
     * @returns {Object} Transformed process object
     */
    transformProcessData(proc) {
        return {
            pid: proc.pid,
            user: proc.user || 'system',
            cpu: proc.cpu || 0,
            memory: proc.memory || 0,
            time: this.generateTime(),
            port: null, // API doesn't provide port info
            command: proc.name || 'unknown',
            file: null,
            service: proc.name ? proc.name.split(' ')[0] : 'unknown',
            parent: null,
            children: [],
            transparency: this.calculateTransparency(proc.name ? proc.name.split(' ')[0] : 'unknown'),
            startTime: Date.now() - (Math.random() * 3600000) // Random start time within the last hour
        };
    }
    
    /**
     * Simulate processes (fallback if API fails)
     */
    simulateProcesses() {
        if (this.processes.length === 0) {
            // Create initial simulated processes if none exist
            this.createInitialSimulatedProcesses();
        } else {
            // Update existing processes
            this.processes.forEach(process => {
                process.cpu += (Math.random() - 0.5) * 2;
                process.cpu = Math.max(0, Math.min(100, process.cpu));
    
                process.memory += (Math.random() - 0.5) * 1;
                process.memory = Math.max(0, Math.min(100, process.memory));
            });
    
            // Occasionally add new processes
            if (Math.random() < 0.1 && this.processes.length < 50) {
                this.addRandomProcess();
            }
        }
    
        // Sort and apply filter
        this.sortProcesses();
        this.applyFilter();
        
        return this.processes;
    }
    
    /**
     * Create initial simulated processes
     */
    createInitialSimulatedProcesses() {
        const baseProcesses = [
            { command: 'systemd', user: 'root', cpu: 0.5, memory: 1.2 },
            { command: 'nginx', user: 'www-data', cpu: 1.5, memory: 3.2 },
            { command: 'node app.js', user: 'nodejs', cpu: 5.2, memory: 8.7 },
            { command: 'python3 server.py', user: 'python', cpu: 3.7, memory: 6.5 }
        ];
        
        baseProcesses.forEach((proc, index) => {
            this.processes.push({
                pid: this.processCounter++,
                user: proc.user,
                cpu: proc.cpu,
                memory: proc.memory,
                time: this.generateTime(),
                port: index % 2 === 0 ? 8000 + index * 100 : null,
                command: proc.command,
                file: proc.command.includes('node') ? '/var/www/html/app.js' : null,
                service: proc.command.split(' ')[0],
                parent: null,
                children: [],
                transparency: 0.9,
                startTime: Date.now() - (Math.random() * 3600000)
            });
        });
    }
    
    /**
     * Add a random process to the simulation
     */
    addRandomProcess() {
        const commands = ['node app.js', 'python3 server.py', 'java -jar app.jar', 'go run main.go'];
        const command = commands[Math.floor(Math.random() * commands.length)];
        const port = Math.random() < 0.3 ? Math.floor(Math.random() * 9000) + 1000 : null;

        this.processes.push({
            pid: this.processCounter++,
            user: 'user',
            cpu: Math.random() * 5,
            memory: Math.random() * 10,
            time: this.generateTime(),
            port: port,
            command: command,
            file: command.includes('node') ? '/var/www/html/app.js' : null,
            service: command.split(' ')[0],
            parent: null,
            children: [],
            transparency: 0.9,
            startTime: Date.now()
        });
    }
    
    /**
     * Build process hierarchy by establishing parent-child relationships
     */
    buildProcessHierarchy() {
        // Create parent-child relationships
        this.processes.forEach(process => {
            if (process.parent) {
                const parent = this.processes.find(p => 
                    p.service === process.parent || p.pid === process.parent
                );
                if (parent) {
                    parent.children.push(process.pid);
                    process.parentPid = parent.pid;
                }
            }
        });
    }
    
    /**
     * Sort processes according to current sort configuration
     */
    sortProcesses() {
        const { column, direction } = this.sortConfig;
        const multiplier = direction === 'asc' ? 1 : -1;
        
        this.processes.sort((a, b) => {
            switch (column) {
                case 'pid':
                    return (a.pid - b.pid) * multiplier;
                case 'user':
                    return a.user.localeCompare(b.user) * multiplier;
                case 'cpu':
                    return (a.cpu - b.cpu) * multiplier;
                case 'mem':
                    return (a.memory - b.memory) * multiplier;
                case 'time':
                    // Convert time strings to seconds for comparison
                    const aTime = this.timeToSeconds(a.time);
                    const bTime = this.timeToSeconds(b.time);
                    return (aTime - bTime) * multiplier;
                case 'port':
                    // Handle null ports
                    if (!a.port && !b.port) return 0;
                    if (!a.port) return 1 * multiplier;
                    if (!b.port) return -1 * multiplier;
                    return (a.port - b.port) * multiplier;
                case 'command':
                    return a.command.localeCompare(b.command) * multiplier;
                default:
                    return (a.cpu - b.cpu) * multiplier; // Default to CPU sorting
            }
        });
    }
    
    /**
     * Apply filter to processes based on filterText
     */
    applyFilter() {
        if (!this.filterText) {
            this.filteredProcesses = [...this.processes];
            return;
        }
        
        const filter = this.filterText.toLowerCase();
        this.filteredProcesses = this.processes.filter(process => {
            return (
                process.pid.toString().includes(filter) ||
                process.user.toLowerCase().includes(filter) ||
                process.command.toLowerCase().includes(filter) ||
                (process.port && process.port.toString().includes(filter))
            );
        });
    }
    
    /**
     * Set sort configuration
     * @param {string} column - Column to sort by
     * @param {string} direction - Sort direction ('asc' or 'desc')
     */
    setSortConfig(column, direction) {
        this.sortConfig = { column, direction };
        this.sortProcesses();
        this.applyFilter();
    }
    
    /**
     * Set filter text
     * @param {string} text - Filter text
     */
    setFilterText(text) {
        this.filterText = text;
        this.applyFilter();
    }
    
    /**
     * Get process by PID
     * @param {number} pid - Process ID
     * @returns {Object} Process object
     */
    getProcessByPid(pid) {
        return this.processes.find(p => p.pid === pid);
    }
    
    /**
     * Get process depth in hierarchy
     * @param {Object} process - Process object
     * @returns {number} Depth in hierarchy
     */
    getProcessDepth(process) {
        let depth = 0;
        let current = process;
        
        while (current.parentPid) {
            depth++;
            current = this.getProcessByPid(current.parentPid);
            if (!current || depth > 10) break; // Prevent infinite loops
        }
        
        return depth;
    }
    
    /**
     * Generate random time string (HH:MM:SS)
     * @returns {string} Time string
     */
    generateTime() {
        const hours = Math.floor(Math.random() * 24);
        const minutes = Math.floor(Math.random() * 60);
        const seconds = Math.floor(Math.random() * 60);
        
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    /**
     * Convert time string (HH:MM:SS) to seconds for sorting
     * @param {string} timeString - Time string
     * @returns {number} Total seconds
     */
    timeToSeconds(timeString) {
        if (!timeString) return 0;
        const [hours, minutes, seconds] = timeString.split(':').map(Number);
        return hours * 3600 + minutes * 60 + seconds;
    }
    
    /**
     * Calculate transparency for a service
     * @param {string} service - Service name
     * @returns {number} Transparency value (0-1)
     */
    calculateTransparency(service) {
        // Different services have different transparency levels
        const transparencyMap = {
            'systemd': 0.3,      // Core system - very transparent
            'kernel': 0.2,       // Kernel processes - most transparent
            'nginx': 0.8,        // Web server - less transparent
            'node': 0.9,         // Application - visible
            'mysql': 0.7,        // Database - moderate transparency
            'redis': 0.7,        // Cache - moderate transparency
            'sshd': 0.6,         // SSH daemon - moderate transparency
            'docker': 0.5,       // Container runtime - more transparent
            'bash': 1.0,         // Shell - fully visible
            'python3': 0.9       // Python apps - visible
        };
        return transparencyMap[service] || 0.8;
    }
    
    /**
     * Kill a process
     * @param {number} pid - Process ID
     * @param {string} signal - Signal to send (TERM, KILL, etc.)
     */
    killProcess(pid, signal = 'TERM') {
        // In a real application, this would call an API endpoint
        console.log(`Killing process ${pid} with signal ${signal}`);
        
        // Remove the process from our list
        const index = this.processes.findIndex(p => p.pid === pid);
        if (index !== -1) {
            this.processes.splice(index, 1);
            this.applyFilter();
        }
    }
}
