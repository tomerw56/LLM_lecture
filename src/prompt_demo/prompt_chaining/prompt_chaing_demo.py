import torch
from diffusers import StableDiffusionPipeline,DPMSolverMultistepScheduler
model_path = r"d:\models\stable-diffusion-2-1"
pipe = StableDiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
prompt = "a photo of an astronaut riding a horse on mars"
print(f"prompt: {prompt}")
images=pipe(prompt)
print(f"len(images) = {len(images)}")
image = pipe(prompt).images[0]
image.save("./astronaut_rides_horse.png")