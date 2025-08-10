from huggingface_hub import InferenceClient
import traceback

API_TOKEN = "Your API Key"

client = InferenceClient(token=API_TOKEN)

def generate_text(prompt):
    try:
        response = client.text_generation(prompt, model="distilgpt2")
        generated_text = response[0]['generated_text']
        return generated_text
    except Exception as e:
        print("Exception occurred:")
        traceback.print_exc()
        return f"Error generating text: {e}"

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    output = generate_text(prompt)
    print("Generated Text:")
    print(output)
