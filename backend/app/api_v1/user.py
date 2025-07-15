# module to manage user routes and logic

# imports
from flask_smorest import Blueprint, abort
from sqlalchemy.sql.functions import user
from ..models import User
from ..schema import IdSchema, QuerySchema
from ..exceptions import APIError
from flask import current_app
from ..utils import role_required
from flask_jwt_extended import get_jwt_identity
from ..extensions import db, cache


user_bp = Blueprint(
    "user", __name__, url_prefix="/user", description="user related routes"
)


@user_bp.route("/by_id", methods=["GET"])
@cache.cached(timeout=60, query_string=True)
@user_bp.arguments(IdSchema, location="query")
@role_required("admin", "user")
def get_user_by_id(args):
    """
    Get user by id
    """
    try:
        id = args.get("id")
        if not id:
            raise APIError("id must be given as query parameter!", 404)

        user = User.query.get(id)
        if user:
            return user.to_dict()

        return {"message": "No user found!"}, 404

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@user_bp.route("", methods=["GET"])
@cache.cached(timeout=60, query_string=True)
@user_bp.arguments(QuerySchema, location="query")
@role_required("admin")
def get_users(args):
    """
    Get all users with pagination
    """
    try:
        page = args.get("page", 1)
        per_page = args.get("per_page", 10)
        query = args.get("query", "")

        print(per_page)

        if query:
            users_paginated = User.query.filter(User.name.ilike(f"%{query}%")).paginate(
                page=page, per_page=per_page
            )
        else:
            users_paginated = User.query.paginate(page=page, per_page=per_page)

        return {
            "total": users_paginated.total,
            "page": users_paginated.page,
            "pages": users_paginated.pages,
            "has_next": users_paginated.has_next,
            "has_prev": users_paginated.has_prev,
            "users": [user.to_dict() for user in users_paginated.items],
        }

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@user_bp.route("/me", methods=["GET"])
@role_required("user")
def get_current_user():
    """
    Get current user details from token
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            raise APIError("No user id found in token!", 401)
        user = User.query.get(user_id)
        if user:
            return user.to_dict(for_dashboard=True)
        return {"message": "No user found!"}, 404
    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)
    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")
