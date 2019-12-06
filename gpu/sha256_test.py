import unittest
import sha256
import helper
import logic


class MyTestCase(unittest.TestCase):
    def test_instance(self):
        sha = sha256.SHA256('Hello world!')
        self.assertIsNotNone(sha)

    def test_leading_zeros(self):
        h = helper.Helper()
        too_short = h.add_leading_zeros('1234')
        just_right = h.add_leading_zeros('12345678')
        too_long = h.add_leading_zeros('123456789')

        self.assertEqual(too_short, '00001234')
        self.assertEqual(just_right, '12345678')
        self.assertEqual(too_long, '0000000123456789')

    def test_convert_string_to_binary(self):
        h = helper.Helper()

        small = helper.Helper('a')
        medium = helper.Helper('example')
        large = helper.Helper('this is a long string!')

        small.convert_string_to_binary()
        medium.convert_string_to_binary()
        large.convert_string_to_binary()

        self.assertEqual(small.binary_msg_plus_one, '011000011')
        self.assertEqual(medium.binary_msg_plus_one, '011001010111100001100001011011010111000001101100011001011')
        self.assertEqual(large.binary_msg_plus_one, '011101000110100001101001011100110010000001101001011100110010000001100001001000000110110001101111011011100110011100100000011100110111010001110010011010010110111001100111001000011')

    def test_add_padding(self):
        small = helper.Helper('a')
        medium = helper.Helper('example' * 10)
        large = helper.Helper('this is a long string!' * 100)

        small.convert_string_to_binary()
        small.add_padding()

        medium.convert_string_to_binary()
        medium.add_padding()

        large.convert_string_to_binary()
        large.add_padding()

        # print(large.get_msg_length())

        self.assertEqual(len(small.binary_msg_with_padding_and_length) % 512, 0)
        self.assertEqual(len(medium.binary_msg_with_padding_and_length) % 512, 0)
        self.assertEqual(len(large.binary_msg_with_padding_and_length) % 512, 0)

    def test_breaking_into_chunks(self):
        large = helper.Helper('this is a long string!' * 100)
        large.convert_string_to_binary()
        large.add_padding()
        large.break_message_into_chunks()

        self.assertEqual(len(large.chunks), 35)

        # print(large.chunks)

    def test_copy_chunks(self):
        medium = helper.Helper('example' * 10)
        medium.convert_string_to_binary()
        medium.add_padding()
        medium.break_message_into_chunks()

        medium.copy_chunk_bits()
        for i in range(16):
            self.assertEqual(len(medium.w[i]), 32)

        small = helper.Helper('a')
        small.convert_string_to_binary()
        small.add_padding()
        small.break_message_into_chunks()

        small.copy_chunk_bits()
        for i in range(16):
            self.assertEqual(len(small.w[i]), 32)

    # Arithmetic/shift/rotate only tests ARITHMETIC - it does not check for aligned zeros (i.e. '0010' instead of '10')

    def test_rotate_bits(self):
        bits = '00101'
        rotated_bits = logic.rotate_bits(bits, 2)  # shift right by 2 spaces
        excess_rotations = logic.rotate_bits(bits, 14)  # more rotations than bits (cyclic)
        self.assertEqual(rotated_bits, '01001')
        self.assertEqual(excess_rotations, '01010')

    def test_shift_bits(self):
        bits = '10100'
        tiny_shift = logic.shift_bits(bits, 1)  # test that zeros fill in
        big_shift = logic.shift_bits(bits, 3)  # test drop-off of bits
        self.assertEqual(tiny_shift, '1010')
        self.assertEqual(big_shift, '10')

    def test_arithmetic(self):
        byte1 = '10101010'
        byte2 = '10010010'
        _xor = logic.xor_binary_strings(byte1, byte2)[2:]
        _xor = helper.Helper.add_leading_zeros(helper.Helper(), _xor)

        _and = logic.and_binary_strings(byte1, byte2)[2:]
        _and = helper.Helper.add_leading_zeros(helper.Helper(), _and)

        _not = logic.not_binary_string(byte1)[2:]

        _add = logic.add_binary_strings(byte1, byte2)[2:]

        self.assertEqual(_xor, '00111000')
        self.assertEqual(_and, '10000010')
        self.assertEqual(_not, '11111111111111111111111101010101')
        self.assertEqual(_add, '100111100')

    def test_extend_words(self):
        short = helper.Helper('abc')
        short.convert_string_to_binary()
        short.add_padding()
        short.break_message_into_chunks()

        short.copy_chunk_bits()
        short.extend_words()
        for i in range(64):
            self.assertEqual(len(short.w[i]), 32)

        # randomly-chosen assertions throughout w to validate the extension computation
        self.assertEqual(logic.binary_string_to_binary_int(short.w[16]), 1633837952)
        self.assertEqual(logic.binary_string_to_binary_int(short.w[43]), 657669027)
        self.assertEqual(logic.binary_string_to_binary_int(short.w[58]), 2682456414)

    def test_compress(self):
        short = helper.Helper('abc')
        short.convert_string_to_binary()
        short.add_padding()
        short.break_message_into_chunks()

        short.copy_chunk_bits()
        short.extend_words()
        short.compress()

        self.assertEqual(short.h[0], '10111010011110000001011010111111')
        self.assertEqual(short.h[1], '10001111000000011100111111101010')
        self.assertEqual(short.h[2], '01000001010000010100000011011110')
        self.assertEqual(short.h[3], '01011101101011100010001000100011')
        self.assertEqual(short.h[4], '10110000000000110110000110100011')
        self.assertEqual(short.h[5], '10010110000101110111101010011100')
        self.assertEqual(short.h[6], '10110100000100001111111101100001')
        self.assertEqual(short.h[7], '11110010000000000001010110101101')

        long = helper.Helper('abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq')
        long.convert_string_to_binary()
        long.add_padding()
        long.break_message_into_chunks()

        long.copy_chunk_bits()
        long.extend_words()
        long.compress()

        self.assertEqual(long.h[0], '10000101111001100101010111010110')
        self.assertEqual(long.h[1], '01000001011110100001011110010101')
        self.assertEqual(long.h[2], '00110011011000110011011101101010')
        self.assertEqual(long.h[3], '01100010010011001101111001011100')
        self.assertEqual(long.h[4], '01110110111000001001010110001001')
        self.assertEqual(long.h[5], '11001010110001011111100000010001')
        self.assertEqual(long.h[6], '11001100010010110011001011000001')
        self.assertEqual(long.h[7], '11110010000011100101001100111010')

    def test_digest(self):
        short = helper.Helper('abc')
        short.convert_string_to_binary()
        short.add_padding()
        short.break_message_into_chunks()

        long = helper.Helper('abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq')
        long.convert_string_to_binary()
        long.add_padding()
        long.break_message_into_chunks()

        self.assertEqual(short.digest(), 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
        self.assertEqual(long.digest(), '248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1')


if __name__ == '__main__':
    unittest.main()

