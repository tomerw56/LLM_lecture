import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def query_model(model_path:str,prompt:str,max_new=200, temperature=0.7)->str:
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        trust_remote_code=True,
    )

    # Switch to eval mode
    model.eval()

    print("\n🔥 Model loaded. You can now test prompts.\n")


    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        add_special_tokens=True,
    )

    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new,
            temperature=temperature,
            do_sample=True,
        )

    return tokenizer.decode(output[0], skip_special_tokens=True)
if __name__ == "__main__":
    prompt = "Extract the product information:\n<div class='product'><h2>iPad Air</h2><span class='price'>$1344</span><span class='category'>audio</span><span class='brand'>Dell</span></div>"

    print("working with original model...")
    response = query_model(model_path=r"./models/Phi-3-mini-4k-instruct-bnb-4bit", prompt=prompt)
    print("\nResponse:\n", response)

    print("working with retrained model...")
    response=query_model(model_path="retrained_model",prompt=prompt)
    print("\nResponse:\n", response)
