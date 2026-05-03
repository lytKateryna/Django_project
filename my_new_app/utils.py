from datetime import datetime, timezone
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from typing import Any
from django.http import HttpResponse
from django.contrib.auth.models import User

ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"
COOKIE_HTTPONLY = True
COOKIE_SECURE = False
COOKIE_SAMESITE = "Strict"
COOKIE_PATH = "/"


def get_token_expiry_datetime(token: AccessToken | RefreshToken):
    return datetime.fromtimestamp(int(token['exp']), tz=timezone.utc)


def build_cookies_kwargs(expires: datetime) -> dict[str, Any]:
    return {
        "httponly": COOKIE_HTTPONLY,
        "secure": COOKIE_SECURE,
        "samesite": COOKIE_SAMESITE,
        "path": COOKIE_PATH,
        "expires": expires,
    }

def set_access_cookie(response: HttpResponse, access_token: str) -> None:
    token = AccessToken(access_token)
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=str(token),
        **build_cookies_kwargs(get_token_expiry_datetime(token))
    )

def set_refresh_cookie(response: HttpResponse, refresh_token: str) -> None:
    token = RefreshToken(refresh_token)
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=str(token),
        **build_cookies_kwargs(get_token_expiry_datetime(token))
    )

def set_jwt_cookies(response: HttpResponse, user: User) -> None:
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    set_access_cookie(response, str(access_token))
    set_refresh_cookie(response, str(refresh_token))

    # access_expiry = datetime.utcfromtimestamp(access_token['exp'])
    # refresh_expiry = datetime.utcfromtimestamp(refresh_token['exp'])
    #
    # response.set_cookie(
    #     key='access_token',
    #     value=str(access_token),
    #     httponly=True,
    #     secure=False,
    #     samesite='lax',
    #     expires=access_expiry
    # )
    #
    # response.set_cookie(
    #     key='refresh_token',
    #     httponly=True,
    #     secure=False,
    #     samesite='lax',
    #     expires=refresh_expiry
    # )

def clear_jwt_cookies(response: HttpResponse) -> None:
    response.delete_cookie(key=ACCESS_COOKIE_NAME, path=COOKIE_PATH)
    response.delete_cookie(key=REFRESH_COOKIE_NAME, path=COOKIE_PATH)
