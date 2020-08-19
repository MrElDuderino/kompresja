# Autor: Jakub Iwon (236612)

import math

def count(color_map):

    count_all = {}
    count_red = [0 for _ in range(256)]
    count_green = [0 for _ in range(256)]
    count_blue = [0 for _ in range(256)]

    for row in color_map:
        for p in row:
            (r, g, b) = p
            if p in count_all:
                count_all[p] +=1
            else:
                count_all[p] = 1
            count_red[r] +=1
            count_green[g] +=1
            count_blue[b] +=1

    return count_all, count_red, count_green, count_blue


def entropy(color_map):

    count_all, count_red, count_green, count_blue = count(color_map)
    n = len(color_map) * len(color_map[0])

    entropy_all = calculate_entropy(count_all, n)
    entropy_red = calculate_entropy(count_red, n)
    entropy_green = calculate_entropy(count_green, n)
    entropy_blue = calculate_entropy(count_blue, n)

    return entropy_all, entropy_red, entropy_green, entropy_blue


def calculate_entropy(count, n):

    entropy = 0
    if isinstance(count, dict):
        for _, c in count.items():
            entropy += c * (math.log(n, 2) - math.log(c, 2))
    elif isinstance(count, list):
        for c in count:
            if c == 0:
                continue
            entropy += c * (math.log(n, 2) - math.log(c, 2))
    entropy /= n

    return entropy