#build docker build -t flux-demo .
#use docker run --rm -it --gpus all -v /mnt/d/models:/models -v ${PWD}:/app flux-demo
#note you need to set the model correct directory

# Use a verified PyTorch + CUDA image
FROM pytorch/pytorch:2.5.0-cuda12.1-cudnn9-runtime


# Install dependencies
RUN apt-get update && apt-get install -y git git-lfs && rm -rf /var/lib/apt/lists/*
RUN git lfs install

# Working directory
WORKDIR /app
RUN python -m pip install  --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip

# Install Python packages for diffusers pipeline
RUN pip install --no-cache-dir diffusers transformers accelerate safetensors torch torchvision protobuf sentencepiece

# Copy demo script
COPY demo.py .

# Run demo by default
CMD ["python", "demo.py"]
