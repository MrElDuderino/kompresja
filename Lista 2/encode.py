# Autor: Jakub Iwon (236612)

from binary_tree import BinaryTree
import constant


def encode(input_path, output_path):

    try:
        with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file:

            tree = BinaryTree(alphabet_size=constant.SIZE)
            symbol = input_file.read(1)
            symbols_count = 0

            while symbol:

                tree.insert(symbol)
                symbol = input_file.read(1)
                symbols_count += 1

            encoded_bytes = tree.get_encoded_bytes()
            print("Stopień kompresji: " + str(symbols_count/len(encoded_bytes)))
            output_file.write(bytes(encoded_bytes))
            # tree.print_tree()

    except FileNotFoundError:
        print("Plik " + input_path + " nie istnieje.")
