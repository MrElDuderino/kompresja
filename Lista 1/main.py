#Autor: Jakub Iwon (236612)

import math
import sys

import constant


def calculate_entropy(count, n):

    entropy = 0
    for b in count:
        if b == 0:
            continue
        entropy += b * (math.log(n, 2) - math.log(b, 2))

    entropy /= n
    return entropy


def calculate_conditional_entropy(count, conditional_count, n):

    conditional_entropy = 0

    for i, b_x in enumerate(count):

        if b_x == 0:
            continue

        for b_yx in conditional_count[i]:

            if b_yx == 0:
                continue

            conditional_entropy += b_yx * (math.log(b_x, 2) - math.log(b_yx, 2))

    conditional_entropy = conditional_entropy/n

    return conditional_entropy


def count_bytes():

    count = [0 for i in range(constant.SIZE)]
    conditional_count = [[0 for i in range(constant.SIZE)] for j in range(constant.SIZE)]
    n = 0

    with open(sys.argv[1], "rb") as f:

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


def main():

    count, conditional_count, n = count_bytes()
    entropy = calculate_entropy(count, n)
    conditional_entropy = calculate_conditional_entropy(count, conditional_count, n)
    print("\nNazwa pliku: " + sys.argv[1])
    print("\nEntropia: " + str(entropy))
    print("Entropia warunkowa: " + str(conditional_entropy))
    print("\nRóżnica: " + str(entropy - conditional_entropy))


main()
