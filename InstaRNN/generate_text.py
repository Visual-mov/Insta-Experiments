import sys
from model import InstaRNNModel

SAVE_TEXT = True
TEXT_LENGTH = 3000
START = ""

if len(sys.argv) <= 2:
    print("Usage: python3 generate_text.py [dataset] [weights]\ndataset - Generated text log file\nweights - Saved weights for the model.")
    exit()
file = open(sys.argv[1]).readlines()
weights_dir = sys.argv[2]

model = InstaRNNModel(1, weights_dir, file)
model.init_model()
model.load_weights()

text = model.get_text(TEXT_LENGTH, START)
if SAVE_TEXT:
    out = open("Generated_text.txt",'w')
    out.write(text)
    out.close()
else:
    print('\n' + text)