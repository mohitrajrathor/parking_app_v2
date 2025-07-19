# to handle backgorund tasks


# import

import os
import logging
from celery import shared_task
from app.extensions import db, mail
from flask_mail import Message
from app.models import User
from flask import current_app
from app import create_app

app = create_app()


@shared_task
def test():
    """
    A simple test task to verify Celery setup.
    """
    print("Celery is working!")
    return "Task completed successfully!"


@shared_task
def demo():
    """
    A demo task to showcase Celery functionality.
    """
    print("Demo task executed!")
    return "Demo task completed successfully!"


@shared_task
def daily_remainders():
    """
    A task to send daily reminders to users.
    """
    with app.app_context():
        template_path = os.path.join(
            current_app.root_path, "email_templates", "daily_reminder.html"
        )

        try:
            with open(template_path, "r") as f:
                template = f.read()
        except Exception as e:
            logging.error(f"[daily_remainders] Could not read template: {e}")
            return f"Template not found: {template_path}"

        users = db.session.query(User).all()
        sent_count = 0
        for user in users:
            try:
                msg = Message(
                    subject="Daily Reminder",
                    sender="admin@parkly.com",
                    recipients=[user.email],
                    html=template.replace(
                        "{USER_NAME}", user.name if user.name else "User"
                    ),
                )
                mail.send(msg)
                sent_count += 1
            except Exception as e:
                logging.error(f"[daily_remainders] Failed to send to {user.email}: {e}")
        return f"Daily reminders sent successfully! ({sent_count} sent)"
