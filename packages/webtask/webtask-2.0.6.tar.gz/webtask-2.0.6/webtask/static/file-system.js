// Virtual file system for process file browsing
class VirtualFileSystem {
    constructor() {
        this.fileSystem = this.initializeFileSystem();
    }

    initializeFileSystem() {
        return {
            '/': {
                type: 'directory',
                size: 4096,
                modified: new Date('2025-05-22T10:00:00'),
                permissions: 'drwxr-xr-x',
                owner: 'root',
                group: 'root',
                children: {
                    'bin': this.createSystemBinDirectory(),
                    'etc': this.createEtcDirectory(),
                    'var': this.createVarDirectory(),
                    'usr': this.createUsrDirectory(),
                    'home': this.createHomeDirectory(),
                    'opt': this.createOptDirectory(),
                    'tmp': this.createTmpDirectory(),
                    'proc': this.createProcDirectory(),
                    'sys': this.createSysDirectory()
                }
            }
        };
    }

    createSystemBinDirectory() {
        return {
            type: 'directory',
            size: 4096,
            modified: new Date('2025-05-20T09:00:00'),
            permissions: 'drwxr-xr-x',
            owner: 'root',
            group: 'root',
            children: {
                'bash': {
                    type: 'executable',
                    size: 1234567,
                    modified: new Date('2025-05-15T14:30:00'),
                    permissions: '-rwxr-xr-x',
                    owner: 'root',
                    group: 'root',
                    content: `#!/bin/bash
# GNU bash, version 5.1.16(1)-release
# This is the Bourne Again SHell (bash)
# 
# Bash is an sh-compatible command language interpreter that
# executes commands read from the standard input or from a file.
# 
# Copyright (C) 2020 Free Software Foundation, Inc.
# License GPLv3+: GNU GPL version 3 or later
echo "Bash shell - version 5.1.16"
echo "Type 'help' for more information."`,
                    mime_type: 'application/x-executable'
                },
                'node': {
                    type: 'executable',
                    size: 45678901,
                    modified: new Date('2025-05-18T11:20:00'),
                    permissions: '-rwxr-xr-x',
                    owner: 'root',
                    group: 'root',
                    content: `#!/usr/bin/env node
// Node.js JavaScript runtime
// Version: v18.20.3
// 
// Node.js® is a JavaScript runtime built on Chrome's V8 JavaScript engine.
// Node.js uses an event-driven, non-blocking I/O model that makes it
// lightweight and efficient.

console.log('Node.js v18.20.3');
console.log('Usage: node [options] [V8 options] [script.js | -e "script" | -] [--] [arguments]');`,
                    mime_type: 'application/x-executable'
                },
                'python3': {
                    type: 'executable',
                    size: 23456789,
                    modified: new Date('2025-05-16T08:45:00'),
                    permissions: '-rwxr-xr-x',
                    owner: 'root',
                    group: 'root',
                    content: `#!/usr/bin/python3
# Python 3.9.2 (default, Feb 28 2021, 17:03:44)
# [GCC 10.2.1 20210110] on linux
# 
# Python is an interpreted, interactive, object-oriented programming
# language. It is often compared to Tcl, Perl, Scheme or Java.

import sys
print(f"Python {sys.version}")
print("Type help(), copyright(), credits() or license() for more information.")`,
                    mime_type: 'text/x-python'
                },
                'systemctl': {
                    type: 'executable',
                    size: 2345678,
                    modified: new Date('2025-05-14T16:00:00'),
                    permissions: '-rwxr-xr-x',
                    owner: 'root',
                    group: 'root',
                    content: `#!/bin/bash
# systemctl - Control the systemd system and service manager
# 
# systemctl [OPTIONS...] {COMMAND} ...
# 
# Query or send control commands to the systemd system manager.

echo "systemctl - systemd service control utility"
echo "Usage: systemctl [OPTIONS...] {COMMAND} ..."`,
                    mime_type: 'application/x-executable'
                }
            }
        };
    }

