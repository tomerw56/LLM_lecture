#Docker for lora
## local folder
i have downloaded the model from https://huggingface.co/unsloth/Phi-3-mini-4k-instruct-bnb-4bit to the local folder and placed it under ```models```
the local folder should containe
- retrain.py
- test_cuda.py
- json_extraction_dataset_500.json
-the model -> model/Phi-3-mini-4k-instruct-bnb-4bit
## Activation
Build ```docker build -t unsloth-gpu .```
Execute 
```
docker run --gpus all -it --rm \
    -v "$(pwd)":/workspace \
    unsloth-gpu bash
Inside the container you will land in:
```
you will see
```/workspace```
which mirrors your host folder.

That means your Python script, JSON dataset, and outputs appear both inside the container and on your Windows drive.

Test GPU ```python test_cuda.py```
you should see:

```CUDA available: True Device: NVIDIA GeForce RTX XXXX```
run code
```python retrain.py```

## what i missed
i did not suceed in converting to ollam model with llama.cpp , i recomand you try it.
