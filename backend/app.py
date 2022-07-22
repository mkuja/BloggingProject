from dotenv import load_dotenv

from blogging.di.db_services_container import db_services_container
from blogging.di.other_services_container import app_services_container
from blogging.init import init

load_dotenv()

app_services_container.wire(modules=["app"], packages=["blogging"])
db_services_container.wire(modules=["app"], packages=["blogging"])

app = init.init()
