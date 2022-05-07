<h2><i>Deep Distributed System Training</i></h2>

The purpose of this program is to speed up the learning of the deep learning model and prevent the system from crashing.<br>
This program speeds up training by dividing a data set between multiple clients.
Each client is responsible for teaching the deep learning model with only the part of the data set that is specified for it, not the entire data set.<br>

<img src="https://github.com/AntonioMinkowski/Deep-Distributed-Training-Systems/blob/main/how_it_works.png" alt="How it's work" title="deep distributed system training"></img>

The server receives the deep learning model and sends it to all clients.
It then determines a portion of the data set for each client and sends it to the client.
Clients begin to learn the deep learning model using the data provided by the server.<br>
Clients teach the model using the k-fold method.
Also clients save logs during training.
Finally, the server collects all the trained models along with the logs from the clients.
