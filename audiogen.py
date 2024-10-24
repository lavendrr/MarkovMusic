import numpy as np
import soundfile as sf

# import sounddevice as sd
from math import ceil, pi


def get_omega(f, fs):
    """Returns normalized angular frequency for a given frequency and sample rate. Accepts int/float arguments for frequency in Hz and sample rate in Hz."""
    wc = 2 * np.pi * f / fs
    return wc


def bpm2sec(bpm):
    """Outputs beat length in seconds for a given bpm. Accepts an int/float argument for bpm."""
    sec = 60 / bpm
    return sec


def midi2freq(midi):
    """Converts a given MIDI value to frequency in Hz. Negative values return -1 to indicate a rest. Accepts an int/float argument for the MIDI value, although technically speaking MIDI values should be ints between 0-127."""
    if midi < 0:
        freq = -1
    else:
        freq = 2 ** ((midi - 69) / 12) * 440  # MIDI formula
    return freq


def square_term(k, f, t):
    """Calculates the k-th term of the Fourier series for a square wave with given f and t. Accepts arguments for k (int), frequency in Hz (int/float), and time in seconds (int/float)."""
    term = np.sin(2 * pi * (2 * k - 1) * f * t) / (2 * k - 1)
    return term


def square(f, t):
    """Uses NumPy to efficiently calculate the sum of Fourier series terms up to k = 21 for a square wave at the given frequency for duration t. Accepts int/float arguments for frequency in Hz and time in seconds."""
    sum = 0
    for k in range(1, 21):
        sum += square_term(k, f, t)
    sum *= 4 / pi
    return sum


def confirmation(prompt, opt1, opt2):
    """Prompts the user to pick one of two options, repeating the question until they select one. Accepts string arguments for the prompt and each of the two options."""
    cont = False
    while (
        cont == False
    ):  # repeat the question until one of the options is properly selected
        choice = input(f"{prompt} ({opt1}/{opt2}): ").lower()
        if choice in (opt1, opt2):
            cont = True
        else:
            print(f"Please respond with either {opt1} or {opt2}.")
    return choice


melodyin = input(
    "Input the melody as a comma-separated list of frequencies (negative value equals a rest): "
).split(
    ","
)  # take input of MIDI values and remove commas
melodyclean = [
    float(item) for item in melodyin if True
]  # strip whitespace (if it's there) and return list of ints only (negatives included)
print(melodyclean)
melodyclean = np.array(melodyclean) + 7.0

bpm = float(input("Input the tempo in beats per minute (BPM): "))

timbre = confirmation("Input the timbre: ", "square", "sin")

# Initialize sound properties, note arrays, and envelopes
fs = 44100  # sample rate in Hz
amplitude = 1 / 12  # linear gain
φ = 0  # initial phase in radians between 0 and 2π (= 360°)

note_samples = ceil(bpm2sec(bpm) * fs)  # length of single note in samples
note_array_samples = np.arange(
    note_samples
)  # array of indices in samples for the length of one note
note_array_seconds = (
    note_array_samples / fs
)  # array of indices in seconds for the length of one note

out = np.empty(shape=1)  # initialize empty output array
env_length = ceil(
    note_samples / 10
)  # set the envelope length to 1/10 of the note length
attack = np.linspace(
    0, 1, env_length
)  # generate ramps with the corresponding number of samples
decay = np.linspace(1, 0, env_length)

for note in melodyclean:
    # f = midi2freq(note) # Get frequency from MIDI
    f = note
    if f == -1:  # output a rest if the input frequency is negative
        x = note_array_samples * 0
    else:
        if timbre == "square":
            x = amplitude * square(
                f, note_array_seconds
            )  # Calculate sample amplitudes via square (summing Fourier terms = additive synth)
        elif timbre == "sin":
            ω = get_omega(f, fs)  # Get normalized angular frequency
            x = (amplitude * 1.5) * np.sin(
                ω * note_array_samples + φ
            )  # Calculate sample amplitudes via sin (increase amplitude since sin is perceptually quieter)
    x[:env_length] = (
        x[:env_length] * attack
    )  # apply the envelopes (in-place multiply doesn't work because of datatypes)
    x[-env_length:] = x[-env_length:] * decay
    out = np.concatenate((out, x))  # add note to output array

# playing = False

# if confirmation('Play the soundfile?','y','n') == 'y':
#     sd.play(out,fs)
#     print('Playing...')
#     playing = True

if confirmation("Save the soundfile?", "y", "n") == "y":
    print("Saving...")
    sf.write("out.wav", out, fs)
    print("Successfully saved!")

# if playing == True:
#     sd.wait() # If sound is still playing, wait for it to finish before ending the program
#     print('Playback complete!')
