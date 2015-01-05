import numpy as np
import cv2
import cv2.cv as cv
import math
import scipy.stats
from time import time

print "RAViF : RApid Video Fingerprinter 3.0 - butterflo"
print "-------------------------------------------------"

blocks = 64

while blocks <= 192:
    f = open("input.txt","r")
    liststr = []
    while True:
        path = f.readline()
        if not path: break
        liststr.append(path.rstrip())
    f.close()

    #bits = 8
    #blocks = 1 << bits
    #print "processing " + str(len(liststr)) + " files"
    #print "depth: " + str(bits) + " bits"
    print "hash length: " + str(blocks * 6)

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

        #print "filename: " + liststr[c] + " ( " + str(frame_count) + " frames )"

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
        cap.release()
        fp = fp_R + fp_G + fp_B

        o.write(fp + "\n")
        file_done = time()
	speed.append(file_done - file_start)
    o.close()

    #print "processed in " + str(runtime) + " seconds"

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
            #print v
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

    #print "eval ok"

    blocks += 16
