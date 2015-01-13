RApid VIdeo Fingerprinter (for python)

Description:
RAViF is an proof-of-idea implementation of video fingerprinting algorithm I am working on.

Dependencies:
opencv
numpy

Files:
input.txt - put video file path here.
ravif.py  - reads input.txt and generates video fingerprints of specified bit depth. default value is 7. writes to output.txt.
output.txt- stores video fingerprints.
eval.py   - reads output.txt and evaluates similarities from -1 to +1. writes to eval.csv.