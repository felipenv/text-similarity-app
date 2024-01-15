import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import pandas as pd
import logging as logger
logger.getLogger().setLevel(logger.INFO)

nltk.download('punkt')
nltk.download('stopwords')


class Model:
    def __init__(self):
        """
        wv: gensim keyed vectors model
        phrases: dataframe with column Phrases read at app startup
        phrases_dict: same phrases but in dictionary with keys as sentence id,
        also done at startup
        tokenized: sentences tokenized with stopwords removed
        """
        self.wv = None
        self.stopwords = set(stopwords.words('english'))
        self.phrases = None
        self.phrases_dict = {}
        self.tokenized = {}
        self.phrases_embeddings = {}

    def fetch_model_from_drive(self, url, filename, model_path) -> None:
        os.system(f"wget {url} -O {filename}")
        os.system(f"gzip -d {filename}")
        os.system(f"mv {filename.removesuffix('.gz')} {model_path}"
                f"/{filename.removesuffix('.gz')}")

    def remove_stop_words(self, sentence):
        word_tokens = word_tokenize(sentence)
        filtered_sentence = [w for w in word_tokens if not w.lower() in self.stopwords]
        return filtered_sentence

    def load_phrases(self, config):
        self.phrases = pd.read_csv(config['data']['path'],
                                    encoding='latin').drop_duplicates().reset_index()
        self.phrases_dict = {index: row['Phrases'] for index, row in
                              self.phrases.iterrows()}

    def load_model(self, wv):
        self.wv = wv

    def tokenize_phrases(self):
        for sentence_id in self.phrases_dict:
            tokens = self.remove_stop_words(self.phrases_dict[sentence_id])
            self.tokenized[sentence_id] = tokens

    def embed_sentence(self, tk_sentence):
        embedding = np.zeros(300)

        for token in tk_sentence:
            if token in self.wv.key_to_index:
                emb_token = self.wv.get_vector(token)
            else:
                logger.warning(f"{token} not in vocabulary")
                emb_token = np.zeros(300)

            embedding += emb_token # sum all embeddings in sentence

        norm_embed = embedding / np.linalg.norm(embedding)

        return norm_embed

    def embed_all(self):
        for tokenized_id in self.tokenized:
            self.phrases_embeddings[tokenized_id] = self.embed_sentence(self.tokenized[tokenized_id])
