# testing routes logic

# import
from flask_smorest import Blueprint
from flask_mail import Message
from flask_jwt_extended import jwt_required
from ..extensions import mail


test_bp = Blueprint("test", __name__, url_prefix="/test")


###### routes ######
@test_bp.route("/")
def test():
    return "test route are working!"


@test_bp.route("/test-email")
def test_email():
    msg = Message("Test Subject", recipients=["test@example.com"])
    msg.body = "This is a test email sent to the local aiosmtpd server."
    msg.sender = "admin@parkly.com"
    mail.send(msg)
    return "Email sent to local SMTP server!"


@test_bp.route("/jwt_test")
@jwt_required()
def jwt_test():
    return "jwt not working if you get this message!"


@test_bp.route("/start-task")
def start_task():
    from ..tasks import test

    result = test.delay()
    return {"task_id": result.id}


@test_bp.route("/result/<task_id>")
def get_result(task_id):
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
    from ..tasks.demo_tasks import demo

    result = demo.delay()
    return {"task_id": result.id}


@test_bp.route("/result/demo/<task_id>")
def get_demo_result(task_id):
    from ..tasks.demo_tasks import demo

    result = demo.AsyncResult(task_id)
    if result.ready():
        return {
            "status": "DONE" if result.ready() else "PENDING",
            "result": result.result,
        }
    else:
        return {"status": "PENDING"}
