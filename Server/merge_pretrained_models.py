import os 
import tensorflow as tf
import sys

# List of pre trained models in .h5 format in "pre_trained_models/" directory.
model_path = [model for model in os.listdir(f'pre_trained_models/') if model.endswith('.h5')]
models = []

# If the "model_path" list length was 0, it means that there are no pre-trained models.
if len(model_path) == 0:
    sys.exit('There is no pre trained model!')

# Loading the base deep learning model and extracting the input shape from that.
base_model_path = [model for model in os.listdir('model/') if model.endswith('.h5')]
base_model = tf.keras.models.load_model(base_model_path[0])
input_shape = base_model.input_shape

# Ensembling the pre trained models
Input = tf.keras.layers.Input(shape=input_shape)

for model in model_path:
    temp = tf.keras.models.load_model(f'{os.getcwd()}/{model}')
    temp = temp(Input)
    models.append(temp)

Output = tf.keras.layers.average(models)
ensemble_model = tf.keras.models.Model(inputs=Input, outputs=Output)

if not os.path.exists('ensembled_model/'):
    os.mkdir('ensembled_model')

ensemble_model.save('ensembled_model/ensembled.h5')