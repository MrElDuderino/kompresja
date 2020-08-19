# Autor: Jakub Iwon (236612)

def decode(input_path, output_path):

    with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file:

        dictionary = {}
        entries_no = 256
        dictionary_size = 512
        word_size = 9

        for i in range(0, entries_no):
            dictionary[i] = bytes([i])

        bit_string = convert_to_bit_string(input_file)

        previous_code = int(bit_string[:word_size], 2)
        output_file.write(dictionary[previous_code])
        ind = word_size
        bit_length = len(bit_string)

        while (ind + word_size) <= bit_length:

            previous = dictionary[previous_code]
            code = int(bit_string[ind:ind+word_size], 2)
            ind += word_size

            if code in dictionary:
                entry = dictionary[code]
                output_file.write(entry)
                dictionary[entries_no] = previous + bytes([entry[0]])
            else:
                entry = previous + bytes([previous[0]])
                dictionary[entries_no] = entry
                output_file.write(entry)

            entries_no += 1

            if entries_no == dictionary_size-1:
                dictionary_size *= 2
                word_size += 1

            previous_code = code



def convert_to_bit_string(input_file):

    bit_string = ""
    b = input_file.read(1)

    while b:
        b = ord(b)
        code = bin(b)[2:].rjust(8, '0')
        bit_string += code
        b = input_file.read(1)

    padded_info = bit_string[:8]
    padding = int(padded_info, 2)

    bit_string = bit_string[8:]
    if padding > 0:
        bit_string = bit_string[:-1 * padding]

    return bit_string