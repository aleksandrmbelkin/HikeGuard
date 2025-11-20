import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class QASystem:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = "qa/model"
        self.tokenizer = None
        self.model = None
    
    def load_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path).to(self.device)
    
    def answer_question(self, context, question):
        # Более строгий промпт для коротких ответов
        prompt = f"""Дай краткий ответ на вопрос на основе контекста.
        
Контекст: {context}

Вопрос: {question}

Краткий ответ:"""
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=50,      # Сильно уменьшаем максимальную длину
                min_new_tokens=1,       # Минимум 1 токен
                temperature=0.3,        # Низкая температура для точности
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.5, # Сильный штраф за повторения
                no_repeat_ngram_size=2,
                length_penalty=0.5,     # Штрафуем длинные ответы
                early_stopping=True     # Останавливаемся когда ответ готов
            )
        
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer = full_response.replace(prompt, "").strip()
        
        # Дополнительная очистка ответа
        answer = self._clean_answer(answer)
        
        return answer
    
    def _clean_answer(self, answer):
        """Очищает ответ от лишних частей"""
        # Обрезаем при первом переходе на новую строку
        if '\n' in answer:
            answer = answer.split('\n')[0]
        
        # Обрезаем при начале нового вопроса или контекста
        stop_phrases = ['Вопрос:', 'Контекст:', '###', '---', 'Ответ:', 'Краткий ответ:']
        for phrase in stop_phrases:
            if phrase in answer:
                answer = answer.split(phrase)[0]
        
        # Обрезаем слишком длинные ответы (больше 3 предложений)
        sentences = answer.split('. ')
        if len(sentences) > 3:
            answer = '. '.join(sentences[:3]) + '.'
        
        return answer.strip()

def main():
    qa = QASystem()
    qa.load_model()
    
    context = "Эверест - высочайшая гора мира высотой 8848 метров. Первое восхождение совершили Эдмунд Хиллари и Тенцинг Норгей в 1953 году."
    question = "Кто первым покорил Эверест?"
    
    answer = qa.answer_question(context, question)
    print(f"Ответ: {answer}")

if __name__ == "__main__":
    main()