"""
The helper.py file is the implementation of the algoirthm that can be found
on the wikipedia article here: https://en.wikipedia.org/wiki/SHA-2#Pseudocode

You will find similar naming schemes used from the wiki

(c) Christophe Brown 2019

"""
import logic


class Helper:
    h_init = [0x6a09e667, 0xbb67ae85,
              0x3c6ef372, 0xa54ff53a,
              0x510e527f, 0x9b05688c,
              0x1f83d9ab, 0x5be0cd19]

    k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
         0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
         0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
         0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
         0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
         0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
         0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
         0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

    msg = None
    binary_msg = None
    binary_msg_plus_one = None
    binary_msg_with_padding = None
    binary_msg_with_padding_and_length = None
    chunks = []
    w = []
    h = []  # this is iteratively updated later in the program

    digest = ''

    def __init__(self, message="hello world"):
        self.msg = message
        self.w = []
        self.h = []
        self.chunks = []
        for i in range(len(self.h_init)):
            self.h.append(self.extend_to_32_bit(bin(self.h_init[i])[2:]))

    def add_leading_zeros(self, val):
        zeros_to_add = 8 - (len(val))
        if zeros_to_add < 0:
            zeros_to_add = 8 - len(val) % 8
        if zeros_to_add == 0:
            return val

        val = zeros_to_add * '0' + val
        return val

    def extend_to_32_bit(self, val):
        if '0b' in val:
            val = val[2:]

        while len(val) < 32:
            val = self.add_leading_zeros('0' + val)

        return val[-32:]

    def convert_string_to_binary(self):
        ascii_collection = [(ord(c)) for c in self.msg]

        ascii_long_form = ''
        for char in range(len(ascii_collection)):
            without_leading_zeros = bin(ascii_collection[char])[2:]  # index [2:] gets rid of the "0b"
            with_leading_zeros = self.add_leading_zeros(without_leading_zeros)
            ascii_long_form = ascii_long_form + with_leading_zeros

        self.binary_msg = ascii_long_form

        # append 1 (per hash function spec)
        self.binary_msg_plus_one = ascii_long_form + '1'

    def add_padding(self):
        # msg_length + 1 + K = 448 % 512
        msg_length_plus_1 = len(self.binary_msg_plus_one)

        k = 0
        while (msg_length_plus_1 + k) % 512 != 448 % 512:
            k += 1

        self.binary_msg_with_padding = self.binary_msg_plus_one + k * '0'

        # must now satisfy msg_length + 1 + K + 64 % 512 = 0
        # this is accomplished by appending the 64-bit representation of the input msg length
        msg_length_in_binary = bin(len(self.binary_msg))[2:]  # index [2:] gets rid of the "0b"
        msg_length_padding = 0
        while len(msg_length_in_binary) + msg_length_padding < 64:
            msg_length_padding += 1

        self.binary_msg_with_padding_and_length = self.binary_msg_with_padding + msg_length_padding*'0' + msg_length_in_binary

    def pre_process(self):
        self.convert_string_to_binary()
        self.add_padding()
        self.break_message_into_chunks()

    def get_msg_length(self):
        return len(self.binary_msg_with_padding_and_length)

    def break_message_into_chunks(self):
        chunk_count = int(self.get_msg_length() / 512)

        for i in range(chunk_count):
            self.chunks.append(self.binary_msg_with_padding_and_length[(i*512):((i+1)*512)])
        # print(f'found {len(self.chunks)} chunks in self.chunks, the chunk count is {chunk_count}')

    # this function can be done on GPU?
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
            w_i = logic.and_binary_strings(w_i_no_padding, '11111111111111111111111111111111')[2:]
            w_i = self.extend_to_32_bit(w_i)

            self.w[i] = w_i

    def compress(self):
        # this compression function happens for every 512-bit chunk,
        # so after one 512-bit chunk is compressed, it calls this function
        # for the next chunk to be process with the updated 'h' list

        # initialize working registers / variables
        a = self.h[0]
        b = self.h[1]
        c = self.h[2]
        d = self.h[3]
        e = self.h[4]
        f = self.h[5]
        g = self.h[6]
        h = self.h[7]

        for i in range(64):

            # S1
            e_rot_6 = logic.rotate_bits(e, 6)
            e_rot_11 = logic.rotate_bits(e, 11)
            e_rot_25 = logic.rotate_bits(e, 25)
            s1_xor_1 = logic.xor_binary_strings(e_rot_6, e_rot_11)
            _S1 = logic.xor_binary_strings(s1_xor_1, e_rot_25)[2:]
            _S1 = self.extend_to_32_bit(_S1)

            # ch
            e_and_f = logic.and_binary_strings(e, f)
            not_e = logic.not_binary_string(e)
            ch_and_1 = logic.and_binary_strings(not_e, g)
            _ch = logic.xor_binary_strings(e_and_f, ch_and_1)[2:]
            _ch = self.extend_to_32_bit(_ch)

            # temp1
            add_1 = logic.add_binary_strings(h, _S1)
            add_1 = logic.and_binary_strings(add_1, '11111111111111111111111111111111')[2:]
            add_2 = logic.add_binary_strings(_ch, self.extend_to_32_bit(bin(self.k[i])[2:]))
            add_2 = logic.and_binary_strings(add_2, '11111111111111111111111111111111')[2:]
            add_3 = logic.add_binary_strings(add_1, add_2)
            add_3 = logic.and_binary_strings(add_3, '11111111111111111111111111111111')[2:]
            _temp1 = logic.add_binary_strings(add_3, self.w[i])
            _temp1 = logic.and_binary_strings(_temp1, '11111111111111111111111111111111')[2:]
            _temp1 = self.extend_to_32_bit(_temp1)

            # S0
            a_rot_2 = logic.rotate_bits(a, 2)
            a_rot_13 = logic.rotate_bits(a, 13)
            a_rot_22 = logic.rotate_bits(a, 22)
            s0_xor_1 = logic.xor_binary_strings(a_rot_2, a_rot_13)
            _S0 = logic.xor_binary_strings(s0_xor_1, a_rot_22)[2:]
            _S0 = self.extend_to_32_bit(_S0)

            # maj
            a_and_b = logic.and_binary_strings(a, b)
            a_and_c = logic.and_binary_strings(a, c)
            b_and_c = logic.and_binary_strings(b, c)
            maj_xor_1 = logic.xor_binary_strings(a_and_b, a_and_c)
            _maj = logic.xor_binary_strings(maj_xor_1, b_and_c)[2:]
            _maj = self.extend_to_32_bit(_maj)

            # temp2
            _temp2 = logic.and_binary_strings(logic.add_binary_strings(_S0, _maj)[2:], '11111111111111111111111111111111')[2:]
            _temp2 = self.extend_to_32_bit(_temp2)

            # Every ADD operation must & 0xFFFFFFFF (in case of overflow) and be extended back to 32 bits (in case < 32 bits)
            h = self.extend_to_32_bit(g)
            g = self.extend_to_32_bit(f)
            f = self.extend_to_32_bit(e)
            e = logic.and_binary_strings(logic.add_binary_strings(d, _temp1)[2:], '11111111111111111111111111111111')[2:]
            e = self.extend_to_32_bit(e)

            d = self.extend_to_32_bit(c)
            c = self.extend_to_32_bit(b)
            b = self.extend_to_32_bit(a)
            a = logic.and_binary_strings(logic.add_binary_strings(_temp1, _temp2)[2:], '11111111111111111111111111111111')[2:]
            a = self.extend_to_32_bit(a)

        self.h[0] = logic.and_binary_strings(logic.add_binary_strings(self.h[0], a)[2:],
                                             '11111111111111111111111111111111')[2:]
        self.h[0] = self.extend_to_32_bit(self.h[0])

        self.h[1] = logic.and_binary_strings(logic.add_binary_strings(self.h[1], b)[2:],
                                             '11111111111111111111111111111111')[2:]
        self.h[1] = self.extend_to_32_bit(self.h[1])

        self.h[2] = logic.and_binary_strings(logic.add_binary_strings(self.h[2], c)[2:],
                                             '11111111111111111111111111111111')[2:]
        self.h[2] = self.extend_to_32_bit(self.h[2])

        self.h[3] = logic.and_binary_strings(logic.add_binary_strings(self.h[3], d)[2:],
                                             '11111111111111111111111111111111')[2:]
        self.h[3] = self.extend_to_32_bit(self.h[3])

        self.h[4] = logic.and_binary_strings(logic.add_binary_strings(self.h[4], e)[2:],
                                             '11111111111111111111111111111111')[2:]
        self.h[4] = self.extend_to_32_bit(self.h[4])

        self.h[5] = logic.and_binary_strings(logic.add_binary_strings(self.h[5], f)[2:],
                                             '11111111111111111111111111111111')[2:]
        self.h[5] = self.extend_to_32_bit(self.h[5])

        self.h[6] = logic.and_binary_strings(logic.add_binary_strings(self.h[6], g)[2:],
                                             '11111111111111111111111111111111')[2:]
        self.h[6] = self.extend_to_32_bit(self.h[6])

        self.h[7] = logic.and_binary_strings(logic.add_binary_strings(self.h[7], h)[2:],
                                             '11111111111111111111111111111111')[2:]
        self.h[7] = self.extend_to_32_bit(self.h[7])


    def digest(self):
        # print(f'found {len(self.chunks)} chunks in self.chunks')
        for chunk in self.chunks:
            self.copy_chunk_bits(chunk)
            self.extend_words()
            self.compress()
            self.digest = ''
            for h in self.h:
                hex_h = hex(logic.binary_string_to_binary_int(h))
                hex_h_length = len(hex_h)
                hex_h = str(hex_h)[2:]
                if len(hex_h) < 8:
                    hex_h = self.add_leading_zeros(hex_h)
                self.digest += hex_h

        return self.digest
