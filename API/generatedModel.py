import random
import io
from keras.models import load_model
import mysql.connector
import pandas as pd
import numpy as np


maxlen = 100

with io.open(f'C:/Users/artur/code/NPL/proyecto/Generative model/vocabulary.txt', encoding="utf-8") as f:
    text = f.read().lower()
text = text.replace("\n", " ")  # We remove newlines chars for nicer display

chars = sorted(list(set(text)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

model = load_model(f'C:/Users/artur/code/NPL/proyecto/Generative model/tweets.v1.modelgenerative.hdf5')

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generate(model, sentence, diversity):
    generated = ""
    for i in range(100):
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence)  :
            x_pred[0, t, char_indices[char]] = 1.0
        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]
        sentence = sentence[1:] + next_char
        generated += next_char

    return generated

def predict_get():
    # connect to the database
    db_connection = mysql.connector.connect(
        host="localhost", 
        user="root",
        passwd="",
        database="databasecovid"
    )
    df = pd.read_sql('SELECT pure_tweet, toxic FROM {}'.format('tweetsCovid'), con = db_connection)
    df = df[df['toxic'] == 1]
    toxic_tweet = np.random.choice(df['pure_tweet'].to_numpy(), 1)[0]
    toxic_tweet = toxic_tweet.lower()
    gen_text = generate(model, toxic_tweet, 0.5)
    return (toxic_tweet,gen_text)
    

def predict_post(text: str, diversity: float = 0.5):
    text = text.lower()
    gen_text = generate(model, text, diversity)
    return gen_text