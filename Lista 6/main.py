# Autor: Jakub Iwon (236612)

import sys
import os
from math import log10, isnan, nan


def parse_tga(file, signed=False):

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
            color_map[y][x] = tuple(reversed(((read_int(file, 1, signed), read_int(file, 1, signed), read_int(file, 1, signed)))))

    end_bytes = []
    append_to_list(end_bytes, file.read())

    return start_bytes, color_map, end_bytes


def to_tga(start_bytes, color_map, end_bytes, output_path, signed=False):

    with open(output_path, 'wb') as file:

        file.write(bytes(start_bytes))

        map_width = len(color_map[0])
        map_height = len(color_map)

        for y in range(map_height):
            for x in range(map_width):
                (r, g, b) = color_map[y][x]
                file.write(b.to_bytes(1, byteorder='little', signed=signed))
                file.write(g.to_bytes(1, byteorder='little', signed=signed))
                file.write(r.to_bytes(1, byteorder='little', signed=signed))

        file.write(bytes(end_bytes))


def read_int(file, n, signed):
    return int.from_bytes(file.read(n), 'little', signed=signed)


def append_to_list(byte_list, file_bytes):

    for b in file_bytes:
        byte_list.append(b)


def encode(input_path, output_path, bits_no):

    interval_size = 256 // (2 ** bits_no)

    with open(input_path, 'rb') as input_file:

        start_bytes, color_map, end_bytes = parse_tga(input_file)
        color_map_height = len(color_map)
        color_map_width = len(color_map[0])
        encoded_color_map = [[None for _ in range(color_map_width)] for _ in range(color_map_height)]
        recons_r = recons_g = recons_b = 0

        for y in range(color_map_height):
            for x in range(color_map_width):
                (r, g, b) = color_map[y][x]
                enc_diff_r = (r - recons_r) // interval_size
                enc_diff_g = (g - recons_g) // interval_size
                enc_diff_b = (b - recons_b) // interval_size
                d_r = enc_diff_r * interval_size + interval_size//2
                d_g = enc_diff_g * interval_size + interval_size//2
                d_b = enc_diff_b * interval_size + interval_size//2

                encoded_color_map[y][x] = (enc_diff_r, enc_diff_g, enc_diff_b)
                recons_r += d_r
                recons_g += d_g
                recons_b += d_b

        to_tga(start_bytes, encoded_color_map, end_bytes, output_path, signed=True)
        return color_map


def decode(input_path, output_path, bits_no):

    interval_size = 256 // (2 ** bits_no)

    with open(input_path, 'rb') as input_file:

        start_bytes, color_map, end_bytes = parse_tga(input_file, signed=True)
        color_map_height = len(color_map)
        color_map_width = len(color_map[0])
        decoded_color_map = [[None for _ in range(color_map_width)] for _ in range(color_map_height)]
        recons_r = recons_g = recons_b = 0

        for y in range(color_map_height):
            for x in range(color_map_width):

                (r, g, b) = color_map[y][x]
                r = r * interval_size + interval_size//2
                g = g * interval_size + interval_size//2
                b = b * interval_size + interval_size//2

                d_r = r + recons_r
                d_g = g + recons_g
                d_b = b + recons_b

                d_r = 255 if d_r > 255 else d_r
                d_g = 255 if d_g > 255 else d_g
                d_b = 255 if d_b > 255 else d_b

                d_r = 0 if d_r < 0 else d_r
                d_g = 0 if d_g < 0 else d_g
                d_b = 0 if d_b < 0 else d_b

                decoded_color_map[y][x] = (d_r, d_g, d_b)
                recons_r += r
                recons_g += g
                recons_b += b


        to_tga(start_bytes, decoded_color_map, end_bytes, output_path, signed=False)
        return decoded_color_map


def divide(nominator, denominator):
    return nominator/denominator if denominator != 0 else nan


def print_errors(color_map, decoded_color_map):

    color_map_height = len(color_map)
    color_map_width = len(color_map[0])
    n = color_map_height * color_map_width
    mse = mse_r = mse_g = mse_b = 0
    snr = snr_r = snr_g = snr_b = 0

    for y in range(color_map_height):
        for x in range(color_map_width):
            (r, g, b) = color_map[y][x]
            (dec_r, dec_g, dec_b) = decoded_color_map[y][x]
            red_error, green_error, blue_error = (r - dec_r)**2, (g - dec_g)**2, (b - dec_b)**2
            mse += red_error + green_error + blue_error
            mse_r += red_error
            mse_g += green_error
            mse_b += blue_error
            snr += r ** 2 + g ** 2 + b ** 2
            snr_r += r ** 2
            snr_g += g ** 2
            snr_b += b ** 2


    mse = divide(mse, 3 * n)
    mse_r = divide(mse_r, n)
    mse_g = divide(mse_g, n)
    mse_b = divide(mse_b, n)
    snr = divide(divide(snr, 3 * n), mse)
    snr_r = divide(divide(snr_r, n), mse_r)
    snr_g = divide(divide(snr_g, n), mse_g)
    snr_b = divide(divide(snr_b, n), mse_b)

    print("mse = {}".format(mse))
    print("mse(r) = {}".format(mse_r))
    print("mse(g) = {}".format(mse_g))
    print("mse(b) = {}".format(mse_b))
    print("SNR = {} ({}dB)".format(snr, 10*log10(snr)))
    print("SNR(r) = {} ({}dB)".format(snr_r, 10*log10(snr_r)))
    print("SNR(g) = {} ({}dB)".format(snr_g, 10*log10(snr_g)))
    print("SNR(b) = {} ({}dB)".format(snr_b, 10*log10(snr_b)))


def main():

    if len(sys.argv) < 3:
        print("Za mała liczba argumentów wejściowych.")
        print("Sposób uruchomienia <obraz do zakodowania/odkodowania> <liczba bitów kwantyzatora>")
        sys.exit()

    input_path = sys.argv[1]
    bits_no = int(sys.argv[2])
    directory = os.path.dirname(input_path)
    if directory:
        directory += "/"
    output_path = directory + "encoded.tga"


    if bits_no < 1 or bits_no > 7:
        print("Liczba bitów kwantyzatora powinna być z zakresu 1...7")
        sys.exit()

    try:

        decoded_path = directory + "decoded.tga"
        color_map = encode(input_path, output_path, bits_no)
        decoded_color_map = decode(output_path, decoded_path, bits_no)
        print_errors(color_map, decoded_color_map)


    except FileNotFoundError:
        print("Plik " + input_path + " nie istnieje.")
        sys.exit()


if __name__ == '__main__':

    main()
