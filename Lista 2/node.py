# Autor: Jakub Iwon (236612)

class Node:

    def __init__(self, n, parent=None, symbol=None, weight=0):
        self.left = None
        self.right = None
        self.parent = parent
        self.weight = weight
        self.n = n
        self.symbol = symbol
        self.bit_path = ''

    def increment_weight(self):
        self.weight += 1

    def print_node(self):

        print("N: " + str(self.n) + "  Weight: " + str(self.weight) +
              "  Symbol: " + str(self.symbol) + ' Path: ' + str(self.bit_path))