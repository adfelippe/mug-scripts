#!/usr/bin/python

import os
import commands
import re
import sys

# params: 
# 1) NAME
# 2) WIDTH=$2
# 3) HEIGHT=$3
# 4) DEV=/dev/media0
# 5) PAD=0
# 7) CODE=RGB888_1X24
# 8) VERBOSE=
def change_sd_fmt(params, mdev):
    print "==========================================="
    print "%s, Pad %d" % (params['name'], params['pad'])
    print "==========================================="
    #print params

    # Add quotes in the name
    name = "\'" + params['name'] + "\'"

    # Print the old format
    cmd = "sudo media-ctl %s -d %s --get-v4l2 \"%s:%d\"" % (params['verbose'], mdev, name, params['pad'])
    print '>' + cmd
    os.system(cmd)

    # Set the new format
    cmd = "sudo media-ctl %s -d %s -V \"%s:%s [fmt:%s/%dx%d]\"" % (params['verbose'], mdev, name, params['pad'], params['code'], params['width'], params['height'])
    print '>' + cmd
    os.system(cmd)

    # Print the new format
    cmd = "sudo media-ctl %s -d %s --get-v4l2 \"%s:%d\"" % (params['verbose'], mdev, name, params['pad'])
    print '>' + cmd
    output = commands.getstatusoutput(cmd)
    print output[1]
    if output[0] != 0:
        print ""
        print "ERR: Could not apply format"
        exit(-1)

    # Check if we could apply the format
    new_fmt = re.search(':(.*)/(.*)]', output[1])
    if not new_fmt or \
        new_fmt.group(1) != params['code'] or \
        new_fmt.group(2) != "%dx%d" % (params['width'], params['height']):

        print ""
        print "ERR: Could not apply format"
        exit(-1)

# params
# 1) NAME
# 2) WIDTH=$2
# 3) HEIGHT=$3
# 4) VDEV=/dev/video0
# 5) FORMAT=SBGGR8
def change_vid_fmt(params):
    print "==========================================="
    print params['name']
    print "==========================================="

    cmd = 'yavta --enum-formats '+ params['dev']
    print '>' + cmd
    os.system(cmd)

    cmd = "yavta -f %s -s %dx%d %s" % (params['fmt'], params['width'], params['height'], params['dev'])
    print '>' + cmd
    output = commands.getstatusoutput(cmd)
    print output[1]
    if output[0] != 0:
        print ""
        print "ERR: Could not apply format"
        exit(-1)

    # Check if we could apply the format
    new_fmt = re.search('Video format: (.*?) .*? (.*?) ', output[1])
    if not new_fmt or \
        new_fmt.group(1) != params['fmt'] or \
        new_fmt.group(2) != "%dx%d" % (params['width'], params['height']):

        print ""
        print "ERR: Could not apply format"
        exit(-1)

    print ""

if __name__ == "__main__":
    MDEV='/dev/media0'

    if len(sys.argv) != 2:
        print "Usage %s <pad_config>" % sys.argv[0]
        print "Where <pad_config> is in pad_config/<pad_config>.py"
        exit(-1)

    sys.dont_write_bytecode = True # avoid .pyc from the modules
    sys.path.append("/home/helen/kernel-scripts/pad_config/")

    exec('import %s' % sys.argv[1])
    mod = sys.modules[sys.argv[1]]
    if not mod.pads:
        print "File %s doesn't define pads variable" % sys.argv[1]
        exit(-1)

    #print pads

    for pad in mod.pads:
        if 'code' in pad:
            change_sd_fmt(pad, MDEV)
        else:
            change_vid_fmt(pad)

    print "==========================================="
    print "SUMMARY"
    print "==========================================="
    cmd = 'sudo media-ctl -p -d ' + MDEV
    print '>' + cmd
    os.system(cmd)
