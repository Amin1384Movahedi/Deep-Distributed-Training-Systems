import tensorflow as tf
import numpy as np
import socket
import os
from config_loader.config_loader import load
import sys
from train_logger.train_logger import train_history_logger

# Create our trainer
def norm_train(X_train, Y_train, X_test, Y_test, num_epochs, batch_size, optimizer, loss_func, model_path, log_path):
    # Load the model
    model = tf.keras.models.load_model(f'{model_path}/{socket.gethostname()}.h5')

    # Compile the model
    model.compile(optimizer=optimizer, loss=loss_func, metrics=['accuracy'])

    # Create the callbacks
    model_checkpoint = tf.keras.callbacks.ModelCheckpoint(f'{model_path}/{socket.gethostname()}_ModelWeight.h5', 
                                                            monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
    logger = tf.keras.callbacks.CSVLogger(f'{log_path}/{socket.gethostname()}_ModelTrainingLog.log')

    callbacks = [model_checkpoint, logger]

    network_history = model.fit(X_train, Y_train,
                                epochs=num_epochs,
                                batch_size=batch_size,
                                shuffle=True,
                                verbose=1,
                                callbacks=callbacks,
                                validation_data=(X_test, Y_test))

    # Plot newwork_history
    train_history_logger(network_history, 0, log_path)