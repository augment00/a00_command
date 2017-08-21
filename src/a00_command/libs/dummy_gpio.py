BOARD = "board"
OUT = "out"

def setmode( mode):
    print "setmode", mode

def setup(pin, direction):
    print "output", pin, direction

def output(pin, value):
    print "output", pin, value

def cleanup():
    print "cleanup"