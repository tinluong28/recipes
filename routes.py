from config import app
from controller_functions import test

app.add_url_rule('/test', view_func=test)
