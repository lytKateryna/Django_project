import time
from typing import Callable

from django.http import HttpRequest
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from my_new_app.utils import clear_jwt_cookies, set_access_cookie, ACCESS_COOKIE_NAME, REFRESH_COOKIE_NAME


class JWTMiddleware:
    exclude_paths = {
        '/auth-login/',
        '/register/',
        '/api-token-refresh/',
    }

    excluded_path_prefixes = {
        "/admin/",
        "/api-auth/",
    }

    def __init__(self, get_response: Callable):
        self.get_response = get_response
        self.refresh_window_sec = self._build_refresh_window_sec()

    def __call__(self, request: HttpRequest, *args, **kwargs):
        if self._should_skip(request=request):
            return self.get_response(request)

        access_token = self._get_access_cookie(request)
        refresh_token = self._get_refresh_cookie(request)

        minted_access_token: str | None = None

        should_clear_cookies: bool = False

        if access_token and not self._is_access_expiring(access_token):
            self._set_auth_header(request, access_token)

        elif refresh_token and self._is_refresh_token_valid(refresh_token):
            minted_access_token = self._mint_access_token(refresh_token)

            if minted_access_token:
                self._set_auth_header(request, minted_access_token)
            else:
                should_clear_cookies = True

        else:
            should_clear_cookies = True

        response = self.get_response(request)

        if should_clear_cookies:
            clear_jwt_cookies(response=response)

        elif minted_access_token:
            set_access_cookie(response=response, access_token=minted_access_token)

        return response

    def _build_refresh_window_sec(self) -> int:
        access_token_lifetime = int(
            api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()

        )
        return max(1, min(30, access_token_lifetime // 4))

    def _should_skip(self, request: HttpRequest) -> bool:
        return request.path in self.exclude_paths or request.path.startswith(
            tuple(self.excluded_path_prefixes)
        )

    def _has_auth_cookies(
            self,
            access_token: str | None,
            refresh_token: str | None
    ) -> bool:
        return bool(access_token or refresh_token)

    def _get_access_cookie(self, request: HttpRequest) -> str | None:
        return request.COOKIES.get(ACCESS_COOKIE_NAME)

    def _get_refresh_cookie(self, request: HttpRequest) -> str | None:
        return request.COOKIES.get(REFRESH_COOKIE_NAME)

    def _set_auth_header(
            self,
            request: HttpRequest,
            access_token: str
    ) -> None:
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"

    def _is_refresh_token_valid(self, refresh_token: str | None) -> bool:
        if not refresh_token:
            return False
        try:
            RefreshToken(refresh_token)
            return True
        except Exception:
            return False

    def _mint_access_token(self, refresh_token: str | None) -> str | None:
        if not refresh_token:
            return None
        try:
            refresh = RefreshToken(refresh_token)
            return str(refresh.access_token)
        except TokenError:
            return None

    def _is_access_expiring(self, access_token: str) -> bool:
        try:
            token = AccessToken(access_token)
            exp_timestamp = int(token["exp"])
            current_timestamp = int(time.time())
            return exp_timestamp <= current_timestamp + self.refresh_window_sec
        except Exception as e:
            print("ACCESS TOKEN ERROR:", e)
            return True
