# Autor: Jakub Iwon (236612)

from binary_tree import BinaryTree
import constant


def decode(input_path, output_path):

    try:
        with open(input_path, 'rb') as file, open(output_path, 'wb') as output:

            bit_string = ""

            byte = file.read(1)
            while byte:

                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            padded_info = bit_string[:8]
            padding = int(padded_info, 2)

            bit_string = bit_string[8:]
            if padding > 0:
                bit_string = bit_string[:-1 * padding]

            tree = BinaryTree(alphabet_size=constant.SIZE)
            i = 0
            current_node = tree.root
            symbols = bytearray()

            while i < len(bit_string):

                if is_leaf(current_node):
                    if tree.nyt_node is current_node:
                        symbol = int(bit_string[i:i+8], 2)
                        i += 8
                    else:
                        symbol = current_node.symbol

                    tree.insert(symbol)
                    current_node = tree.root
                    symbols.append(symbol)

                else:

                    bit = bit_string[i]
                    if bit == '0':
                        current_node = current_node.left
                    else:
                        current_node = current_node.right

                    if i == len(bit_string) - 1:
                        if is_leaf(current_node):
                            if tree.nyt_node is current_node:
                                symbol = int(bit_string[i:i + 8], 2)
                                i += 8
                            else:
                                symbol = current_node.symbol
                            symbols.append(symbol)
                            tree.insert(symbol)

                    i += 1

            output.write(bytes(symbols))

    except FileNotFoundError:
        print("Plik " + input_path + " nie istnieje.")


def is_leaf(node):

    if node.left is None and node.right is None:
        return True
    else:
        return False
