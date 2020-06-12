import sys, re
import numpy as np
import matplotlib.pyplot as plt

def main(argv):
    if len(argv) <= 1:
        print("Usage: python3 most-messages.py [file]\nfile - Generated text log")
        exit()
    file = open(argv[1],"r").readlines()

    data = getData(file)
    data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    messageData = [t[1] for t in data]
    names = [t[0] for t in data]

    for i in range(len(names)):
        percent = messageData[i]/sum(messageData)*100
        names[i] = f"{names[i]} - {round(percent,2)}%"

    plot(messageData,names)

def plot(data, names):
    plt.figure(figsize=(12,6))
    plt.pie(data, shadow=True, radius=1.25, startangle=90)
    plt.legend([name.replace('_','') for name in names], bbox_to_anchor=(1,0), loc="lower right", bbox_transform=plt.gcf().transFigure)
    plt.title("Amount of messages sent by user", bbox={'pad':5, 'facecolor':'0.8'}, y=1.05)
    plt.show()

def getData(file):
    data = {}
    for line in file:
        if line[0] not in ['\n','=']:
            name = line.split('<')[1].split('>')[0]
            if name in data.keys():
                data[name] += 1
            else:
                data[name] = 0
    return data

if __name__ == "__main__":
    main(sys.argv)