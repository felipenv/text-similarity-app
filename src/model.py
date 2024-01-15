import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
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

    @staticmethod
    def fetch_model_from_drive(self, url, filename, model_path) -> None:
        os.sys(f"wget {url} -O {filename}")
        os.sys(f"gzip -d {filename}")
        os.sys(f"mv {filename.removesuffix('.gz')} {model_path}/{filename.removesuffix('.gz')}")

    def remove_stop_words(self, sentence):
        word_tokens = word_tokenize(sentence)
        filtered_sentence = [w for w in word_tokens if not w.lower() in self.stopwords]
        return filtered_sentence

    def tokenize_phrases(self):
        for sentence_id in self.phrases_dict:
            tokens = self.remove_stop_words(self.phrases_dict[sentence_id])
            self.tokenized[sentence_id] = tokens

    def embed_sentence(self, sentence):
        pass