import flask
def create_app():
    app = flask.Flask(__name__)
    app.config['ERROR_404_HELP'] = False
    return app

app = create_app()
