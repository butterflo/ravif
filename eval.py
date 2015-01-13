import os
import sys
import numpy as np
from time import time
from base64 import b64decode
from binascii import hexlify
from scipy.stats import pearsonr

print "RAViF : RApid Video Fingerprinter"
print "---------------------------------------------"
print "evaluating.."

f = open("output.txt","r")
fp = []
while True:
    fpstr = f.readline()
    if not fpstr: break
    fp.append(hexlify(b64decode(fpstr.rstrip())))
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

o = open("eval.csv","w",0)
o.write(",")
for x in range(len(chR)):
    o.write(liststr[x] + ",")
o.write("\n")

for x in range(len(chR)):
    o.write(liststr[x] + ",")
    for y in range(len(chR)):
        if y <= x:
            cor_r = pearsonr(chR[x],chR[y])            
            cor_g = pearsonr(chG[x],chG[y])
            cor_b = pearsonr(chB[x],chB[y])

            si = abs(cor_r[0] + cor_g[0] + cor_b[0])/3
            o.write(str(si) + ",")
    o.write("\n")
o.close()
print "eval ok"
