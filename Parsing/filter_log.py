import sys, string, emoji

CHARS = list(string.printable) + list(emoji.UNICODE_EMOJI.keys())

def filter_func(str):
    for c in str:
        if c not in CHARS: return False    
    return True

if len(sys.argv) < 1:
    print("Give message log to filter as argument.")
    exit()
lines = open(sys.argv[1]).readlines()

print(set(lines[0]))
lines = list(filter(filter_func, lines))
file = open("Filtered_log.txt","w")
file.write("".join(lines))
file.close()
