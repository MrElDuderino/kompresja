# Autor: Jakub Iwon (236612)

def encode(input_path, output_path):

    dictionary = {}
    entries_no = 256
    dictionary_size = 512
    word_size = 9
    encoded_bit_string = ""

    for i in range(0, entries_no):
        dictionary[bytes([i])] = '{0:09b}'.format(i)

    with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file:

        previous_symbol = input_file.read(1)
        symbol = input_file.read(1)

        while symbol:

            word = previous_symbol + symbol

            if word in dictionary:
                previous_symbol = word
            else:

                encoded_bit_string += dictionary[previous_symbol]

                dictionary[word] = "{0:b}".format(entries_no)
                previous_symbol = symbol

                if entries_no == dictionary_size-1:
                    dictionary_size *= 2
                    word_size += 1
                    update_dictionary_words(dictionary, word_size)

                entries_no += 1

            symbol = input_file.read(1)

        encoded_bit_string += dictionary[previous_symbol]
        encoded_bit_string = add_padding(encoded_bit_string)

        encoded_bytes = []

        for i in range(0, len(encoded_bit_string), 8):
            byte_string = encoded_bit_string[i:i+8]
            encoded_bytes.append(int(byte_string, 2))

        encoded_bytes = bytearray(encoded_bytes)
        output_file.write(encoded_bytes)


def update_dictionary_words(dictionary, word_width):

    for index, word in dictionary.items():
        if len(word) < word_width:
            while len(dictionary[index]) < word_width:
                dictionary[index] = '0' + dictionary[index]

def add_padding(encoded_bit_string):

    padding = 8 - (len(encoded_bit_string) % 8)
    for i in range(0, padding):
        encoded_bit_string += '0'

    padding_info = "{0:08b}".format(padding)
    encoded_bit_string = padding_info + encoded_bit_string
    return encoded_bit_string
