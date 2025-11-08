
from diffusers import DiffusionPipeline
import torch


# Local path to your model (mounted into container)
model_path = "/models/stable-diffusion-xl-base-1.0"

print(f"Loading model from: {model_path}")

pipe = DiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float32, use_safetensors=True)
pipe.to("cuda")



# if using torch < 2.0
# pipe.enable_xformers_memory_efficient_attention()

prompt = "An astronaut riding a green horse"
print(f"processing {prompt}")
images = pipe(prompt=prompt, num_inference_steps=10, guidance_scale=7.5).images[0]
images.save("demo.png")