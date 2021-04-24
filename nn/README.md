# Neural Networks
###### Nick DeMarchis, April 23, 2021, [ned004@](mailto:ned004@bucknell.edu)

## Getting started
* ensure that all files in the `nn` folder are initialized with the following file structure:
**PLEASE NOTE** that both `malmoEnv` and `malmoenv` folders are untracked. they must be installed following the guidelines [here](https://eg.bucknell.edu/~cld028/courses/357-SP21/NN/Neural_Net_Assignment.html).
    * `malmoEnv`
        * `Include`
        * `Lib`
        * `Scripts`
        * `pyvenv.cfg`
    * `malmoenv`
        * `malmoenv`
            * `Minecraft`
            * `Schemas`
            * `...`
    * `MalmoSim.py`
    * `NN.py`
    * `NeuralMMAgent.py`
* ensure that all necessary dependencies are installed, run: 
    ```cmd
    python -m pip install gym lxml numpy pillow
    ```
* follow directions [here](https://eg.bucknell.edu/~cld028/courses/357-SP21/NN/Neural_Net_Assignment.html#getting-started-with-malmo) to set up for your environment, this was developed on the Linux space so here's what was done:
    * in terminal 1, set at level `nn`, run 
        ```
        source malmoEnv/bin/activate
        ```
    * in terminal 2, set at the level `nn\malmoenv\malmoenv`, run:
        ```
        module load java/1.8
        sh Minecraft/launchClient.sh -port 9000 -env
        ```
    * in terminal 1, after the Minecraft window has loaded and you're at the landing screen, run 
        ```
        python MalmoSim.py
        ```
that's it! you should be all good to go, training your neural network

## Info and customizations
`NN.py`, implemented in `MalmoSim.py`, uses a Keras neural-network that is trained at runtime. that is, no record is stored between runs. this is definitely something that could be further implemented in the future.  

To change the number of epochs used in the simulation, go to line 62 in `NN.py`. This is a clunky implementation, but one that works. It's part of the core of the neural net, as displayed below:
```python
def train_net(self, inny, outy, max_sse, max_num_epoch):
    model = Sequential()
    model.add(Dense(self.num_in_nodes, input_dim=len(inny[0]), activation="relu"))
    for i in range(self.num_hid_layers):
        model.add(Dense(self.num_hid_nodes, activation='relu'))
    model.add(Dense(len(outy[0]), activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # fit the keras model on the dataset
    model.fit(inny, outy, epochs=1000, batch_size=10)
    _, accuracy = model.evaluate(inny, outy)
    print('Accuracy: %.2f' % (accuracy*100))
```

## For growth
Is my clever way of saying that I didn't do everything that I desired to. For example, I didn't have time to implement the graphing utility, so in order to start the program, it's necessary to close out of the empty `matplotlib` window. Obviously that's something huge missing on my part, but my tunnel vision on getting *some* neural net working ended up coming first. I hope, for the final project, to have a larger hand in practically implementing the neural net. This was *fun* (or should I say stuff like this has the potential to be even more fun), and I just wish that I had more time to complete it. 