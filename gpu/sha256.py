import helper
import helper_gpu
import numpy as np
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 

class SHA256:
    hasher = None
    msg = None
    chunks = None
    message_length = None

    def __init__(self, message, processor='cpu'):
        if (processor == 'cpu'):
            self.hasher = helper.Helper(message)
        elif (processor == 'gpu'):
            self.hasher = helper_gpu.HelperGPU(message)

        self.msg = message
        self.message_length = len(message)

    def preprocess(self):
        self.hasher.pre_process()
        self.msg = self.hasher.binary_msg_with_padding_and_length
        self.chunks = self.hasher.chunks

    def copy_chunks(self):
        self.hasher.copy_chunk_bits()    
        self.hasher.extend_words()

    def compression_function(self): #comme
        self.hasher.compress()

    def digest(self):
        return self.hasher.digest()


if __name__ == '__main__':
    message = 'the quick brown fox jumped over the lazy dog'     
       
    hash_pre = time.time()
    s = SHA256(message, 'cpu')
    s.preprocess()
    print('(SHA-256) is: {}'.format(s.digest()))
    hash_post = time.time()
    print('Copy chunks finished in {} seconds'.format(s.hasher.timer))
    print('SHA (msg) generated in {} seconds'.format(hash_post-hash_pre))
    
    hash_pre = time.time()
    s = SHA256(message, 'gpu')
    s.preprocess()
    print('(SHA-256) is: {}'.format(s.digest()))
    hash_post = time.time()
    print('Copy chunks finished in {} seconds'.format(s.hasher.timer))
    print('SHA (msg) generated in {} seconds'.format(hash_post-hash_pre))
        
    files = ["1kb.txt" , "10kb.txt", "100kb.txt"]#,"1mb.txt", "bible.txt"]
    sizes = ["1 KB", "10 KB", "100 KB"]#, "1 MB", "Bible"]
    
    files_to_include = len(files)
    
    hash_times = np.zeros((files_to_include,2))
    copy_times = np.zeros((files_to_include,2))
    
    for i in range(len(files)):
        with open(files[i], 'r') as file:
            message = file.read().replace('\n', '')
            
            hash_pre = time.time()
            s = SHA256(message, 'cpu')
            s.preprocess()
            print('(SHA-256) is: {}'.format(s.digest()))
            hash_post = time.time()
            hash_time = hash_post-hash_pre
            print('==========CPU==========')
            print('Copy chunks finished in {} seconds'.format(s.hasher.timer))
            print('SHA ({}) generated in {} seconds'.format(files[i],hash_post-hash_pre))
            
            hash_times[i][0] = hash_time
            copy_times[i][0] = s.hasher.timer
        
        with open(files[i], 'r') as file:
            message = file.read().replace('\n', '')
            
            hash_pre = time.time()
            s = SHA256(message, 'gpu')
            s.preprocess()
            print('(SHA-256) is: {}'.format(s.digest()))
            hash_post = time.time()
            hash_time = hash_post-hash_pre
            print('==========GPU==========')
            print('Copy chunks finished in {} seconds'.format(s.hasher.timer))
            print('SHA ({}) generated in {} seconds'.format(files[i],hash_post-hash_pre))   
            
            hash_times[i][1] = hash_time
            copy_times[i][1] = s.hasher.timer
            
    
               
    scale_max = files_to_include
    mpl.style.use('seaborn')
    #plt.plot(range(0,scale_max),hash_times[:,0],'r',linewidth=2)
    #plt.plot(range(0,scale_max),hash_times[:,1],'b',linewidth=2)
    plt.plot(range(0,scale_max),copy_times[:,0],'c',linewidth=2)
    plt.plot(range(0,scale_max),copy_times[:,1],'y',linewidth=2)
    plt.title('Python vs PyCUDA')
    plt.ylabel('Execution Time (sec)')
    plt.xlabel('Size of Input Text File')
    x = np.array([0,1,2,3])
    plt.xticks(x, sizes)
    #plt.yscale('log')
    #cpu_plot_hash = mpatches.Patch(color='r', label='Total hash time (CPU)')
    #gpu_plot_hash = mpatches.Patch(color='b', label='Total hash time (GPU)')
    cpu_plot_copy = mpatches.Patch(color='c', label='Copy time (CPU)')
    gpu_plot_copy = mpatches.Patch(color='y', label='Copy time (GPU)')
    plt.legend(handles=[cpu_plot_copy, gpu_plot_copy]) # 
    #plt.legend(handles=[cpu_plot_hash, gpu_plot_hash, cpu_plot_copy, gpu_plot_copy]) # 
    plt.savefig('cuda_plot.png')
    plt.show()    
    
    
        

    
 