import math
from fractions import Fraction


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

    def find_most_consonant(self, current_note):
        most_consonant_note = 0
        lowest_sum = 1000

        for n in self.scale:
            if n != current_note:
                frac = simplify_fraction(current_note, n)
                frac_sum = frac[0] + frac[1]
                if frac_sum < lowest_sum:
                    lowest_sum = frac_sum
                    most_consonant_note = n

        return most_consonant_note


c_just_scale = [261, 293.625, 326.25, 348.0, 391.5, 435.0, 489.375, 522.0]
