// Process data and simulation engine
class ProcessDataEngine {
    constructor() {
        this.processTemplates = this.initializeProcessTemplates();
        this.serviceDefinitions = this.initializeServiceDefinitions();
        this.portRegistry = this.initializePortRegistry();
    }

    initializeProcessTemplates() {
        return [
            // System Processes (High Transparency)
            {
                name: 'kernel',
                command: '[kernel]',
                user: 'root',
                type: 'kernel',
                transparency: 0.2,
                cpu_range: [0, 2],
                memory_range: [0, 5],
                ports: [],
                files: [],
                description: 'Linux kernel core process',
                children_count: [3, 8]
            },
            {
                name: 'systemd',
                command: '/sbin/init',
                user: 'root',
                type: 'system',
                transparency: 0.3,
                cpu_range: [0, 1],
                memory_range: [1, 3],
                ports: [],
                files: ['/etc/systemd/system.conf'],
                description: 'System and service manager',
                children_count: [10, 20]
            },
            {
                name: 'kthreadd',
                command: '[kthreadd]',
                user: 'root',
                type: 'kernel',
                transparency: 0.2,
                cpu_range: [0, 0.5],
                memory_range: [0, 1],
                ports: [],
                files: [],
                description: 'Kernel thread daemon',
                children_count: [5, 15]
            },

            // Network Services (Medium Transparency)
            {
                name: 'nginx',
                command: 'nginx: master process /usr/sbin/nginx',
                user: 'root',
                type: 'service',
                transparency: 0.7,
                cpu_range: [0.5, 3],
                memory_range: [2, 8],
                ports: [80, 443],
                files: ['/etc/nginx/nginx.conf', '/var/www/html/index.html'],
                description: 'HTTP and reverse proxy server',
                children_count: [2, 8]
            },
            {
                name: 'nginx-worker',
                command: 'nginx: worker process',
                user: 'www-data',
                type: 'service',
                transparency: 0.6,
                cpu_range: [1, 8],
                memory_range: [3, 12],
                ports: [80, 443],
                files: ['/var/www/html/index.html'],
                description: 'Nginx worker process',
                parent: 'nginx'
            },
            {
                name: 'apache2',
                command: '/usr/sbin/apache2 -DFOREGROUND',
                user: 'root',
                type: 'service',
                transparency: 0.7,
                cpu_range: [0.8, 4],
                memory_range: [5, 15],
                ports: [80, 443],
                files: ['/etc/apache2/apache2.conf', '/var/www/html/index.html'],
                description: 'Apache HTTP Server',
                children_count: [3, 10]
            },

            // Database Services
            {
                name: 'mysql',
                command: '/usr/sbin/mysqld',
                user: 'mysql',
                type: 'service',
                transparency: 0.8,
                cpu_range: [2, 15],
                memory_range: [10, 30],
                ports: [3306],
                files: ['/etc/mysql/mysql.conf.d/mysqld.cnf'],
                description: 'MySQL database server'
            },
            {
                name: 'postgres',
                command: '/usr/lib/postgresql/13/bin/postgres',
                user: 'postgres',
                type: 'service',
                transparency: 0.8,
                cpu_range: [1, 12],
                memory_range: [8, 25],
                ports: [5432],
                files: ['/etc/postgresql/13/main/postgresql.conf'],
                description: 'PostgreSQL database server',
                children_count: [2, 6]
            },
            {
                name: 'redis',
                command: '/usr/bin/redis-server',
                user: 'redis',
                type: 'service',
                transparency: 0.7,
                cpu_range: [0.5, 5],
                memory_range: [3, 15],
                ports: [6379],
                files: ['/etc/redis/redis.conf'],
                description: 'Redis in-memory data structure store'
            },

            // Application Processes (Low Transparency)
            {
                name: 'node-app',
                command: 'node /var/www/html/app.js',
                user: 'user',
                type: 'application',
                transparency: 0.9,
                cpu_range: [3, 20],
                memory_range: [15, 40],
                ports: [3000, 8080],
                files: ['/var/www/html/app.js', '/var/www/html/package.json'],
                description: 'Node.js application server'
            },
            {
                name: 'python-app',
                command: 'python3 /opt/app/server.py',
                user: 'user',
                type: 'application',
                transparency: 0.9,
                cpu_range: [2, 18],
                memory_range: [12, 35],
                ports: [5000, 8000],
                files: ['/opt/app/server.py', '/opt/app/requirements.txt'],
                description: 'Python web application'
            },

            // System Utilities
            {
                name: 'sshd',
                command: '/usr/sbin/sshd -D',
                user: 'root',
                type: 'service',
                transparency: 0.6,
                cpu_range: [0, 2],
                memory_range: [1, 5],
                ports: [22],
                files: ['/etc/ssh/sshd_config'],
                description: 'SSH daemon'
            },
            {
                name: 'cron',
                command: '/usr/sbin/cron -f',
                user: 'root',
                type: 'service',
                transparency: 0.5,
                cpu_range: [0, 1],
                memory_range: [0.5, 2],
                ports: [],
                files: ['/etc/crontab'],
                description: 'Cron daemon'
            },

            // Development Tools
            {
                name: 'code-server',
                command: 'node /usr/lib/code-server/out/node/entry.js',
                user: 'user',
                type: 'application',
                transparency: 0.9,
                cpu_range: [5, 25],
                memory_range: [50, 200],
                ports: [8080],
                files: [],
                description: 'VS Code Server'
            },

            // Container Services
            {
                name: 'docker',
                command: '/usr/bin/dockerd',
                user: 'root',
                type: 'service',
                transparency: 0.5,
                cpu_range: [1, 8],
                memory_range: [10, 50],
                ports: [2376],
                files: ['/etc/docker/daemon.json'],
                description: 'Docker daemon',
                children_count: [0, 5]
            },
            {
                name: 'containerd',
                command: '/usr/bin/containerd',
                user: 'root',
                type: 'service',
                transparency: 0.4,
                cpu_range: [0.5, 4],
                memory_range: [5, 20],
                ports: [],
                files: ['/etc/containerd/config.toml'],
                description: 'Container runtime'
            }
        ];
    }

