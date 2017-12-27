import os

def reboot():
    print "rebooting"
    file_path = "/etc/opt/augment00/rebootme"
    if not os.path.exists(file_path):
        with open(file_path, "r") as f:
            f.write("reboot")