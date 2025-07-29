#!/usr/bin/env python3
import subprocess
import sys
import os
import time
import shutil
import json
import threading
from datetime import datetime, timedelta
from pathlib import Path

VPN_STATE_FILE = "/opt/yt-dlp-mullvad/vpn_state.json"
RECONNECT_INTERVAL = 300  # 5 minutes in seconds
_refresh_thread = None
_stop_refresh = False

def run_command(cmd, check=True):
    """Execute a shell command and return output"""
    try:
        result = subprocess.run(
            cmd, shell=True, check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if check:
            print(f"Command failed: {cmd}\nError: {e.stdout}")
            raise
        return e.stdout

def check_mullvad_installed():
    """Check if Mullvad CLI is available"""
    if not shutil.which("mullvad"):
        print("Error: Mullvad CLI not found.")
        print("Please install Mullvad VPN:")
        print("curl -fsSLo /tmp/mullvad.deb https://mullvad.net/download/app/deb/latest/")
        print("sudo apt install -y /tmp/mullvad.deb")
        sys.exit(1)

def ensure_state_dir():
    """Ensure the state directory exists"""
    state_dir = os.path.dirname(VPN_STATE_FILE)
    if state_dir:
        Path(state_dir).mkdir(parents=True, exist_ok=True)

def save_vpn_state(connected, account=None, last_connect_time=None):
    """Save VPN state to file"""
    ensure_state_dir()
    state = {
        "connected": connected, 
        "account": account,
        "last_connect_time": last_connect_time or (datetime.now().isoformat() if connected else None),
        "pid": os.getpid() if connected else None
    }
    
    try:
        with open(VPN_STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save VPN state: {e}")

def get_vpn_state():
    """Load VPN state from file"""
    try:
        if os.path.exists(VPN_STATE_FILE):
            with open(VPN_STATE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load VPN state: {e}")
    
    return {"connected": False, "account": None, "last_connect_time": None}

def should_reconnect():
    """Check if VPN should be reconnected based on time interval"""
    state = get_vpn_state()
    if not state.get("connected") or not state.get("last_connect_time"):
        return True
    
    try:
        last_connect = datetime.fromisoformat(state["last_connect_time"])
        time_since_connect = datetime.now() - last_connect
        return time_since_connect.total_seconds() >= RECONNECT_INTERVAL
    except (ValueError, TypeError):
        return True

def connect_vpn(mullvad_account, background=False):
    """Connect to Mullvad VPN with given account"""
    check_mullvad_installed()
    
    if not background:
        print(f"Logging into Mullvad with account: {mullvad_account}")
    
    try:
        # Login to account
        run_command(f"mullvad account login {mullvad_account}")
        
        # Connect to VPN
        if not background:
            print("Connecting to Mullvad VPN...")
        run_command("mullvad connect")
        
        # Wait for connection to establish
        time.sleep(10)
        
        # Verify connection
        status = run_command("mullvad status", check=False)
        if "Connected" not in status:
            raise Exception(f"VPN connection failed. Status: {status}")
        
        # Save state
        save_vpn_state(True, mullvad_account, datetime.now().isoformat())
        
        if not background:
            print("✅ VPN connected successfully!")
            print("🔄 Auto-refresh enabled (reconnects every 5 minutes)")
        
        return True
        
    except Exception as e:
        print(f"❌ VPN connection failed: {e}")
        save_vpn_state(False)
        return False

def disconnect_vpn():
    """Disconnect from Mullvad VPN"""
    check_mullvad_installed()
    
    # Stop background refresh first
    stop_background_refresh()
    
    print("Disconnecting from Mullvad VPN...")
    try:
        run_command("mullvad disconnect")
        save_vpn_state(False)
        print("✅ VPN disconnected successfully!")
        return True
    except Exception as e:
        print(f"❌ VPN disconnection failed: {e}")
        return False

def get_connection_status():
    """Get detailed connection status"""
    check_mullvad_installed()
    
    try:
        status_output = run_command("mullvad status", check=False)
        account_output = run_command("mullvad account get", check=False)
        
        state = get_vpn_state()
        
        # Parse connection status
        connected = "Connected" in status_output
        
        # Parse account info
        account = None
        if "Account:" in account_output:
            account = account_output.split("Account:")[1].strip()
        
        # Calculate time info
        last_connect_time = None
        next_refresh = None
        time_until_refresh = None
        
        if state.get("last_connect_time"):
            try:
                last_connect_time = datetime.fromisoformat(state["last_connect_time"])
                next_refresh = last_connect_time + timedelta(seconds=RECONNECT_INTERVAL)
                time_until_refresh = max(0, (next_refresh - datetime.now()).total_seconds())
            except (ValueError, TypeError):
                pass
        
        return {
            "connected": connected,
            "status_output": status_output,
            "account": account,
            "last_connect_time": last_connect_time,
            "next_refresh": next_refresh,
            "time_until_refresh": time_until_refresh,
            "auto_refresh_active": _refresh_thread is not None and _refresh_thread.is_alive()
        }
        
    except Exception as e:
        return {
            "connected": False,
            "error": str(e),
            "status_output": f"Error getting status: {e}"
        }

def background_refresh_worker(account):
    """Background worker that refreshes VPN connection every 5 minutes"""
    global _stop_refresh
    
    while not _stop_refresh:
        time.sleep(30)  # Check every 30 seconds
        
        if _stop_refresh:
            break
            
        if should_reconnect():
            print(f"\n🔄 Auto-refreshing VPN connection for new IP...")
            if connect_vpn(account, background=True):
                print(f"✅ VPN refreshed successfully at {datetime.now().strftime('%H:%M:%S')}")
            else:
                print(f"❌ VPN refresh failed at {datetime.now().strftime('%H:%M:%S')}")

def start_background_refresh(account):
    """Start background VPN refresh thread"""
    global _refresh_thread, _stop_refresh
    
    # Stop existing refresh if running
    stop_background_refresh()
    
    _stop_refresh = False
    _refresh_thread = threading.Thread(target=background_refresh_worker, args=(account,), daemon=True)
    _refresh_thread.start()

def stop_background_refresh():
    """Stop background VPN refresh thread"""
    global _refresh_thread, _stop_refresh
    
    _stop_refresh = True
    if _refresh_thread and _refresh_thread.is_alive():
        _refresh_thread.join(timeout=2)
    _refresh_thread = None

def connect_with_auto_refresh(mullvad_account):
    """Connect to VPN and start auto-refresh background process"""
    if connect_vpn(mullvad_account):
        start_background_refresh(mullvad_account)
        return True
    return False

def ensure_vpn_connection():
    """Ensure VPN is connected, show helpful message if not"""
    check_mullvad_installed()
    
    try:
        status_output = run_command("mullvad status", check=False)
        if "Connected" in status_output:
            return True
        else:
            print("❌ VPN is not connected!")
            print("\nTo connect VPN:")
            print("  ytp-dl vpn connect <your_mullvad_account>")
            print("\nTo check VPN status:")
            print("  ytp-dl vpn status")
            return False
    except Exception as e:
        print(f"❌ Error checking VPN status: {e}")
        print("\nTo connect VPN:")
        print("  ytp-dl vpn connect <your_mullvad_account>")
        return False

def setup_persistent_connection():
    """Setup persistent VPN connection (for systemd service)"""
    state = get_vpn_state()
    if state.get("connected") and state.get("account"):
        print("Setting up persistent VPN connection...")
        return connect_with_auto_refresh(state["account"])
    else:
        print("No previous VPN connection found. Use 'ytp-dl vpn connect <account>' first.")
        return False