    createEtcDirectory() {
        return {
            type: 'directory',
            size: 4096,
            modified: new Date('2025-05-22T09:30:00'),
            permissions: 'drwxr-xr-x',
            owner: 'root',
            group: 'root',
            children: {
                'nginx': {
                    type: 'directory',
                    size: 4096,
                    modified: new Date('2025-05-21T15:00:00'),
                    permissions: 'drwxr-xr-x',
                    owner: 'root',
                    group: 'root',
                    children: {
                        'nginx.conf': {
                            type: 'config',
                            size: 2048,
                            modified: new Date('2025-05-21T15:00:00'),
                            permissions: '-rw-r--r--',
                            owner: 'root',
                            group: 'root',
                            content: `# nginx.conf - Main nginx configuration file

user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 768;
    use epoll;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/atom+xml image/svg+xml;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}`,
                            mime_type: 'text/plain'
                        },
                        'sites-available': {
                            type: 'directory',
                            size: 4096,
                            modified: new Date('2025-05-21T15:30:00'),
                            permissions: 'drwxr-xr-x',
                            owner: 'root',
                            group: 'root',
                            children: {
                                'default': {
                                    type: 'config',
                                    size: 1024,
                                    modified: new Date('2025-05-21T15:30:00'),
                                    permissions: '-rw-r--r--',
                                    owner: 'root',
                                    group: 'root',
                                    content: `# Default nginx virtual host configuration

server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \\.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
    }

    location ~ /\\.ht {
        deny all;
    }
}`,
                                    mime_type: 'text/plain'
                                }
                            }
                        }
                    }
                },
                'systemd': {
                    type: 'directory',
                    size: 4096,
                    modified: new Date('2025-05-20T12:00:00'),
                    permissions: 'drwxr-xr-x',
                    owner: 'root',
                    group: 'root',
                    children: {
                        'system': {
                            type: 'directory',
                            size: 4096,
                            modified: new Date('2025-05-20T12:00:00'),
                            permissions: 'drwxr-xr-x',
                            owner: 'root',
                            group: 'root',
                            children: {
                                'nginx.service': {
                                    type: 'service',
                                    size: 512,
                                    modified: new Date('2025-05-20T12:00:00'),
                                    permissions: '-rw-r--r--',
                                    owner: 'root',
                                    group: 'root',
                                    content: `[Unit]
Description=The nginx HTTP and reverse proxy server
Documentation=http://nginx.org/en/docs/
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t
ExecStart=/usr/sbin/nginx
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed

[Install]
WantedBy=multi-user.target`,
                                    mime_type: 'text/plain'
                                },
                                'mysql.service': {
                                    type: 'service',
                                    size: 678,
                                    modified: new Date('2025-05-19T14:20:00'),
                                    permissions: '-rw-r--r--',
                                    owner: 'root',
                                    group: 'root',
                                    content: `[Unit]
Description=MySQL Community Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target

[Service]
Type=forking
User=mysql
Group=mysql
ExecStart=/usr/sbin/mysqld --defaults-file=/etc/mysql/mysql.conf.d/mysqld.cnf --daemonize --pid-file=/run/mysqld/mysqld.pid
ExecReload=/bin/kill -HUP $MAINPID
TimeoutSec=600
Restart=on-failure
RestartPreventExitStatus=1

[Install]
WantedBy=multi-user.target`,
                                    mime_type: 'text/plain'
                                }
                            }
                        }
                    }
                },
                'hosts': {
                    type: 'config',
                    size: 158,
                    modified: new Date('2025-05-22T10:15:00'),
                    permissions: '-rw-r--r--',
                    owner: 'root',
                    group: 'root',
                    content: `127.0.0.1       localhost
127.0.1.1       webserver

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters`,
                    mime_type: 'text/plain'
                }
            }
        };
    }

