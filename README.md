# TorHost - Tor Hidden Service Setup Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Tor-Hidden%20Service-red.svg" alt="Tor Service">
</p>

<p align="center">
  <b>One-command setup for Tor hidden services (onion services)</b>
</p>

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Support](#support)

## Features

- **One-command setup** - Create Tor hidden services instantly
- **Automatic Tor installation** - Detects and installs Tor if missing
- **Custom port support** - Expose any local port as an onion service
- **Secure by default** - Uses Tor v3 onion services (latest standard)
- **Cross-distro support** - Works on Debian, Ubuntu, Fedora, Arch, etc.
- **Clean output** - Minimal, professional interface
- **Troubleshooting included** - Helpful error messages and recovery steps

## Installation

### Method 1: Install from source (Recommended)

```bash
# Clone the repository
git clone https://github.com/bytebreach/torhost.git
cd torhost

# Install globally
sudo python3 setup.py install

# Or install in development mode
pip3 install -e .
```

### Method 2: Install via pip

```bash
pip3 install torhost
```

## Quick Start

1. **Start a local service** (e.g., web server on port 8080):
   ```bash
   python3 -m http.server 8080 &
   ```

2. **Create a Tor hidden service**:
   ```bash
   sudo torhost --port 8080
   ```

3. **Access your onion service**:
   - Copy the onion address shown in the output
   - Open it in Tor Browser
   - Your local service is now accessible via Tor!

## Usage

### Basic Syntax

```bash
sudo torhost [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--port PORT` | Local port to expose as onion service | `8080` |
| `--help` | Show help message | - |

### Running as a Module

If installed globally, use:
```bash
sudo torhost --port 3000
```

If not installed, use:
```bash
sudo python3 -m torhost.cli --port 3000
```

## Examples

### Example 1: Expose a web server

```bash
# Start a Python web server
python3 -m http.server 8000 &

# Create onion service for port 8000
sudo torhost --port 8000
```

### Example 2: Expose a Node.js application

```bash
# Start Node.js app on port 3000
node app.js &

# Create onion service
sudo torhost --port 3000
```

### Example 3: Expose SSH server

```bash
# Create onion service for SSH (port 22)
sudo torhost --port 22
```

### Testing Your Onion Service

```bash
# Test with curl (requires tor running)
curl --socks5-hostname localhost:9050 http://your-onion-address.onion

# Or use torsocks
torsocks curl http://your-onion-address.onion
```

## Troubleshooting

### Common Issues

#### 1. "Root privileges required"
```bash
# Always run with sudo
sudo torhost
```

#### 2. "Tor not found" on non-Debian systems
```bash
# Install Tor manually for your distribution

# Arch Linux
sudo pacman -S tor

# Fedora/RHEL
sudo dnf install tor

# OpenSUSE
sudo zypper install tor
```

#### 3. Onion address not generating
```bash
# Check Tor logs
sudo journalctl -u tor -n 50

# Check hidden service directory
sudo ls -la /var/lib/tor/hidden_service/

# Verify Tor is running
sudo systemctl status tor

# Restart Tor manually
sudo systemctl restart tor
```

#### 4. "Connection refused" when accessing onion
- Ensure your local service is running
- Check firewall settings
- Verify the port is correct
- Test locally first: `curl http://localhost:PORT`

### Log Files

- **Tor logs**: `/var/log/tor/log` or `journalctl -u tor`
- **Hidden service directory**: `/var/lib/tor/hidden_service/`
- **Configuration file**: `/etc/tor/torrc`

### Reporting Issues

Please report bugs and feature requests on the [GitHub Issues](https://github.com/bytebreach/torhost/issues) page.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/bytebreach/torhost/issues)
- **Email**: mrfidal@proton.me
- **Documentation**: [Read the docs](https://github.com/bytebreach/torhost/blob/main/README.md)

## Acknowledgments

- [The Tor Project](https://www.torproject.org/) for making online privacy possible
- Contributors and testers who help improve this tool
- The open source community for inspiration and support

---

<p align="center">
  Made by <a href="https://github.com/bytebreach">ByteBreach</a>
</p>

<p align="center">
  <sub>Use responsibly. Respect privacy.</sub>
</p>
