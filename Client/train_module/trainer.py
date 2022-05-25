import tensorflow as tf
from sklearn.model_selection import KFold
import numpy as np
import matplotlib.pyplot as plt
import socket
import os
from config_loader.config_loader import load
import sys

# Create the history logger function
# This function plot the network_history object and save it in .png format in log/ folder
def train_history_logger(network_history, fold_no, log_path):
    # Extracting losses and accuracy from history
    history = network_history.history

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
    plt.savefig(f'{log_path}/history_of_losses({fold_no}).png')

    # Plot accuracy and validation accuracy per each epochs and saving the figure in log folder
    plt.figure()
    plt.grid()
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.plot(accuracies)
    plt.plot(validation_accuracies)
    plt.legend(['accuracy', 'validation_accuracy'])
    plt.savefig(f'{log_path}//history_of_accuracies({fold_no}).png')

# Create our trainer
def train(X_train, Y_train, X_test, Y_test):
    try:
        model_path = f'{os.getcwd()}/model'

        # Make sure the name of model's file we want to train is exists
        if not os.path.exists(model_path):
            sys.exit(f'{socket.gethostname()}.h5 is not exist!') 

        # Logs and Callbacks
        log_path = os.getcwd() + '/log'
        if not os.path.exists(log_path):
            os.mkdir('log')

        # Extract train parameters
        num_epochs, batch_size, optimizer, loss_func = load()
        
        # Define number of folds
        num_folds = 10

        # Define per-fold score containers
        accuracy_per_fold = []
        loss_per_fold = []


        # Define the K-fold Cross Validator
        kfold = KFold(n_splits=num_folds, shuffle=True)

        # Merge inputs and targets
        X = np.concatenate((X_train, X_test), axis=0)
        Y = np.concatenate((Y_train, Y_test), axis=0)

        # Load the model
        origin_model = tf.keras.models.load_model(f'{model_path}/{socket.gethostname()}.h5')

        # Compile the model
        origin_model.compile(optimizer=optimizer, loss=loss_func, metrics=['accuracy'])

        # K-fold Cross Validation model evaluation
        fold_no = 1
        for train, test in KFold.split(X, Y):
            # Make a copy from origin model
            model = origin_model

            # Create the callbacks
            model_checkpoint = tf.keras.callbacks.ModelCheckpoint(f'{model_path}/{socket.gethostname()}_ModelWeight({fold_no}).h5', 
                                                                    monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
            logger = tf.keras.callbacks.CSVLogger(f'{log_path}/{socket.gethostname()}_ModelTrainingLog.log')

            callbacks = [model_checkpoint, logger]

            network_history = model.fit(X[train], Y[train],
                                        epochs=num_epochs,
                                        batch_size=batch_size,
                                        shufle=True,
                                        verbose=1,
                                        callbacks=callbacks,
                                        validation_data=(X[test], Y[test]))

            # Plot newwork_history
            train_history_logger(network_history, fold_no, log_path)

            # Generate generalization metrics
            scores = model.evaluate(X[test], Y[test], verbose=0)
            print(f'Score for fold {fold_no}: {model.metrics_names[0]} of {scores[0]}; {model.metrics_names[1]} of {scores[1]*100}%')
            accuracy_per_fold.append(scores[1] * 100)
            loss_per_fold.append(scores[0])

            # Clear the tensorflow session
            tf.keras.backend.clear_session()

            # Increase fold number
            fold_no = fold_no + 1

        with open(f'{log_path}/accuracy_per_fold.log', 'w') as f:
            f.write(str(accuracy_per_fold))

        with open(f'{log_path}/loss_per_fold.log', 'w') as f:
            f.write(str(loss_per_fold))

    except Exception as e:
        with open(f'{log_path}/training_exception.log', 'w') as f:
            f.write(str(e))