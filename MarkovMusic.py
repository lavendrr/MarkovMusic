import math
from fractions import Fraction
import numpy as np
import random


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

    def markov(self):
        matrix = np.array(np.zeros(shape=(8, 8)))
        probabilities = []
        x = 0
        while x < 8:
            probabilities.append(0.2 - ((3 / 140) * x))
            x += 1

        for note in self.scale:
            sorted_scale = self.consonant_sort(note[1])
            for index, note2 in enumerate(sorted_scale):
                matrix.T[note[0]][note2[0]] = probabilities[index]

        return matrix


def _12tet(root):
    scale = []
    semitone = 0
    while semitone < 13:
        scale.append((2 ** (semitone / 12)) * root)
        semitone += 1
    return scale


def _12tet_major(root):
    scale = []
    semitone = 0
    while semitone < 13:
        if semitone not in (1, 3, 6, 8, 10):
            scale.append((2 ** (semitone / 12)) * root)
        semitone += 1
    return scale


def _just_12tone(root):
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


def _just_minor(root):
    scale = []
    ratios = [
        1 / 1,
        9 / 8,
        6 / 5,
        4 / 3,
        3 / 2,
        8 / 5,
        7 / 4,
        2 / 1,
    ]
    semitone = 0
    while semitone < 8:
        print(semitone)
        scale.append(root * ratios[semitone])
        semitone += 1
    return scale


def melody(length, scale, markov):
    current_note = scale[0]
    melody = [current_note[1]]
    l = 0
    while l < length:
        current_note_matrix = np.zeros(shape=(8, 1))
        current_note_matrix.T[0][current_note[0]] = 1
        probabilities = np.matmul(markov, current_note_matrix)
        outcome = random.choices(scale, probabilities.T[0])
        melody.append(outcome[0][1])
        current_note = outcome[0]
        l += 1
    return melody


# c_just_scale = [261, 293.625, 326.25, 348.0, 391.5, 435.0, 489.375, 522.0]

# g_sharp_minor_scale = _just_minor(207.6525)

scale = _12tet_major(311.127)

mus = MusicGen(scale)
m = mus.markov()
mel = melody(10, mus.scale, m)
print(mel)
