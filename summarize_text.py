import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

def get_word_meaning(word):
    meanings = wordnet.synsets(word)
    return meanings[0].definition() if meanings else "Meaning not found."