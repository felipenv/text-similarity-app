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

config = yaml.safe_load(open("/home/app/config/config.yaml", "r"))
model = Model()


def cosine_similarity(u, v):
    return np.dot(u, v)/(np.linalg.norm(u)*np.linalg.norm(v))


@app.on_event("startup")
async def startup_event():
    if config['download_model']['filename'].removesuffix('.gz') not in \
            os.listdir(config['download_model']['model_path']):
        logger.info("downloading model...\n")

        model.fetch_model_from_drive(config['download_model']["url"], config[
            'download_model']["filename"], config['download_model']["model_path"])
    else:
        logger.info("model already downloaded...\n")

    # load model
    wv = KeyedVectors.load_word2vec_format(
        f"{config['download_model']['model_path']}/"
                                           f"{config['download_model']['filename'].removesuffix('.gz')}", binary=True, limit=1000000)
    model.load_model(wv)
    logger.info("model loaded to memory..\n")

    # load phrases and tokenize
    model.load_phrases(config)
    model.tokenize_phrases()

    logger.info("data loaded and tokenized...\n")
    logger.info("embedding data...\n")
    model.embed_all()
    logger.info("embedding completed...\n")


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
async def tokens():
    return model.tokenized


@app.get("/batch_phrases_similarity")
async def phrases_similarity():
    sim_df = pd.DataFrame(
        np.diag(np.diag(np.ones(shape=(len(model.phrases), len(model.phrases))))))

    for c in sim_df.columns:
        for r in range(0, c + 1):
            similarity = cosine_similarity(model.phrases_embeddings[c],
                                           model.phrases_embeddings[r])
            sim_df[c][r] = similarity
            sim_df[r][c] = similarity # matrix is simetric on the diagonal

    return sim_df


@app.get("/most_similar")
async def most_similar(sentence):
    max_similarity = 0
    max_id = None
    tokenized_sentence = model.remove_stop_words(sentence)
    embedded_sentence = model.embed_sentence(tokenized_sentence)

    for id in model.phrases_embeddings:
        similarity = cosine_similarity(embedded_sentence, model.phrases_embeddings[id])
        if similarity > max_similarity:
            max_similarity = similarity
            max_id = id

    return {"sentence_similar:": model.phrases_dict[max_id],
            "similarity:": max_similarity}
