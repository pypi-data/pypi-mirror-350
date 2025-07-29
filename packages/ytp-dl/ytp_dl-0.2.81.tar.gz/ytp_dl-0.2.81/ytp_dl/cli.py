#!/usr/bin/env python3
import argparse
import sys
from .downloader import download_video
from .vpn_manager import (
    connect_with_auto_refresh, disconnect_vpn, get_connection_status, 
    setup_persistent_connection, get_vpn_state
)

def handle_download(args):
    """Handle video download command"""
    result = download_video(
        url=args.url,
        resolution=args.resolution,
        extension=args.extension
    )
    
    if result:
        print(f"Successfully downloaded: {result}")
    else:
        print("Download failed")
        sys.exit(1)

def handle_vpn_connect(args):
    """Handle VPN connect command"""
    if connect_with_auto_refresh(args.account):
        print("VPN connection established with auto-refresh enabled!")
    else:
        print("Failed to connect VPN")
        sys.exit(1)

def handle_vpn_status(args):
    """Handle VPN status command"""
    status = get_connection_status()
    
    print(f"VPN Status: {'🟢 Connected' if status['connected'] else '🔴 Disconnected'}")
    print(f"Raw Status: {status['status_output']}")
    
    if status.get('account'):
        print(f"Account: {status['account']}")
    
    if status['connected'] and status.get('last_connect_time'):
        print(f"Connected Since: {status['last_connect_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        if status.get('time_until_refresh') is not None:
            minutes_left = int(status['time_until_refresh'] // 60)
            seconds_left = int(status['time_until_refresh'] % 60)
            print(f"Next IP Refresh: in {minutes_left}m {seconds_left}s")
            
        refresh_status = "🟢 Active" if status.get('auto_refresh_active') else "🔴 Inactive"
        print(f"Auto-Refresh: {refresh_status}")
    
    if status.get('error'):
        print(f"Error: {status['error']}")

def handle_vpn_disconnect(args):
    """Handle VPN disconnect command"""
    if disconnect_vpn():
        print("VPN disconnected successfully!")
    else:
        print("Failed to disconnect VPN")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="YouTube video downloader with Mullvad VPN")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Download command (default behavior)
    download_parser = subparsers.add_parser('download', help='Download a video (default)')
    download_parser.add_argument("url", help="YouTube URL")
    download_parser.add_argument("--resolution", help="Desired resolution (e.g., 1080)", default=None)
    download_parser.add_argument("--extension", help="Desired file extension (e.g., mp4, mp3)", default=None)
    
    # VPN management commands
    vpn_parser = subparsers.add_parser('vpn', help='VPN management commands')
    vpn_subparsers = vpn_parser.add_subparsers(dest='vpn_command', help='VPN commands')
    
    # VPN connect
    connect_parser = vpn_subparsers.add_parser('connect', help='Connect to Mullvad VPN with auto-refresh')
    connect_parser.add_argument('account', help='Mullvad account number')
    
    # VPN status
    vpn_subparsers.add_parser('status', help='Check VPN connection status')
    
    # VPN disconnect
    vpn_subparsers.add_parser('disconnect', help='Disconnect from VPN and stop auto-refresh')
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'vpn':
        if args.vpn_command == 'connect':
            handle_vpn_connect(args)
        elif args.vpn_command == 'status':
            handle_vpn_status(args)
        elif args.vpn_command == 'disconnect':
            handle_vpn_disconnect(args)
        else:
            vpn_parser.print_help()
    elif args.command == 'download':
        handle_download(args)
    else:
        # Default behavior: if no subcommand, treat as download
        # Check if first arg looks like a URL
        if len(sys.argv) >= 2 and ('youtube.com' in sys.argv[1] or 'youtu.be' in sys.argv[1]):
            # Parse as old-style download command for backwards compatibility
            parser = argparse.ArgumentParser(description="YouTube video downloader with Mullvad VPN")
            parser.add_argument("url", help="YouTube URL")
            parser.add_argument("--resolution", help="Desired resolution (e.g., 1080)", default=None)
            parser.add_argument("--extension", help="Desired file extension (e.g., mp4, mp3)", default=None)
            
            args = parser.parse_args()
            handle_download(args)
        else:
            parser.print_help()

if __name__ == "__main__":
    main()