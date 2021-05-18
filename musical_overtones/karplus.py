from collections import deque
import random
import time
import numpy as np
import pygame
import argparse
import wave
from matplotlib import pyplot as plt
import os

g_show_plot = False  # show plot in action?

# Notes of a Pentatonic MInor scale: C4-E(b)-F-G-B(b)-C5
pm_notes = {'C4': 262, 'Eb': 311, 'F': 349, 'G': 391, 'Bb': 466}


def generate_note(freq):
    """Generate note of given frequency"""
    n_samples = 44100
    sample_rate = 44100
    n = int(sample_rate / freq)  # buffer's length
    # Ring buffer
    # range [-0.5, 0.5]
    buffer = deque([random.random() - 0.5 for i in range(n)])
    if g_show_plot:
        axline, = plt.plot(buffer)
    # Samples buffer
    samples = np.array([0]*n_samples, 'float32')
    for i in range(n_samples):
        samples[i] = buffer[0]
        avg = 0.996*0.5*(buffer[0] + buffer[1])  # 0.996 is attenuation
        buffer.append(avg)
        buffer.popleft()
        if g_show_plot and i % 1000 == 0:
            axline.set_ydata(buffer)
            plt.draw()

    # Convert samples to 16-bit values
    samples = np.array(samples*32767, 'int16')
    return samples


def write_wave(filename, data):
    """Write audio data to a wav file."""
    with wave.open(filename, "wb") as f:
        n_channels = 1
        sample_width = 2
        frame_rate = 44100
        n_frames = 44100
        # Set params
        f.setparams((n_channels, sample_width, frame_rate,
                    n_frames, 'NONE', 'noncompressed'))
        f.writeframes(data)


class NotePlayer:
    """Note constructor"""

    def __init__(self):
        # sampling rate 44100, 16-bit signed values, a single channel, a buffer size 2048
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        # Dictionary of notes
        self.notes = {}

    def add(self, filename):
        """Create a sound object and store it in the notes dictionary."""
        self.notes[filename] = pygame.mixer.Sound(
            filename)  # create a new Sound object from a file

    def play(self, filename):
        """Play a random note."""
        try:
            self.notes[filename].play()
        except:
            print(f"{filename} not found!")

    def play_random(self):
        """Play a random note"""
        index = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[index]
        note.play()


def main():
    """"""
    parser = argparse.ArgumentParser(
        description="Generating sounds with Karpus String Algorithm.")
    # Add arguments
    parser.add_argument('--display', action='store_true',
                        required=False)  # set up plot to show wave
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)

    args = parser.parse_args()

    # Show plot if flag set
    if args.display:
        g_show_plot = True
        plt.ion()  # Enable interactive mode

    # Create note player
    nplayer = NotePlayer()

    print("creating notes...")
    for name, freq in list(pm_notes.items()):
        filename = f'{name}.wav'
        if not os.path.exists(filename):
            data = generate_note(freq)
            print(f"creating {filename}...")
            write_wave(filename, data)
        else:
            print('File already exists. Skipping...')

        # Add note to player
        nplayer.add(f'{name}.wav')

        # Play note if display flag set
        if args.display:
            nplayer.play(f'{name}.wav')
            time.sleep(0.5)

    # Play random tune
    if args.play:
        while True:
            try:
                nplayer.play_random()
                # Add rests between notes played
                rest = np.random.choice(
                    [1, 2, 4, 8], 1, p=[0.15, 0.7, 0.1, 0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()


if __name__ == '__main__':
    main()
