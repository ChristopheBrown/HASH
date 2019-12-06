def binary_string_to_binary_int(val):
    return int(val, base=2)


def rotate_bits(bits, amount):
    if amount >= len(bits):  # more rotations than bits
        amount = amount % len(bits)

    # slice string in two parts for left and right
    early = bits[0: len(bits) - amount]
    late = bits[len(bits) - amount:]
    # concatenate two parts together
    return late + early


def shift_bits(bits, amount):
    shift = str(bin(binary_string_to_binary_int(bits) >> amount))
    if '0b' in shift:  # [2:0] removes the '0b' on binary values
        shift = shift[2:]
    return shift


def xor_binary_strings(str1, str2):
    a = binary_string_to_binary_int(str1)
    b = binary_string_to_binary_int(str2)
    return bin(a ^ b)


def and_binary_strings(str1, str2):
    a = binary_string_to_binary_int(str1)
    b = binary_string_to_binary_int(str2)
    return bin(a & b)


def not_binary_string(str1):
    a = binary_string_to_binary_int(str1)
    return bin(~a & 0xFFFFFFFF)  # mask result to avoid negatives (chars are not negative)


def add_binary_strings(str1, str2):
    a = binary_string_to_binary_int(str1)
    b = binary_string_to_binary_int(str2)
    return bin(a + b)
