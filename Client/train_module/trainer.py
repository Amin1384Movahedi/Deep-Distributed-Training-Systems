import tensorflow as tf
import socket
import os 

# This trainer module uses k-fold method to train the model
# Create our trainer
def train(model, epochs, batch_size):
    model_path = os.getcwd() + '/' + socket.gethostname() + '.h5'

    # Make sure the name of model's file we want to train is exists
    if not os.path.exists(model_path):
        return F'{socket.gethostname()}.h5 is not exist!'

    # Load the model file
    model = tf.keras.models.load_model(model_path)

    # Logs and Callbacks
    log_path = os.getcwd() + 'logs'
    if not os.path.exists(log_path):
        os.mkdir('log')

    model_checkpoint = tf.keras.callbacks.ModelCheckpoint(log_path + '/' + socket.gethostname() + '_ModelWeight.h5')
    logger = tf.keras.callbacks.CSVLogger(log_path + '/' + socket.gethostname() + '_ModelTrainingLog.h5')