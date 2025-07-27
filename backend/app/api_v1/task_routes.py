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
@task_bp.doc(
    summary="Send daily reminders",
    description="Triggers the daily reminders background task. Requires admin role.",
    tags=["Task", "Admin"],
    security=[{"BearerAuth": []}],
    responses={
        200: {"description": "Task triggered successfully."},
        401: {"description": "Unauthorized."},
        500: {"description": "Internal Server Error."},
    },
)
@role_required("admin")
def send_daily_remainders():
    """
    Triggers the daily reminders background task.

    This endpoint is restricted to admin users and returns a task ID upon successful initiation.
    Handles APIError and general exceptions with appropriate logging and error responses.
    """
    try:
        from ..tasks import daily_remainders

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
@task_bp.doc(
    summary="Send monthly report",
    description="Trigger the asynchronous sending of a monthly report email to the authenticated user. Requires user role.",
    tags=["Task", "User"],
    security=[{"BearerAuth": []}],
    responses={
        200: {"description": "Monthly report task triggered."},
        401: {"description": "Unauthorized."},
        500: {"description": "Internal Server Error."},
    },
)
@role_required("user")
def send_monthly_report():
    """
    Endpoint to trigger the asynchronous sending of a monthly report email to the authenticated user.

    Requires the user role. Returns a message and task ID upon successful task initiation.
    Handles APIError and general exceptions with appropriate logging and error responses.
    """
    try:
        identity = get_jwt_identity()

        from ..tasks import user_monthly_report

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
@task_bp.doc(
    summary="Send all data report",
    description="Initiate sending a user's all-time data report via email. Requires user role.",
    tags=["Task", "User"],
    security=[{"BearerAuth": []}],
    responses={
        200: {"description": "All data report task triggered."},
        401: {"description": "Unauthorized."},
        500: {"description": "Internal Server Error."},
    },
)
@role_required("user")
def send_all_data():
    """
    Endpoint to initiate sending a user's all-time data report via email.

    Requires the user role. Triggers an asynchronous task to generate and send the report,
    and returns a message with the task ID. Handles API and general exceptions.
    """
    try:
        identity = get_jwt_identity()

        from ..tasks import user_all_time_report

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
