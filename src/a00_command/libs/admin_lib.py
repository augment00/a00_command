import subprocess

def reboot():
    cmd = "reboot"
    subprocess.call(cmd, shell=True)