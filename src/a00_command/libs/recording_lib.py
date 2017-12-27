import os
import shutil
import requests


MEDIA_FILE_PATH = "/var/opt/augment00/recordings/media"
TEST_MEDIA_FILE_PATH = "/var/opt/augment00/dev/recordings/test_mov.mov"


def start_recording(media_type):
    print "starting to record %s" % media_type
    if os.path.exists(MEDIA_FILE_PATH):
        os.remove(MEDIA_FILE_PATH)

    ## just copy file for tests

    shutil.copy(TEST_MEDIA_FILE_PATH, MEDIA_FILE_PATH)


def stop_recording(media_type, upload_url, confirm_url):

    ## stop recording

    with open(MEDIA_FILE_PATH, "rb") as f:
        rsp = requests.put(upload_url, data=f)


    if rsp.status_code < 300:
        status_code = 200
        message = "ok"
    else:
        status_code = rsp.status_code
        message = rsp.content

    print "stopped recording: %s %s" % (status_code, message)

    results = {
        "status_code": status_code,
        "message": message
    }

    rsp = requests.post(confirm_url, json=results)

    print "confirmed recording: %s" % (rsp.status_code)




