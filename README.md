# LLM_lecture
this is a bunch of demos thst go with my llm hands on team ppt

# Image creation
we use https://huggingface.co/stabilityai/stable-diffusion-2-1
in order to work wit it i followed the documentation on that page

but in general

Pick the right command based on your GPU driver version.
use ```nvidia-smi```

If you have CUDA 12.1 (most modern cards):
```uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121```
If you have CUDA 11.8:
```uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118```
Verify GPU:
```python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"```
You should see:
your graphic card
🤖 4️⃣ Install Transformers, Accelerate, and Diffusers
```Use uv pip install for speed (it reuses wheels from cache):```
```uv pip install transformers accelerate huggingface_hub safetensors```
For image/text-to-image models (like FLUX):
```uv pip install diffusers[torch]```
Optional (for performance):
```uv pip install xformers```