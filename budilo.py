#!/usr/bin/env python3.7

import time, subprocess, sys, os, os.path

lang="en+f2"

def print_std(stderr):
    if stderr is None or len(stderr) == 0:
        return
    print(stderr)

def speak(s):
    cmd = ['/usr/bin/espeak', '-v'+lang, '-k0', '-g', '10', '-s150', '--stdout', s]
    cps = subprocess.run(cmd, capture_output=True)
    print_std(cps.stderr)
    cpp = subprocess.run(['/usr/bin/aplay', '-q'], input=cps.stdout)
    print_std(cpp.stderr)

def saytime():
    ltime = time.localtime()
    weekday = ( "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
               )[ltime.tm_wday]
    rds = { 1 : 'st', 2 : 'nd', 3 : 'rd' }
    mday = str(ltime.tm_mday) + rds.get(ltime.tm_mday%10, "th")
    hs = "hours" if ltime.tm_hour > 1 else 'hour'
    ms = "minutes" if ltime.tm_min > 1 else 'minute'
    ttime = "{} {} {} {}".format(ltime.tm_hour, hs, ltime.tm_min, ms)
    speak(weekday + ', ' + mday + ", " + ttime)

def playdir(dirpath):
    names = []
    with os.scandir(dirpath) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file() and entry.name.lower().endswith('.mp3'):
                names.append(entry.name)

    for name in sorted(names):
        fullpath = os.path.join(dirpath, name)
        saytime()
        time.sleep(1)
        speak(name[:-4])
        try:
            subprocess.run(['/usr/bin/mpg321', fullpath])
        except:
            pass

playdir(sys.argv[1])
