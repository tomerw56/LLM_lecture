#build with docker build -t unsloth-gpu .
# run with 

# Base image with CUDA + cuDNN
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y git git-lfs && rm -rf /var/lib/apt/lists/*
RUN git lfs install

# Install Python + basic tools
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv git wget curl && \
    rm -rf /var/lib/apt/lists/*


# Make python3 the default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
RUN python -m pip install  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip

# Install CUDA-enabled PyTorch for Linux
RUN pip install torch torchvision torchaudio 

# Install Unsloth + dependencies
RUN pip install unsloth transformers trl datasets accelerate bitsandbytes

#SETUP certificates
RUN apt-get update && apt-get install  ca-certificates && update-ca-certificates

# Set the working directory
WORKDIR /workspace

# Default command: bash shell
CMD ["/bin/bash"]
