/**
 * UI Manager Module
 * Handles all UI-related functionality
 */
class UIManager {
    constructor(processManager, systemMonitor, fileSystemManager) {
        this.processManager = processManager;
        this.systemMonitor = systemMonitor;
        this.fileSystemManager = fileSystemManager;
        this.previewVisible = false;
    }
    
    /**
     * Bind all UI event listeners
     */
    bindEvents() {
        // Process filter input
        const filterInput = document.getElementById('search-filter');
        if (filterInput) {
            filterInput.addEventListener('input', (e) => {
                this.processManager.setFilterText(e.target.value);
                this.renderProcesses();
            });
        }
        
        // Process sort headers
        document.querySelectorAll('.process-header .sortable').forEach(header => {
            header.addEventListener('click', (e) => {
                const column = e.target.dataset.sort;
                const currentDirection = this.processManager.sortConfig.direction;
                const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
                
                // Update sort indicators
                document.querySelectorAll('.process-header .sortable').forEach(h => {
                    h.classList.remove('sort-asc', 'sort-desc');
                });
                
                e.target.classList.add(`sort-${newDirection}`);
                
                // Update sort configuration
                this.processManager.setSortConfig(column, newDirection);
                
                // Re-render processes
                this.renderProcesses();
            });
        });
        
        // Process action buttons
        document.addEventListener('click', (e) => {
            // Handle kill button
            if (e.target.classList.contains('kill-button') || e.target.closest('.kill-button')) {
                const button = e.target.classList.contains('kill-button') ? e.target : e.target.closest('.kill-button');
                const pid = parseInt(button.dataset.pid);
                this.processManager.killProcess(pid, 'TERM');
            } 
            // Handle more button
            else if (e.target.classList.contains('more-button') || e.target.closest('.more-button')) {
                const button = e.target.classList.contains('more-button') ? e.target : e.target.closest('.more-button');
                const pid = parseInt(button.dataset.pid);
                this.toggleKillOptions(pid);
            }
            // Handle pause button
            else if (e.target.classList.contains('pause-button') || e.target.closest('.pause-button')) {
                const button = e.target.classList.contains('pause-button') ? e.target : e.target.closest('.pause-button');
                const pid = parseInt(button.dataset.pid);
                this.processManager.killProcess(pid, 'STOP');
            }
            // Handle restart button
            else if (e.target.classList.contains('restart-button') || e.target.closest('.restart-button')) {
                const button = e.target.classList.contains('restart-button') ? e.target : e.target.closest('.restart-button');
                const pid = parseInt(button.dataset.pid);
                this.processManager.killProcess(pid, 'HUP');
            }
            // Handle kill options
            else if (e.target.classList.contains('kill-option')) {
                const pid = parseInt(e.target.dataset.pid);
                const signal = e.target.dataset.signal;
                if (pid && signal) {
                    this.processManager.killProcess(pid, signal);
                    this.toggleKillOptions(pid); // Close the dropdown
                }
            }
        });
        
        // Process row selection
        document.addEventListener('click', (e) => {
            if (e.target.closest('.process-row') && !e.target.closest('.kill-options') && !e.target.closest('.process-preview')) {
                const row = e.target.closest('.process-row');
                const pid = parseInt(row.dataset.pid);
                
                this.selectProcess(pid);
            }
        });
        
        // Advanced controls toggle
        const advancedToggle = document.getElementById('advanced-toggle');
        if (advancedToggle) {
            advancedToggle.addEventListener('click', () => {
                document.getElementById('advanced-controls').classList.toggle('show');
            });
        }
        
        // Close preview button
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('preview-close-button')) {
                this.closePreview();
            }
        });
        
        // Preview thumbnails
        document.addEventListener('click', (e) => {
            // Check if the clicked element or any of its parents has the preview-thumbnail class
            let target = e.target;
            while (target && !target.classList?.contains('preview-thumbnail')) {
                target = target.parentElement;
            }
            
            if (target && target.dataset.pid) {
                const pid = parseInt(target.dataset.pid);
                this.showProcessPreview(pid, e);
            }
        });
        
        // Escape key to close modals
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                if (this.previewVisible) {
                    this.closePreview();
                } else if (document.getElementById('advanced-controls').classList.contains('show')) {
                    document.getElementById('advanced-controls').classList.remove('show');
                }
            }
        });
    }
    
    /**
     * Render the process list
     */
    renderProcesses() {
        const container = document.getElementById('process-list');
        if (!container) return;
        
        // Clear existing processes
        container.innerHTML = '';
        
        // Render each process
        this.processManager.filteredProcesses.forEach(process => {
            const row = this.createProcessRow(process);
            container.appendChild(row);
        });
        
        // Update process count
        const countElement = document.getElementById('process-count');
        if (countElement) {
            countElement.textContent = `${this.processManager.filteredProcesses.length} processes`;
        }
    }
    
    /**
     * Create a process row element
     * @param {Object} process - Process object
     * @returns {HTMLElement} Process row element
     */
    createProcessRow(process) {
        const row = document.createElement('div');
        row.className = 'process-row';
        row.dataset.pid = process.pid;
        row.dataset.parent = process.ppid || 0;
        row.dataset.level = process.level || 0;
        
        // Generate the preview thumbnail
        const thumbnail = this.generatePreviewThumbnail(process);
        
        // Generate command with icon
        const commandWithIcon = this.generateCommandWithIcon(process);
        
        row.innerHTML = `
            <div class="process-card-header">
                <div class="process-actions">
                    <div class="action-buttons">
                        <button class="kill-button" data-pid="${process.pid}" title="Kill Process">
                            <span class="kill-icon">×</span>
                        </button>
                        <button class="pause-button" data-pid="${process.pid}" title="Pause Process">
                            <span class="pause-icon">⏸</span>
                        </button>
                        <button class="restart-button" data-pid="${process.pid}" title="Restart Process">
                            <span class="restart-icon">↻</span>
                        </button>
                        <button class="stop-button" data-pid="${process.pid}" title="Stop Process">
                            <span class="stop-icon">⏹</span>
                        </button>
                        <button class="info-button" data-pid="${process.pid}" title="Process Info">
                            <span class="info-icon">ℹ</span>
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="process-card-body">
                <div class="process-preview">
                    ${thumbnail}
                </div>
            </div>
            
            <div class="process-card-footer">
                <div class="info-badge pid-badge" title="Process ID">${process.pid}</div>
                <div class="info-badge user-badge" title="User">${process.user}</div>
                <div class="info-badge time-badge" title="Process Time">${process.time}</div>
                ${process.port ? `<div class="info-badge port-badge" title="Port">:${process.port}</div>` : ''}
            </div>
            
            <div class="kill-dropdown" id="dropdown-${process.pid}">
                <div class="kill-dropdown-header">Process Actions - PID ${process.pid}</div>
                <div class="kill-option" data-pid="${process.pid}" data-signal="TERM">
                    <span class="signal-icon">✓</span> SIGTERM (Terminate)
                </div>
                <div class="kill-option" data-pid="${process.pid}" data-signal="KILL">
                    <span class="signal-icon">⚡</span> SIGKILL (Force Kill)
                </div>
                <div class="kill-option" data-pid="${process.pid}" data-signal="INT">
                    <span class="signal-icon">⏹</span> SIGINT (Interrupt)
                </div>
                <div class="kill-option" data-pid="${process.pid}" data-signal="HUP">
                    <span class="signal-icon">🔄</span> SIGHUP (Restart)
                </div>
                <div class="kill-option" data-pid="${process.pid}" data-signal="STOP">
                    <span class="signal-icon">⏸</span> SIGSTOP (Pause)
                </div>
                <div class="kill-option" data-pid="${process.pid}" data-signal="CONT">
                    <span class="signal-icon">▶️</span> SIGCONT (Resume)
                </div>
            </div>
        `;
        
        row.style.opacity = process.transparency;
        
        return row;
    }
    
    /**
     * Generate command text with appropriate icon
     * @param {Object} process - Process object
     * @returns {string} HTML for the command with icon
     */
    generateCommandWithIcon(process) {
        let iconHtml = '';
        const command = process.command || '';
        const path = process.path || '';
        
        // Determine the type of icon based on the process service or command
        if (process.service === 'nginx') {
            iconHtml = '<span class="command-icon nginx-icon">NGINX</span>';
        } else if (process.service === 'node') {
            iconHtml = '<span class="command-icon node-icon">NODE</span>';
        } else if (process.service === 'python' || command.includes('python')) {
            iconHtml = '<span class="command-icon python-icon">PY</span>';
        } else if (process.service === 'java' || command.includes('java')) {
            iconHtml = '<span class="command-icon java-icon">JAVA</span>';
        } else if (process.service === 'mysql' || command.includes('mysql')) {
            iconHtml = '<span class="command-icon mysql-icon">SQL</span>';
        } else if (command.includes('firefox')) {
            iconHtml = '<span class="command-icon firefox-icon">FF</span>';
        } else if (command.includes('chrome')) {
            iconHtml = '<span class="command-icon chrome-icon">CR</span>';
        } else if (command.includes('pycharm')) {
            iconHtml = '<span class="command-icon pycharm-icon">PC</span>';
        } else if (command.includes('vscode') || command.includes('code')) {
            iconHtml = '<span class="command-icon vscode-icon">VS</span>';
        } else {
            iconHtml = '<span class="command-icon process-icon">PROC</span>';
        }
        
        return `<div class="command-with-icon">
            ${iconHtml} 
            <div class="command-details">
                <span class="command-text">${command}</span>
                <span class="command-path">${path}</span>
            </div>
        </div>`;
    }
    
    /**
     * Generate a preview thumbnail for a process
     * @param {Object} process - Process object
     * @returns {string} HTML for the preview thumbnail
     */
    generatePreviewThumbnail(process) {
        // Create metrics visualization that will be used in all previews
        const metricsHTML = `
            <div class="process-metrics">
                <div class="metric-item">
                    <div class="metric-label">CPU</div>
                    <div class="metric-value">${process.cpu.toFixed(1)}%</div>
                    <div class="metric-bar">
                        <div class="metric-fill cpu-fill" style="width: ${Math.min(process.cpu, 100)}%"></div>
                    </div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">MEM</div>
                    <div class="metric-value">${process.memory.toFixed(1)}%</div>
                    <div class="metric-bar">
                        <div class="metric-fill mem-fill" style="width: ${Math.min(process.memory, 100)}%"></div>
                    </div>
                </div>
            </div>
        `;

        // Check if this is a web service (has a port)
        if (process.port) {
            return `
                <div class="web-service-preview">
                    <div class="preview-header">
                        <span class="preview-title">Web Service on Port ${process.port}</span>
                    </div>
                    <div class="preview-content">
                        <div class="port-badge">:${process.port}</div>
                        ${metricsHTML}
                    </div>
                </div>
            `;
        }

        // Check if this is a text file
        const command = process.command || '';
        if (command.match(/\.(txt|md|log|json|js|py|html|css)$/i)) {
            const fileType = command.split('.').pop().toLowerCase();
            let fileContent = '';
            
            try {
                if (this.fileSystemManager) {
                    fileContent = this.fileSystemManager.getFileContent(command);
                    
                    // Handle HTML content differently
                    if (fileType === 'html') {
                        return `
                            <div class="html-preview">
<!--                                <div class="preview-header">-->
<!--                                    <span class="preview-title">HTML Preview</span>-->
<!--                                </div>-->
                                <iframe srcdoc="${fileContent.replace(/"/g, '&quot;')}" style="width:100%; height:70%; transform: scale(0.2); transform-origin: 0 0; border: none;"></iframe>
                                ${metricsHTML}
                            </div>
                        `;
                    }
                    
                    // For code files, show syntax highlighted preview
                    if (['js', 'py', 'css', 'json'].includes(fileType)) {
                        return `
                            <div class="code-preview">
                                <div class="preview-header">
                                    <span class="preview-title">${fileType.toUpperCase()} File</span>
                                </div>
                                <pre class="code-content ${fileType}-content">${fileContent.substring(0, 100)}${fileContent.length > 100 ? '...' : ''}</pre>
                                ${metricsHTML}
                            </div>
                        `;
                    }
                    
                    // For other text files
                    return `
                        <div class="text-preview">
<!--                            <div class="preview-header">-->
<!--                                <span class="preview-title">Text File</span>-->
<!--                            </div>-->
                            <div class="text-content">${fileContent.substring(0, 100)}${fileContent.length > 100 ? '...' : ''}</div>
                            ${metricsHTML}
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Error generating preview for file:', error);
            }
        }

        // Generate command icon for use in thumbnails
        const commandIcon = this.generateCommandWithIcon(process);

        // Default generic preview
        return `
            <div class="generic-preview">
<!--                <div class="preview-header">-->
<!--                    <span class="preview-title"></span>-->
<!--                </div>-->
                <div class="preview-content">
                    <div class="command-display">${commandIcon}</div>
                    ${metricsHTML}
                </div>
            </div>
        `;
    }
    
    /**
     * Show process preview
     * @param {number} pid - Process ID
     * @param {Event} event - Click event
     */
    showProcessPreview(pid, event) {
        if (event) {
            event.stopPropagation();
        }
        
        const process = this.processManager.getProcessByPid(pid);
        if (!process) return;
        
        const overlay = document.getElementById('preview-overlay');
        const title = document.getElementById('preview-title');
        const body = document.getElementById('preview-body');
        
        if (!overlay || !title || !body) return;
        
        title.textContent = `Process Preview: ${process.command} (PID: ${process.pid})`;
        
        // Calculate additional information
        const uptime = this.formatTime(process.time);
        const memoryUsage = (process.memory * 100).toFixed(2) + '%';
        const cpuUsage = (process.cpu * 100).toFixed(2) + '%';
        const status = process.transparency < 0.8 ? 'Background Process' : 'Active Process';
        const startTime = new Date(Date.now() - process.time * 1000).toLocaleString();
        
        // Generate preview content based on process type
        if (process.file) {
            // Get file content from fileSystemManager if available, otherwise use local method
            const content = this.fileSystemManager ? 
                this.fileSystemManager.getFileContent(process.file) : 
                this.getFileContent(process.file);
            if (content) {
                const fileExtension = process.file.split('.').pop();
                
                if (fileExtension === 'html') {
                    body.innerHTML = `
                        <div class="preview-info-section">
                            <h3>HTML Preview</h3>
                            <div class="preview-iframe-container">
                                <iframe srcdoc="${this.escapeHTML(content)}"></iframe>
                            </div>
                        </div>
                        <div class="preview-info-section">
                            <h3>Source Code</h3>
                            <pre><code>${this.escapeHTML(content)}</code></pre>
                        </div>
                    `;
                } else if (fileExtension === 'js' || fileExtension === 'css' || fileExtension === 'json' || fileExtension === 'sh') {
                    body.innerHTML = `
                        <div class="preview-info-section">
                            <h3>${fileExtension.toUpperCase()} File Preview</h3>
                            <pre><code>${this.escapeHTML(content)}</code></pre>
                        </div>
                    `;
                }
            }
        } else {
            // Show process info for non-file processes
            
            // Create a visual representation of the process
            const cpuBarWidth = Math.min(100, process.cpu * 100);
            const memBarWidth = Math.min(100, process.memory * 100);
            const cpuBar = `<div class="preview-bar"><div class="preview-bar-fill" style="width: ${cpuBarWidth}%"></div></div>`;
            const memBar = `<div class="preview-bar"><div class="preview-bar-fill" style="width: ${memBarWidth}%"></div></div>`;
            
            body.innerHTML = `
                <div class="preview-info-section">
                    <h3>Process Information</h3>
                    <div class="preview-info-row"><span class="preview-info-label">PID:</span> <span>${process.pid}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Command:</span> <span>${process.command}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">User:</span> <span>${process.user}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">CPU:</span> <span>${cpuUsage} ${cpuBar}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Memory:</span> <span>${memoryUsage} ${memBar}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Uptime:</span> <span>${uptime}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Started:</span> <span>${startTime}</span></div>
                    <div class="preview-info-row"><span class="preview-info-label">Status:</span> <span>${status}</span></div>
                </div>
                <div class="preview-info-section">
                    <h3>Process Visualization</h3>
                    <div class="process-visualization">
                        <div class="process-icon">${process.service ? process.service.toUpperCase() : 'PROC'}</div>
                        <div class="process-details">
                            <div class="process-name">${process.command}</div>
                            <div class="process-stats">
                                <div class="stat-item">CPU: ${cpuUsage}</div>
                                <div class="stat-item">MEM: ${memoryUsage}</div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        overlay.classList.add('show');
        this.previewVisible = true;
    }
    
    /**
     * Close the process preview
     */
    closePreview() {
        const overlay = document.getElementById('preview-overlay');
        if (overlay) {
            overlay.classList.remove('show');
        }
        this.previewVisible = false;
    }
    
    /**
     * Toggle kill options dropdown
     * @param {number} pid - Process ID
     */
    toggleKillOptions(pid) {
        const dropdown = document.getElementById(`dropdown-${pid}`);
        if (dropdown) {
            // Close all other dropdowns first
            document.querySelectorAll('.kill-dropdown').forEach(d => {
                if (d.id !== `dropdown-${pid}`) {
                    d.classList.remove('show');
                }
            });
            
            // Toggle this dropdown
            dropdown.classList.toggle('show');
            
            // Add a click outside listener to close the dropdown
            const closeListener = (e) => {
                if (!e.target.closest('.kill-dropdown') && 
                    !e.target.closest('.kill-button') && 
                    !e.target.closest('.more-button')) {
                    dropdown.classList.remove('show');
                    document.removeEventListener('click', closeListener);
                }
            };
            
            document.addEventListener('click', closeListener);
        }
    }
    
    /**
     * Select a process
     * @param {number} pid - Process ID
     */
    selectProcess(pid) {
        this.processManager.selectedPid = pid;
        
        // Update selected PID display
        const selectedPidElement = document.getElementById('selected-pid');
        if (selectedPidElement) {
            selectedPidElement.textContent = pid;
        }
        
        // Remove previous selection
        document.querySelectorAll('.process-row').forEach(r => {
            r.style.background = '';
        });
        
        // Highlight selected row
        const row = document.querySelector(`.process-row[data-pid="${pid}"]`);
        if (row) {
            row.style.background = 'rgba(0, 255, 255, 0.1)';
        }
    }
    
    /**
     * Format time string
     * @param {string} timeString - Time string (HH:MM:SS)
     * @returns {string} Formatted time string
     */
    formatTime(timeString) {
        if (!timeString) return '00:00:00';
        return timeString;
    }
    
    /**
     * Get file content from file system
     * @param {string} path - File path
     * @returns {string} File content or null if not found
     */
    getFileContent(path) {
        // In a real application, this would fetch the file content from an API
        // For now, we'll return some dummy content based on the file extension
        if (path.endsWith('.html')) {
            return '<!DOCTYPE html><html><head><title>Sample HTML</title></head><body><h1>Sample HTML File</h1><p>This is a sample HTML file content.</p></body></html>';
        } else if (path.endsWith('.js')) {
            return '// Sample JavaScript file\nfunction hello() {\n  console.log("Hello, world!");\n}\n\nhello();';
        } else if (path.endsWith('.css')) {
            return '/* Sample CSS file */\nbody {\n  font-family: Arial, sans-serif;\n  margin: 0;\n  padding: 20px;\n}';
        } else if (path.endsWith('.json')) {
            return '{\n  "name": "sample",\n  "version": "1.0.0",\n  "description": "Sample JSON file"\n}';
        } else {
            return null;
        }
    }
    
    /**
     * Escape HTML special characters
     * @param {string} html - HTML string
     * @returns {string} Escaped HTML string
     */
    escapeHTML(html) {
        if (!html) return '';
        return html
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
}
