from dotenv import load_dotenv
from flask import Flask

from blogging.containers import container
import blogging.database.models as models


def load_blog_dotenv(secrets_file: str):
    load_dotenv(secrets_file)


def create_app():
    load_blog_dotenv(container.config.secrets.get("secrets_file"))
    app = Flask(__name__)
    app.config.update({
        # Update config here.
    })
    return app


app = create_app()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
