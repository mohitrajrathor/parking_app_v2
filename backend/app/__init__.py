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
        static_url_path="/",
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
    @cache.cached(24 * 60 * 60)
    def index():
        try:
            return render_template("index.html")
        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            raise e

    @app.route("/<path:path>")
    @cache.cached(24 * 60 * 60)
    def static_files(path):
        try:
            # Check if the requested file exists in the static folder
            file_path = os.path.join(app.static_folder, path)
            if os.path.isfile(file_path):
                return send_from_directory(app.static_folder, path)
            # If the file doesn't exist, serve index.html for Vue routing
            return render_template("index.html")
        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            raise e

    @app.errorhandler(404)
    @cache.cached(24 * 60 * 60)
    def not_found(error):
        return render_template("index.html")

    @app.errorhandler(500)
    @cache.cached(24 * 60 * 60)
    def internal_error(error):
        return {"message": "Internal Server Error"}, 500

    print(app.config["MAIL_SERVER"], app.config["MAIL_PORT"])

    return app
