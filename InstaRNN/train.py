import sys
import matplotlib.pyplot as plt
from model import InstaRNNModel

# Save graph of training loss & accuracy
DRAW_METRICS = True

if len(sys.argv) <= 3:
    print("Usage: python3 train.py [dataset] [weights] [epochs]\ndataset - Generated text log file\nweights - File name to save trained weights.\nepochs - Number of epochs to train")
    exit()
training_data = open(sys.argv[1]).readlines()
weight_dir = sys.argv[2]
epochs = int(sys.argv[3])

model = InstaRNNModel(64, weight_dir, training_data)
model.create_dataset(100, 10000)
model.init_model()
model.train_model(epochs)

if DRAW_METRICS:
    plt.plot(model.history.history["accuracy"], label="Accuracy")
    plt.plot(model.history.history["loss"], label="Training loss")
    plt.legend()
    plt.savefig("metrics.png")