## RAViF
RApid Video Fingerprinter (for python)

### Description
RAViF is an proof-of-idea implementation of video fingerprinting algorithm I am working on. This algorithm does not process every frame; instead it attempts to sample the frames with given bit depth, thus saving great amount of time. Default is `bitdepth=7` which means each video file is divided into 2^7=128 blocks in time dimension. This may seem unreasonable at glance, but it works and gives a stable result. Similarity evaluation is based on Pearson Correlation Coefficient. Note that this algorithm cannot recognize any partial relationships due to its design.

### Dependencies
- opencv
- numpy
- scipy

### Files

- **input.txt** - put video file path here
- **ravif.py**  - reads input.txt and generates video fingerprints of specified bit depth. default value is 7. writes to output.txt
- **output.txt**- stores video fingerprints
- **eval.py**   - reads output.txt and evaluates similarities from 0 to 1. writes to eval.csv