    createVarDirectory() {
        return {
            type: 'directory',
            size: 4096,
            modified: new Date('2025-05-22T11:00:00'),
            permissions: 'drwxr-xr-x',
            owner: 'root',
            group: 'root',
            children: {
                'www': {
                    type: 'directory',
                    size: 4096,
                    modified: new Date('2025-05-22T10:45:00'),
                    permissions: 'drwxr-xr-x',
                    owner: 'root',
                    group: 'root',
                    children: {
                        'html': {
                            type: 'directory',
                            size: 4096,
                            modified: new Date('2025-05-22T10:45:00'),
                            permissions: 'drwxr-xr-x',
                            owner: 'www-data',
                            group: 'www-data',
                            children: {
                                'index.html': {
                                    type: 'html',
                                    size: 1024,
                                    modified: new Date('2025-05-22T10:45:00'),
                                    permissions: '-rw-r--r--',
                                    owner: 'www-data',
                                    group: 'www-data',
                                    content: `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to nginx!</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            padding: 40px;
            text-align: center;
            max-width: 600px;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }
        p {
            color: #666;
            line-height: 1.6;
            font-size: 1.1em;
        }
        .status {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            margin-top: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Welcome to nginx!</h1>
        <p>If you can see this page, the nginx web server is successfully installed and working on this system.</p>
        <p>For online documentation and support please refer to <a href="http://nginx.org/">nginx.org</a>.</p>
        <div class="status">Server Status: Online</div>
    </div>
</body>
</html>`,
                                    mime_type: 'text/html'
                                },
                                'app.js': {
                                    type: 'script',
                                    size: 856,
                                    modified: new Date('2025-05-22T09:30:00'),
                                    permissions: '-rw-r--r--',
                                    owner: 'www-data',
                                    group: 'www-data',
                                    content: `const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// Routes
app.get('/', (req, res) => {
    res.json({
        message: 'Hello World from Node.js!',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        version: process.version,
        environment: process.env.NODE_ENV || 'development'
    });
});

app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        memory: process.memoryUsage(),
        cpu: process.cpuUsage(),
        pid: process.pid
    });
});

app.get('/api/processes', (req, res) => {
    // Simulate process data
    res.json([
        { pid: 1234, name: 'node', cpu: 5.2, memory: 15.8 },
        { pid: 5678, name: 'nginx', cpu: 1.1, memory: 3.4 }
    ]);
});

// Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

// Start server
app.listen(port, () => {
    console.log(\`🚀 Server running at http://localhost:\${port}\`);
    console.log(\`📊 Health check: http://localhost:\${port}/health\`);
    console.log(\`🔧 Environment: \${process.env.NODE_ENV || 'development'}\`);
});

module.exports = app;`,
                                    mime_type: 'application/javascript'
                                },
                                'package.json': {
                                    type: 'config',
                                    size: 512,
                                    modified: new Date('2025-05-22T09:20:00'),
                                    permissions: '-rw-r--r--',
                                    owner: 'www-data',
                                    group: 'www-data',
                                    content: `{
  "name": "webtask-demo-app",
  "version": "1.0.0",
  "description": "Demo Node.js application for webtask monitoring",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js",
    "test": "jest",
    "lint": "eslint ."
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "helmet": "^7.0.0",
    "morgan": "^1.10.0"
  },
  "devDependencies": {
    "nodemon": "^2.0.22",
    "jest": "^29.5.0",
    "eslint": "^8.41.0"
  },
  "keywords": ["node", "express", "api", "webtask"],
  "author": "WebTask Demo",
  "license": "MIT"
}`,
                                    mime_type: 'application/json'
                                }
                            }
                        }
                    }
                },
                'log': {
                    type: 'directory',
                    size: 4096,
                    modified: new Date('2025-05-22T11:30:00'),
                    permissions: 'drwxr-xr-x',
                    owner: 'root',
                    group: 'root',
                    children: {
                        'nginx': {
                            type: 'directory',
                            size: 4096,
                            modified: new Date('2025-05-22T11:30:00'),
                            permissions: 'drwxr-xr-x',
                            owner: 'www-data',
                            group: 'adm',
                            children: {
                                'access.log': {
                                    type: 'log',
                                    size: 45678,
                                    modified: new Date('2025-05-22T11:30:00'),
                                    permissions: '-rw-r--r--',
                                    owner: 'www-data',
                                    group: 'adm',
                                    content: `192.168.1.100 - - [22/May/2025:10:30:45 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
192.168.1.101 - - [22/May/2025:10:31:12 +0000] "GET /app.js HTTP/1.1" 404 162 "-" "curl/7.68.0"
192.168.1.102 - - [22/May/2025:10:32:33 +0000] "POST /api/data HTTP/1.1" 200 85 "http://localhost/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
192.168.1.100 - - [22/May/2025:10:33:15 +0000] "GET /health HTTP/1.1" 200 234 "-" "Python-urllib/3.9"
192.168.1.103 - - [22/May/2025:10:34:22 +0000] "GET /favicon.ico HTTP/1.1" 404 162 "http://localhost/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
192.168.1.100 - - [22/May/2025:10:35:01 +0000] "GET /api/processes HTTP/1.1" 200 456 "-" "PostmanRuntime/7.32.2"`,
                                    mime_type: 'text/plain'
                                },
                                'error.log': {
                                    type: 'log',
                                    size: 2048,
                                    modified: new Date('2025-05-22T11:25:00'),
                                    permissions: '-rw-r--r--',
                                    owner: 'www-data',
                                    group: 'adm',
                                    content: `2025/05/22 10:00:01 [notice] 1234#1234: nginx/1.18.0 (Ubuntu)
2025/05/22 10:00:01 [notice] 1234#1234: built by gcc 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)
2025/05/22 10:00:01 [notice] 1234#1234: OS: Linux 5.4.0-150-generic
2025/05/22 10:00:01 [notice] 1234#1234: getrlimit(RLIMIT_NOFILE): 1024:1024
2025/05/22 10:00:01 [notice] 1235#1235: start worker processes
2025/05/22 10:00:01 [notice] 1235#1235: start worker process 1236
2025/05/22 10:31:12 [error] 1236#1236: *1 open() "/var/www/html/app.js" failed (13: Permission denied), client: 192.168.1.101, server: _, request: "GET /app.js HTTP/1.1", host: "localhost"`,
                                    mime_type: 'text/plain'
                                }
                            }
                        }
                    }
                }
            }
        };
    }

