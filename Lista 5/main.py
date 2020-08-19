# Autor: Jakub Iwon (236612)

import sys
from math import log10, isnan, nan


def parse_tga(input_path):

    with open(input_path, 'rb') as file:

        start_bytes = []
        append_to_list(start_bytes, file.read(12))

        image_width_bytes = file.read(2)
        image_height_bytes = file.read(2)

        append_to_list(start_bytes, image_width_bytes)
        append_to_list(start_bytes, image_height_bytes)

        image_width = int.from_bytes(image_width_bytes, 'little')
        image_height = int.from_bytes(image_height_bytes, 'little')

        append_to_list(start_bytes, file.read(2))

        color_map = [[None for _ in range(image_width)] for _ in range(image_height)]
        for y in range(image_height):
            for x in range(image_width):
                color_map[y][x] = tuple(reversed(((read_int(file, 1), read_int(file, 1), read_int(file, 1)))))

        end_bytes = []
        append_to_list(end_bytes, file.read())

        return start_bytes, color_map, end_bytes


def read_int(file, n):
    return int.from_bytes(file.read(n), 'little')


def append_to_list(byte_list, file_bytes):

    for b in file_bytes:
        byte_list.append(b)


def to_tga(start_bytes, color_map, end_bytes, output_path):

    with open(output_path, 'wb') as file:

        file.write(bytes(start_bytes))

        map_width = len(color_map[0])
        map_height = len(color_map)


        for y in range(map_height):
            for x in range(map_width):
                (r, g, b) = color_map[y][x]
                file.write(bytes([b]))
                file.write(bytes([g]))
                file.write(bytes([r]))


        file.write(bytes(end_bytes))


def quantization(color_map, red_bits, green_bits, blue_bits,):

    red_size = 256 // (2**red_bits)
    green_size = 256 // (2**green_bits)
    blue_size = 256 // (2**blue_bits)

    n = 0
    mse = mse_red = mse_green = mse_blue = 0
    snr = snr_red = snr_green = snr_blue = 0

    map_width = len(color_map[0])
    map_height = len(color_map)

    for y in range(map_height):
        for x in range(map_width):
            (r, g, b) = color_map[y][x]
            rq = (r // red_size) * red_size + (red_size//2)
            gq = (g // green_size) * green_size + (green_size // 2)
            bq = (b // blue_size) * blue_size + (blue_size // 2)
            n += 1
            red_error, green_error, blue_error = (r - rq)**2, (g - gq)**2, (b - bq)**2
            mse_red += red_error
            mse_green += green_error
            mse_blue += blue_error
            mse += red_error + green_error + blue_error
            snr += r**2 + g**2 + b**2
            snr_red += r**2
            snr_green += g**2
            snr_blue += b**2
            color_map[y][x] = (rq, gq, bq)

    mse =  divide(mse, 3*n)
    mse_red = divide(mse_red, n)
    mse_green = divide(mse_green, n)
    mse_blue = divide(mse_blue, n)
    snr = divide(divide(snr, 3*n), mse)
    snr_red = divide(divide(snr_red, n), mse_red)
    snr_green = divide(divide(snr_green, n), mse_green)
    snr_blue = divide(divide(snr_blue, n), mse_blue)

    return color_map, mse, mse_red, mse_green, mse_blue, snr, snr_red, snr_green, snr_blue

def divide(nominator, denominator):
    return nominator/denominator if denominator != 0 else nan

def toDecibels(n):

    return 10*log10(n) if not isnan(n) else nan

def main():

    if len(sys.argv) < 6:
        print("Za mała liczba argumentów wejściowych.")
        print("Sposób uruchomienia <obraz wejściowy> <obraz wyjściowy> <# bitów czerwień> <# bitów zieleń> <# bitów niebieski>")
        sys.exit()

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    red_bits = int(sys.argv[3])
    green_bits = int(sys.argv[4])
    blue_bits = int(sys.argv[5])

    try:
        start_bytes, color_map, end_bytes = parse_tga(input_path)
        color_map, mse, mse_r, mse_g, mse_b, snr, snr_red, snr_green, snr_blue = quantization(color_map, red_bits, green_bits, blue_bits)
        to_tga(start_bytes, color_map, end_bytes, output_path)
        print("mse = {}".format(mse))
        print("mse(r) = {}".format(mse_r))
        print("mse(g) = {}".format(mse_g))
        print("mse(b) = {}".format(mse_b))
        print("SNR = {} ({}dB)".format(snr, 10*log10(snr)))
        print("SNR(r) = {} ({}dB)".format(snr_red, toDecibels(snr_red)))
        print("SNR(g) = {} ({}dB)".format(snr_green, toDecibels(snr_green)))
        print("SNR(b) = {} ({}dB)".format(snr_blue, toDecibels(snr_blue)))


    except FileNotFoundError:
        print("Plik " + input_path + " nie istnieje.")
        sys.exit()


if __name__ == '__main__':
    main()
