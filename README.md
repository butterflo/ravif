## RAViF
RApid Video Fingerprinter (for python)

### Description
RAViF is an proof-of-idea implementation of a video fingerprinting algorithm I developed. This algorithm attempts to sample `2^k` frames along timeline with specified bit depth `k` to reduce the time computing fingerprints. Default for `k` is `bitdepth=7` which means `2^7 == 128` frames are sampled across the time dimension.

RAViF uses RGB value of a single pixel at the center of each sampled frame, with the pixel values smoothed with a blur kernel, and of course each of the frame sizes normalized. This sampling scheme provides robustness to 'simple' manipulations such as resize, horizontal/vertical axis flip, and global brightness/contrast adjusts, taking advantage of the observation that 'complex' manipulations such as timewise or framewise cropping requires a video editing tool, usually not viable to general audience. Similarity evaluation is based on Pearson correlation.

Another feature of this sampling scheme is that the extracted fingerprints are readily expandable to arbitrary bit depth, although this feature is not explicitly implemented.

### Dependencies
- opencv
- numpy
- scipy

### Files

- **input.txt** - put video file path here
- **ravif.py**  - reads input.txt and generates video fingerprints of specified bit depth. default value is 7. writes to output.txt
- **output.txt**- stores video fingerprints
- **eval.py**   - reads output.txt and evaluates similarities from 0 to 1. writes to eval.csv
