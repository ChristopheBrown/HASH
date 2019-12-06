import helper
import pycuda.driver as cuda
from pycuda import compiler, gpuarray, tools, cumath
from pycuda.compiler import SourceModule
import pycuda.autoinit
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class HelperGPU(Helper):

    def __init__(self, message="hello world"):
        self.msg = message
        self.w = []
        self.h = []
        self.chunks = []
        for i in range(len(self.h_init)):
            self.h.append(self.extend_to_32_bit(bin(self.h_init[i])[2:]))
            
        self.copy_kernel_code = ''' 
__global__ void copy_chunks()

}       
'''

        self.extend_kernel_code = ''' 
__global__ void extend_words()

}       
'''
        # compile the kernel code
        self.copy_kernel = compiler.SourceModule(self.copy_kernel)
        self.extend_kernel = compiler.SourceModule(self.extend_kernel)
         
        # get the kernel function from the compiled module
        self.copy   = mod.get_function("copy_chunks")
        self.extend = mod.get_function("extend_words")
        
        
'''
Parallelize the following.

At this point in the algorithm, the message has been coverted to 8-bit binary
representation of the ASCII. This binary representation is put into one long string
where (string_length % 512 = 0).

The string is then broken up into (string_length / 512) chunks.

For each chunk, there will be a copy, an extend, and a compress

The compress can only happen sequentially (not parallel) because there are dependencies
between each consecutive iteration. The copy and extend, however, are not 
bound by this constrainy

Per the wikipedia article (https://en.wikipedia.org/wiki/SHA-2#Pseudocode), 
the instructions here are as follows:

    create a 64-entry message schedule array w[0..63] of 32-bit words
      (copy)   copy chunk into first 16 words w[0..15] of the message schedule array
      (extend) Extend the first 16 words into the remaining 48 words w[16..63] of the message schedule array
    
The for loop within copy (as seen in either the wiki article or the helper.py source code),
simply writes to [0:16) array locations individually, attention should be made to indexing properly
One thread per index is necessary - 16 threads

The foor loop within extend (as seen in either the wiki article or the helper.py source code),
performs several bitwise operations and writes to [16:64) array locations individually
One thread per index is necessary - 48 threads
Alternatively, more threads can be used, e.g.:
- each index is a threadIdx with a multiple of 10 (0, 10, 20, 30,...,)
- each thread in between the multiples of hand a single bitwise operator
i.e. threadIdx = 0 is responsible for index 16, threadIdx = 1 is responsible for s0_p1,
threadIdx = 2 is responsible for s0_p2, threadIdx = 3 is responsible for s0_p3 and so on.
The "in-between" threads calculate a value for the indexing threads to write back the final value


'''

    def copy_chunk_bits(self, new_chunk=None):
        self.w = ['0'*32] * 64
        if new_chunk is None:
            chunk = self.binary_msg_with_padding_and_length[0:512]
        else:
            chunk = new_chunk

        for i in range(16):  # 16 = 512-bit chunk / 32-word segments
            self.w[i] = (chunk[(i*32):((i+1)*32)])  


    def extend_words(self):
        for i in range(16, 64):  # now extend the rest of w[]
            s0_p1 = logic.rotate_bits(self.w[i-15], 7)
            s0_p2 = logic.rotate_bits(self.w[i-15], 18)
            s0_p3 = logic.shift_bits(self.w[i-15], 3)
            s0_xor1 = logic.xor_binary_strings(s0_p1, s0_p2)[2:]
            s0 = logic.xor_binary_strings(s0_xor1, s0_p3)
            s0 = self.extend_to_32_bit(s0)

            s1_p1 = logic.rotate_bits(self.w[i-2], 17)
            s1_p2 = logic.rotate_bits(self.w[i-2], 19)
            s1_p3 = logic.shift_bits(self.w[i-2], 10)
            s1_xor1 = logic.xor_binary_strings(s1_p1, s1_p2)[2:]
            s1 = logic.xor_binary_strings(s1_xor1, s1_p3)
            s1 = self.extend_to_32_bit(s1)

            add1 = logic.add_binary_strings(self.w[i-16], s0)
            add1 = self.extend_to_32_bit(add1)

            add2 = logic.add_binary_strings(self.w[i-7], s1)
            add2 = self.extend_to_32_bit(add2)


            w_i_no_padding = logic.add_binary_strings(add1, add2)
            w_i_no_padding = self.extend_to_32_bit(w_i_no_padding)


            # truncate overflow bits - cap at 32 bits
            w_i = logic.and_binary_strings(w_i_no_pad
            
            
            
            
            
            
            
            
            
            
            
            
            
# bonus function for users who would like to see their system configuration
def dev_info():
    dev_data = pycuda.tools.DeviceData()

    print("CUDA device info")
    print(" - Max threads: {}".format(dev_data.max_threads))
    print(" - Thread blocks per mp: {}".format(dev_data.thread_blocks_per_mp))
    print(" - Shared memory: {}".format(dev_data.shared_memory))
    print("")

    return dev_data
    