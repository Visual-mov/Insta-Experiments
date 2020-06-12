import tensorflow as tf
import numpy as np
import os, random, string
import matplotlib.pyplot as plt

# thanks Tensorflow for text generation tutorial.

def loss(labels, logits):
      return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

class InstaRNNModel():
    def __init__(self, batch_size, weight_dir, file):
        self.batch_size = batch_size
        self.weight_dir = weight_dir
        self.file = file
        self.text = "".join(file)
        
        self.chars = sorted(set(self.text))
        self.tochar = np.array(self.chars)
        self.vectorize = {c : n for n,c in enumerate(self.chars)}
    
    def init_model(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(len(self.chars), 256, batch_input_shape=[self.batch_size, None]),
            tf.keras.layers.GRU(550, return_sequences=True, stateful=True, recurrent_initializer="glorot_uniform"),
            tf.keras.layers.Dense(len(self.chars))
        ])
        self.model.compile(optimizer="adam", loss=loss, metrics=["accuracy"])

    def train_model(self, epochs):
        self.history = self.model.fit(self.dataset,epochs=epochs)
        self.model.save_weights(self.weight_dir)
    
    def create_dataset(self, seq_length, buffer_length):
        self.vector_text = np.array([self.vectorize[i] for i in self.text])
        self.dataset = tf.data.Dataset.from_tensor_slices(self.vector_text).batch(seq_length+1, drop_remainder=True)
        self.dataset = self.dataset.map(self.split_targets)
        self.dataset = self.dataset.shuffle(buffer_length).batch(self.batch_size, drop_remainder=True)

    def get_text(self, length, start=""):
        text = []
        letters = string.ascii_letters + ' '
        if start == "": start = letters[random.randint(0,len(letters)-1)]
        input = tf.expand_dims([self.vectorize[c] for c in start],0)

        self.model.reset_states()
        for i in range(length):
            # Get probabilities given the input character and state of the RNN.
            predictions = tf.squeeze(self.model.predict(input), 0)
            # Get one-character prediction using categorical distribution.
            predicted = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()
            # Set the current character as the next input for the network.
            input = tf.expand_dims([predicted], 0)

            text.append(self.tochar[predicted])
        return start + "".join(text)

    def load_weights(self):
        self.batch_size = 1
        self.init_model()
        self.model.load_weights(self.weight_dir)
        self.model.build(tf.TensorShape([1, None]))

    def split_targets(self, string):
        return string[:-1], string[1:]