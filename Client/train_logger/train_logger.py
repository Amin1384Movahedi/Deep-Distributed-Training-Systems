import matplotlib.pyplot as plt

# Create the history logger function
# This function plot the network_history object and save it in .png format in log/ folder
def train_history_logger(network_history, index, log_path):
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
    plt.savefig(f'{log_path}/history_of_losses({index}).png')

    # Plot accuracy and validation accuracy per each epochs and saving the figure in log folder
    plt.figure()
    plt.grid()
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.plot(accuracies)
    plt.plot(validation_accuracies)
    plt.legend(['accuracy', 'validation_accuracy'])
    plt.savefig(f'{log_path}//history_of_accuracies({index}).png')