# Autor: Jakub Iwon (236612)

from DoubleError import DoubleError
import sys
import random


H = [[0, 0, 0, 1, 1, 1, 1, 0],
     [0, 1, 1, 0, 0, 1, 1, 0],
     [1, 0, 1, 0, 1, 0, 1, 0],
     [1, 1, 1, 1, 1, 1, 1, 1]]

G = [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, 1],
     [0, 1, 1, 1],
     [1, 0, 1, 1],
     [1, 1, 0, 1],
     [1, 1, 1, 0]]


def matrix_multiplication(matrix, vector):

    result_matrix = [0 for x in range(len(matrix))]

    for i in range(len(matrix)):
        for k in range(len(vector)):
            result_matrix[i] = (result_matrix[i] + matrix[i][k] * vector[k]) % 2

    return result_matrix

def check_parity(a):
    return matrix_multiplication(H, a)

def get_hamming_code(a):

    code = matrix_multiplication(G, a)
    return code

def bit_array_to_byte(a):

    bitstring = ''.join([str(n) for n in a])
    return int(bitstring, 2)


def decode_hamming_code(a):

    parity = check_parity(a)
    syndrome = bit_array_to_byte(parity[:-1])
    parity_bit = parity[-1]
    decoded = a[:4]

    if syndrome != 0 and parity_bit == 1:
        bit_num = syndrome-1
        if bit_num < 4:
            decoded[bit_num] = (decoded[bit_num]+1) % 2
    elif syndrome != 0 and parity_bit == 0:
        raise DoubleError("Double error occurred")

    return decoded

def to_bit_array(b):
    bit_array = []
    for i in range(7,-1,-1):
        bit_array.append(1 & b >> i)
    return bit_array


def encode(input_path, output_path):

    with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file:

        b = input_file.read(1)
        count = 0

        while b:
            bit_array = to_bit_array(ord(b))
            code1 = get_hamming_code(bit_array[:4])
            code2 = get_hamming_code(bit_array[4:])
            output_file.write(bytes([bit_array_to_byte(code1)]))
            output_file.write(bytes([bit_array_to_byte(code2)]))
            b = input_file.read(1)
            count += 1


def decode(input_path, output_path):

    with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file:

        b = input_file.read(1)
        double_errors = 0

        while b:

            bit_array = to_bit_array(ord(b))

            try:
                decoded1 = decode_hamming_code(bit_array)
            except DoubleError:
                decoded1 = bit_array[4:]
                double_errors += 1

            b = input_file.read(1)
            bit_array = to_bit_array(ord(b))

            try:
                decoded2 = decode_hamming_code(bit_array)
            except DoubleError:
                decoded2 = bit_array[4:]
                double_errors += 1

            decoded = decoded1 + decoded2
            output_file.write(bytes([bit_array_to_byte(decoded)]))
            b = input_file.read(1)

        return double_errors

def noise(probability, input_path, output_path):

    with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file:

        b = input_file.read(1)

        while b:
            bit_array = to_bit_array(ord(b))
            for i in range(len(bit_array)):
                if random.random() <= probability:
                    bit_array[i] = bit_array[i]^1
            output_file.write(bytes([bit_array_to_byte(bit_array)]))
            b = input_file.read(1)

def check(path1, path2):

    with open(path1, 'rb') as file1, open(path2, 'rb') as file2:

        b1 = file1.read(1)
        b2 = file2.read(1)
        errors = 0

        while b1 and b2:

            bit_array1 = to_bit_array(ord(b1))
            bit_array2 = to_bit_array(ord(b2))
            if(bit_array1[:4] != bit_array2[:4]):
                errors += 1
            if(bit_array1[4:] != bit_array2[4:]):
                errors += 1
            b1 = file1.read(1)
            b2 = file2.read(1)

        return errors

def main():

    if len(sys.argv) < 4:
        print("Za mała liczba argumentów wejściowych.")
        print("Sposób uruchomienia <opcja: koder, szum, dekoder, sprawdz> (prawdopodobieństwo) <plik wejściowy> <plik wyjściowy>")
        sys.exit()

    option = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]

    try:
        if option == "koder":
            encode(input_path, output_path)
        elif option == "szum":
            probability = float(sys.argv[2])
            if probability < 0 or probability > 1:
                print("Prawdopodobieństwo powinno być z zakresu 0...1")
                sys.exit(0)
            input_path = sys.argv[3]
            output_path = sys.argv[4]
            noise(probability, input_path, output_path)
        elif option == "dekoder":
            double_errors = decode(input_path, output_path)
            print("Liczba podwójnych błedów = {}".format(double_errors))
        elif option == "sprawdz":
            errors = check(input_path, output_path)
            print("Liczba różniących się bloków = {}".format(errors))
        else:
            print("Niepoprawna opcja. Dostępne opcje: koder, szum, dekoder, sprawdz")

    except FileNotFoundError:
        print("Nieistniejący plik.")


if __name__ == '__main__':
    main()
