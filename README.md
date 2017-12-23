## RAViF
RApid Video Fingerprinter (for python)

### Description
RAViF is an proof-of-idea implementation of video fingerprinting algorithm I am working on. This algorithm attempts to sample `2^k` frames along timeline with specified bit depth `k` to reduce the time computing fingerprints. Default for `k` is `bitdepth=7` which means each video file is divided into `2^7 == 128` blocks in time dimension.

RAViF uses RGB value of only one pixel located at the center of each sampled frame, with the pixel values smoothed with a blur kernel. Similarity evaluation is based on Pearson correlation. This scheme provides robustness to 'simple' manipulations such as resize, horizontal/vertical axis flip, and global brightness/contrast adjusts, taking advantage of the observation that 'complex' manipulations such as timewise or framewise cropping requires a video editing tool, usually not viable to general audience.

### Dependencies
- opencv
- numpy
- scipy

### Files

- **input.txt** - put video file path here
- **ravif.py**  - reads input.txt and generates video fingerprints of specified bit depth. default value is 7. writes to output.txt
- **output.txt**- stores video fingerprints
- **eval.py**   - reads output.txt and evaluates similarities from 0 to 1. writes to eval.csv
