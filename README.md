## RAViF
RApid Video Fingerprinter (for python)

### Description
RAViF is an proof-of-idea implementation of video fingerprinting algorithm I am working on. This algorithm does not process every frame; instead it attempts to sample the frames with given bit depth, thus saving great amount of time. Default is `bitdepth=7`. Similarity evaluation is based on Pearson Correlation Coefficient. Note that this algorithm cannot recognize any partial relationships.

### Dependencies
- opencv
- numpy
- scipy

### Files

- **input.txt** - put video file path here
- **ravif.py**  - reads input.txt and generates video fingerprints of specified bit depth. default value is 7. writes to output.txt
- **output.txt**- stores video fingerprints
- **eval.py**   - reads output.txt and evaluates similarities from 0 to 1. writes to eval.csv
