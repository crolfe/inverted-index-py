from flask import Flask


app = None


def get_app():
    global app

    if app is None:
        app = Flask(__name__)

    return app


def init():
    app = get_app()

    from inverted_index.api.search import search_bp
    app.register_blueprint(search_bp)

    return app


if __name__ == '__main__':
    app = init()
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
