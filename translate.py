from transformers import MarianMTModel, MarianTokenizer

def translate_text(text, model_name="Helsinki-NLP/opus-mt-ar-pl"):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)  # type: ignore
    return tokenizer.decode(translated[0], skip_special_tokens=True)
