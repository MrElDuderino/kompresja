# Autor: Jakub Iwon (236612)

from entropy import entropy
import sys

def get_color_map(input_path):

    with open(input_path, 'rb') as file:

        file.read(12)

        image_width = read_int(file, 2)
        image_height = read_int(file, 2)

        file.read(1)
        direction = read_int(file, 1)

        x_range = range(image_width)
        y_range = range(image_height)

        if direction & 16:
            x_range = range(image_width-1, -1, -1)

        if not direction & 32:
            y_range = range(image_height-1, -1, -1)

        color_map = [[None for x in range(image_width)] for y in range(image_height)]
        for y in y_range:
            for x in x_range:
                color_map[y][x] = tuple(reversed(((read_int(file, 1), read_int(file, 1), read_int(file, 1)))))

        return color_map

def read_int(file, n):
    return int.from_bytes(file.read(n), 'little')


def jpeg_ls(color_map):

    image_width, image_height = len(color_map[0]), len(color_map)
    maps = []
    funcs = [scheme1, scheme2, scheme3, scheme4, scheme5, scheme6, scheme7, scheme8]
    for i in range(len(funcs)):
        maps.append([[None for x in range(image_width)] for y in range(image_height)])

    for i, func in enumerate(funcs):
        for x in range(image_width):
            for y in range(image_height):
                w, n, nw = surroundings(color_map, x, y)
                map = maps[i]
                map[y][x] = subtract(color_map[y][x], func(w, n, nw))

    return maps

def surroundings(color_map, x, y):

    black = (0, 0, 0)
    w_x, w_y = x - 1, y
    n_x, n_y = x, y - 1
    nw_x, nw_y = x - 1, y - 1

    w = color_map[w_y][w_x] if w_x >= 0 else black
    n = color_map[n_y][n_x] if n_y >= 0 else black
    nw = color_map[nw_y][nw_x] if nw_x >= 0 and nw_y >= 0 else black

    return w, n, nw

def subtract(tuple1, tuple2):

    t1 = (tuple1[0] - tuple2[0]) % 256
    t2 = (tuple1[1] - tuple2[1]) % 256
    t3 = (tuple1[2] - tuple2[2]) % 256

    return (t1, t2, t3)


def scheme1(w, n, nw):
    return (w[0], w[1], w[2])

def scheme2(w, n, nw):
    return (n[0], n[1], n[2])

def scheme3(w, n, nw):
    return (nw[0], nw[1], nw[2])

def scheme4(w, n, nw):

    x1 = n[0] + w[0] - nw[0]
    x2 = n[1] + w[1] - nw[1]
    x3 = n[2] + w[2] - nw[2]

    return (x1, x2, x3)


def scheme5(w, n, nw):

    x1 = n[0] + round((w[0] - nw[0])/2)
    x2 = n[1] + round((w[1] - nw[1])/2)
    x3 = n[2] + round((w[2] - nw[2])/2)

    return (x1, x2, x3)


def scheme6(w, n, nw):

    x1 = w[0] + round((n[0] - nw[0])/2)
    x2 = w[1] + round((n[1] - nw[1])/2)
    x3 = w[2] + round((n[2] - nw[2])/2)

    return (x1, x2, x3)


def scheme7(w, n, nw):

    x1 = round((n[0] + w[0])/2)
    x2 = round((n[1] + w[1])/2)
    x3 = round((n[2] + w[2])/2)

    return (x1, x2, x3)


def scheme8(w, n, nw):

    x = [0, 0, 0]

    for i in range(len(x)):

        if nw[i] >= max(w[i], n[i]):
            x[i] = max(w[i], n[i])
        elif nw[i] <= min(w[i], n[i]):
            x[i] = min(w[i], n[i])
        else:
            x[i] = w[i] + n[i] - nw[i]

    return tuple(x)


def main():

    if len(sys.argv) < 2:
        print("Za mała liczba argumentów wejściowych.")
        sys.exit()

    try:
        color_map = get_color_map(sys.argv[1])
    except FileNotFoundError:
        print("Plik " + sys.argv[1] + " nie istnieje.")
        sys.exit()


    print("\nDane wejściowe\n")
    entropy_all, entropy_red, entropy_green, entropy_blue = entropy(color_map)
    print("Entropia: " + str(entropy_all))
    print("Entropia - kolor czerwony: " + str(entropy_red))
    print("Entropia - kolor zielony: " + str(entropy_green))
    print("Entropia - kolor niebieski: " + str(entropy_blue) + "\n\n")

    maps = jpeg_ls(color_map)
    entropies = {}
    entropies_red = {}
    entropies_green = {}
    entropies_blue = {}

    for i, map in enumerate(maps):

        if i == 7:
            print("Nowy standard\n")
        else:
            print("Schemat " + str(i+1) + "\n")

        entropy_all, entropy_red, entropy_green, entropy_blue = entropy(map)
        entropies[i] = entropy_all
        entropies_red[i] = entropy_red
        entropies_green[i] = entropy_green
        entropies_blue[i] = entropy_blue

        print("Entropia: " + str(entropy_all))
        print("Entropia - kolor czerwony: " + str(entropy_red))
        print("Entropia - kolor zielony: " + str(entropy_green))
        print("Entropia - kolor niebieski: " + str(entropy_blue) + "\n\n")

    minimal = min(entropies, key=entropies.get)
    print("Metoda optymalna - całość: " + str(minimal+1) + ", entropia: " + str(entropies[minimal]))
    minimal = min(entropies_red, key=entropies_red.get)
    print("Metoda optymalna - kolor czerwony: " + str(minimal+1) + ", entropia: " + str(entropies_red[minimal]))
    minimal = min(entropies_green, key=entropies_green.get)
    print("Metoda optymalna - kolor zielony: " + str(minimal+1) + ", entropia: " + str(entropies_green[minimal]))
    minimal = min(entropies_blue, key=entropies_blue.get)
    print("Metoda optymalna - kolor niebieski: " + str(minimal+1) + ", entropia: " + str(entropies_blue[minimal]))


if __name__ == '__main__':

    main()