import sys, re
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# word-freq.py

def main(argv):
    if len(argv) <= 2:
        print("Usage: python3 word-freq.py [file] [keys]\nfile - Generated text log\nkeys - Keywords to search for (seperated by commas).")
        exit()
    file = open(argv[1],"r").readlines()
    keys = argv[2].split(',')
    dates = getDates(file)
    sortDates(dates)
    data = getWordData(file, dates, keys)
    plot(dates, data, keys)

def plot(x, y, keys):
    plt.figure(figsize=(14, 6))
    plt.title(f"Frequency of word(s):\n{', '.join(keys)}\nover time.")
    plt.bar(x, y, linewidth=4, color=(1.0, 0.5, 0.5, 1.0))
    plt.ylabel("Time word(s) were used per day")
    plt.xlabel("Day")
    plt.ylim(0, max(y)+5)
    yLen = int(len(y)/25)
    plt.xticks(np.arange(len(y))[::yLen], x[::yLen], rotation=33, fontsize=6)
    plt.show()

def getWordData(file, dates, keywords):
    vals = {}
    for date in dates: vals[date] = 0
    for line in file:
        for i in range(len(line) - 1): 
            message = line[i:len(line) - 1]
            if line[i-3:i] == ">: ":
                vals[getDate(line)] += len(list(findKeys(keywords, message)))
                break
    return [vals[date] for date in dates]

def findKeys(keys, message):
    for key in keys:
        if re.compile(r'\b({0})\b'.format(key)).search(message) != None:
            yield key

def getDates(file):
    dates = []
    for line in file:
        date = getDate(line)
        if date not in dates and date != "":
            dates.append(date)
    return dates

def sortDates(dates):
    dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))

def getDate(line):
    date = ""
    for i in range(len(line)):
        if line[i:i+2] == " |" or line[i] in ["=","\n"]: break
        date += line[i]
    return date

if __name__ == "__main__":
    main(sys.argv)