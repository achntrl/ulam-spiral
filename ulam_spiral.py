from math import log
from random import random, randint
from time import time

import numpy as np
from PIL import Image


def create_spiral(n):
    """Creates a (2 * n + 1) by (2 * n + 1) filled with numbers in
    spiral pattern. E.g. for n = 1:
        [[5 4 3]
         [6 1 2]
         [7 8 9]]
    """
    if n < 1:
        print("create_spiral expects n >= 1")
        exit(-1)
    spiral = np.zeros((2 * n + 1, 2 * n + 1), np.uint64)
    # We start at the center of the spiral
    current_position = (n, n)
    current_number = 1
    current_direction = 'd'

    while(current_position != (2 * n, 2 * n + 1)):
        spiral[current_position] = current_number
        current_number += 1

        # If the next direction if free, we fill in that direction
        if spiral[move(current_position, next_direction(current_direction))] == 0:
            current_direction = next_direction(current_direction)
            current_position = move(current_position, current_direction)
        # else we keep going in our direction
        else:
            current_position = move(current_position, current_direction)

    return spiral


def next_direction(direction):
    return {
        'u': 'l',
        'l': 'd',
        'd': 'r',
        'r': 'u',
    }[direction]


def move(current_position, direction):
    if direction == 'u':
        return (current_position[0] - 1, current_position[1])
    elif direction == 'd':
        return (current_position[0] + 1, current_position[1])
    elif direction == 'l':
        return (current_position[0], current_position[1] - 1)
    elif direction == 'r':
        return (current_position[0], current_position[1] + 1)
    else:
        print('direction should be u, d, l or r')
        exit(-1)


def generate_image(n, prime_function, name):
    spiral = create_spiral(n)
    img = np.zeros(spiral.shape, np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if prime_function(int(spiral[i, j])):
                img[i, j] = 255
    # Zoom x4
    final_size = tuple(4 * x for x in img.shape)
    display = Image.fromarray(img, 'L')
    display.resize(final_size, Image.NEAREST).save('output/{}_{}.png'.format(str(n), name))


def random_prime(n):
    if n == 1:
        return False
    if random() <= 1 / log(n):
        return True
    return False


def true_random(n):
    if random() < 0.5:
        return True
    return False


def is_prime_fermat(n):
    if n == 1:
        return False
    if n == 2:
        return True

    for i in range(20):
        x = randint(1, n-1)
        if pow(x, n-1, n) != 1:
            return False
    return True


if __name__ == '__main__':
    n = 200
    t1 = time()

    generate_image(n, true_random, 'true_random')
    t2 = time()
    print('True Random in {:.2f} s'.format(t2 - t1))

    generate_image(n, random_prime, 'random')
    t3 = time()
    print('Random in {:.2f} s'.format(t3 - t2))

    generate_image(n, is_prime_fermat, 'fermat')
    t4 = time()
    print('Fermat prime in {:.2f} s'.format(t4 - t3))
