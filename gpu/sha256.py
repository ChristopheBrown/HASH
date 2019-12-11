import helper
import helper_gpu
import time

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
        
    files = ["1kb.txt" , "10kb.txt", '100kb.txt']
    
    for f in files:
        with open(f, 'r') as file:
            message = file.read().replace('\n', '')
            
            hash_pre = time.time()
            s = SHA256(message, 'cpu')
            s.preprocess()
            print('(SHA-256) is: {}'.format(s.digest()))
            hash_post = time.time()
            print('==========CPU==========')
            print('Copy chunks finished in {} seconds'.format(s.hasher.timer))
            print('SHA ({}) generated in {} seconds'.format(f,hash_post-hash_pre))   
        
        with open(f, 'r') as file:
            message = file.read().replace('\n', '')
            
            hash_pre = time.time()
            s = SHA256(message, 'gpu')
            s.preprocess()
            print('(SHA-256) is: {}'.format(s.digest()))
            hash_post = time.time()
            print('==========GPU==========')
            print('Copy chunks finished in {} seconds'.format(s.hasher.timer))
            print('SHA ({}) generated in {} seconds'.format(f,hash_post-hash_pre))      
    
        

    
 