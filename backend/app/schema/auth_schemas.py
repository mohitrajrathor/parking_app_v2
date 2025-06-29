# to store auth schemas

# imports
from marshmallow import Schema, fields, validates, ValidationError
import re


class TokenSchema(Schema):
    role = fields.Str(required=True)
    token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)
    message = fields.Str()


class AdminLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates("password")
    def validate_password(self, value, **kwargs):
        if len(value) < 8:
            raise ValidationError("Password must have at least 8 letters!")

        if not re.search(r"[A-Z]", value):
            raise ValidationError("Password must have at least 1 Uppercase letter!")
        if not re.search(r"[a-z]", value):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r"[0-9]", value):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError(
                "Password must contain at least one special character."
            )


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates("password")
    def validate_password(self, value, **kwargs):
        if len(value) < 8:
            raise ValidationError("Password must have at least 8 letters!")

        if not re.search(r"[A-Z]", value):
            raise ValidationError("Password must have at least 1 Uppercase letter!")
        if not re.search(r"[a-z]", value):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r"[0-9]", value):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError(
                "Password must contain at least one special character."
            )


class UserSignupSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    name = fields.Str(required=True)
    dob = fields.Str(required=True)
    profession = fields.Str(required=True)
    address = fields.Str(required=True)
    pincode = fields.Str(required=True)
    phone = fields.Str(required=True)

    @validates("password")
    def validate_password(self, value, **kwargs):
        if len(value) < 8:
            raise ValidationError("Password must have at least 8 letters!")

        if not re.search(r"[A-Z]", value):
            raise ValidationError("Password must have at least 1 Uppercase letter!")
        if not re.search(r"[a-z]", value):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r"[0-9]", value):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValidationError(
                "Password must contain at least one special character."
            )
