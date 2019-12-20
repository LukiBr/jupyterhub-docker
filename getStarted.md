# Start

Dear user,

this ReadMe should prepare you to work with the DBVIS GPU Server.  
It is conceived as a guide to using every possibility of the server.

# Usage

There are two major options to use the server:
 - Jupyter Notebooks
 - Terminal Access

## Jupyter Notebooks

Jupyter Notebooks are built as a Python or R terminal emulation.
It enables easier access to build small programs faster and more efficient.
You can create a new one by pressing the New button and select a new Python or R kernel.
It is advised to use them as you can test your Python or R code more easily with them and if your development stage is over, you can export them as Python or R scripts.

## Terminal Access

Another option is the built-in terminal and editor of Jupyterhub.
You can open nearly every text file with the editor provided by Jupyterhub. This works like a typical desktop environment by either clicking on the file or by creating a new one.
Opening a terminal works with New button and then the terminal button.
Afterward, you can navigate to your script and run it with the command line.

# Advises

## Server Resources

* Make sure you do not use mor than 20 GB of RAM, otherwise the server will kill you process. 
* Please do not use the CPUs for training models

## Virtual Environment

The server is equipped with the many python frameworks and libraries. In case you need additional libraries you can create a virtual environment to add them and start Jupyter notebook via the new virtual environment. Use the following snippet to create a new virtual environment:

1. Open a terminal and follow the instructions below:  
  ```
 ## Init conda ##
 conda init bash
 exec bash

 ## Create new conda environment using all already install packages ##
 ## and add an example package                                      ##
 # Create env (using all already installed packages => --clone base)
 conda create --prefix=$name --clone base
 # Activate new env
 conda activate $HOME/name
 # Install new packages, here e.g. upgrade to tensorflow 2.0
 pip install tensorflow-gpu
 # Add the new environment as a new ipython kernel to be able to start notebooks from it
 ipython kernel install --user --name=$name 
 # deactivate env
 conda deactivate

 # remove an env
 conda env remove --p $HOME/$name
  ```

2. Now you can create new Jupyter notebooks using the virtual environment from the jupyterlab launcher.

## GPU Status

You can see the available GPUs as well as the available VRAM by typing `nvidia-smi` in a terminal.

## GPU Usage

Please make sure to just use **only one** GPU at the same time. After checking for an available GPU, you can specify the GPU (by id) inside your Jupyter notebooks using the following snippet:

```
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"]="0"         # the ID of the GPU (view via nvidia-smi)
```

**After finishing using the GPUs, please explicitly stop your Juypter notebooks, since otherwise the VRAM occupied might not be freed.**

## Tensorflow

If you are using Tensorflow or a framework, which runs Tensorflow in the background, it is advised to use:
```
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config, ...)
```
or Keras
```
from keras import backend as K
config = K.tf.ConfigProto()
config.gpu_options.allow_growth = True
K.set_session(K.tf.Session(config=config))
```
To limit the amount of GPU memory Tensorflow uses.
Else Tensorflow will use all available GPU memory, which blocks other users and leads to your process is killed.


# Dont's

- Do not use more space than you need. This means if your data is too large, use the database server to store it. There are enough options to use Python and a database server efficiently.
- Do not block all of the available space of the different GPUs. Either block one GPU entirely or try to use the allow growth option of tensorflow.
