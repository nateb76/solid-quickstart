"""
Native macOS launcher for vAI Send Mail.
Starts the Streamlit server as a subprocess, opens a pywebview window,
and tears everything down when the window closes.
"""

import os
import sys
import socket
import subprocess
import threading
import time
import signal

import webview


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def get_app_dir():
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "vai_app")
    return os.path.dirname(os.path.abspath(__file__))


def wait_for_server(port, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(("127.0.0.1", port))
                return True
        except (ConnectionRefusedError, OSError):
            time.sleep(0.3)
    return False


def main():
    port = find_free_port()
    app_dir = get_app_dir()
    app_py = os.path.join(app_dir, "app.py")

    env = os.environ.copy()
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    env["STREAMLIT_SERVER_HEADLESS"] = "true"

    if getattr(sys, "frozen", False):
        python_exe = sys.executable
        streamlit_main = os.path.join(app_dir, "_streamlit_run.py")
        with open(streamlit_main, "w") as f:
            f.write(
                f"import sys; sys.argv = ['streamlit', 'run', {repr(app_py)}, "
                f"'--server.port={port}', '--server.headless=true', "
                f"'--browser.gatherUsageStats=false', '--global.developmentMode=false']; "
                f"from streamlit.web.cli import main; main()"
            )
        cmd = [python_exe, streamlit_main]
    else:
        cmd = [
            sys.executable, "-m", "streamlit", "run", app_py,
            f"--server.port={port}",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
        ]

    server_process = subprocess.Popen(
        cmd,
        cwd=app_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if not wait_for_server(port):
        server_process.kill()
        print("Failed to start Streamlit server.")
        sys.exit(1)

    url = f"http://127.0.0.1:{port}"

    def on_closed():
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()

    window = webview.create_window(
        "vAI Send Mail",
        url,
        width=1400,
        height=900,
        min_size=(1000, 700),
        background_color="#0a0c10",
    )

    window.events.closed += on_closed

    webview.start()


if __name__ == "__main__":
    main()
