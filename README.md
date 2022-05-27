<h2><i>Deep Distributed System Training</i></h2>

The purpose of this program is to speed up the learning of the deep learning model and prevent the system from crashing.<br>
This program speeds up training by dividing a data set between multiple clients.
Each client is responsible for teaching the deep learning model with only the part of the dataset that is specified for it, not the entire data set.<br>

<img src="https://github.com/AntonioMinkowski/Deep-Distributed-Training-Systems/blob/main/how_it_works.png" alt="How it's work" title="deep distributed system training"></img>

The server receives the deep learning model and sends it to all clients.
It then determines a portion of the data set for each client and sends it to the client.
Clients begin to train the deep learning model using the data provided by the server.<br>
Clients train the model using the k-fold method and normal model.fit() method.
User can choose the normalizer method for input data.<br>
Also clients save logs during training.
Finally, the server collects all the trained models along with the logs from the clients.<br><br>

<img src="https://github.com/AntonioMinkowski/Deep-Distributed-Training-Systems/blob/main/simple_diagram.jpeg" alt="Diagram" title="deep distributed system training diagram"></img>

First we need to create and compile our deep learning model in the tensorflow framework and finally save it in h5 format using model.save() and place it in the model folder on the server.<br>
To use this program at first we need to enter the IP and server port then the server is activated.<br>
If we want to start training deep learning model, we have to enter the letter Y in the next question. If we enter the letter n, the server starts collecting models from clients.
But if we enter the letter y, then we have to enter the model name, the number of clients that do the training processes.<br>
User should set a passphrase for the server and all of clients have to enter the passphrase to connect to the server.<br><br>

And then we have to enter the training parameters such as number of epoch, batch size and so on.
The server then sends the learning model file and dataset to all clients that connect to the server.<br>
Finally we can use the training data in three ways, we can use the dataset as .npz or .csv or .xlsx files located on the server in the dataset directory.<br> 
Note: Input and output data must be separate, input data files must be in the dataset/X path and output data must be in the dataset/Y path.
We can use multiple files in different formats.<br>
If we manually distribute the data in the clients, we can enter the number "2" to the clients to send the command to load the dataset from the dataset/X and dataset/Y folders located in the clients.<br>
We can also use the dataset that exists in the keras module, for this we have to enter the number "3" and then we have to enter the name of the dataset and the value of the dataset.<br>
Then user have to choose the normalizer method for input data, user can use "Simple Feature Scaling", "Min-Max" and "Z-Score" normalizer.<br>
After that, user have to choose the training method, for K-Fold Cross Validation method we must enter "1" and to use normal model.fit() method we have to enter "2".<br>
Next we need to enter the input and output order of the data that the program loaded from keras module.
If we want our deep learning model to receive input data and predict output data, we must enter XY, and if we want our deep learning model to receive input data and reconstruct input data, like an autoencoder model, we must XX Enter.<br><br>

<h2>LICENSE</h2>
<hr>
<a href='https://github.com/AntonioMinkowski/Deep-Distributed-Training-Systems/blob/main/LICENSE'> License </a>