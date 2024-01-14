import logging as logger
import os
import yaml
from gensim.models import KeyedVectors

from fastapi import FastAPI
from .model import Model

logger.getLogger().setLevel(logger.INFO)

app = FastAPI()

model = Model()
config = yaml.safe_load(open("/home/app/config/config.yaml", "r"))


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


@app.get("/model")
async def model_available():
    if model.wv is not None:
        return {"message": "model is available"}
    else:
        return {"message": "model is not loaded"}


