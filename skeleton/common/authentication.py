from fastapi import HTTPException
from services.users_service import verify_jwt_token, get_by_id, is_token_blacklisted


def get_user_or_raise_401(token: str):
    payload = verify_jwt_token(token)
    if payload:
        user_id = payload.get("user_id")
        if is_token_blacklisted(token):
            raise HTTPException(status_code=401, detail="User is logged out! Please log in order to perform this task!")
        user = get_by_id(user_id)
        if user:
            return user
    return HTTPException(status_code=401, detail="Invalid token")
