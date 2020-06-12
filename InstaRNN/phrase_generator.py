import sys, pyttsx3, random
from tkinter import *
from model import InstaRNNModel

def main(argv):
    if len(argv) < 2:
        print("Usage: python3 phrase_generator.py [dataset] [weights]\ndataset - Generated text log file\nweights - Saved weights for the model.")
        exit()
    root = Tk()
    file = open(argv[1]).readlines()
    model = InstaRNNModel(1, argv[2], file)
    
    model.init_model()
    model.load_weights()
    window = PhraseGenerator(root, file, model)
    root.mainloop()

class PhraseGenerator:
    def __init__(self, root, file, model):
        self.root = root
        self.engine = pyttsx3.init()
        self.file = file
        self.model = model

        self.starts = [
            "What if ", "I'm thinking about ",
            "It would be interesting if ", "Y'know ",
            "I think ", "What about ",
            "What do you ", "My name is ",
            "Can you ", "Would you ",
            "That would be ", "No ",
            "Yes ", "That's not ", "That is"
        ]
        self.root.geometry("600x150")
        self.root.resizable(False, False)
        self.root.title("Generate a Phrase!")
        self.phrase_string = StringVar()
        self.start_string = StringVar()
        self.phrase_text = Label(self.root, textvariable=self.phrase_string, font=("Courier", 20), bg="white")
        self.start_text = Label(self.root, textvariable=self.start_string, font=("Courier", 15), bg="white")
        self.phrase_button = Button(root, text="What will I say?", command=self.display_phrase)
        self.phrase_button.pack(side=BOTTOM)
        self.start_text.pack()
        self.phrase_text.pack()
        self.engine.setProperty("rate", 155)
        self.engine.setProperty("voice", "english-us")

    def display_phrase(self):
        start = self.starts[random.randint(0,len(self.starts)-1)]
        self.start_string.set(start)
        self.phrase = self.model.get_text(35, start)
        self.phrase = self.clean_phrase(self.phrase)
        self.root.after(10, self.say_phrase)
        self.phrase_string.set(self.phrase.replace(start,""))
        print(self.phrase)
        
        
    def say_phrase(self):
        self.engine.say(self.phrase)
        self.engine.runAndWait()
    
    def clean_phrase(self, phrase):
        return "".join([phrase[j] for j in range(len(phrase)) if ord(phrase[j]) in range(65536)]).replace('\n',' ')
        
if __name__ == "__main__":
    main(sys.argv)