import pickle
from gensim.utils import simple_preprocess
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress INFO and WARNING logs from TensorFlow

import logging
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)  # Suppress absl logs
absl.logging.set_stderrthreshold('error')


model_path = os.path.join(os.path.dirname(__file__), 'model_pickle.pkl')


word_index_path= os.path.join(os.path.dirname(__file__), 'word_index.pkl')
with open(model_path,'rb') as f:
    model=pickle.load(f)

with open(word_index_path,'rb') as ff:
    word_index=pickle.load(ff)




def pred(text):

    token=simple_preprocess(text)

    sequence=[word_index.get(word,0) for word in token]
    padded=pad_sequences([sequence],padding='post',maxlen=10)

    prediction = model.predict(padded)

    predicted_index = prediction.argmax(axis=1)[0]
    emoji_dict = {0: '😇', 1: '😊', 2: '😍', 3: '😎', 4: '😡', 5: '😢',
              6: '😱', 7: '😴', 8: '🤒', 9: '🤓', 10: '🤔', 11: '🤗',
              12: '🤯', 13: '🥳'}

    predicted_emoji = emoji_dict[predicted_index]
    return predicted_emoji

