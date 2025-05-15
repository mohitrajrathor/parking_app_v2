# factory file of mad 2 project backend application.

# imports
from flask import Flask, render_template, send_from_directory
import os
from .configs import Config
from .extensions import db, migrate, jwt, mail


def create_app():
    app = Flask(
        __name__,
        static_folder="../../frontend/dist",
        template_folder="../../frontend/dist",
    )

    ####### configs ########
    app.config.from_object(Config)

    ####### extension init #######
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    jwt.init_app(app)
    mail.init_app(app)

    ####### models init #######
    with app.app_context():
        from .models import create_models, populate

        create_models()
        populate()

    ####### Basic routes #######
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/<path:path>")
    def static_path(path):
        file_path = os.path.join(app.static_folder, path)
        if os.path.isfile(file_path):
            return send_from_directory(app.static_folder, path)
        else:
            return render_template("index.html")

    return app
