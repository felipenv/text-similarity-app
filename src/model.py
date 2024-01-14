import os


class Model:
    def __init__(self):
        self.wv = None

    def fetch_model_from_drive(self, url, filename, model_path):
        os.sys(f"wget {url} -O {filename}")
        os.sys(f"gzip -d {filename}")
        os.sys(f"mv {filename.removesuffix('.gz')} {model_path}/{filename.removesuffix('.gz')}")