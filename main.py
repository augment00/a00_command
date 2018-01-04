#!/usr/bin/env python

import time
import os
import sys
import json
from raven import Client

try:
    import a00_command
except ImportError:
    BASE_DIR = os.path.dirname(__file__)
    SRC_DIR = os.path.join(BASE_DIR, "src")
    sys.path.insert(0, SRC_DIR)
    import a00_command

try:
    import RPi.GPIO as gpio
except ImportError:
    import a00_command.libs.dummy_gpio as gpio

from a00_command import Commander
from a00_command.libs.test_lib import say
from a00_command.libs.admin_lib import reboot
#from a00_command.libs.recording_lib import start_record_audio, stop_record_audio
#from a00_command.libs.recording_lib import start_record_video, stop_record_video
#from a00_command.libs.recording_lib import start_timelapse, stop_timelapse, take_picture
from a00_command.libs.recording_lib import start_recording, stop_recording

CREDS_PATH = os.environ["CREDENTIALS_PATH"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
CUSTOM_TOKEN_URL = os.environ["FIREBASE_CUSTOM_TOKEN_URL"]
AUTH_DOMAIN = os.environ["FIREBASE_AUTH_DOMAIN"]
DB_URL = os.environ["FIREBASE_DB_URL"]
SENTRY_URL = os.environ.get("SENTRY_URL")

def main():

    print "command starting"

    # read in the credentials from file
    with open(CREDS_PATH) as f:
        creds = json.loads(f.read())

    # make one
    commander = Commander(creds,
                          GOOGLE_API_KEY,
                          CUSTOM_TOKEN_URL,
                          AUTH_DOMAIN,
                          DB_URL)

    # add a function to be called by the commander
    commander.add_function("say", say)
    commander.add_function("reboot", reboot)
    # commander.add_function("start_record_audio", start_record_audio)
    # commander.add_function("stop_record_audio", stop_record_audio)
    # commander.add_function("start_record_video", start_record_video)
    # commander.add_function("stop_record_video", stop_record_video)
    # commander.add_function("stop_record_video", start_timelapse)
    # commander.add_function("stop_record_video", stop_timelapse)
    # commander.add_function("stop_record_video", take_picture)
    commander.add_function("start_recording", start_recording)
    commander.add_function("stop_recording", stop_recording)

    # start it
    commander.start()
    time.sleep(2)

    sentry_client = Client(SENTRY_URL) if SENTRY_URL is not None else None

    while True:
        try:
            # ask it to process any waiting messages
            commander.tick(sentry_client)
            time.sleep(0.5)
        except KeyboardInterrupt:
            commander.stop()
            gpio.cleanup()
            break
        except SystemExit:
            # stop it
            commander.stop()
            gpio.cleanup()
            break


if __name__ == "__main__":
    main()