    initializeServiceDefinitions() {
        return {
            'nginx': {
                status: 'active',
                enabled: true,
                uptime: '5d 12h 34m',
                restart_count: 2,
                description: 'The nginx HTTP and reverse proxy server',
                dependencies: ['network.target'],
                config_files: ['/etc/nginx/nginx.conf', '/etc/nginx/sites-enabled/default'],
                log_files: ['/var/log/nginx/access.log', '/var/log/nginx/error.log']
            },
            'mysql': {
                status: 'active',
                enabled: true,
                uptime: '12d 8h 15m',
                restart_count: 0,
                description: 'MySQL Community Server',
                dependencies: ['network.target', 'multi-user.target'],
                config_files: ['/etc/mysql/mysql.conf.d/mysqld.cnf'],
                log_files: ['/var/log/mysql/error.log']
            },
            'sshd': {
                status: 'active',
                enabled: true,
                uptime: '15d 2h 45m',
                restart_count: 1,
                description: 'OpenBSD Secure Shell server',
                dependencies: ['network.target'],
                config_files: ['/etc/ssh/sshd_config'],
                log_files: ['/var/log/auth.log']
            },
            'docker': {
                status: 'active',
                enabled: true,
                uptime: '8d 16h 22m',
                restart_count: 3,
                description: 'Docker Application Container Engine',
                dependencies: ['multi-user.target', 'containerd.service'],
                config_files: ['/etc/docker/daemon.json'],
                log_files: ['/var/log/docker.log']
            }
        };
    }

