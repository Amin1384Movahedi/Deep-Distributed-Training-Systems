import tensorflow as tf
import socket
import os 

# # Create our trainer
# def train(model, epochs, batch_size):
#     model_path = os.getcwd() + '/' + socket.gethostname() + '.h5'

#     # Make sure the name of model's file we want to train is exists
#     if not os.path.exists(model_path):
#         return F'{socket.gethostname()}.h5 is not exist!'

#     # Load the model file
#     model = tf.keras.models.load_model(model_path)

#     history = model.fit(X, Y,
#                         epochs=epochs,
#                         batch_size=batch_size,
#                         shuffle=True,
#                         )