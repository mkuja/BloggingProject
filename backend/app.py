from flask import Flask
from dotenv import load_dotenv



def load_blog_dotenv(secrets_file: str):
    load_dotenv(secrets_file)


def app_factory():
    app = Flask(__name__)
    return app

app = app_factory()

import blogging.api.endpoints
