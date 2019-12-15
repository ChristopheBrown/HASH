# HASH

HASH stands for Hardware Acceleration of Secure Hashing. This repo is an engineering study of SHA-256 algorithm parallelized using python and pyCUDA. 

The cpu source code (developed with anaconda python 3.7) implementation adapts from the SHA-256 wikipedia artcile pseudocode here: https://en.wikipedia.org/wiki/SHA-2#Pseudocode

contact: cb3534@columbia.edu

The cpu implementation is unit tested and is consistent with hashing algorithms that can be found online.

To run: 

-Ensure CUDA, Python, matplotlib, and numpy are installed and runnable on your machine.
-Clone this repo
-Open "gpu/sha256.py" and modify the "files" array in __main__ to run the code with whichever files you like. Large files will take longer
-Run "python sha256.py"
-Optional, modify the matplotlib code at the bottom to produce graphs.


Useful links in making this:
 -SHA-256 calculator: https://xorbin.com/tools/sha256-hash-calculator
 -Decimal-Hex-Binary converter: https://www.mathsisfun.com/binary-decimal-hexadecimal-converter.html
 -Examples used for unit testing: https://csrc.nist.gov/csrc/media/projects/cryptographic-standards-and-guidelines/documents/examples/sha256.pdf
 -Step-by-step SHA-256: https://tools.ietf.org/html/rfc4634#page-6
 
 
