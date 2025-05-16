# testing routes logic

# import
from flask import Blueprint
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
