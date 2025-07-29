class WebTask {
    /**
     * Initialize the WebTask application
     */
    constructor() {
        // Process management
        this.processes = [];
        this.filteredProcesses = [];
        this.selectedPid = null;
        this.processCounter = 1000;
        this.filterText = '';
        this.sortConfig = {
            column: 'cpu',
            direction: 'desc'
        };
        
        // File system
        this.fileSystem = {};
        this.currentPath = '/';
        
        // System monitoring
        this.cpuCores = 4; // Will be updated from API
        this.cpuHistory = [];
        this.cpuCoreValues = [];
        
        // Application state
        this.startTime = Date.now();
        this.updateInterval = 3000; // Update every 3 seconds
        
        // Initialize application components
        this._initializeComponents();
    }
    
    /**
     * Initialize all application components
     * @private
     */
    _initializeComponents() {
        // Initialize file system first
        this.initializeFileSystem();
        
        // Fetch initial data from API
        this.fetchInitialData();
        
        // Bind UI event handlers
        this.bindEvents();
    }

    //==============================
    // FILE SYSTEM MANAGEMENT
    //==============================
    
    /**
     * Initialize the virtual file system with a realistic directory structure
     */
    initializeFileSystem() {
        this.fileSystem = {
            '/': {
                type: 'directory',
                children: this._createRootFileSystem()
            }
        };
    }
    
    /**
     * Create the root file system structure
     * @private
     * @returns {Object} Root file system structure
     */
    _createRootFileSystem() {
        return {
            'bin': { 
                type: 'directory', 
                children: this._createBinDirectory() 
            },
            'etc': { 
                type: 'directory', 
                children: this._createEtcDirectory() 
            },
            'var': { 
                type: 'directory', 
                children: this._createVarDirectory() 
            },
            'home': { 
                type: 'directory', 
                children: this._createHomeDirectory() 
            }
        };
    }
    
    /**
     * Create the /bin directory structure
     * @private
     * @returns {Object} Bin directory structure
     */
    _createBinDirectory() {
        return {
            'bash': { 
                type: 'executable', 
                size: 1234567, 
                content: '#!/bin/bash\n# Bash shell executable\n# System shell program' 
            },
            'node': { 
                type: 'executable', 
                size: 45678901, 
                content: '#!/usr/bin/env node\n// Node.js runtime executable' 
            },
            'python3': { 
                type: 'executable', 
                size: 23456789, 
                content: '#!/usr/bin/python3\n# Python 3 interpreter' 
            }
        };
    }
    
    /**
     * Create the /etc directory structure
     * @private
     * @returns {Object} Etc directory structure
     */
    _createEtcDirectory() {
        return {
            'nginx': { 
                type: 'directory', 
                children: {
                    'nginx.conf': { 
                        type: 'config', 
                        size: 2048, 
                        content: 'server {\n    listen 80;\n    server_name localhost;\n    location / {\n        root /var/www/html;\n    }\n}' 
                    }
                }
            },
            'systemd': { 
                type: 'directory', 
                children: {
                    'system': { 
                        type: 'directory', 
                        children: {
                            'nginx.service': { 
                                type: 'service', 
                                size: 512, 
                                content: '[Unit]\nDescription=The nginx HTTP and reverse proxy server\n[Service]\nType=forking\nExecStart=/usr/sbin/nginx\n[Install]\nWantedBy=multi-user.target' 
                            }
                        }
                    }
                }
            }
        };
    }
    
    /**
     * Create the /var directory structure
     * @private
     * @returns {Object} Var directory structure
     */
    _createVarDirectory() {
        return {
            'www': { 
                type: 'directory', 
                children: {
                    'html': { 
                        type: 'directory', 
                        children: {
                            'index.html': { 
                                type: 'html', 
                                size: 1024, 
                                content: '<!DOCTYPE html>\n<html>\n<head>\n    <title>Welcome to nginx!</title>\n    <style>\n        body { font-family: Arial; background: #f0f0f0; }\n        .container { max-width: 800px; margin: 50px auto; padding: 20px; }\n        h1 { color: #333; text-align: center; }\n    </style>\n</head>\n<body>\n    <div class="container">\n        <h1>Welcome to nginx!</h1>\n        <p>If you can see this page, the nginx web server is successfully installed and working.</p>\n    </div>\n</body>\n</html>' 
                            },
                            'app.js': { 
                                type: 'script', 
                                size: 856, 
                                content: 'const express = require(\'express\');\nconst app = express();\nconst port = 3000;\n\napp.get(\'/\', (req, res) => {\n    res.send(\'Hello World from Node.js!\');\n});\n\napp.listen(port, () => {\n    console.log(`Server running at http://localhost:${port}`);\n});' 
                            }
                        }
                    }
                }
            }
        };
    }
    
    /**
     * Create the /home directory structure
     * @private
     * @returns {Object} Home directory structure
     */
    _createHomeDirectory() {
        return {
            'user': { 
                type: 'directory', 
                children: {
                    'documents': { 
                        type: 'directory', 
                        children: {
                            'notes.txt': { 
                                type: 'text', 
                                size: 256, 
                                content: 'Important system notes:\n1. Remember to update the server weekly\n2. Check logs for any suspicious activity\n3. Backup the database nightly' 
                            }
                        }
                    },
                    'projects': { 
                        type: 'directory', 
                        children: {
                            'webapp': { 
                                type: 'directory', 
                                children: {
                                    'index.js': { 
                                        type: 'script', 
                                        size: 1024, 
                                        content: 'const http = require(\'http\');\n\nconst server = http.createServer((req, res) => {\n    res.statusCode = 200;\n    res.setHeader(\'Content-Type\', \'text/plain\');\n    res.end(\'Hello World\\n\');\n});\n\nserver.listen(8080, \'localhost\', () => {\n    console.log(\'Server running at http://localhost:8080/\');\n});' 
                                    },
                                    'package.json': { 
                                        type: 'json', 
                                        size: 512, 
                                        content: '{\n  "name": "webapp",\n  "version": "1.0.0",\n  "description": "A simple web application",\n  "main": "index.js",\n  "scripts": {\n    "start": "node index.js"\n  },\n  "dependencies": {\n    "express": "^4.17.1"\n  }\n}' 
                                    }
                                }
                            }
                        }
                    }
                }
            }
        };
    }
    
    /**
     * Get file content from the virtual file system
     * @param {string} path - Path to the file
     * @returns {string|null} File content or null if not found
     */
    getFileContent(path) {
        const file = this._getItemAtPath(path);
        if (!file || file.type === 'directory') {
            return null;
        }
        return file.content;
    }
    
    /**
     * Get item (file or directory) at the specified path
     * @private
     * @param {string} path - Path to the item
     * @returns {Object|null} Item or null if not found
     */
    _getItemAtPath(path) {
        if (path === '/') {
            return this.fileSystem['/'];
        }
        
        const parts = path.split('/').filter(Boolean);
        let current = this.fileSystem['/'];
        
        for (const part of parts) {
            if (!current.children || !current.children[part]) {
                return null;
            }
            current = current.children[part];
        }
        
        return current;
    }

    //==============================
    // API INTEGRATION & DATA FETCHING
    //==============================
    
    /**
     * Fetch initial data from API to set up the application
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

    //==============================
    // PERIODIC UPDATES & SCHEDULING
    //==============================
    
    /**
     * Start periodic updates of system and process data
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
        this.updateProcesses();
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
        // Generate a random CPU usage value
        const cpuUsage = Math.random() * 100;
        
        // Update CPU cores
        this.updateCpuCores(cpuUsage);
        
        // Update CPU history
        this.cpuHistory.push(cpuUsage);
        if (this.cpuHistory.length > 60) {
            this.cpuHistory.shift();
        }
        
        // Update CPU history chart
        this.updateCpuHistoryChart(cpuUsage);
    }

    
    // Fetch system information from API
    fetchSystemInfo() {
        return fetch('/api/system')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Update CPU cores count
                this.cpuCores = data.cpu.cores || 4;
                
                // Initialize CPU core values array if needed
                if (this.cpuCoreValues.length !== this.cpuCores) {
                    this.cpuCoreValues = Array(this.cpuCores).fill(0);
                }
                
                // Update CPU usage display
                const cpuUsage = data.cpu.percent;
                document.getElementById('cpu-percent').textContent = cpuUsage.toFixed(1) + '%';
                
                // Update memory usage
                const memUsage = data.memory.percent;
                document.getElementById('mem-fill').style.width = memUsage + '%';
                document.getElementById('mem-percent').textContent = memUsage.toFixed(1) + '%';
                
                // Update load average
                const loadAvg = data.cpu.load_avg[0].toFixed(2);
                document.getElementById('load-avg').textContent = loadAvg;
                
                // Update uptime
                const uptimeSeconds = data.uptime;
                const hours = Math.floor(uptimeSeconds / 3600);
                const minutes = Math.floor((uptimeSeconds % 3600) / 60);
                const seconds = uptimeSeconds % 60;
                document.getElementById('uptime').textContent =
                    `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                
                // Simulate individual core values (API doesn't provide per-core data)
                this.simulateCpuCores(cpuUsage);
                
                // Update CPU history chart
                this.updateCpuHistoryChart(cpuUsage);
            });
    }
    
    // Fetch processes from API
    fetchProcesses() {
        return fetch('/api/processes')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Transform API data to match our process format
                this.processes = data.map(process => ({
                    pid: process.pid,
                    user: process.user,
                    cpu: process.cpu,
                    memory: process.memory,
                    time: this.formatTime(process.cpu_times?.user || 0),
                    port: this.detectPort(process.name),
                    command: process.name,
                    file: null,
                    service: this.detectService(process.name),
                    parent: null,
                    children: [],
                    transparency: this.calculateTransparency(this.detectService(process.name)),
                    startTime: Date.now() - Math.random() * 3600000 // Not provided by API
                }));
                
                // Build process hierarchy
                this.buildProcessHierarchy();
                
                // Sort processes according to current sort configuration
                this.sortProcesses();
                
                // Apply any active filters
                this.applyFilter();
                
                // Render the updated process list
                this.renderProcesses();
            });
    }
    
    // Detect service name from command
    detectService(command) {
        if (!command) return 'unknown';
        
        const commandLower = command.toLowerCase();
        if (commandLower.includes('systemd')) return 'systemd';
        if (commandLower.includes('nginx')) return 'nginx';
        if (commandLower.includes('node')) return 'node';
        if (commandLower.includes('python')) return 'python3';
        if (commandLower.includes('bash')) return 'bash';
        if (commandLower.includes('ssh')) return 'sshd';
        if (commandLower.includes('mysql')) return 'mysql';
        if (commandLower.includes('redis')) return 'redis';
        if (commandLower.includes('docker')) return 'docker';
        
        // Extract first word as service name
        return command.split(' ')[0];
    }
    
    // Detect port from command
    detectPort(command) {
        if (!command) return null;
        
        // Common port patterns
        const portPatterns = {
            'nginx': 80,
            'apache': 80,
            'node': 3000,
            'python -m http.server': 8000,
            'ssh': 22,
            'mysql': 3306,
            'redis': 6379
        };
        
        // Check for port patterns
        for (const [pattern, port] of Object.entries(portPatterns)) {
            if (command.toLowerCase().includes(pattern)) {
                return port;
            }
        }
        
        // Try to extract port from command (e.g., "server --port=8080")
        const portMatch = command.match(/--port[=\s](\d+)|:(\d+)/);
        if (portMatch) {
            return parseInt(portMatch[1] || portMatch[2]);
        }
        
        return null;
    }
    
    // Format time in seconds to HH:MM:SS
    formatTime(seconds) {
        seconds = Math.floor(seconds);
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    
    // Simulate CPU cores data (API doesn't provide per-core data)
    simulateCpuCores(overallCpuUsage) {
        // Base the simulation on the overall CPU usage
        const baseLoad = overallCpuUsage * 0.8; // 80% of the overall load as base
        
        for (let i = 0; i < this.cpuCores; i++) {
            // Each core gets the base load plus individual variation
            let coreLoad = baseLoad;
            
            // Add some random variation to each core
            coreLoad += (Math.random() - 0.5) * 20;
            
            // Add occasional spikes to random cores
            if (Math.random() < 0.1) {
                coreLoad += Math.random() * 30;
            }
            
            // Ensure value is between 0-100
            coreLoad = Math.min(100, Math.max(0, coreLoad));
            
            // Store the value
            this.cpuCoreValues[i] = coreLoad;
            
            // Update the visual elements
            this.updateCpuCoreDisplay(i, coreLoad);
        }
    }
    
    // Update a single CPU core display
    updateCpuCoreDisplay(coreIndex, value) {
        const fillElement = document.getElementById(`cpu-core-fill-${coreIndex}`);
        const valueElement = document.getElementById(`cpu-core-value-${coreIndex}`);
        
        if (fillElement && valueElement) {
            fillElement.style.width = value + '%';
            valueElement.textContent = value.toFixed(1) + '%';
            
            // Add color indication based on load
            if (value > 80) {
                fillElement.style.backgroundColor = '#ff3300';
            } else if (value > 50) {
                fillElement.style.backgroundColor = '#ffcc00';
            } else {
                fillElement.style.backgroundColor = '#33cc33';
            }
        }
    }
    
    // Fallback to simulated data if API fails
    simulateData() {
        console.log('Using simulated data');
        
        // Create simulated processes
        const processTemplates = [
            { cmd: 'systemd', user: 'root', port: null, service: 'systemd', parent: null },
            { cmd: '/usr/sbin/nginx', user: 'www-data', port: 80, service: 'nginx', parent: 1 },
            { cmd: 'nginx: worker process', user: 'www-data', port: 80, service: 'nginx', parent: 'nginx' },
            { cmd: 'node /var/www/html/app.js', user: 'user', port: 3000, service: 'node', parent: null },
            { cmd: 'python3 -m http.server 8000', user: 'user', port: 8000, service: 'python3', parent: null },
            { cmd: 'sshd: /usr/sbin/sshd -D', user: 'root', port: 22, service: 'sshd', parent: null }
        ];

        this.processes = processTemplates.map((template, index) => ({
            pid: this.processCounter + index,
            user: template.user,
            cpu: Math.random() * 15,
            memory: Math.random() * 25,
            time: this.formatTime(Math.random() * 3600),
            port: template.port,
            command: template.cmd,
            file: null,
            service: template.service,
            parent: template.parent,
            children: [],
            transparency: this.calculateTransparency(template.service),
            startTime: Date.now() - Math.random() * 3600000
        }));

        this.processCounter += processTemplates.length;
        this.buildProcessHierarchy();
        this.sortProcesses();
        this.applyFilter();
        this.renderProcesses();
        
        // Initialize CPU cores display
        this.initializeCpuCoresDisplay();
        
        // Start simulated updates
        setInterval(() => {
            this.updateSimulatedData();
        }, 3000);
    }
    
    // Update simulated data
    updateSimulatedData() {
        // Update CPU usage
        const cpuUsage = Math.random() * 100;
        document.getElementById('cpu-percent').textContent = cpuUsage.toFixed(1) + '%';
        
        // Update memory usage
        const memUsage = Math.random() * 100;
        document.getElementById('mem-fill').style.width = memUsage + '%';
        document.getElementById('mem-percent').textContent = memUsage.toFixed(1) + '%';
        
        // Update load average
        const loadAvg = (Math.random() * 4).toFixed(2);
        document.getElementById('load-avg').textContent = loadAvg;
        
        // Update uptime
        const uptime = Date.now() - this.startTime;
        const hours = Math.floor(uptime / 3600000);
        const minutes = Math.floor((uptime % 3600000) / 60000);
        const seconds = Math.floor((uptime % 60000) / 1000);
        document.getElementById('uptime').textContent =
            `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // Simulate CPU cores
        this.simulateCpuCores(cpuUsage);
        
        // Update CPU history chart
        this.updateCpuHistoryChart(cpuUsage);
        
        // Update process data
        this.processes.forEach(process => {
            process.cpu += (Math.random() - 0.5) * 2;
            process.cpu = Math.max(0, Math.min(100, process.cpu));

            process.memory += (Math.random() - 0.5) * 1;
            process.memory = Math.max(0, Math.min(100, process.memory));
        });
        
        // Sort and render processes
        this.sortProcesses();
        this.applyFilter();
        this.renderProcesses();
    }

    initializeCpuCoresDisplay() {
        const container = document.getElementById('cpu-cores-container');
        container.innerHTML = ''; // Clear container
        
        // Update the cores count in the UI
        document.getElementById('cpu-cores-count').textContent = this.cpuCores;
        
        // Create elements for each CPU core
        for (let i = 0; i < this.cpuCores; i++) {
            const coreElement = document.createElement('div');
            coreElement.className = 'cpu-core';
            coreElement.innerHTML = `
                <div class="cpu-core-label">Core ${i}</div>
                <div class="cpu-core-bar">
                    <div class="cpu-core-fill" id="cpu-core-fill-${i}" style="width: 0%"></div>
                </div>
                <div class="cpu-core-value" id="cpu-core-value-${i}">0%</div>
            `;
            container.appendChild(coreElement);
        }
        
        // Initialize CPU history chart
        this.initializeCpuHistoryChart();
    }
    
    // Update CPU cores with simulated activity
    updateCpuCores() {
        // Simulate CPU core activity with some correlation between cores
        // This creates more realistic patterns where cores tend to work together
        const baseLoad = Math.random() * 40; // Base load affects all cores
        
        for (let i = 0; i < this.cpuCores; i++) {
            // Each core gets the base load plus individual variation
            // Some cores will spike higher than others to simulate real workloads
            let coreLoad = baseLoad;
            
            // Add some random variation to each core
            coreLoad += Math.random() * 60;
            
            // Add occasional spikes to random cores
            if (Math.random() < 0.1) {
                coreLoad += Math.random() * 40;
            }
            
            // Ensure value is between 0-100
            coreLoad = Math.min(100, Math.max(0, coreLoad));
            
            // Store the value
            this.cpuCoreValues[i] = coreLoad;
            
            // Update the visual elements
            const fillElement = document.getElementById(`cpu-core-fill-${i}`);
            const valueElement = document.getElementById(`cpu-core-value-${i}`);
            
            if (fillElement && valueElement) {
                fillElement.style.width = coreLoad + '%';
                valueElement.textContent = coreLoad.toFixed(1) + '%';
                
                // Add color indication based on load
                if (coreLoad > 80) {
                    fillElement.style.backgroundColor = '#ff3300';
                } else if (coreLoad > 50) {
                    fillElement.style.backgroundColor = '#ffcc00';
                } else {
                    fillElement.style.backgroundColor = '#33cc33';
                }
            }
        }
    }
    
    // Initialize the CPU history chart
    initializeCpuHistoryChart() {
        // We'll use a simple canvas-based chart for CPU history
        this.cpuHistoryCanvas = document.getElementById('cpu-history-chart');
        this.cpuHistoryContext = this.cpuHistoryCanvas.getContext('2d');
        
        // Initialize with empty data
        this.cpuHistory = Array(50).fill(0);
        
        // Set canvas size
        this.cpuHistoryCanvas.width = this.cpuHistoryCanvas.parentElement.clientWidth;
    }
    
    // Update the CPU history chart with new data
    updateCpuHistoryChart(cpuUsage) {
        // Add new value to history and remove oldest
        this.cpuHistory.push(cpuUsage);
        if (this.cpuHistory.length > 50) {
            this.cpuHistory.shift();
        }
        
        // Clear canvas
        const ctx = this.cpuHistoryContext;
        const canvas = this.cpuHistoryCanvas;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw chart background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw grid lines
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.beginPath();
        for (let i = 0; i < 5; i++) {
            const y = canvas.height * (i / 4);
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
        }
        ctx.stroke();
        
        // Draw CPU history line
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

    generateTime() {
        const seconds = Math.floor(Math.random() * 3600);
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    applyFilter() {
        if (!this.filterText) {
            this.filteredProcesses = [...this.processes];
        } else {
            const filter = this.filterText.toLowerCase();
            this.filteredProcesses = this.processes.filter(process =>
                process.pid.toString().includes(filter) ||
                process.user.toLowerCase().includes(filter) ||
                process.command.toLowerCase().includes(filter) ||
                process.service.toLowerCase().includes(filter) ||
                (process.port && process.port.toString().includes(filter))
            );
        }
        document.getElementById('filtered-count').textContent = this.filteredProcesses.length;
    }

    updateSystemStats() {
        // Calculate overall CPU usage as average of all cores
        this.updateCpuCores();
        
        const cpuUsage = this.cpuCoreValues.reduce((sum, value) => sum + value, 0) / this.cpuCores;
        const memUsage = Math.random() * 100;
        const loadAvg = (Math.random() * 4).toFixed(2);

        document.getElementById('cpu-percent').textContent = cpuUsage.toFixed(1) + '%';

        document.getElementById('mem-fill').style.width = memUsage + '%';
        document.getElementById('mem-percent').textContent = memUsage.toFixed(1) + '%';

        document.getElementById('load-avg').textContent = loadAvg;

        // Update uptime
        const uptime = Date.now() - this.startTime;
        const hours = Math.floor(uptime / 3600000);
        const minutes = Math.floor((uptime % 3600000) / 60000);
        const seconds = Math.floor((uptime % 60000) / 1000);
        document.getElementById('uptime').textContent =
            `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
        // Update CPU history chart
        this.updateCpuHistoryChart(cpuUsage);
    }

    //==============================
    // PROCESS MANAGEMENT
    //==============================
    
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
        this.renderProcesses();
        
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
     * Convert time string (HH:MM:SS) to seconds for sorting
     * @param {string} timeString - Time string in HH:MM:SS format
     * @returns {number} Total seconds
     */
    timeToSeconds(timeString) {
        if (!timeString) return 0;
        const [hours, minutes, seconds] = timeString.split(':').map(Number);
        return hours * 3600 + minutes * 60 + seconds;
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
     * Generate a preview thumbnail for a process
     * @param {Object} process - Process object
     * @returns {string} HTML for the thumbnail
     */
    generatePreviewThumbnail(process) {
        let thumbnailContent = '';
        let thumbnailClass = 'preview-thumbnail';

        if (process.file && this.getFileContent(process.file)) {
            const fileContent = this.getFileContent(process.file);
            const fileExtension = process.file.split('.').pop();

            switch (fileExtension) {
                case 'html':
                    thumbnailClass += ' html-preview';
                    thumbnailContent = `<div class="html-preview">${fileContent}</div>`;
                    break;
                case 'js':
                    thumbnailClass += ' bash-script';
                    thumbnailContent = fileContent.substring(0, 50) + '...';
                    break;
                case 'sh':
                    thumbnailClass += ' bash-script';
                    thumbnailContent = fileContent.substring(0, 50) + '...';
                    break;
                default:
                    if (process.service) {
                        thumbnailClass += ' service-status';
                        thumbnailContent = `<div>⚙️</div><div>${process.service}</div>`;
                    }
            }
        } else if (process.port) {
            thumbnailClass += ' port-indicator';
            thumbnailContent = `<div>🌐</div><div>:${process.port}</div>`;
        } else if (process.service) {
            thumbnailClass += ' service-status';
            thumbnailContent = `<div>⚙️</div><div>${process.service}</div>`;
        }

        return { 'class': thumbnailClass, content: thumbnailContent };
    }

    renderProcesses() {
        const processList = document.getElementById('process-list');
        processList.innerHTML = '';

        this.filteredProcesses.forEach(process => {
            const row = document.createElement('div');
            row.className = 'process-row';

            if (process.cpu > 10) row.classList.add('high-cpu');
            if (process.memory > 20) row.classList.add('high-mem');
            if (process.transparency < 0.8) row.classList.add('transparent');

            // Add hierarchy indicator
            let hierarchyIndicator = '';
            if (process.parentPid) {
                const depth = this.getProcessDepth(process);
                const hierarchyClass = depth === 1 ? 'child' : 'grandchild';
                hierarchyIndicator = `<div class="process-hierarchy ${hierarchyClass}"></div>`;
            }

            const thumbnail = this.generatePreviewThumbnail(process);

            row.innerHTML = `
                ${hierarchyIndicator}
                <div>${process.pid}</div>
                <div>${process.user}</div>
                <div>${process.cpu.toFixed(1)}</div>
                <div>${process.memory.toFixed(1)}</div>
                <div>${process.time}</div>
                <div>${process.port || '-'}</div>
                <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${process.command}">
                    ${process.command}
                </div>
                <div class="process-preview" onclick="webtask.showPreview(${process.pid})">
                    <div class="${thumbnail['class']}">${thumbnail.content}</div>
                    <span class="preview-icon">👁️</span>
                </div>
                <div class="kill-options">
                    <button class="kill-btn" onclick="webtask.toggleKillDropdown(event, ${process.pid})">
                        KILL ▼
                    </button>
                    <div class="kill-dropdown" id="dropdown-${process.pid}">
                        <div class="kill-option" onclick="webtask.killProcessWithSignal(${process.pid}, 'TERM')">
                            SIGTERM (Graceful)
                        </div>
                        <div class="kill-option danger" onclick="webtask.killProcessWithSignal(${process.pid}, 'KILL')">
                            SIGKILL (Force)
                        </div>
                        <div class="kill-option" onclick="webtask.killProcessWithSignal(${process.pid}, 'INT')">
                            SIGINT (Interrupt)
                        </div>
                        <div class="kill-option" onclick="webtask.killProcessWithSignal(${process.pid}, 'HUP')">
                            SIGHUP (Hangup)
                        </div>
                    </div>
                </div>
            `;

            row.style.opacity = process.transparency;

            row.addEventListener('click', (e) => {
                if (!e.target.closest('.kill-options') && !e.target.closest('.process-preview')) {
                    this.selectedPid = process.pid;
                    document.getElementById('selected-pid').textContent = process.pid;

                    // Remove previous selection
                    document.querySelectorAll('.process-row').forEach(r =>
                        r.style.background = '');
                    row.style.background = '#444';
                }
            });

            row.addEventListener('dblclick', () => {
                this.showProcessDetails(process.pid);
            });

            processList.appendChild(row);
        });

        document.getElementById('process-count').textContent = this.processes.length;
        document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
    }

    getProcessDepth(process) {
        let depth = 0;
        let current = process;
        while (current.parentPid) {
            depth++;
            current = this.processes.find(p => p.pid === current.parentPid);
            if (!current) break;
        }
        return depth;
    }

    getFileContent(filePath) {
        const parts = filePath.split('/').filter(Boolean);
        let current = this.fileSystem['/'];

        for (const part of parts) {
            if (current.children && current.children[part]) {
                current = current.children[part];
            } else {
                return null;
            }
        }

        return current.content || null;
    }

    showPreview(pid) {
        const process = this.processes.find(p => p.pid === pid);
        if (!process) return;

        const overlay = document.getElementById('preview-overlay');
        const title = document.getElementById('preview-title');
        const body = document.getElementById('preview-body');

        title.textContent = `Process Details - PID ${pid}: ${process.command}`;

        // Calculate additional information
        const uptime = this.formatTime(process.time);
        const memoryUsage = (process.memory * 100).toFixed(2) + '%';
        const cpuUsage = (process.cpu * 100).toFixed(2) + '%';
        const status = process.transparency < 0.8 ? 'Background Process' : 'Active Process';
        const startTime = new Date(Date.now() - process.time * 1000).toLocaleString();
        
        if (process.file && this.getFileContent(process.file)) {
            const content = this.getFileContent(process.file);
            const isHTML = process.file.endsWith('.html');

            // Create a structured view with file information and content
            body.className = 'preview-body process-info';
            body.innerHTML = `
                <div class="preview-info-section">
                    <h3>Process Information</h3>
                    <div class="preview-info-row"><span class="preview-info-label">PID:</span> <span>${process.pid}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">User:</span> <span>${process.user}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Command:</span> <span>${process.command}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">CPU Usage:</span> <span>${cpuUsage}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Memory Usage:</span> <span>${memoryUsage}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Uptime:</span> <span>${uptime}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Started:</span> <span>${startTime}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Status:</span> <span>${status}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">File:</span> <span>${process.file}</span></div>
                </div>
                <div class="preview-info-section">
                    <h3>File Content</h3>
                    <div class="file-content ${isHTML ? 'html-content' : ''}">${isHTML ? content : this.escapeHTML(content)}</div>
                </div>
            `;
        } else if (process.port) {
            // Create a structured view for network services
            body.className = 'preview-body process-info';
            body.innerHTML = `
                <div class="preview-info-section">
                    <h3>Process Information</h3>
                    <div class="preview-info-row"><span class="preview-info-label">PID:</span> <span>${process.pid}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">User:</span> <span>${process.user}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Command:</span> <span>${process.command}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">CPU Usage:</span> <span>${cpuUsage}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Memory Usage:</span> <span>${memoryUsage}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Uptime:</span> <span>${uptime}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Started:</span> <span>${startTime}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Status:</span> <span>${status}</span></div>
                </div>
                <div class="preview-info-section">
                    <h3>Network Information</h3>
                    <div class="preview-info-row"><span class="preview-info-label">Port:</span> <span>${process.port}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Service Type:</span> <span>${process.service || 'Unknown'}</span></div>
    
    this.filteredProcesses.sort((a, b) => {
        let valueA, valueB;
        
        switch(column) {
            case 'pid':
                return (a.pid - b.pid) * multiplier;
            case 'user':
                return (a.user.localeCompare(b.user)) * multiplier;
            case 'cpu':
                return (a.cpu - b.cpu) * multiplier;
            case 'mem':
                return (a.mem - b.mem) * multiplier;
            case 'time':
                return (a.time - b.time) * multiplier;
            case 'port':
                // Handle null ports
                if (!a.port && !b.port) return 0;
                if (!a.port) return 1 * multiplier;
                if (!b.port) return -1 * multiplier;
                return (a.port - b.port) * multiplier;
            case 'command':
                return (a.command.localeCompare(b.command)) * multiplier;
            default:
                return 0;
        }
    });

    // Re-render the processes with the new sort order
    this.renderProcesses();
}

renderProcesses() {
    const processList = document.getElementById('process-list');
    processList.innerHTML = '';

    this.filteredProcesses.forEach(process => {
        const row = document.createElement('div');
        row.className = 'process-row';

        if (process.cpu > 10) row.classList.add('high-cpu');
        if (process.memory > 20) row.classList.add('high-mem');
        if (process.transparency < 0.8) row.classList.add('transparent');

        // Add hierarchy indicator
        let hierarchyIndicator = '';
        if (process.parentPid) {
            const depth = this.getProcessDepth(process);
            const hierarchyClass = depth === 1 ? 'child' : 'grandchild';
            hierarchyIndicator = `<div class="process-hierarchy ${hierarchyClass}"></div>`;
        }

        const thumbnail = this.generatePreviewThumbnail(process);

        row.innerHTML = `
            ${hierarchyIndicator}
            <div class="sortable" data-sort="pid">${process.pid}</div>
            <div class="sortable" data-sort="user">${process.user}</div>
            <div class="sortable" data-sort="cpu">${process.cpu.toFixed(1)}</div>
            <div class="sortable" data-sort="mem">${process.memory.toFixed(1)}</div>
            <div class="sortable" data-sort="time">${process.time}</div>
            <div class="sortable" data-sort="port">${process.port || '-'}</div>
            <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${process.command}">
                ${process.command}
            </div>
            <div class="process-preview" onclick="webtask.showPreview(${process.pid})">
                <div class="${thumbnail['class']}">${thumbnail.content}</div>
                <span class="preview-icon">👁️</span>
            </div>
            <div class="kill-options">
                <button class="kill-btn" onclick="webtask.toggleKillDropdown(event, ${process.pid})">
                    KILL ▼
                </button>
                <div class="kill-dropdown" id="dropdown-${process.pid}">
                    <div class="kill-option" onclick="webtask.killProcessWithSignal(${process.pid}, 'TERM')">
                        SIGTERM (Graceful)
                    </div>
                    <div class="kill-option danger" onclick="webtask.killProcessWithSignal(${process.pid}, 'KILL')">
                        SIGKILL (Force)
                    </div>
                    <div class="kill-option" onclick="webtask.killProcessWithSignal(${process.pid}, 'INT')">
                        SIGINT (Interrupt)
                    </div>
                    <div class="kill-option" onclick="webtask.killProcessWithSignal(${process.pid}, 'HUP')">
                        SIGHUP (Hangup)
                    </div>
                </div>
            </div>
        `;

        row.style.opacity = process.transparency;

        row.addEventListener('click', (e) => {
            if (!e.target.closest('.kill-options') && !e.target.closest('.process-preview')) {
                this.selectedPid = process.pid;
                document.getElementById('selected-pid').textContent = process.pid;

                // Remove previous selection
                document.querySelectorAll('.process-row').forEach(r =>
                    r.style.background = '');
                row.style.background = '#444';
            }
        });

        row.addEventListener('dblclick', () => {
            this.showProcessDetails(process.pid);
        });

        processList.appendChild(row);
    });

    document.getElementById('process-count').textContent = this.processes.length;
    document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
}

bindEvents() {
    // Filter processes when typing in the search box
    document.getElementById('search-filter').addEventListener('input', (e) => {
        this.filterText = e.target.value.toLowerCase();
        this.filterProcesses();
        this.renderProcesses();
    });

    // Global click handler for closing dropdowns
    document.addEventListener('click', (e) => {
        const dropdowns = document.querySelectorAll('.kill-dropdown.show');
        dropdowns.forEach(dropdown => {
            if (!e.target.closest('.kill-options') && !e.target.closest('.process-preview')) {
                dropdown.classList.remove('show');
            }
        });
    });

    // Add click handlers for sortable columns
    document.querySelectorAll('.sortable').forEach(column => {
        column.addEventListener('click', (e) => {
            const sortBy = column.getAttribute('data-sort');
            this.sortProcesses(sortBy);
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'F1') {
            e.preventDefault();
            const advancedControls = document.getElementById('advanced-controls');
            advancedControls.classList.toggle('show');
        } else if (e.key === 'F2') {
            e.preventDefault();
            this.openFileBrowser();
        } else if (e.key === 'F5') {
            e.preventDefault();
            this.toggleTreeView();
        } else if (e.key === 'F6') {
            e.preventDefault();
            this.toggleSortOrder();
        } else if (e.key === 'F9') {
            e.preventDefault();
            if (this.selectedPid) {
                this.killProcess(this.selectedPid);
            }
        } else if (e.key === 'F10' || e.key === 'Escape') {
            e.preventDefault();
            if (document.getElementById('file-browser-modal').classList.contains('show')) {
                this.closeFileBrowser();
            } else if (document.getElementById('process-details-modal').classList.contains('show')) {
                this.closeProcessDetails();
            } else if (document.getElementById('preview-overlay').classList.contains('show')) {
                document.getElementById('preview-overlay').classList.remove('show');
            } else if (document.getElementById('advanced-controls').classList.contains('show')) {
                document.getElementById('advanced-controls').classList.remove('show');
            }
        }
    });
}

// Initialize webtask
const webtask = new WebTask();