import logging as logger
import os
import numpy as np
import pandas as pd
import yaml
from gensim.models import KeyedVectors

from fastapi import FastAPI
from .model import Model

logger.getLogger().setLevel(logger.INFO)

app = FastAPI()

model = Model()
config = yaml.safe_load(open("/home/app/config/config.yaml", "r"))


def cosine_similarity(u, v):
    return np.dot(u, v)/(np.linalg.norm(u)*np.linalg.norm(v))


@app.on_event("startup")
async def startup_event():
    if config['download_model']['filename'].removesuffix('.gz') not in \
            os.listdir(config['download_model']['model_path']):
        logger.info("downloading model...")

        model.fetch_model_from_drive(config['download_model']["url"], config[
            'download_model']["filename"], config['download_model']["model_path"])
    else:
        logger.info("model already downloaded...")

    # load model
    wv = KeyedVectors.load_word2vec_format(
        f"{config['download_model']['model_path']}/"
                                           f"{config['download_model']['filename'].removesuffix('.gz')}", binary=True, limit = 1000000)
    model.wv = wv
    logger.info("model loaded to memory..")

    # load phrases and tokenize
    model.phrases = pd.read_csv(config['data']['path'], encoding='latin')
    model.phrases_dict = {index: row['Phrases'] for index, row in
                          model.phrases.iterrows()}
    model.tokenize_phrases()
    logger.info("data loaded and tokenized..")


@app.get("/model")
async def model_available():
    if model.wv is not None:
        return {"message": "model is available"}
    else:
        return {"message": "model is not loaded"}

@app.get("/phrases")
async def phrases():
    return model.phrases_dict

@app.get("/tokenized")
async def phrases():
    return model.tokenized