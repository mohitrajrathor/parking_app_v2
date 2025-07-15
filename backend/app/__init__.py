# factory file of mad 2 project backend application.

# imports
from flask import Flask, render_template, send_from_directory
import os
from .configs import Config
from .extensions import db, migrate, jwt, mail, cors, celery_init_app, api, cache


def create_app():
    app = Flask(
        __name__,
        static_folder="../../frontend/dist/",
        template_folder="../../frontend/dist/",
    )

    ####### configs ########
    app.config.from_object(Config)

    ####### extension init #######
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(
        app,
        resources={r"/api_v1/*": {"origins": ["http://localhost:5173", "*"]}},
        supports_credentials=True,
    )
    cache.init_app(app)

    celery_init_app(app)

    ####### models init #######
    with app.app_context():
        from .utils import create_models, populate

        create_models()
        populate()

    ####### blueprints ########
    from .api_v1 import api_v1

    api.register_blueprint(api_v1)

    ####### Basic routes #######
    @app.route("/")
    @cache.cached(timeout=60 * 60 * 24)
    def index():
        return render_template("index.html")

    @app.route("/<path:path>")
    @cache.cached(timeout=60 * 60 * 24)
    def static_path(path):
        file_path = os.path.join(app.static_folder or "", path)
        if os.path.isfile(file_path):
            return send_from_directory(app.static_folder or "", path)
        else:
            return render_template("index.html")

    @app.errorhandler(500)
    @cache.cached(timeout=60 * 60 * 24)
    def internal_error(error):
        return {"message": "Internal Server Error"}, 500

    return app
