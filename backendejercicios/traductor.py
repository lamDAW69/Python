from transformers import TFMarianMTModel, MarianTokenizer

# Cargar el modelo y el tokenizer
model_name = 'Helsinki-NLP/opus-mt-es-en'
model = TFMarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)

def traducir_a_ingles(texto):
    # Tokenizar la entrada en español
    inputs = tokenizer(texto, return_tensors="tf", padding=True)

    # Realizar la traducción
    translated = model.generate(**inputs)

    # Decodificar y devolver la traducción
    traduccion = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    
    return traduccion

