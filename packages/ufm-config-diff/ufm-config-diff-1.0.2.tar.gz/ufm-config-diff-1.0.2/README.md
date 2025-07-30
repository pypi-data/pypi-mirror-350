# UFM Configuration Differentiator Tool

[![PyPI version](https://badge.fury.io/py/ufm-config-diff.svg)](https://badge.fury.io/py/ufm-config-diff)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful, production-ready tool to compare UFM (Unified Fabric Manager) configurations between two NVIDIA Docker images with advanced interactive HTML reports, table sorting/filtering, and email notifications.

## 🚀 Features

### Core Functionality
- **Docker Image Comparison**: Compare UFM configurations between two Docker images
- **Automatic Version Detection**: Extract and compare UFM, SHARP, MFT, and OpenSM versions
- **Configuration Analysis**: Identify differences in 5+ configuration files (gv.cfg, opensm.conf, sharp_am.cfg, mft.conf, etc.)
- **Smart Version Ordering**: Automatically displays higher version on the right for easier comparison

### Interactive HTML Reports
- **📊 Advanced Table Sorting**: Click column headers to sort ascending/descending
- **🔍 Real-time Filtering**: Search across all table content with instant results
- **🏷️ Status-based Filters**: Filter by Modified/New Parameter/Deleted Parameter
- **🎨 Color-coded Status**: Visual indicators for different change types
- **📱 Responsive Design**: Works perfectly on desktop and mobile devices
- **🖨️ Print-friendly**: Clean printing with hidden controls

### Professional Features
- **📧 Email Reports**: Send HTML reports with version comparison tables
- **⚡ Auto-yes Mode**: Non-interactive mode for automation and CI/CD
- **🔧 Network Interface Support**: Configure fabric and management interfaces
- **📁 Results Persistence**: Save configuration files for future reference
- **🎯 Zero External Dependencies**: Self-contained JavaScript functionality

## 📦 Installation

### Install from PyPI

#### Method 1: Using pipx (Recommended for CLI tools)
```bash
# Install pipx if not available
sudo apt install pipx  # On Ubuntu/Debian
# or
brew install pipx      # On macOS

# Install ufm-config-diff
pipx install ufm-config-diff
```

#### Method 2: Using virtual environment (Recommended for development)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install ufm-config-diff
```

#### Method 3: System-wide installation (Advanced users)
```bash
# For systems with externally-managed-environment restrictions
pip install ufm-config-diff --break-system-packages

# Standard installation (older Python versions)
pip install ufm-config-diff
```

### Install from Source
```bash
git clone https://github.com/Mellanox/ufm-config-diff.git
cd ufm-config-diff

# Using virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install .

# Or system-wide (if needed)
pip install . --break-system-packages
```

### Development Installation
```bash
git clone https://github.com/Mellanox/ufm-config-diff.git
cd ufm-config-diff

# Using virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Or system-wide (if needed)
pip install -e . --break-system-packages
```

## 🔧 Package Management

### Upgrade to Latest Version
```bash
pip install --upgrade ufm-config-diff
```

### Check Current Version
```bash
pip show ufm-config-diff
```

### Uninstall
```bash
pip uninstall ufm-config-diff
```

## 📋 Prerequisites

- **Python**: 3.6 or higher
- **Docker**: Installed and running
- **System Access**: Root/sudo privileges for Docker operations
- **Network Ports**: Free ports required by UFM (80, 443, 8000, 6306, 8005, 8888, 2022)
- **InfiniBand Interface**: Configured with IP address and in "up" state (if comparing IB configurations)

## 🎯 Usage Examples

### Basic Usage
```bash
# Compare two UFM Docker images
ufm-config-diff old_image.tar.gz new_image.tar.gz license_file.lic

# Example with real files
ufm-config-diff ufm_6.20.0-1.ubuntu22.x86_64-docker.img.gz \
                ufm_6.21.0-8.ubuntu22.x86_64-docker.img.gz \
                nvidia-ufm-enterprise-evaluation.lic
```

### Advanced Usage
```bash
# With network interface configuration
ufm-config-diff old_image.tar.gz new_image.tar.gz license_file.lic \
                --fabric-interface ib0 \
                --mgmt-interface eth0

# With custom output file and timestamp
ufm-config-diff old_image.tar.gz new_image.tar.gz license_file.lic \
                ufm_comparison_report_$(date +%Y%m%d_%H%M%S).html

# Non-interactive mode for automation
ufm-config-diff old_image.tar.gz new_image.tar.gz license_file.lic \
                --yes

# With email notification
ufm-config-diff old_image.tar.gz new_image.tar.gz license_file.lic \
                --email admin@company.com
```

### Using the Standalone Report Generator
```bash
# Generate report from existing configuration files
python -m ufm_config_diff.create_simple_table_report
```

## 📊 Interactive HTML Report Features

The generated HTML reports include:

### 🔍 **Filtering & Search**
- **Text Search**: Type in the search box to filter across all content
- **Status Filters**: Click buttons to show only Modified/New/Deleted parameters
- **Clear Filters**: Reset all filters with one click

### 📈 **Sorting**
- **Column Headers**: Click any column header to sort
- **Visual Indicators**: ↑ (ascending) / ↓ (descending) arrows
- **Smart Status Sorting**: Modified → New → Deleted order

### 🎨 **Visual Design**
- **Color-coded Rows**: 
  - 🟡 Yellow: Modified parameters
  - 🟢 Green: New parameters added
  - 🔴 Red: Parameters deleted
- **Professional Styling**: NVIDIA-branded design
- **Responsive Layout**: Adapts to screen size

### 📧 **Email Integration**
- **HTML Email Body**: Includes version comparison table
- **Professional Formatting**: Clean, corporate-style emails
- **Attachment Support**: Full HTML report attached

## 🔧 Configuration Files Analyzed

| File | Description | Version Extraction |
|------|-------------|-------------------|
| `gv.cfg` | UFM Global View configuration | ✅ |
| `opensm.conf` | OpenSM subnet manager configuration | ✅ |
| `sharp_am.cfg` | SHARP aggregation manager configuration | ✅ |
| `mft.conf` | Mellanox Firmware Tools configuration | ✅ |
| `ufm_version` | UFM version information | ✅ |

## 📁 Output Structure

```
results/
├── old_configs/           # Server 1 configuration files
│   ├── gv.cfg
│   ├── opensm.conf
│   ├── sharp_am.cfg
│   ├── mft.conf
│   └── ufm_version
├── new_configs/           # Server 2 configuration files
│   └── [same files]
├── version_comparison.md  # Human-readable version report
├── version_comparison.json # Machine-readable version data
└── ufm_comparison_report_YYYYMMDD_HHMMSS.html # Interactive report
```

## 🚨 Troubleshooting

### Common Issues

**Externally-Managed-Environment Error**
```bash
# Error: externally-managed-environment
# Solution 1: Use pipx (recommended)
sudo apt install pipx
pipx install ufm-config-diff

# Solution 2: Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install ufm-config-diff

# Solution 3: Override system protection (advanced users only)
pip install ufm-config-diff --break-system-packages
```

**Docker Permission Denied**
```bash
sudo usermod -aG docker $USER
# Log out and log back in
```

**Port Already in Use**
```bash
# Check what's using UFM ports
sudo netstat -tulpn | grep -E ':(80|443|8000|6306|8005|8888|2022)\s'
```

**UFM Already Installed**
```bash
# The tool will automatically detect and offer to uninstall
# Or use --yes flag for automatic handling
ufm-config-diff old.gz new.gz license.lic --yes
```

**Email Not Sending**
```bash
# Set SMTP server environment variable
export SMTP_SERVER=your-smtp-server.com
ufm-config-diff old.gz new.gz license.lic --email user@company.com
```

**Command Not Found After Installation**
```bash
# If installed with pipx, ensure pipx bin directory is in PATH
pipx ensurepath

# If installed in virtual environment, make sure it's activated
source venv/bin/activate

# If installed system-wide, try:
which ufm-config-diff
```

## 🔄 Version History

### v1.0.0 (Latest)
- ✅ Interactive table sorting and filtering
- ✅ Black status column text for better readability
- ✅ Enhanced email reports with version comparison
- ✅ Improved MFT version extraction
- ✅ Font consistency across all tables
- ✅ Professional timestamped report filenames
- ✅ Zero external dependencies

### v0.2.0
- Basic UFM configuration comparison
- HTML report generation
- Docker image support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Mellanox/ufm-config-diff/issues)
- **Documentation**: [GitHub Wiki](https://github.com/Mellanox/ufm-config-diff/wiki)
- **Email**: support@nvidia.com

## 🏢 About NVIDIA

This tool is developed and maintained by NVIDIA for the InfiniBand and Ethernet networking community.

---

**Made with ❤️ by NVIDIA** 