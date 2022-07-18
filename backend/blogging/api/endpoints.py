from app import app

from ..containers import container


PREFIX = container.config.mandatory_settings.api_prefix()


@app.route(f"{PREFIX}/user/", methods=["POST"])
def create_user(data):
    print(data)

