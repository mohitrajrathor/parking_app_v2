# handle tasks routes

# imports
from flask_smorest import Blueprint, abort
from ..exceptions import APIError
from flask import current_app
from ..utils import role_required
from flask_jwt_extended import get_jwt_identity

# blueprint
task_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/tasks",
    description="Tasks related endpoints",
)


@task_bp.route("/send_daily_remainders")
@role_required("admin")
def send_daily_remainders():
    """
    Endpoint to trigger the daily reminders task.
    """
    try:
        from app.tasks import daily_remainders

        task_id = daily_remainders.delay()
        return {
            "message": "Request recieved, remainder will be sent shortly.",
            "task_id": str(task_id),
        }

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@task_bp.route("/send_monthly_report")
@role_required("user")
def send_monthly_report():
    """
    Endpoint to trigger the monthly report task.
    """
    try:
        identity = get_jwt_identity()

        from app.tasks import user_monthly_report

        task_id = user_monthly_report.delay(user_id=identity)
        return {
            "message": "Request recieved, you will get monthly report via mail shortly.",
            "task_id": str(task_id),
        }
    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@task_bp.route("/send_all_data_report")
@role_required("user")
def send_all_data():
    """
    Endpoint to send all data to a user
    """
    try:
        identity = get_jwt_identity()

        from app.tasks import user_all_time_report

        task_id = user_all_time_report.delay(user_id=identity)
        return {
            "message": "Request recieved, you will get all data report via mail shortly.",
            "task_id": str(task_id),
        }

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")
