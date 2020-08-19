# Autor: Jakub Iwon (236612)

import math
import constant


def calculate_entropy(count, n):

    entropy = 0
    for b in count:
        if b == 0:
            continue
        entropy += b * (math.log(n, 2) - math.log(b, 2))

    entropy /= n
    return entropy


def count_bytes(input_file):

    count = [0 for i in range(constant.SIZE)]
    conditional_count = [[0 for i in range(constant.SIZE)] for j in range(constant.SIZE)]
    n = 0

    with open(input_file, "rb") as f:

        byte = f.read(1)

        if byte:
            byte_int = int.from_bytes(byte, "big")
            count[byte_int] += 1
            conditional_count[0][byte_int] += 1
            n += 1
            previous_byte = byte_int
            byte = f.read(1)

        while byte:
            byte_int = int.from_bytes(byte, "big")
            count[byte_int] += 1
            conditional_count[previous_byte][byte_int] += 1
            n += 1
            previous_byte = byte_int
            byte = f.read(1)
    return count, conditional_count, n


def get_entropy(input_file):

    count, _, n = count_bytes(input_file)
    entropy = calculate_entropy(count, n)
    return entropy
