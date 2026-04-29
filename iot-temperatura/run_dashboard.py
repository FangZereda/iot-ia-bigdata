import subprocess
import sys

cmd = [sys.executable, "-m", "streamlit", "run", "main.py", "--server.headless", "true"]
subprocess.run(cmd)