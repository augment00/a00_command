import os
import shutil
import requests

import sounddevice as sd
import soundfile as sf
import Queue
import threading
import picamera
import subprocess
import time

CHANNELS = 1
RATE = 44100
# FLAC_OUTPUT_FILENAME_TEMPLATE = "%s.flac"
# VIDEO_OUTPUT_FILENAME_TEMPLATE = "%s.h264"
# PICTURE_OUTPUT_FILENAME_TEMPLATE = "%s.jpg"

# MEDIA_FILE_PATH = "/var/opt/augment00/recordings/media"
VIDEO_FILE_PATH = "/var/opt/augment00/recordings/video.h264"
MP4_FILE_PATH = "/var/opt/augment00/recordings/video.mp4"
AUDIO_FILE_PATH = "/var/opt/augment00/recordings/audio.flac"
# TEST_MEDIA_FILE_PATH = "/var/opt/augment00/dev/recordings/test_mov.mov"

# for video, the picamera library provides a camera object
cam = picamera.PiCamera()

def audiorecording_callback(indata, frames, time, status):
    """This function is called (from a separate thread) for each audio block."""
    q.put(indata.copy())

# for audio, we record the audio stream in a queue object and use threading to start and stop
q = Queue.Queue()
t = None

def write_audiofile(q):
    t = threading.currentThread()
    with sf.SoundFile(AUDIO_FILE_PATH, mode='x', samplerate=RATE, channels=CHANNELS) as f:
        with sd.InputStream(samplerate=RATE, channels=CHANNELS, callback=audiorecording_callback):
            while getattr(t, "do_run", True):
                f.write(q.get())
            f.close()



def start_recording(media_type):
    """This function is called to start recording."""
    print "starting to record %s" % media_type

    # ## just copy file for tests
    # ## TODO start recording to the file MEDIA_FILE_PATH instead of this copy
    # shutil.copy(TEST_MEDIA_FILE_PATH, MEDIA_FILE_PATH)

    if media_type == "audio":
        if os.path.exists(AUDIO_FILE_PATH):
            os.remove(AUDIO_FILE_PATH)
        # generate audio filename from timestamp so that uploaded files are easy to identify
        global t
        t = threading.Thread(target=write_audiofile, args=(q,))
        t.do_run = True
        t.start()

    if media_type == "video":
        if os.path.exists(VIDEO_FILE_PATH):
            os.remove(VIDEO_FILE_PATH)
        cam.start_recording(VIDEO_FILE_PATH)

def stop_recording(media_type, upload_url, confirm_url):
    """This function is called to stop recording."""

    if media_type == "audio":
        t.do_run = False
        t.join()
        with open(AUDIO_FILE_PATH, "rb") as f:
            rsp = requests.put(upload_url, data=f)

    if media_type == "video":
        cam.stop_recording()
        if os.path.exists(MP4_FILE_PATH):
            os.remove(MP4_FILE_PATH)

        cmd = "MP4Box -add %s %s" % (VIDEO_FILE_PATH, MP4_FILE_PATH)
        subprocess.call(cmd, shell=True)

        with open(MP4_FILE_PATH, "rb") as f:
            rsp = requests.put(upload_url, data=f)

    ## leave this stuff - it uploading the file and sends a confirmation to the web app

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

# the functions stubs below are for future reference in case we'd like
# to add functions to take pictures and doing picture timelapse recording

# def start_record_audio():
#     timestamp = time.strftime("audio_%Y%m%d-%H%M%S")
#     filename = FLAC_OUTPUT_FILENAME % timestamp
#     pass
#
# def stop_record_audio():
#     pass
#
# def start_record_video():
#     timestamp = time.strftime("video_%Y%m%d-%H%M%S")
#     filename = VIDEO_OUTPUT_FILENAME_TEMPLATE % timestamp
#     pass
#
# def stop_record_video():
#     pass
#
# def take_picture():
#     timestamp = time.strftime("picture_%Y%m%d-%H%M%S")
#     filename = PICTURE_OUTPUT_FILENAME_TEMPLATE % timestamp
#     pass
#
# def start_timelapse():
#     timestamp = time.strftime("timelapse_%Y%m%d-%H%M%S")
#     filename = VIDEO_OUTPUT_FILENAME_TEMPLATE % timestamp
#     pass
#
# def stopt_timelapse():
#     pass
