# Autor: Jakub Iwon (236612)

import sys
import os
from encode import encode
from decode import decode
from entropy import get_entropy


def main():

    if len(sys.argv) < 4:
        print("Za mała liczba argumentów wejściowych.")
        print("Sposób uruchomienia (kodowanie): --encode <input file> <output file>")
        print("Sposób uruchomienia (dekodowanie): --decode <input file> <output file>")
        sys.exit()

    input_path = sys.argv[2]
    output_path = sys.argv[3]

    try:
        if sys.argv[1] == "--encode":
            original_size = os.path.getsize(input_path)
            print("Rozmiar pliku do zakodowania: " + str(original_size))
            encode(input_path, output_path)
            compressed_size = os.path.getsize(output_path)
            print("Rozmiar skompresowanego pliku: " + str(compressed_size))
            print("Stopień kompresji: " + str(original_size/compressed_size))
            original_entropy = get_entropy(input_path)
            print("Entropia pliku do zakodowania: " + str(original_entropy))
            compressed_entropy = get_entropy(output_path)
            print("Entropia skompresowanego pliku: " + str(compressed_entropy))
        elif sys.argv[1] == "--decode":
            decode(input_path, output_path)
        else:
            print("Niepoprawna opcja.")
            print("Opcje: --encode | --decode")
    except FileNotFoundError:
        print("Plik " + input_path + " nie istnieje.")
        sys.exit()


if __name__ == '__main__':
    main()
