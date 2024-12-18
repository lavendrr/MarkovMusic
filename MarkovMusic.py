import math
from audiogen import melody_output, chord_output
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
        self.matrix = self.markov()

    def calc_interval(self, note1, note2):
        frac = simplify_fraction(note1, note2)
        frac_sum = frac[0] + frac[1]
        return frac_sum

    def consonant_sort(self, current_note):
        sort = []
        sort = sorted(self.scale, key=lambda x: self.calc_interval(current_note, x[1]))

        return sort

    def markov(self):
        n = len(self.scale)
        matrix = np.array(np.zeros(shape=(n, n)))
        probabilities = []
        x = 0
        while x < len(self.scale):
            probabilities.append(2 / (n - 1) - ((2 / (n * (n - 1))) * x))
            x += 1

        for note in self.scale:
            sorted_scale = self.consonant_sort(note[1])
            for index, note2 in enumerate(sorted_scale):
                matrix.T[note[0]][note2[0]] = probabilities[index]

        return matrix

    def melody(self, length):
        current_note = self.scale[0]
        melody = [current_note[1]]
        l = 0
        while l < length:
            current_note_matrix = np.zeros(shape=(len(self.scale), 1))
            current_note_matrix.T[0][current_note[0]] = 1
            probabilities = np.matmul(self.matrix, current_note_matrix)
            outcome = random.choices(self.scale, probabilities.T[0])
            melody.append(outcome[0][1])
            current_note = outcome[0]
            l += 1
        return melody

    def chords(self, length):
        current_note = self.scale[0]
        chords = [[current_note[1], current_note[1]]]
        l = 0
        while l < length:
            chord = []

            current_note_matrix = np.zeros(shape=(len(self.scale), 1))
            current_note_matrix.T[0][current_note[0]] = 1
            probabilities = np.matmul(self.matrix, current_note_matrix)

            # Select 2 notes randomly
            outcome = random.choices(self.scale, probabilities.T[0])
            # Add the two note frequencies in a list
            chord.append(outcome[0][1])

            next_note_matrix = np.zeros(shape=(len(self.scale), 1))
            next_note_matrix.T[0][outcome[0][0]] = 1
            chord_probabilities = np.matmul(self.matrix, next_note_matrix)

            chord_outcome = random.choices(self.scale, chord_probabilities.T[0])
            chord.append(chord_outcome[0][1])

            chords.append(chord)

            current_note = outcome[0]
            l += 1

        return chords


def _ntet(root, divisions=12):
    scale = []
    semitone = 0
    while semitone < divisions + 1:
        scale.append((2 ** (semitone / divisions)) * root)
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
        scale.append(root * ratios[semitone])
        semitone += 1
    return scale

def pythag(root):
    scale = []
    ratios = [
        1/1,
        256/243,
        9/8,
        32/37,
        81/64,
        4/3,
        1024/729,
        729/512,
        3/2,
        128/81,
        27/16,
        16/9,
        243/128,
        2/1
    ]
    semitone = 0
    while semitone < 12:
        scale.append(root * ratios[semitone])
        semitone += 1
    return scale


# TESTING / EXAMPLE USAGE (31tet scale based on Eb above middle C)
# scale = _ntet(311.127, 15)
scale = pythag(420)
print(scale)

mus = MusicGen(scale)
# mel = mus.melody(12)
mel = mus.chords(30)
print(mel)
chord_output(mel, 180, "sin")
# melody_output(mel, 130, "square")
