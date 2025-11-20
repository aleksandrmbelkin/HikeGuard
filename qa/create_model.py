from transformers import AutoTokenizer, AutoModelForCausalLM
import os

def download_model():
    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
    local_path = "qa/model"
    
    print("Скачивание модели для генерации ответов...")
    os.makedirs(local_path, exist_ok=True)
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    tokenizer.save_pretrained(local_path)
    model.save_pretrained(local_path)
    
    print(f"Модель сохранена в {local_path}")

if __name__ == "__main__":
    download_model()