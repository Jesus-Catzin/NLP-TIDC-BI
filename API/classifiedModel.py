import json

from keras.preprocessing.text import tokenizer_from_json
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# open and store the tokenizer 
with open('C:/Users/artur/code/NPL/proyecto/Classification Model/tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)
    
# open and store the model 
model = load_model('C:/Users/artur/code/NPL/proyecto/Classification Model/FinalModel.model', compile = True)

def predict(text):

    split_word = [word.split() for word in [text]]
    split_word = [[word for word in split_word[0] if word in tokenizer.word_index]]
    tokenizer.fit_on_texts(split_word) 
    X_data = tokenizer.texts_to_sequences(split_word)
    X_data = pad_sequences(X_data, padding = 'pre', maxlen = 20)
    toxic = int((model.predict(X_data) > 0.5).astype(int)[0][0])

    if toxic == 0:
        return "No toxic"
    if toxic == 1:
        return "Toxic"
