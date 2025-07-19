# handle tasks routes

# imports
from flask_smorest import Blueprint


# blueprint
task_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/tasks",
    description="Tasks related endpoints",
)


@task_bp.route("/send_daily_remainders")
def send_daily_remainders():
    """
    Endpoint to trigger the daily reminders task.
    This is just a placeholder; actual task logic should be implemented.
    """
    from app.tasks import daily_remainders

    task_id = daily_remainders.delay()
    return {
        "message": "Daily reminders task has been triggered.",
        "task_id": str(task_id),
    }


@task_bp.route("/send_monthly_report")
def send_monthly_report():
    """
    Endpoint to trigger the monthly report task.
    This is just a placeholder; actual task logic should be implemented.
    """
    ...
