![webtask-logo.svg](webtask-logo.svg)

# webtask 🖥️

[webtask](https://pypi.org/project/webtask/) package to start web top version in browser, [kill] like a pro!


A modern, web-based system monitor inspired by htop with advanced file browsing, process transparency layers, and miniature file previews. Monitor your system processes through a sleek terminal-style web interface with real-time updates and comprehensive process management capabilities.


## ✨ Features

### 🔄 **Real-time Process Monitoring**
- Live CPU and memory usage tracking with color-coded indicators
- Process hierarchy visualization with parent-child relationships
- Advanced transparency layers showing process importance levels
- Interactive process selection and detailed information modals

### 🗂️ **Integrated File Browser**
- Complete virtual file system navigation (/bin, /etc, /var, /usr)
- Real file content preview with syntax highlighting
- Directory breadcrumb navigation
- File type recognition with appropriate icons

### 🔍 **Miniature Process Previews**
- **Bash Scripts**: Terminal-style preview with actual script content
- **HTML Web Pages**: Rendered at 10% scale showing live webpage content
- **Service Files**: Status indicators with configuration previews
- **Port Services**: Connection information and service details

### 🎯 **Advanced Process Management**
- Kill by PID, service name, port number, or username
- Multiple signal types (SIGTERM, SIGKILL, SIGINT, SIGHUP, SIGUSR1, SIGUSR2)
- Bulk operations on filtered processes
- Process dependency tracking

### 👁️ **Transparency System**
- **Kernel Processes**: 20% opacity (most background)
- **System Processes**: 30% opacity
- **Background Services**: 50% opacity
- **User Services**: 70% opacity
- **User Applications**: 90% opacity (most visible)

### ⌨️ **Keyboard Shortcuts**
| Key | Action |
|-----|--------|
| `F1` | Toggle advanced controls |
| `F2` | Open file browser |
| `F5` | Toggle tree view |
| `F6` | Change sort order |
| `F9` | Kill selected process |
| `F10` or `q` | Quit webtask |
| `ESC` | Close modals/dropdowns |

## 🚀 Quick Start


![webtask-grid.png](webtask-grid.png)

### Installation

```bash
pip install webtask
```

### Usage

Simply run the command to start webtask:

```bash
webtask
```

This will:
1. Start a local web server on `http://localhost:8000`
2. Automatically open webtask in your default browser
3. Begin real-time system monitoring with file browser capabilities

### Advanced Usage

```bash
# Custom host and port
webtask --host 0.0.0.0 --port 9000

# Disable auto-browser opening
webtask --no-browser

# Check version
webtask --version
```
### Alternative Installation

Using Poetry (for development):

```bash
git clone https://github.com/devopsterminal/webtask.git
cd webtask
poetry install
poetry run webtask
```

## 🎨 Interface Overview

### **System Stats Header**
- Real-time CPU and memory usage bars with gradient indicators
- System load average and uptime counter
- Color-coded resource utilization

### **Advanced Controls Panel** (F1)
- Kill by PID, service name, port, or user
- Signal type selection for graceful or forced termination
- Bulk operations on filtered processes

### **Process List with Previews**
- **PID**: Process identifier with hierarchy indicators
- **USER**: Process owner with permission levels
- **CPU%/MEM%**: Resource usage with visual highlighting
- **PORT**: Network port information with service detection
- **COMMAND**: Full command line with truncation
- **PREVIEW**: Miniature file/service preview thumbnail
- **ACTION**: Advanced kill options with signal selection

### **File Browser** (F2)
- Navigate through system directories
- View actual file content with syntax highlighting
- File type recognition and appropriate previews
- Breadcrumb navigation for easy directory traversal

## 🛠️ Architecture

### **Modular Design**
```
webtask/static/
├── index.html          # Main HTML structure
├── styles.css          # Core styling and responsive design
├── webtask.js          # Main application logic
├── process-data.js    # Process simulation and data engine
├── file-system.js     # Virtual file system implementation
├── file-icons.css     # File type styling and icons
├── config.json        # Application configuration
└── manifest.json      # Progressive Web App manifest
```

### **Process Transparency Logic**
The transparency system helps identify process importance:
- **System/Kernel**: Highly transparent (20-30%) - critical but background
- **Services**: Moderately transparent (50-70%) - important but service-level
- **Applications**: Least transparent (90%) - direct user interaction

### **File Preview System**
- **HTML Files**: Rendered using iframe with 10% CSS transform scale
- **Script Files**: Syntax-highlighted code preview with line numbers
- **Config Files**: Structured display with key-value highlighting
- **Log Files**: Real-time log tail with color coding

## 🔧 Configuration

WebTop can be configured through `config.json`:

```json
{
  "webtop": {
    "transparency": {
      "system_processes": 0.3,
      "user_processes": 0.9
    },
    "preview": {
      "html_scale": 0.1,
      "thumbnail_size": {"width": 60, "height": 40}
    },
    "process_monitor": {
      "update_interval": 2000,
      "max_processes": 100
    }
  }
}
```

## 🧪 Development

### **Requirements**
- Python 3.7+
- Poetry (for dependency management)
- Modern web browser with ES6+ support

### **Setup**
```bash
git clone https://github.com/devopsterminal/webtop.git
cd webtop
poetry install
poetry run webtop
```

### **Running Tests**
```bash
poetry run pytest --cov=webtop
```

### **Code Quality**
```bash
poetry run black webtop tests     # Format code
poetry run flake8 webtop tests    # Lint code
poetry run mypy webtop             # Type checking
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### **Development Workflow**
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make changes and add tests
4. Run the test suite (`poetry run pytest`)
5. Format code (`poetry run black .`)
6. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
7. Push to the branch (`git push origin feature/AmazingFeature`)
8. Open a Pull Request

### **Feature Ideas**
- Real system integration (replace simulation)
- Docker container monitoring
- Network connection visualization
- Custom process grouping
- Export capabilities for system snapshots
- Plugin system for custom metrics

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the excellent [htop](https://htop.dev/) system monitor
- Built with modern web technologies for cross-platform compatibility
- File system design inspired by Unix/Linux directory structures

## 📊 Technical Specifications

### **Browser Compatibility**
- Chrome/Chromium 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### **Performance**
- Handles 100+ processes efficiently
- 2-second update intervals
- Responsive design for 800px+ screens
- Progressive Web App capabilities

### **Security**
- No external dependencies for frontend
- Local-only operation (no data transmission)
- Read-only file system simulation
- Process operations are simulated (safe for demonstration)

---

Made with ❤️ for system administrators and developers who love comprehensive, visual tools.

**Version 2.0.0** - Now with file browsing and transparency layers!

### webtask-2


#### List
![webtask-list.png](webtask-list.png)




### webtask-1
![webtask-1.png](webtask-1.png)