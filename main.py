#!/usr/bin/env python

import time
import os
import sys
import json

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

CREDS_PATH = os.environ["CREDENTIALS_PATH"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
CUSTOM_TOKEN_URL = os.environ["FIREBASE_CUSTOM_TOKEN_URL"]
AUTH_DOMAIN = os.environ["FIREBASE_DB_URL"]
DB_URL = os.environ["GOOGLE_API_KEY"]


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

    # start it
    commander.start()
    time.sleep(2)

    while True:
        try:
            # ask it to process any waiting messages
            commander.tick()
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