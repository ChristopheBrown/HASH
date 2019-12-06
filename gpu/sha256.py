import helper
import helper_gpu


class SHA256:
    msg = None
    chunks = None
    message_length = None

    def __init__(self, message):
        self.hasher = helper.Helper(message)

        self.msg = message
        self.message_length = len(message)

    def preprocess(self):
        self.hasher.pre_process()
        self.msg = self.hasher.binary_msg_with_padding_and_length
        self.chunks = self.hasher.chunks

    def copy_chunks(self):
        self.hasher.copy_chunk_bits()
        self.hasher.extend_words()

    def compression_function(self):
        self.hasher.compress()

    def digest(self):
        return self.hasher.digest()


if __name__ == '__main__':
    message = 'the quick brown fox jumped over the lazy dog'

    s = SHA256(message)
    s.preprocess()
    # ensure your version of python supports the statement below
    print('input message is: {} \ndigest (SHA-256) is: {}'.format(message, s.digest()))
