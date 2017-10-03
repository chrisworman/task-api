#!env/bin/python
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
#app.config.from_object('config')
#app.config.from_pyfile('config.py')

# Now we can access the configuration variables via app.config["VAR_NAME"].

# Routes ...

@app.route('/')
def index():
    return "Tasks api v1.1"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
