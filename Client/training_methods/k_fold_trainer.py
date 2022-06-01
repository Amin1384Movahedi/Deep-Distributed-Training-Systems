import tensorflow as tf
from sklearn.model_selection import KFold
import numpy as np
import socket
import os
from train_logger.train_logger import train_history_logger

# Create our trainer
def KFold_train(X_train, Y_train, X_test, Y_test, num_epochs, batch_size, optimizer, loss_func, model_path, log_path):
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
    for train, test in kfold.split(X, Y):
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
                                    shuffle=True,
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