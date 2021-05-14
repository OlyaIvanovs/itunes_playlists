import plistlib
import numpy as np
from matplotlib import pyplot as plt


def find_duplicates(file_name):
    """Find duplicate tracks in given playlist."""
    print(f"Finding duplicate tracks in {file_name}...")
    # Read in a playlist
    with open(file_name, 'rb') as fp:
        plist = plistlib.load(fp)
        tracks = plist['Tracks']
    # Create a track name dictionary
    track_names = {}
    for track_id, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            if name in track_names:
                # if a name and duration match, increment the count
                # round the track length to the nearest second
                if duration//1000 == track_names[name][0]//1000:
                    count = track_names[name][1]
                    track_names[name] = (duration, count+1)
            else:
                # Add dictionary entry as tuple (duration, 1)
                track_names[name] = (duration, 1)
        except:
            # ignore
            pass
    # Store duplicates as (name, count) tuples
    dups = []
    for k, v in track_names.items():
        if v[1] > 1:
            dups.append((v[1], k))
    # Save duplicates to a file
    dups_len = len(dups)
    if dups_len > 0:
        print(f"Found {dups_len} duplicates. Track names saved to dup.txt")
    else:
        print("no duplicates found!")
    with open("dups.txt", "w") as f:
        for val in dups:
            f.write(f"[{val[0]}] {val[1]}")


def find_common_tracks(file_names):
    """Find common tracks across multiple playlists."""
    track_names_sets = []
    for file_name in file_names:
        track_names = set()
        # Read in playlist
        with open(file_name, 'rb') as fp:
            plist = plistlib.load(fp)
            tracks = plist['Tracks']
        # Iterate through the tracks
        for track_id, track in tracks.items():
            try:
                track_names.add(track['Name'])
            except:
                pass
        track_names_sets.append(track_names)
    # Get the set of common tracks
    common_tracks = set.intersection(*track_names_sets)
    len_common_tracks = len(common_tracks)
    if len_common_tracks > 0:
        with open("common.txt", "w") as f:
            for track in common_tracks:
                f.write(f"{track} \n")
        print(f"{len_common_tracks} found. Track names written to common.txt")
    else:
        print("No common tracks")


def plot_stats(file_name):
    """Gather ratings and track durations and plot."""
    with open(file_name, 'rb') as f:
        plist = plistlib.load(f)
        tracks = plist['Tracks']
    # Create lists of song ratings and track durations
    ratings, durations = [], []
    for track_id, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass
    if ratings == [] or durations == []:
        print(f"No valid Album Rating/Total Time data in {file_name}")
        return

    # Scatter plot
    x = np.array(durations, np.int32)
    x = x/60000.0  # convert to minutes
    y = np.array(ratings, np.int32)

    fig, axs = plt.subplots(2)
    fig.suptitle("Playlists statistics")

    axs[0].plot(x, y, 'ro')
    axs[0].axis([0, 1.05*np.max(x), -1, 110])
    axs[0].set(xlabel='Track duration', ylabel='Track rating')

    # Plot histogram
    axs[1].hist(x, bins=20)
    axs[1].set(xlabel='Track duration', ylabel='Count')

    # Show plot
    plt.show()


def main():
    """Analyze playlist files (.xml) exported from iTunes."""
    find_duplicates('test_files/mymusic.xml')
    find_common_tracks(['test_files/pl1.xml', 'test_files/pl2.xml'])
    plot_stats('test_files/mymusic.xml')


if __name__ == '__main__':
    main()
