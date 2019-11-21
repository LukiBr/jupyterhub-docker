FROM jupyter/scipy-notebook

USER root

#############################
##         START           ##
## Install CUDA base image ##
#############################
# Source: https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu18.04/10.1/base/Dockerfile

RUN apt-get update && apt-get install -y --no-install-recommends \
gnupg2 curl ca-certificates && \
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | apt-key add - && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list && \
    apt-get purge --autoremove -y curl && \
rm -rf /var/lib/apt/lists/*

ENV CUDA_VERSION 10.1.243

ENV CUDA_PKG_VERSION 10-1=$CUDA_VERSION-1

# For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
        cuda-cudart-$CUDA_PKG_VERSION \
cuda-compat-10-1 && \
ln -s cuda-10.1 /usr/local/cuda

# Required for nvidia-docker v1
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=10.1 brand=tesla,driver>=384,driver<385 brand=tesla,driver>=396,driver<397 brand=tesla,driver>=410,driver<411"

###################
## CUDA base END ##
###################

###################
##      START    ##
## CUDA runtime  ##
## Source: https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu18.04/10.1/runtime/Dockerfile
###################

ENV NCCL_VERSION 2.4.8

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-$CUDA_PKG_VERSION \
cuda-nvtx-$CUDA_PKG_VERSION \
libnccl2=$NCCL_VERSION-1+cuda10.1 && \
    apt-mark hold libnccl2

####################
## CUDA runtime   ##
##       END      ##
####################

#########################
##         START       ##
## CUDA runtime cudnn7 ##
## Source: https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu18.04/10.1/runtime/cudnn7/Dockerfile

ENV CUDNN_VERSION 7.6.4.38
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcudnn7=$CUDNN_VERSION-1+cuda10.1 \
&& \
    apt-mark hold libcudnn7

## CUDA runtime cudnn 7 ##
##         END          ##
##########################


######################################################
## Jupyterlab container of university of versaille  ##
## Source: The repo forked from                     ##
######################################################

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata \
    gfortran \
    gcc \
    scilab \
    pari-gp \
    libpari-dev \
    libgmp-dev \
    build-essential \
    wget \
    sudo \
    cmake \
    curl \
    g++ \
    git \
    pkg-config \
    software-properties-common \
    python3-dev \
    libzmq3-dev \
    libcurl4-gnutls-dev \
    libssl-dev \
    graphviz \
    libgraphviz-dev \
    libboost-all-dev \
    libgflags-dev \
    libgoogle-glog-dev \
    libhdf5-serial-dev \
    libleveldb-dev \
    liblmdb-dev \
    libopencv-dev \
    libprotobuf-dev \
    libsnappy-dev \
    protobuf-compiler \
    libopenblas-dev \
    && apt-get clean


USER $NB_UID

# Update conda
RUN conda update -n root conda && \
    fix-permissions $CONDA_DIR

# Add some R stuff
RUN conda install --quiet --yes \
    r-base \
    r-irkernel \
    r-plyr \
    r-devtools \
    r-tidyverse \
    r-shiny \
    r-rmarkdown \
    r-forecast \
    r-rsqlite \
    r-reshape2 \
    r-nycflights13 \
    r-caret \
    r-rcurl \
    r-crayon \
    r-randomforest \
    r-htmltools \
    r-sparklyr \
    r-htmlwidgets \
    r-hexbin=1.27 \
    jupyterhub \
    julia && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR

ENV CPATH=$CONDA_DIR/include

RUN pip install \
    pari_jupyter \
    scilab-kernel && \
    fix-permissions $CONDA_DIR


## Stuff of Uni Versailles Image  ##
##          END             ##
##############################

###################################
## Content of our old GPU Image ##
###################################

# Install KERAS + SCIKIT + Data Science Libs
RUN pip install -U \
                virtualenv \
                cython \
		            scipy \
		            numpy \
		            keras \
		            scikit-learn \
		            psycopg2-binary \
		            sqlalchemy \
		            bokeh \
		            matplotlib \
		            pandas \
		            nltk \
		            pydot \
		            seaborn \
		            graphviz \
	 	            xgboost \
		            catboost \
		            opencv-python \
		            tqdm \
		            tslearn \
                bert-serving-server \
                bert-serving-client && \
                fix-permissions $CONDA_DIR

USER root

# Install nodejs to be able to use the extension manager in jupyterlab
RUN conda install -c conda-forge nodejs && \
    fix-permissions $CONDA_DIR

# Install Tensorboard for jupyterlab
RUN jupyter labextension install jupyterlab_tensorboard && \
    fix-permissions $CONDA_DIR

# Install bash kernel
RUN pip install bash_kernel && \
    fix-permissions $CONDA_DIR
RUN python -m bash_kernel.install && \
    fix-permissions $CONDA_DIR

RUN fix-permissions $HOME
# TODO: check if needed, probably not needed
RUN fix-permissions /etc/jupyter/

# Expose Tensorboard
EXPOSE 6006

USER $NB_UID

# Install tensorflow
RUN conda install --quiet --yes tensorflow-gpu tensorboard && \
    fix-permissions $CONDA_DIR
RUN conda install --quiet --yes pytorch torchvision -c pytorch && \
    fix-permissions $CONDA_DIR

# Add conda env hook
COPY ./conda-activate.sh /usr/local/bin/before-notebook.d/
