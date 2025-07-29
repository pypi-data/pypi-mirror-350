/**
 * File System Manager Module
 * Handles file system operations and virtual file system
 */
class FileSystemManager {
    constructor() {
        this.fileSystem = {};
        this.currentPath = '/';
    }
    
    /**
     * Initialize the virtual file system
     */
    initializeFileSystem() {
        this.fileSystem = {
            '/': {
                type: 'directory',
                children: {
                    'bin': { type: 'directory', children: {
                        'bash': { type: 'executable', size: 1234567, content: '#!/bin/bash\n# Bash shell executable\n# System shell program' },
                        'node': { type: 'executable', size: 45678901, content: '#!/usr/bin/env node\n// Node.js runtime executable' },
                        'python3': { type: 'executable', size: 23456789, content: '#!/usr/bin/python3\n# Python 3 interpreter' }
                    }},
                    'etc': { type: 'directory', children: {
                        'nginx': { type: 'directory', children: {
                            'nginx.conf': { type: 'config', size: 2048, content: 'server {\n    listen 80;\n    server_name localhost;\n    location / {\n        root /var/www/html;\n    }\n}' }
                        }},
                        'systemd': { type: 'directory', children: {
                            'system': { type: 'directory', children: {
                                'nginx.service': { type: 'service', size: 512, content: '[Unit]\nDescription=The nginx HTTP and reverse proxy server\n[Service]\nType=forking\nExecStart=/usr/sbin/nginx\n[Install]\nWantedBy=multi-user.target' }
                            }}
                        }}
                    }},
                    'var': { type: 'directory', children: {
                        'www': { type: 'directory', children: {
                            'html': { type: 'directory', children: {
                                'index.html': { type: 'html', size: 1024, content: '<!DOCTYPE html>\n<html>\n<head>\n    <title>Welcome to nginx!</title>\n    <style>\n        body { font-family: Arial; background: #f0f0f0; }\n        .container { max-width: 800px; margin: 50px auto; padding: 20px; }\n        h1 { color: #333; text-align: center; }\n    </style>\n</head>\n<body>\n    <div class="container">\n        <h1>Welcome to nginx!</h1>\n        <p>If you can see this page, the nginx web server is successfully installed and working.</p>\n    </div>\n</body>\n</html>' },
                                'app.js': { type: 'script', size: 856, content: 'const express = require(\'express\');\nconst app = express();\nconst port = 3000;\n\napp.get(\'/\', (req, res) => {\n    res.send(\'Hello World from Node.js!\');\n});\n\napp.listen(port, () => {\n    console.log(`Server running at http://localhost:${port}`);\n});' }
                            }}
                        }}
                    }},
                    'home': { type: 'directory', children: {
                        'user': { type: 'directory', children: {
                            'documents': { type: 'directory', children: {
                                'notes.txt': { type: 'text', size: 256, content: 'Important system notes:\n1. Remember to update the server weekly\n2. Check logs for any suspicious activity\n3. Backup the database nightly' }
                            }},
                            'projects': { type: 'directory', children: {
                                'webapp': { type: 'directory', children: {
                                    'index.js': { type: 'script', size: 1024, content: 'const http = require(\'http\');\n\nconst server = http.createServer((req, res) => {\n    res.statusCode = 200;\n    res.setHeader(\'Content-Type\', \'text/plain\');\n    res.end(\'Hello World\\n\');\n});\n\nserver.listen(8080, \'localhost\', () => {\n    console.log(\'Server running at http://localhost:8080/\');\n});' },
                                    'package.json': { type: 'json', size: 512, content: '{\n  "name": "webapp",\n  "version": "1.0.0",\n  "description": "A simple web application",\n  "main": "index.js",\n  "scripts": {\n    "start": "node index.js"\n  },\n  "dependencies": {\n    "express": "^4.17.1"\n  }\n}' }
                                }}
                            }}
                        }}
                    }}
                }
            }
        };
    }
    
    /**
     * Get file or directory at path
     * @param {string} path - Path to file or directory
     * @returns {Object} File or directory object
     */
    getItemAtPath(path) {
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
    
    /**
     * Get file content
     * @param {string} path - Path to file
     * @returns {string} File content or null if not found
     */
    getFileContent(path) {
        const file = this.getItemAtPath(path);
        if (!file || file.type === 'directory') {
            return null;
        }
        return file.content;
    }
    
    /**
     * List directory contents
     * @param {string} path - Path to directory
     * @returns {Array} Array of items in directory
     */
    listDirectory(path) {
        const dir = this.getItemAtPath(path);
        if (!dir || dir.type !== 'directory') {
            return [];
        }
        
        return Object.entries(dir.children).map(([name, item]) => ({
            name,
            type: item.type,
            size: item.size || 0,
            isDirectory: item.type === 'directory'
        }));
    }
    
    /**
     * Change current directory
     * @param {string} path - Path to change to
     * @returns {boolean} Success
     */
    changeDirectory(path) {
        // Handle absolute paths
        if (path.startsWith('/')) {
            const dir = this.getItemAtPath(path);
            if (dir && dir.type === 'directory') {
                this.currentPath = path;
                return true;
            }
            return false;
        }
        
        // Handle relative paths
        if (path === '..') {
            if (this.currentPath === '/') {
                return true;
            }
            const parts = this.currentPath.split('/').filter(Boolean);
            parts.pop();
            this.currentPath = '/' + parts.join('/');
            return true;
        }
        
        // Handle current directory
        if (path === '.') {
            return true;
        }
        
        // Handle subdirectory
        const newPath = this.currentPath === '/' 
            ? `/${path}` 
            : `${this.currentPath}/${path}`;
            
        const dir = this.getItemAtPath(newPath);
        if (dir && dir.type === 'directory') {
            this.currentPath = newPath;
            return true;
        }
        
        return false;
    }
    
    /**
     * Get file size in human-readable format
     * @param {number} size - File size in bytes
     * @returns {string} Human-readable size
     */
    getHumanReadableSize(size) {
        const units = ['B', 'KB', 'MB', 'GB', 'TB'];
        let unitIndex = 0;
        let fileSize = size;
        
        while (fileSize >= 1024 && unitIndex < units.length - 1) {
            fileSize /= 1024;
            unitIndex++;
        }
        
        return `${fileSize.toFixed(1)} ${units[unitIndex]}`;
    }
}