    createOptDirectory() {
        return {
            type: 'directory',
            size: 4096,
            modified: new Date('2025-05-21T16:00:00'),
            permissions: 'drwxr-xr-x',
            owner: 'root',
            group: 'root',
            children: {
                'app': {
                    type: 'directory',
                    size: 4096,
                    modified: new Date('2025-05-21T16:00:00'),
                    permissions: 'drwxr-xr-x',
                    owner: 'user',
                    group: 'user',
                    children: {
                        'server.py': {
                            type: 'script',
                            size: 1234,
                            modified: new Date('2025-05-21T16:00:00'),
                            permissions: '-rwxr-xr-x',
                            owner: 'user',
                            group: 'user',
                            content: `#!/usr/bin/env python3
"""
Simple Python web server for demonstration
"""

import http.server
import socketserver
import json
import os
from datetime import datetime

PORT = int(os.environ.get('PORT', 5000))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'message': 'Hello from Python!',
                'timestamp': datetime.now().isoformat(),
                'server': 'Python HTTP Server',
                'version': '1.0.0'
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'healthy', 'pid': os.getpid()}
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"🐍 Python server running on port {PORT}")
        print(f"📊 Health check: http://localhost:{PORT}/health")
        httpd.serve_forever()`,
                            mime_type: 'text/x-python'
                        },
                        'requirements.txt': {
                            type: 'config',
                            size: 156,
                            modified: new Date('2025-05-21T15:45:00'),
                            permissions: '-rw-r--r--',
                            owner: 'user',
                            group: 'user',
                            content: `# Python dependencies for demo app
requests==2.31.0
flask==2.3.2
gunicorn==20.1.0
psutil==5.9.5
click==8.1.3`,
                            mime_type: 'text/plain'
                        }
                    }
                }
            }
        };
    }

    createUsrDirectory() {
        return {
            type: 'directory',
            size: 4096,
            modified: new Date('2025-05-20T14:00:00'),
            permissions: 'drwxr-xr-x',
            owner: 'root',
            group: 'root',
            children: {
                'local': {
                    type: 'directory',
                    size: 4096,
                    modified: new Date('2025-05-20T14:00:00'),
                    permissions: 'drwxr-xr-x',
                    owner: 'root',
                    group: 'root',
                    children: {
                        'bin': {
                            type: 'directory',
                            size: 4096,
                            modified: new Date('2025-05-20T14:00:00'),
                            permissions: 'drwxr-xr-x',
                            owner: 'root',
                            group: 'root',
                            children: {
                                'myapp': {
                                    type: 'script',
                                    size: 1234,
                                    modified: new Date('2025-05-20T14:00:00'),
                                    permissions: '-rwxr-xr-x',
                                    owner: 'user',
                                    group: 'user',
                                    content: `#!/bin/bash
# Custom application launcher script
# 
# This script sets up the environment and launches the Node.js application

echo "🚀 Starting MyApp..."

# Set environment variables
export NODE_ENV=production
export PORT=3000
export LOG_LEVEL=info

# Change to app directory
cd /var/www/html || exit 1

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the application
echo "📊 Starting Node.js application on port $PORT"
node app.js`,
                                    mime_type: 'application/x-shellscript'
                                }
                            }
                        }
                    }
                }
            }
        };
    }

