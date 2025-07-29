"""
webtask HTTP Server
"""

import json
import psutil
import socket
import time
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class WebTaskHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for webtask"""
    
    # Define API routes as a class variable to ensure they're available immediately
    api_routes = {}
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Initialize the routes before calling parent's __init__
        self.api_routes = {
            '/api/processes': self.handle_processes,
            '/api/system': self.handle_system_info,
            '/api/services': self.handle_services,
            '/api/disk': self.handle_disk_usage,
        }
        static_dir = Path(__file__).parent / "static"
        super().__init__(*args, directory=str(static_dir), **kwargs)
        
    def do_GET(self) -> None:
        """Handle GET requests, routing API calls or serving static files."""
        if self.path in self.api_routes:
            self.api_routes[self.path]()
        else:
            # Default to serving static files
            super().do_GET()
            
    def send_json_response(self, data: Union[Dict, List], status_code: int = 200) -> None:
        """Send a JSON response with the given data and status code."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def end_headers(self) -> None:
        self.send_header(
            'Cache-Control',
            'no-cache, no-store, must-revalidate'
        )
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def handle_processes(self) -> None:
        """Return a list of running processes."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'user': proc.info['username'],
                    'cpu': proc.info['cpu_percent'],
                    'memory': proc.info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        self.send_json_response(processes)

    def handle_system_info(self) -> None:
        """Return system information."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        system_info = {
            'cpu': {
                'percent': cpu_percent,
                'cores': psutil.cpu_count(),
                'load_avg': [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            },
            'hostname': socket.gethostname(),
            'uptime': int(time.time() - psutil.boot_time())
        }
        self.send_json_response(system_info)

    def handle_services(self) -> None:
        """Return a list of running services."""
        services = []
        # This is a simplified example - you might need to adjust based on the OS
        try:
            if hasattr(psutil, 'win_service_iter'):
                for service in psutil.win_service_iter():
                    services.append({
                        'name': service.name(),
                        'display_name': service.display_name(),
                        'status': service.status()
                    })
            else:
                # Fallback for non-Windows systems
                services = [{'name': 'service1', 'status': 'running'}, 
                           {'name': 'service2', 'status': 'stopped'}]
        except Exception as e:
            services = [{'error': f'Service listing error: {str(e)}'}]
        self.send_json_response(services)

    def handle_disk_usage(self) -> None:
        """Return disk usage information."""
        partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except Exception as e:
                print(f"Error getting disk usage for {partition.mountpoint}: {e}")
        self.send_json_response(partitions)

    def log_message(self, format: str, *args: Any) -> None:
        """Override to prevent logging every request to stderr."""
        pass


class webtaskServer:
    """webtask server wrapper"""
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        open_browser: bool = True
    ) -> None:
        self.host = host
        self.port = port
        self.open_browser = open_browser
        self.server: Optional[HTTPServer] = None

    def run(self) -> None:
        try:
            self.server = HTTPServer((self.host, self.port), WebTaskHandler)
            url = f"http://{self.host}:{self.port}"
            print(f"🚀 Starting webtask server at {url}")
            print("📊 webtask is running! Press Ctrl+C to stop.")
            if self.open_browser:
                threading.Timer(1.0, lambda: webbrowser.open(url)).start()
            if self.server is not None:  # Check for None to satisfy type checker
                self.server.serve_forever()
        except OSError as e:
            if hasattr(e, 'errno') and e.errno in (48, 98):
                print(
                    f"❌ Port {self.port} is already in use. "
                    "Try a different port with --port"
                )
            else:
                raise
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        if self.server:
            print("\n🛑 Stopping webtask server...")
            self.server.shutdown()
            self.server.server_close()
