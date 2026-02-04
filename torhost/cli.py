#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import argparse
import shutil

WHITE = "\033[97m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

DEFAULT_PORT = 8080
SERVICE_NAME = "hidden_service"
WAIT_TIME = 90

def run(cmd, check=False, capture_output=True):
    if capture_output:
        return subprocess.run(
            cmd, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=check
        )
    else:
        return subprocess.run(
            cmd, shell=True,
            check=check
        )


def command_exists(cmd):
    return shutil.which(cmd) is not None


def is_termux():
    return "com.termux" in os.environ.get("PREFIX", "")


def require_sudo():
    if is_termux():
        return False
    if os.geteuid() != 0:
        print(f"{WHITE} [{RED}!{WHITE}] {RED}Root privileges required. Trying to get sudo...")
        try:
            os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
        except FileNotFoundError:
            print(f"{WHITE} [{RED}!{WHITE}] {RED}sudo not found. Continuing without root...")
            return False
        except Exception as e:
            print(f"{WHITE} [{RED}!{WHITE}] {RED}Error with sudo: {e}")
            return False
    return True


def detect_tor_user():
    if is_termux():
        return os.environ.get("USER", "tor")
    
    for user in ("debian-tor", "tor"):
        try:
            run(f"id {user}", check=False)
            return user
        except:
            continue
    
    result = run("ps aux | grep tor | grep -v grep | head -1 | awk '{print $1}'", check=False)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    
    return "tor"


def install_tor():
    if command_exists("tor"):
        print(f"{WHITE} [{GREEN}+{WHITE}] {GREEN}Tor is already installed.")
        return True

    print(f"{WHITE} [{YELLOW}+{WHITE}] {YELLOW}Tor not found. Installing...")

    if is_termux():
        result = run("pkg install tor -y", check=False)
    elif command_exists("apt"):
        if os.geteuid() == 0:
            result = run("apt update && apt install tor -y", check=False)
        else:
            result = run("sudo apt update && sudo apt install tor -y", check=False)
    elif command_exists("apt-get"):
        if os.geteuid() == 0:
            result = run("apt-get update && apt-get install tor -y", check=False)
        else:
            result = run("sudo apt-get update && sudo apt-get install tor -y", check=False)
    elif command_exists("yum"):
        if os.geteuid() == 0:
            result = run("yum install tor -y", check=False)
        else:
            result = run("sudo yum install tor -y", check=False)
    elif command_exists("dnf"):
        if os.geteuid() == 0:
            result = run("dnf install tor -y", check=False)
        else:
            result = run("sudo dnf install tor -y", check=False)
    elif command_exists("pacman"):
        if os.geteuid() == 0:
            result = run("pacman -S tor --noconfirm", check=False)
        else:
            result = run("sudo pacman -S tor --noconfirm", check=False)
    else:
        print(f"{WHITE} [{RED}!{WHITE}] {RED}Unsupported package manager. Install Tor manually.")
        return False

    if result.returncode != 0:
        print(f"{WHITE} [{RED}!{WHITE}] {RED}Failed to install Tor.")
        return False
    
    print(f"{WHITE} [{GREEN}+{WHITE}] {GREEN}Tor installed successfully.")
    return True


def restart_tor():
    if is_termux():
        run("pkill -f tor 2>/dev/null || true", check=False)
        time.sleep(2)
        run("tor 2>/dev/null &", check=False)
        time.sleep(5)
        if run("pgrep -f tor", check=False).returncode == 0:
            return True
        return False
    
    services = [
        "tor@default",
        "tor",
        "tor.service"
    ]
    
    for svc in services:
        if os.geteuid() == 0:
            result = run(f"systemctl restart {svc}", check=False)
        else:
            result = run(f"sudo systemctl restart {svc}", check=False)
        if result.returncode == 0:
            time.sleep(3)
            if os.geteuid() == 0:
                status_result = run(f"systemctl is-active {svc}", check=False)
            else:
                status_result = run(f"sudo systemctl is-active {svc}", check=False)
            if status_result.stdout.strip() == "active":
                return True
    
    run("pkill tor 2>/dev/null || true", check=False)
    time.sleep(2)
    
    result = run("tor --runasdaemon 1 2>/dev/null &", check=False)
    time.sleep(5)
    
    if run("pgrep tor", check=False).returncode == 0:
        return True
    
    return False


def check_tor_running():
    if is_termux():
        result = run("pgrep -f tor", check=False)
        return result.returncode == 0
    
    if os.geteuid() == 0:
        result = run("systemctl is-active tor 2>/dev/null || systemctl is-active tor.service 2>/dev/null || true", check=False)
    else:
        result = run("sudo systemctl is-active tor 2>/dev/null || sudo systemctl is-active tor.service 2>/dev/null || true", check=False)
    
    if result.returncode == 0 and "active" in result.stdout:
        return True
    
    result = run("pgrep -x tor", check=False)
    return result.returncode == 0


def validate_onion_address(onion):
    if not onion:
        return False
    
    onion = onion.strip()
    if len(onion) == 56 and onion.endswith(".onion"):
        return True
    
    if onion.endswith(".onion"):
        return True
    
    return False


