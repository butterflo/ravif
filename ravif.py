import numpy as np
import cv2
import cv2.cv as cv
import os
import sys
from time import time
from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify

print "RAViF : RApid Video Fingerprinter"
print "---------------------------------------------"

bits = 7
blocks = 1 << bits
mbunit = 1048576

f = open("input.txt","r")
liststr = []
filesizes = []
netfilesize = 0
while True:
    path = f.readline()
    if not path: break
    liststr.append(path.rstrip())
    filesize = os.path.getsize(path.rstrip())
    netfilesize += filesize
    filesizes.append(filesize)
f.close()

print "processing " + str(len(liststr)) + " files (" + str(netfilesize / mbunit) + " Mb)"
print "hash depth: " + str(bits) + " bits\n"

o = open("output.txt","w",0)

speed = []

for c in range(len(liststr)):

    file_start = time()
    cap = cv2.VideoCapture(liststr[c])
    
    frame_count = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
    unit_pos = frame_count * 1.0 / blocks
    st = np.array((),np.dtype(np.uint8))
    fp_R = ""
    fp_G = ""
    fp_B = ""

    msg = "[" + str(c) + "/" + str(len(liststr)) + "] " + liststr[c] + " (" + str(filesizes[c]/mbunit) + " Mb)"

    for i in range(blocks):
        pos = int(i * unit_pos)
        cap.set(cv.CV_CAP_PROP_POS_FRAMES,pos)
        ret, frame = cap.read()
        small = cv2.resize(frame,(256,256))
        small = cv2.blur(small,(16,16))
        px = small[128,128]
        fp_R = fp_R + ("%0.2x" % px[0])
        fp_G = fp_G + ("%0.2x" % px[1])
        fp_B = fp_B + ("%0.2x" % px[2])

        sys.stdout.write(msg + " %d%%    \r" % ((i+1)*100/blocks))
        sys.stdout.flush()
    sys.stdout.write("\n")
    cap.release()
    fp_hex = fp_R + fp_G + fp_B
    fp_b64 = b64encode(unhexlify(fp_hex))
    o.write(fp_b64 + "\n")
    file_done = time()
    speed.append(file_done - file_start)
o.close()
