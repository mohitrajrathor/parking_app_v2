# to start celery background jobs

# imports
from app import create_app


parking_app = create_app()
celery_app = parking_app.extensions["celery"]

import app.tasks
