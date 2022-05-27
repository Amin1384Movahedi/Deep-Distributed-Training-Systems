import matplotlib.pyplot as plt
import socket
import os
from config_loader.config_loader import load
import sys
from normalizer import normalize
from k_fold_trainer import KFold_train
from norm_trainer import norm_train

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
        num_epochs, batch_size, optimizer, loss_func, normalizer, train_method = load()

        if normalizer == 1:
            X_train = normalize.Simple_feature_scaling(X_train) 
            Y_train = normalize.Simple_feature_scaling(Y_train) 
            X_test = normalize.Simple_feature_scaling(X_test) 
            Y_test = normalize.Simple_feature_scaling(Y_test) 

        elif normalizer == 2:
            X_train = normalize.Min_Max(X_train) 
            Y_train = normalize.Min_Max(Y_train) 
            X_test = normalize.Min_Max(X_test) 
            Y_test = normalize.Min_Max(Y_test)  

        elif normalizer == 3:
            X_train = normalize.Z_Score(X_train) 
            Y_train = normalize.Z_Score(Y_train) 
            X_test = normalize.Z_Score(X_test) 
            Y_test = normalize.Z_Score(Y_test) 

        if train_method == 1:
            KFold_train(X_train, Y_train, X_test, Y_test, num_epochs, batch_size, optimizer, loss_func, model_path, log_path) 

        elif train_method == 2:
            norm_train(X_train, Y_train, X_test, Y_test, num_epochs, batch_size, optimizer, loss_func, model_path, log_path)

    except Exception as e:
        with open(f'{log_path}/training_exception.log', 'w') as f:
            f.write(str(e))