import sys
import os
import time
import threading
import webbrowser

# Ensure import path is correct
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from runtime.live_runtime_manager import LiveRuntimeManager
from http.server import SimpleHTTPRequestHandler, HTTPServer

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dist_dir = os.path.join(self.root_dir, 'frontend', 'dist')
        target_dir = self.dist_dir if os.path.exists(self.dist_dir) else self.root_dir
        super().__init__(*args, directory=target_dir, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # Legacy dashboard endpoint
        if self.path in ('/legacy', '/Index.html'):
            legacy_file = os.path.join(self.root_dir, 'Index.html')
            if os.path.exists(legacy_file):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(legacy_file, 'rb') as f:
                    self.wfile.write(f.read())
                return

        # Single page app route fallback:
        # If frontend/dist exists, and requested path does not match a file on disk,
        # fallback to index.html so React Router handles the route.
        if os.path.exists(self.dist_dir):
            clean_path = self.path.split('?')[0].lstrip('/')
            file_path = os.path.join(self.dist_dir, clean_path)
            if not os.path.exists(file_path):
                self.path = '/index.html'

        return super().do_GET()

    def log_message(self, format, *args):
        pass  # Disable logging to avoid console spam

def run_demo():
    print("======================================================")
    print(" THERVO - Hyperscale Orchestration Mission Control")
    print(" FINAL PROTOTYPE DEMONSTRATION")
    print("======================================================")
    print("[*] Initializing predictive runtime & orchestration layers...")
    
    # 1. Start backend runtime & API Server
    manager = LiveRuntimeManager()
    manager.mode_live = True  # Enable real telemetry from PC
    manager.start()
    
    # Start HTTP server on port 3000
    print("[*] Starting Dashboard Web Server on port 3000...")
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    def serve_dashboard():
        os.chdir(root_dir)
        server = HTTPServer(('0.0.0.0', 3000), DashboardHandler)
        server.serve_forever()
        
    t = threading.Thread(target=serve_dashboard)
    t.daemon = True
    t.start()
    
    # 2. Open dashboard
    print("[*] Launching Mission Control Dashboard at: http://localhost:3000/")
    webbrowser.open("http://localhost:3000/")
    
    print("[*] Dashboard launched. Running live local telemetry orchestration loop...")
    print("[*] The system is now reading local hardware telemetry and dynamically")
    print("    adjusting Lenovo Legion Toolkit thermal profiles in real-time.")
    print("------------------------------------------------------")
    print("[*] Press Ctrl+C to stop the orchestration.")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Stopping demonstration and exporting artifacts...")
        manager.stop()
        print("[*] Demonstration offline. Goodbye.")
        
if __name__ == "__main__":
    run_demo()
