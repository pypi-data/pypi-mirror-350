# pyLoRaPHY
Full implementation of the physical layer of LoRa. (Python translation of jkadbear/LoRaPHY)

It also contains comments from my understanding of
the code and unique implementation choices optimized for clarity, Pythonic
style, and performance.

Some MATLAB values distingush column and row vectors. They are all treated as
1D arrays here. All indices are C-style.

The original code was (c) 2020-2022 jkadbear licensed under MIT.

As a project developed during Maiyun's participation in the UCSD SRIP program,
The University of California may have claims to this work.

@author: Zhang Maiyun <maz005@ucsd.edu>
Created on Thu May 23 17:28:37 2024

I try to not use `self` in functions that just calculate values and return
them, to allow for easier testing.
Also, while the original implementation passes data with class properties,
this one uses parameters to pass ones that are packet-specific and only
store stable configuration as instance variables.


Implementation checklist:
- [x] Constructor tested
- [x] `init` tested
- [x] `dechirp` tested
- [x] `detect` tested
- [x] `demodulate` tested
- [x] `parse_header` tested
- [x] `dynamic_compensation` tested
- [x] `gray_coding` tested
- [x] `diag_deinterleave` tested
- [x] `hamming_decode` tested
- [x] `sync`
- [x] `decode` tested
- [x] `dewhiten` tested
- [x] `calc_crc` tested

Functions for modulating side stuff:
- [x] `modulate` tested
- [x] `encode` tested
- [x] `gray_decoding` tested
- [x] `calc_sym_num` tested
- [x] `whiten`: (as `dewhiten`)
- [x] `gen_header` tested
- [x] `hamming_encode` tested
- [x] `diag_interleave` tested

These three look like they are not referenced anywhere:
- [ ] `symbols_to_bytes`
- [ ] `calc_payload_len`
- [x] `time_on_air` tested

Other functions:
- [x] `print_bin` (debugging, use logging instead)
- [x] `print_hex` (debugging, use logging instead)
- [x] `log` (debugging, use logging instead)
- [ ] `plot_peak`
- [x] `bit_reduce` (as `xorbits`)
- [x] `word_reduce` merged into `hamming_encode`
- [x] `topn` merged into `dechirp`
- [x] `chirp` tested
- [x] `spec`: use `matplotlib.pyplot.specgram` instead
- [x] `read`: (as `demodulate_file`)
- [x] `write`: use `ndarray.tofile` instead
