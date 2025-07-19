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
from jinja2 import Environment, FileSystemLoader

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
        template_path = os.path.join(current_app.root_path, "email_templates")

        try:
            template_loader = FileSystemLoader(searchpath=template_path)
            env = Environment(loader=template_loader)
            template = env.get_template("daily_reminder.html")
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
                    html=template.render(
                        user={"name": user.name},
                        dashboard_url="http://localhost:1234/user/dashboard",
                    ),
                )
                mail.send(msg)
                sent_count += 1
            except Exception as e:
                logging.error(f"[daily_remainders] Failed to send to {user.email}: {e}")
        return f"Daily reminders sent successfully! ({sent_count} sent)"


@shared_task
def monthly_reports():
    """
    task to generate and send monthly reports to users.
    """
    with app.app_context():
        template_path = os.path.join(current_app.root_path, "email_templates")

        try:
            template_loader = FileSystemLoader(searchpath=template_path)
            env = Environment(loader=template_loader)
            template = env.get_template("monthly_report.html")

        except Exception as e:
            logging.error(f"[monthly_reports] Could not read template: {e}")
            return f"Template not found: {template_path}"

        users = db.session.query(User).all()

        for user in users:
            if not user.email_confirmed:
                continue
            monthly_reports_data = user.monthly_report()
            rendered_template = template.render(**monthly_reports_data)

            msg = Message(
                subject="Monthly Report",
                sender="admin@parkly.com",
                recipients=[user.email],
                html=rendered_template,
            )

            mail.send(msg)

        return "monthly report send successfully!"


@shared_task
def user_monthly_report(user_id: int):
    """
    Send monthly report to specific user
    """
    with app.app_context():
        template_path = os.path.join(current_app.root_path, "email_templates")

        try:
            template_loader = FileSystemLoader(searchpath=template_path)
            env = Environment(loader=template_loader)
            template = env.get_template("monthly_report.html")

        except Exception as e:
            logging.error(f"[monthly_reports] Could not read template: {e}")
            return f"Template not found: {template_path}"

        user = db.session.query(User).filter_by(id=user_id).first()

        if not user:
            return

        if not user.email_confirmed:
            return "User email is not confiremed unable to send report."
        monthly_reports_data = user.monthly_report()
        rendered_template = template.render(**monthly_reports_data)

        msg = Message(
            subject="Monthly Report",
            sender="admin@parkly.com",
            recipients=[user.email],
            html=rendered_template,
        )

        mail.send(msg)

        return "monthly report send successfully!"


@shared_task
def user_all_time_report(user_id: int):
    """
    A task to generate and send monthly reports to users.
    """
    with app.app_context():
        template_path = os.path.join(current_app.root_path, "email_templates")

        try:
            template_loader = FileSystemLoader(searchpath=template_path)
            env = Environment(loader=template_loader)
            template = env.get_template("all_time_report.html")

        except Exception as e:
            logging.error(f"[monthly_reports] Could not read template: {e}")
            return f"Template not found: {template_path}"

        user = db.session.query(User).filter_by(id=user_id).first()

        if not user:
            return

        if not user.email_confirmed:
            return "User email is not confiremed unable to send report."
        all_data = user.all_time_report()
        rendered_template = template.render(**all_data)

        msg = Message(
            subject="All Time Report",
            sender="admin@parkly.com",
            recipients=[user.email],
            html=rendered_template,
        )

        mail.send(msg)

        return "All time report send successfully!"


@shared_task
def parking_promotion(lot: dict):
    """
    Send promotional email to all user whenever a new parking is added.
    """
    with app.app_context():
        template_path = os.path.join(current_app.root_path, "email_templates")

        try:
            template_loader = FileSystemLoader(searchpath=template_path)
            env = Environment(loader=template_loader)
            template = env.get_template("promotion.html")

        except Exception as e:
            logging.error(f"[monthly_reports] Could not read template: {e}")
            return f"Template not found: {template_path}"

        users = db.session.query(User).all()

        if not users:
            return "No users found to sent mails."

        for user in users:
            if not user.email_confirmed:
                return "User email is not confiremed unable to send email."

            rendered_template = template.render(user={"name": user.name}, lot=lot)

            msg = Message(
                subject="New Parking Started",
                sender="admin@parkly.com",
                recipients=[user.email],
                html=rendered_template,
            )

            mail.send(msg)

        return "Promotional mail sent successfully!"