    initializePortRegistry() {
        return {
            22: { service: 'SSH', description: 'Secure Shell' },
            25: { service: 'SMTP', description: 'Simple Mail Transfer Protocol' },
            53: { service: 'DNS', description: 'Domain Name System' },
            80: { service: 'HTTP', description: 'HyperText Transfer Protocol' },
            110: { service: 'POP3', description: 'Post Office Protocol v3' },
            143: { service: 'IMAP', description: 'Internet Message Access Protocol' },
            443: { service: 'HTTPS', description: 'HTTP Secure' },
            993: { service: 'IMAPS', description: 'IMAP over SSL' },
            995: { service: 'POP3S', description: 'POP3 over SSL' },
            3000: { service: 'Node.js', description: 'Node.js Development Server' },
            3306: { service: 'MySQL', description: 'MySQL Database Server' },
            5000: { service: 'Flask', description: 'Flask Development Server' },
            5432: { service: 'PostgreSQL', description: 'PostgreSQL Database Server' },
            6379: { service: 'Redis', description: 'Redis Key-Value Store' },
            8000: { service: 'HTTP-Alt', description: 'Alternative HTTP Port' },
            8080: { service: 'HTTP-Proxy', description: 'HTTP Proxy' },
            9000: { service: 'FastCGI', description: 'FastCGI Process Manager' }
        };
    }

    generateProcess(template, pid) {
        const cpuUsage = template.cpu_range[0] + Math.random() * (template.cpu_range[1] - template.cpu_range[0]);
        const memUsage = template.memory_range[0] + Math.random() * (template.memory_range[1] - template.memory_range[0]);
        const port = template.ports.length > 0 ? template.ports[Math.floor(Math.random() * template.ports.length)] : null;
        const file = template.files.length > 0 ? template.files[Math.floor(Math.random() * template.files.length)] : null;

        return {
            pid: pid,
            name: template.name,
            command: template.command,
            user: template.user,
            type: template.type,
            cpu: cpuUsage,
            memory: memUsage,
            port: port,
            file: file,
            service: template.name,
            transparency: template.transparency,
            description: template.description,
            parent: template.parent || null,
            children: [],
            time: this.generateUptime(),
            startTime: Date.now() - Math.random() * 86400000, // Random start within last 24h
            state: 'R' // Running
        };
    }

    generateUptime() {
        const seconds = Math.floor(Math.random() * 86400); // Up to 24 hours
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    getPortInfo(port) {
        return this.portRegistry[port] || { service: 'Unknown', description: 'Unknown Service' };
    }

    getServiceInfo(serviceName) {
        return this.serviceDefinitions[serviceName] || {
            status: 'unknown',
            enabled: false,
            uptime: '0m',
            restart_count: 0,
            description: 'Unknown service'
        };
    }

    simulateProcessUpdate(process) {
        // Simulate realistic process behavior
        const variation = 0.1; // 10% variation

        // CPU usage variation
        const cpuDelta = (Math.random() - 0.5) * variation * process.cpu;
        process.cpu = Math.max(0, Math.min(100, process.cpu + cpuDelta));

        // Memory usage variation (slower changes)
        const memDelta = (Math.random() - 0.5) * variation * 0.5 * process.memory;
        process.memory = Math.max(0, Math.min(100, process.memory + memDelta));

        // Occasionally change process state
        if (Math.random() < 0.001) { // 0.1% chance
            const states = ['R', 'S', 'D', 'T'];
            process.state = states[Math.floor(Math.random() * states.length)];
        }

        return process;
    }

    generateRandomProcess(pid) {
        const commands = [
            'bash -c "while true; do echo hello; sleep 1; done"',
            'python3 -c "import time; time.sleep(3600)"',
            'node -e "setInterval(() => console.log(Date.now()), 1000)"',
            'java -jar /tmp/app.jar',
            'go run /tmp/main.go',
            'php -S localhost:8080',
            'ruby -e "loop { puts Time.now; sleep 1 }"'
        ];

        const users = ['user', 'www-data', 'nobody', 'daemon'];
        const command = commands[Math.floor(Math.random() * commands.length)];
        const user = users[Math.floor(Math.random() * users.length)];
        const port = Math.random() < 0.3 ? Math.floor(Math.random() * 9000) + 1000 : null;

        return {
            pid: pid,
            name: 'user-process',
            command: command,
            user: user,
            type: 'application',
            cpu: Math.random() * 10,
            memory: Math.random() * 15,
            port: port,
            file: null,
            service: command.split(' ')[0],
            transparency: 0.9,
            description: 'User-generated process',
            parent: null,
            children: [],
            time: this.generateUptime(),
            startTime: Date.now(),
            state: 'R'
        };
    }
}

// Export for use in main application
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProcessDataEngine;
} else {
    window.ProcessDataEngine = ProcessDataEngine;
}