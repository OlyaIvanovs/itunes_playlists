import plistlib


def find_duplicates(file_name):
    """Find duplicate tracks in given playlist."""
    print(f"Finding duplicate tracks in {file_name}...")
    # Read in a playlist
    with open(file_name, 'rb') as fp:
        plist = plistlib.load(fp)
        tracks = plist['Tracks']
    # Create a track name dictionary
    track_names = {}
    duplicates = 0
    for track_id, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            if name in track_names:
                duplicates += 1
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


def main():
    """Analyze playlist files (.xml) exported from iTunes."""
    find_duplicates('test_files/mymusic.xml')


if __name__ == '__main__':
    main()
