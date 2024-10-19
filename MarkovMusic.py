import math
from fractions import Fraction
import numpy as np


def gcd(a, b):
    if a < b:
        return gcd(b, a)

    # base case
    if abs(b) < 0.001:
        return a
    else:
        return gcd(b, a - math.floor(a / b) * b)


def simplify_fraction(num, denom):
    sim = gcd(num, denom)
    return (num / sim, denom / sim)


class MusicGen:
    def __init__(self, scale):
        self.scale = scale

    def calc_interval(self, note1, note2):
        frac = simplify_fraction(note1, note2)
        frac_sum = frac[0] + frac[1]
        return frac_sum

    def consonant_sort(self, current_note):
        sort = []
        sort = sorted(self.scale, key=lambda x: self.calc_interval(current_note, x))

        return sort

    def markov():
        # matrix = np.matrix(np.zeros(shape = (8, 8)))
        # matrix = np.array([[1, 2], [3, 4], [5, 6]])
        matrix = np.array(np.zeros(shape=(8, 8)))
        probabilities = []
        x = 0
        while x < 8:
            probabilities.append(0.2 - ((3 / 140) * x))
            x += 1

        x = 0

        for val in matrix.T[0]:
            # print(val)
            # matrix.T[int(val)] = x
            # x += 1
            matrix.T[0][x] = probabilities[x]
            x += 1

        return matrix


def _12tet(root):
    scale = []
    semitone = 0
    while semitone < 13:
        print(semitone)
        scale.append((2 ** (semitone / 12)) * root)
        semitone += 1
    return scale


def _just(root):
    scale = []
    ratios = [
        1 / 1,
        12 / 11,
        9 / 8,
        6 / 5,
        5 / 4,
        4 / 3,
        3 / 2,
        8 / 5,
        5 / 3,
        7 / 4,
        11 / 6,
        2 / 1,
    ]
    semitone = 0
    while semitone < 12:
        print(semitone)
        scale.append(root * ratios[semitone])
        semitone += 1
    return scale


c_just_scale = [261, 293.625, 326.25, 348.0, 391.5, 435.0, 489.375, 522.0]