    createHomeDirectory() {
        return {
            type: 'directory',
            size: 4096,
            modified: new Date('2025-05-22T09:00:00'),
            permissions: 'drwxr-xr-x',
            owner: 'root',
            group: 'root',
            children: {
                'user': {
                    type: 'directory',
                    size: 4096,
                    modified: new Date('2025-05-22T09:00:00'),
                    permissions: 'drwxr-xr-x',
                    owner: 'user',
                    group: 'user',
                    children: {
                        '.bashrc': {
                            type: 'config',
                            size: 3456,
                            modified: new Date('2025-05-22T09:00:00'),
                            permissions: '-rw-r--r--',
                            owner: 'user',
                            group: 'user',
                            content: `# ~/.bashrc: executed by bash(1) for non-login shells.

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# History configuration
HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=2000

# Append to the history file, don't overwrite it
shopt -s histappend

# Check the window size after each command
shopt -s checkwinsize

# Colored prompt
PS1='\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ '

# Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias grep='grep --color=auto'

# Custom functions
function weather() {
    curl -s "wttr.in/$1"
}

function ports() {
    netstat -tulpn | grep LISTEN
}

echo "Welcome to WebTask Demo System!"`,
                            mime_type: 'text/plain'
                        }
                    }
                }
            }
        };
    }

    createTmpDirectory() {
        return {
            type: 'directory',
            size: 4096,
            modified: new Date('2025-05-22T11:45:00'),
            permissions: 'drwxrwxrwt',
            owner: 'root',
            group: 'root',
            children: {}
        };
    }

    createProcDirectory() {
        return {
            type: 'directory',
            size: 0,
            modified: new Date(),
            permissions: 'dr-xr-xr-x',
            owner: 'root',
            group: 'root',
            children: {
                'version': {
                    type: 'proc',
                    size: 0,
                    modified: new Date(),
                    permissions: '-r--r--r--',
                    owner: 'root',
                    group: 'root',
                    content: 'Linux version 5.4.0-150-generic (buildd@lcy02-amd64-013) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)) #167-Ubuntu SMP Wed May 15 13:04:26 UTC 2025',
                    mime_type: 'text/plain'
                },
                'cpuinfo': {
                    type: 'proc',
                    size: 0,
                    modified: new Date(),
                    permissions: '-r--r--r--',
                    owner: 'root',
                    group: 'root',
                    content: `processor\t: 0
vendor_id\t: GenuineIntel
cpu family\t: 6
model\t\t: 142
model name\t: Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
stepping\t: 10
microcode\t: 0xf0
cpu MHz\t\t: 1800.000
cache size\t: 8192 KB
physical id\t: 0
siblings\t: 8
core id\t\t: 0
cpu cores\t: 4
flags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov`,
                    mime_type: 'text/plain'
                }
            }
        };
    }

    createSysDirectory() {
        return {
            type: 'directory',
            size: 0,
            modified: new Date(),
            permissions: 'dr-xr-xr-x',
            owner: 'root',
            group: 'root',
            children: {}
        };
    }

    // Utility methods
    getFileAtPath(path) {
        const parts = path.split('/').filter(Boolean);
        let current = this.fileSystem['/'];

        for (const part of parts) {
            if (current.children && current.children[part]) {
                current = current.children[part];
            } else {
                return null;
            }
        }

        return current;
    }

    formatFileSize(bytes) {
        const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
        if (bytes === 0) return '0 B';
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    }

    getFileType(filename) {
        const extension = filename.split('.').pop().toLowerCase();
        const typeMap = {
            'html': 'text/html',
            'js': 'application/javascript',
            'py': 'text/x-python',
            'sh': 'application/x-shellscript',
            'conf': 'text/plain',
            'log': 'text/plain',
            'json': 'application/json',
            'txt': 'text/plain',
            'service': 'text/plain'
        };
        return typeMap[extension] || 'application/octet-stream';
    }

    isExecutable(file) {
        return file.permissions && file.permissions.includes('x');
    }

    isDirectory(file) {
        return file.type === 'directory';
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VirtualFileSystem;
} else {
    window.VirtualFileSystem = VirtualFileSystem;
}