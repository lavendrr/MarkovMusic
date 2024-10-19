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
        self.scale = []
        for index, item in enumerate(scale):
            self.scale.append((index, item))

    def calc_interval(self, note1, note2):
        frac = simplify_fraction(note1, note2)
        frac_sum = frac[0] + frac[1]
        return frac_sum

    def consonant_sort(self, current_note):
        sort = []
        sort = sorted(self.scale, key=lambda x: self.calc_interval(current_note, x[1]))

        return sort

    def markov(self, sorted_scale):
        matrix = np.array(np.zeros(shape=(8, 8)))
        probabilities = []
        x = 0
        while x < 8:
            probabilities.append(0.2 - ((3 / 140) * x))
            x += 1

        for index, note in enumerate(sorted_scale):
            # print(f"note index {note[0]}\nnote value {note[1]}")
            # print(f"probability {probabilities[index]}")
            matrix.T[0][note[0]] = probabilities[index]

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

mus = MusicGen(c_just_scale)
s = mus.consonant_sort(261)
m = mus.markov(s)
print(m)
