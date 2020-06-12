import sys, json
import numpy as np
import matplotlib.pyplot as plt

# like-freq.py
# Displays frequency likes over time.

def main(argv):
    if len(argv) <= 2:
        print("Usage: python3 like-freq.py [file] [skip]\nfile - Json file with like data\nskip - Skip every nth date (leave as 0 or 1 to show every date).")
        exit()
    file = json.load(open(argv[1],"r"))
    skipN = int(argv[2])
    data = getData(file)
    
    counts = list(data.values())
    counts = counts[::skipN] if skipN != 0 else counts
    dates = list(data)
    dates = dates[::skipN] if skipN != 0 else dates
    
    days = f"{skipN} days" if skipN != 0 else "day"
    plot(dates, counts, days)

def plot(x, y, days):
    plt.figure(figsize=(14, 6))
    plt.title(f"Amount of likes for every {days}")
    plt.plot(x, y, linewidth=1, color=(0.3, 0.8, 0.3, 1.0))
    plt.ylabel("Likes")
    plt.xlabel("Day")
    plt.ylim(0, max(y)+5)
    yLen = int(np.ceil(len(y)/25))
    plt.xticks(np.arange(len(y))[::yLen], x[::yLen], rotation=33, fontsize=6)
    plt.show()

def getData(file):
    vals = {}
    for like in reversed(file["media_likes"]):
        date = like[0][0:10]
        if date not in vals:
            vals[date] = 0
        else:
            vals[date] += 1
    return vals

if __name__ == "__main__":
    main(sys.argv)