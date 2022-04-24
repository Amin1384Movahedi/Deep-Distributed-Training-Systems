import tensorflow as tf
import socket
import os 

model_path = os.getcwd() + '/' + os.gethostname() + '.h5'

# Load the model file
model = tf.keras.models.load_model(model_path)

# Create our trainer
def train(model, epochs, batch_size, optimizer, loss):
    pass