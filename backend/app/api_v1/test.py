# testing routes logic

# import
from flask_smorest import Blueprint
from flask_mail import Message
from flask_jwt_extended import jwt_required
from ..extensions import mail
from flask import current_app


test_bp = Blueprint("test", __name__, url_prefix="/test")


###### routes ######
@test_bp.route("/")
def test():
    """
    Handles the root route for the test blueprint and returns a confirmation message indicating the test route is operational.
    """
    return "test route are working!"


@test_bp.route("/test-email")
def test_email():
    """
    Sends a test email to the local SMTP server using the configured mail extension.
    The email includes both plain text and HTML content, and is sent from 'admin@parkly.com'
    to 'test@example.com' with the subject 'Test Subject'. This function is intended to verify
    the email sending functionality by checking the local SMTP server logs.
    Returns:
        str: Confirmation message indicating that the email was sent to the local SMTP server.

    """
    msg = Message("Test Subject", recipients=["test@example.com"])
    msg.body = "This is a test email sent to the local aiosmtpd server."
    msg.html = """
        <h1>Test Email</h1>
        <p>This is a test email sent to the local aiosmtpd server.</p>
        <p>To test the email functionality, please check your local SMTP server logs.</p>
        <p>Thank you!</p>
        <p>Best regards,</p>
        <p>Parkly Team</p>
    """
    msg.sender = "admin@parkly.com"
    mail.send(msg)
    return "Email sent to local SMTP server!"


@test_bp.route("/jwt_test")
@jwt_required()
def jwt_test():
    """
    Endpoint to test JWT authentication.

    Returns a message if JWT authentication is not functioning properly.
    """
    return "jwt not working if you get this message!"


@test_bp.route("/start-task")
def start_task():
    """
    Starts the Celery test task asynchronously and returns the task ID.

    Returns:
        dict: A dictionary containing the Celery task ID.
    """
    from ..tasks import test

    result = test.delay()
    return {"task_id": result.id}


@test_bp.route("/result/<task_id>")
def get_result(task_id):
    """
    Retrieve the status and result of a Celery test task by task ID.

    Args:
        task_id (str): The ID of the Celery task.

    Returns:
        dict: A dictionary containing the task status and result (if available).
    """ """
    Starts the Celery demo task asynchronously and returns the task ID.

    Returns:
        dict: A dictionary containing the Celery task ID.
    """
    from ..tasks import test

    result = test.AsyncResult(task_id)
    if result.ready():
        return {
            "status": "DONE" if result.ready() else "PENDING",
            "result": result.result,
        }
    else:
        return {"status": "PENDING"}


@test_bp.route("/demo-task")
def start_demo():
    """
    Starts the demo Celery task asynchronously and returns the task ID.

    Returns:
        dict: A dictionary containing the Celery task ID.
    """
    from ..tasks import demo

    result = demo.delay()
    return {"task_id": result.id}


@test_bp.route("/result/demo/<task_id>")
def get_demo_result(task_id):
    """
    Retrieve the status and result of the demo Celery task by task ID.

    Args:
        task_id (str): The ID of the Celery task.

    Returns:
        dict: A dictionary containing the task status and result if available.
    """
    from ..tasks import demo

    result = demo.AsyncResult(task_id)
    if result.ready():
        return {
            "status": "DONE" if result.ready() else "PENDING",
            "result": result.result,
        }
    else:
        return {"status": "PENDING"}
