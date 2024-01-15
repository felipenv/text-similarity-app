Simple app for checking text similarity

## Build image

```shell
docker image build -f Dockerfile -t text_app .
```

## Run container

```shell
docker run -p 8895:8888 --name=test --cpus=1 --memory=16g --shm-size=8g text_app python3 -m uvicorn src.app:app --host 0.0.0.0 --port 8888 --reload
```

On app startup, it will check if word2vec is available, if not it will download it 
from google drive.

to avoid the download time, you can mount a file `GoogleNews-vectors-negative300. bin` to path `/home/app/model`

## Check on browser 
`localhost:8895/docs`

## Endpoints docs 

- `/model`: says if model is loaded and available
- `/phrases`: shows sentences in the loaded data
- `/tokenized`: shows sentences after tokenization and removal of stop words
- `/batch_phrases_similarity`: compute and returns pairwise similarity between 
  sentences in the dataset
- `/most_similar`: receive sentence as input and returns most similar sentence in 
  dataset and the corresponding similarity score.
