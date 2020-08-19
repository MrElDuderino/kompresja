# Autor: Jakub Iwon (236612)

from node import Node


def to_bit_string(n):
    return ''.join(str(1 & int(n) >> i) for i in range(8)[::-1])


def get_sibling(node):

    if node.parent is not None:
        if node.parent.right is not node:
            return node.parent.right
        else:
            return node.parent.left


class BinaryTree:

    def __init__(self, alphabet_size):

        self.size = 2*alphabet_size+1
        self.root = Node(n=self.size, parent=None)
        self.nyt_node = self.root
        self.present_symbols = {}
        self.encoded_bytes = bytearray()
        self.bit_buffer = ''
        self.count = 0
        self.sum = 0
        self.blocks = {0: [self.root]}

    def insert(self, symbol):

        if symbol in self.present_symbols:

            node = self.present_symbols[symbol]
            self.add_to_buffer(node.bit_path)
            self.update_parent_path(node)

        else:

            if isinstance(symbol, int):
                num = symbol
            else:
                num = ord(symbol)

            self.add_to_buffer(self.nyt_node.bit_path)
            self.add_to_buffer(to_bit_string(num))
            self.insert_symbol(symbol)

    def insert_symbol(self, symbol):

        left_n = self.nyt_node.n-2
        right_n = self.nyt_node.n-1
        self.nyt_node.left = Node(n=left_n, parent=self.nyt_node)
        self.nyt_node.right = Node(n=right_n, parent=self.nyt_node, symbol=symbol, weight=0)

        self.add_to_block(self.nyt_node.left)
        self.add_to_block(self.nyt_node.right)

        self.nyt_node.left.bit_path = self.nyt_node.bit_path + '0'
        self.nyt_node.right.bit_path = self.nyt_node.bit_path + '1'

        self.present_symbols[symbol] = self.nyt_node.right

        self.update_parent_path(self.nyt_node.right)

        self.nyt_node = self.nyt_node.left

    def update_parent_path(self, node_to_update):

        if node_to_update is None:
            return

        max_node = self.find_largest(node_to_update)
        if max_node and max_node is not node_to_update.parent and max_node is not node_to_update:
            self.swap_nodes(node_to_update, max_node)
        else:
            self.delete_from_block(node_to_update)
            node_to_update.weight += 1
            self.add_to_block(node_to_update)
            self.update_parent_path(node_to_update.parent)

    def print_tree(self):
        self.traverse(self.root)

    def traverse(self, node):

        if node is None:
            return

        node.print_node()
        self.traverse(node.left)
        self.traverse(node.right)

    def swap_nodes(self, node1, node2):

        n1 = node1.n
        n2 = node2.n

        node1.n = n2
        node2.n = n1

        if node1.parent is not node2.parent:

            if node1.parent.left is node1:
                node1.parent.left = node2
            else:
                node1.parent.right = node2

            if node2.parent.left is node2:
                node2.parent.left = node1
            else:
                node2.parent.right = node1

            node1_parent = node1.parent
            node1.parent = node2.parent
            node2.parent = node1_parent

            self.update_paths(node1.parent)
            self.update_paths(node2.parent)

        else:
            nodes_parent = node1.parent

            if node1 is nodes_parent.left:
                nodes_parent.left = node2
                nodes_parent.right = node1
            else:
                nodes_parent.left = node1
                nodes_parent.right = node2

            self.update_paths(nodes_parent)

        self.update_parent_path(node1)

    def find_largest(self, node):

        max_node = node
        for nd in self.blocks[node.weight]:
            if nd.n > max_node.n:
                max_node = nd

        return max_node

    def update_paths(self, node):

        if node.left is not None:
            node.left.bit_path = node.bit_path + '0'
            self.update_paths(node.left)

        if node.right is not None:
            node.right.bit_path = node.bit_path + '1'
            self.update_paths(node.right)

    def get_encoded_bytes(self):

        length = len(self.bit_buffer)
        padding = 0

        if length != 0 and length % 8 != 0:
            padding = 8 - length
            for i in range(padding):
                self.bit_buffer += '0'
            num = int(self.bit_buffer, 2)
            self.encoded_bytes.append(num)

        padding_byte = bytearray()
        padding_byte.append(padding)

        self.encoded_bytes = padding_byte + self.encoded_bytes

        print("Średnia długość kodowania: " + str(self.sum/self.count))

        return self.encoded_bytes

    def add_to_buffer(self, bit_path):

        if len(bit_path) > 0:
            self.sum += len(bit_path)
            self.count += 1

        self.bit_buffer += bit_path

        while len(self.bit_buffer) >= 8:
            num = int(self.bit_buffer[0:8], 2)
            self.encoded_bytes.append(num)
            self.bit_buffer = self.bit_buffer[8:]

    def add_to_block(self, node):
        if node.weight in self.blocks:
            self.blocks[node.weight].append(node)
        else:
            self.blocks[node.weight] = [node]

    def delete_from_block(self, node):

        if node.weight in self.blocks:
            self.blocks[node.weight].remove(node)