def main():
    try:
        from torhost.banner import show_banner
        show_banner()
    except ImportError:
        print(f"{WHITE}TORHOST{WHITE}")
        print(f"{WHITE}  {CYAN}({RED}ByteBreach{CYAN}){WHITE}")
        print()

    parser = argparse.ArgumentParser(description="Set up a Tor hidden service")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, 
                       help=f"Local port to expose (default: {DEFAULT_PORT})")
    args = parser.parse_args()
    port = args.port
    
    print(f"{WHITE} [{GREEN}+{WHITE}] {GREEN}Starting Tor Hidden Service setup...")
    
    require_sudo()
    
    if not install_tor():
        print(f"{WHITE} [{RED}!{WHITE}] {RED}Cannot continue without Tor.")
        sys.exit(1)
    
    if not check_tor_running():
        if not restart_tor():
            print(f"{WHITE} [{RED}!{WHITE}] {RED}Failed to start Tor.")
            sys.exit(1)
    
    if is_termux():
        torrc = os.path.expanduser("~/../usr/etc/tor/torrc")
        tor_dir = os.path.expanduser("~/../usr/var/lib/tor")
    else:
        torrc = "/etc/tor/torrc"
        tor_dir = "/var/lib/tor"
    
    tor_user = detect_tor_user()
    
    if not tor_user:
        tor_user = "tor"
    
    hs_dir = f"{tor_dir}/{SERVICE_NAME}"
    hostname_file = f"{hs_dir}/hostname"
    
    print(f"{WHITE} [{GREEN}+{WHITE}] {GREEN}Configuring Tor hidden service...")
    
    try:
        os.makedirs(hs_dir, exist_ok=True, mode=0o700)
        if not is_termux() and os.geteuid() == 0:
            run(f"chown -R {tor_user}:{tor_user} {hs_dir}", check=True)
        run(f"chmod 700 {hs_dir}", check=True)
        run(f"chmod 755 {tor_dir}", check=True)
        
    except Exception as e:
        print(f"{WHITE} [{RED}!{WHITE}] {RED}Failed to create hidden service directory: {e}")
        sys.exit(1)
    
    lines = []
    if os.path.exists(torrc):
        try:
            with open(torrc, "r") as f:
                lines = f.readlines()
        except Exception as e:
            print(f"{WHITE} [{RED}!{WHITE}] {RED}Failed to read torrc: {e}")
            sys.exit(1)
    
    try:
        with open(torrc, "w") as f:
            hidden_service_found = False
            for line in lines:
                if line.strip().startswith("HiddenServiceDir"):
                    hidden_service_found = True
                    continue
                if line.strip().startswith("HiddenServicePort"):
                    continue
                if line.strip().startswith("HiddenServiceVersion"):
                    continue
                f.write(line)
            
            f.write("\n# TorHost Hidden Service Configuration\n")
            f.write(f"HiddenServiceDir {hs_dir}\n")
            f.write("HiddenServiceVersion 3\n")
            f.write(f"HiddenServicePort 80 127.0.0.1:{port}\n")
            
        print(f"{WHITE} [{GREEN}+{WHITE}] {GREEN}Updated torrc configuration.")
        
    except Exception as e:
        print(f"{WHITE} [{RED}!{WHITE}] {RED}Failed to write torrc: {e}")
        sys.exit(1)
    
    print(f"{WHITE} [{GREEN}+{WHITE}] {GREEN}Restarting Tor service...")
    if not restart_tor():
        print(f"{WHITE} [{RED}!{WHITE}] {RED}Failed to restart Tor.")
        sys.exit(1)
    
    print(f"{WHITE} [{GREEN}+{WHITE}] {GREEN}Waiting for onion address...")
    
    for i in range(WAIT_TIME):
        if os.path.exists(hostname_file):
            try:
                with open(hostname_file, "r") as f:
                    onion = f.read().strip()
                
                if validate_onion_address(onion):
                    print(f"\n{WHITE} ╔══════════════════════════════════════════════════════════════╗")
                    print(f"{WHITE} ║{GREEN}                    HIDDEN SERVICE READY                      {WHITE}║")
                    print(f"{WHITE} ╠══════════════════════════════════════════════════════════════╣")
                    print(f"{WHITE}  {GREEN}  Onion Address: {CYAN}http://{onion}                {WHITE}")
                    print(f"{WHITE}  {GREEN}  Local Port   : {CYAN}{port}                                  {WHITE}")
                    print(f"{WHITE} ╚══════════════════════════════════════════════════════════════╝{RESET}")
                    print(f"\n{WHITE} [{GREEN}+{WHITE}] {GREEN}Make sure you have a service running on port {port}")
                    return
            except:
                pass
        
        time.sleep(1)
    
    print(f"{WHITE} [{RED}!{WHITE}] {RED}Timed out waiting for onion address.")
    sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{WHITE} [{RED}!{WHITE}] {RED}Interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n{WHITE} [{RED}!{WHITE}] {RED}Unexpected error: {e}")
        sys.exit(1)
