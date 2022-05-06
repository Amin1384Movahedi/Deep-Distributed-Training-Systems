import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import socket
import os
from config_loader.config_loader import load

# Create the history logger function
# This function plot the network_history object and save it in .png format in log/ folder
def train_history_logger(network_history, log_path):
    history = network_history.history

    # Extracting losses and accuracy from history
    losses = history['loss']
    validation_loss = history['val_loss']
    accuracies = history['accuracy']
    validation_accuracies = history['val_accuracy']

    # Plot losses and validation losses per each epochs and saving the figure in log folder
    plt.figure()
    plt.grid()
    plt.xlabel('Epochs')
    plt.xlabel('Loss')
    plt.plot(losses)
    plt.plot(validation_loss)
    plt.legend(['loss', 'validation_loss'])
    plt.savefig(f'{log_path}/history_of_losses.png')

    # Plot accuracy and validation accuracy per each epochs and saving the figure in log folder
    plt.figure()
    plt.grid()
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.plot(accuracies)
    plt.plot(validation_accuracies)
    plt.legend(['accuracy', 'validation_accuracy'])
    plt.savefig(f'{log_path}//history_of_accuracies.png')

# Create our trainer
def train(X_train, Y_train, X_test, Y_test):
    try:
        model_path = f'{os.getcwd()}/model/{socket.gethostname()}.h5'

        # Make sure the name of model's file we want to train is exists
        if not os.path.exists(model_path):
            return f'{socket.gethostname()}.h5 is not exist!'

        # Logs and Callbacks
        log_path = os.getcwd() + '/log'
        if not os.path.exists(log_path):
            os.mkdir('log')

        # Extract train parameters
        num_epochs, batch_size, optimizer, loss_func = load()

        # Create our callbacks
        model_checkpoint = tf.keras.callbacks.ModelCheckpoint(f'{log_path}/{socket.gethostname()}_ModelWeight.h5')
        logger = tf.keras.callbacks.CSVLogger(f'{log_path}/{socket.gethostname()}_ModelTrainingLog.log')

        callbacks = [model_checkpoint, logger]

        # Load the model
        model = tf.keras.models.load_model(model_path)

        # Compile the model
        model.compile(optimizer=optimizer, loss=loss_func, metrics=['accuracy'])
        
        # Start training
        network_history = model.fit(X_train, Y_train,
                                    epochs=num_epochs,
                                    batch_size=batch_size,
                                    verbose=1,
                                    callbacks=callbacks,
                                    validation_data=(X_test, Y_test))

        # Plot newwork_history
        train_history_logger(network_history, log_path)

    except Exception as e:
        with open(f'{log_path}/training_exception.log', 'w') as f:
            f.write(str(e))