#!/usr/bin/env python3
from flask import Flask, request, send_file, jsonify
import subprocess
import os
from .downloader import validate_environment, download_video
from .vpn_manager import ensure_vpn_connection

app = Flask(__name__)
DOWNLOAD_DIR = "/root"

@app.route('/api/download', methods=['POST'])
def handle_download():
    data = request.get_json(force=True)
    url = data.get("url")
    resolution = data.get("resolution")
    extension = data.get("extension")

    if not url:
        return jsonify(error="Missing 'url'"), 400

    # Check VPN connection before processing
    if not ensure_vpn_connection():
        return jsonify(error="VPN not connected. Use 'ytp-dl vpn connect <account>' first."), 503

    try:
        filename = download_video(
            url=url,
            resolution=resolution,
            extension=extension
        )
        
        if filename and os.path.exists(filename):
            return send_file(filename, as_attachment=True)
        else:
            return jsonify(error="Download failed"), 500
            
    except Exception as e:
        return jsonify(error=f"Download failed: {str(e)}"), 500

@app.route('/api/status', methods=['GET'])
def handle_status():
    """Check API and VPN status"""
    from .vpn_manager import get_connection_status
    
    vpn_status = get_connection_status()
    
    return jsonify({
        "api_status": "running",
        "vpn_connected": vpn_status.get("connected", False),
        "vpn_status": vpn_status.get("status_output", "Unknown"),
        "auto_refresh_active": vpn_status.get("auto_refresh_active", False)
    })

def main():
    """Entry point for the API server"""
    validate_environment()  # Ensure we're in the correct environment
    print("Starting ytp-dl API server...")
    print("💡 Tip: Ensure VPN is connected with 'ytp-dl vpn connect <account>' before making requests")
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()