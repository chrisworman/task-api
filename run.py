#!env/bin/python
import os

from app import create_app

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app(config_name)
app.run(host= "0.0.0.0")
