import numpy as np
import cv2
import cv2.cv as cv
import scipy.stats
import os
import sys
from time import time

print "RAViF : RApid Video Fingerprinter"
print "---------------------------------------------"

blocks = 64
mbunit = 1048576

while blocks <= 192:
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

    bits = 8
    blocks = 1 << bits
    print "processing " + str(len(liststr)) + " files (" + str(netfilesize / mbunit) + " MB)"
    print "hash depth: " + str(bits) + " bits\n"

    o = open("output.txt","w",0)

    speed = []
    runtime = 0.0
    for c in range(len(liststr)):

        file_start = time()
        cap = cv2.VideoCapture(liststr[c])
        
        frame_count = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
        unit_pos = frame_count * 1.0 / blocks
        st = np.array((),np.dtype(np.uint8))
        fp_R = ""
        fp_G = ""
        fp_B = ""

        msg = "[" + str(c) + "/" + str(len(liststr)) + "] " + liststr[c] + " (" + str(filesizes[c]/mbunit) + "MB)"

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
        fp = fp_R + fp_G + fp_B

        o.write(fp + "\n")
        file_done = time()
	speed.append(file_done - file_start)
    o.close()

    print "processed in " + str(runtime) + " seconds"

    f = open("output.txt","r")
    fp = []
    while True:
        fpstr = f.readline()
        if not fpstr: break
        fp.append(fpstr.rstrip())
    f.close()

    f = open("input.txt","r")
    liststr = []
    while True:
        path = f.readline()
        if not path: break
        liststr.append(path.rstrip())
    f.close()

    chR, chG, chB = [], [], []

    for c in range(len(fp)):
        fp_length = len(fp[c])/2
        fp_blocks = fp_length/3

        fpi = []

        for i in range(fp_length):
            v = int(fp[c][i*2:i*2+2],16)
            fpi.append(v)

        chR.append(fpi[0:fp_blocks])
        chG.append(fpi[fp_blocks:fp_blocks*2])
        chB.append(fpi[fp_blocks*2:fp_blocks*3])

    chR = np.array(chR,np.dtype(np.uint8))
    chG = np.array(chG,np.dtype(np.uint8))
    chB = np.array(chB,np.dtype(np.uint8))

    o = open("eval"+str(blocks)+".csv","w",0)
    o.write(",")
    for x in range(len(chR)):
        o.write(liststr[x] + ",")
    o.write("\n")

    for x in range(len(chR)):
        o.write(liststr[x] + ",")
        for y in range(len(chR)):
            if y <= x:
                cor_r = scipy.stats.pearsonr(chR[x],chR[y])
                cor_g = scipy.stats.pearsonr(chG[x],chG[y])
                cor_b = scipy.stats.pearsonr(chB[x],chB[y])

                si = (cor_r[0] + cor_g[0] + cor_b[0])/3
                o.write(str(si) + ",")
        o.write("\n")
    o.write(",")
    for x in range(len(chR)):
        o.write(str(speed[x]) + ",")
    o.close()

    print "eval ok"
