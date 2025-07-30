import hashlib
import hmac
from datetime import datetime
from typing import Optional, Dict, Any, List

import requests
from pydantic import BaseModel


class AuthServiceConfig(BaseModel):
    url: str
    public_key: str
    secret_key: str


class AuthHeaders(BaseModel):
    public_key: str
    timestamp: str
    signature: str
    Authorization: Optional[str] = None


class AuthService:
    def __init__(self, config: AuthServiceConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "X-Public-Key": config.public_key,
                "X-Secret-Key": config.secret_key,
            }
        )
        self.base_url = config.url

    def _get_auth_headers(self, access_token: Optional[str] = None) -> Dict[str, str]:
        timestamp = str(int(datetime.now().timestamp() * 1000))
        signature_data = f"{self.config.public_key}{timestamp}"
        signature = hmac.new(
            self.config.secret_key.encode(), signature_data.encode(), hashlib.sha256
        ).hexdigest()

        headers = {
            "public-key": self.config.public_key,
            "timestamp": timestamp,
            "signature": signature,
        }

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        return headers

    def _handle_error(self, error: Exception) -> Exception:
        if isinstance(error, requests.exceptions.RequestException):
            message = (
                error.response.json().get("message", str(error))
                if error.response
                else str(error)
            )
            return Exception(f"Auth Service Error: {message}")
        return error

    def signup(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Signup a new user."""
        path = "/auth/signup"
        headers = self._get_auth_headers()

        try:
            response = self.session.post(
                f"{self.base_url}{path}", json=params, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def login_with_password(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Login using password."""
        path = "/auth/loginWithPassword"
        headers = self._get_auth_headers()

        try:
            response = self.session.post(
                f"{self.base_url}{path}", json=params, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def login_with_otp(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Login using OTP."""
        path = "/auth/loginWithOtp"
        headers = self._get_auth_headers()

        try:
            response = self.session.post(
                f"{self.base_url}{path}", json=params, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def send_otp_for_login(self, credential: str) -> Dict[str, Any]:
        """Send OTP for login."""
        path = "/auth/sendOtpForLogin"
        headers = self._get_auth_headers()

        try:
            response = self.session.get(
                f"{self.base_url}{path}",
                params={"credential": credential},
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def verify_two_factor_authentication(
        self, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify two factor authentication."""
        path = "/auth/verifyTwoFactorAuthToken"
        headers = self._get_auth_headers()

        try:
            response = self.session.post(
                f"{self.base_url}{path}", json=params, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def logout(self, params: Dict[str, Any]) -> str:
        """Logout user."""
        path = "/auth/userLogout"
        headers = self._get_auth_headers()

        try:
            response = self.session.post(
                f"{self.base_url}{path}", json=params, headers=headers
            )
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise self._handle_error(e)

    def refresh_access_token(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Refresh access token."""
        path = "/auth/refreshAccessToken"
        headers = self._get_auth_headers()

        try:
            response = self.session.get(
                f"{self.base_url}{path}", params=params, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def generate_recovery_codes(self, access_token: str) -> Dict[str, Any]:
        """Generate recovery codes."""
        path = "/secret-keys/generateRecoveryCodes"
        headers = self._get_auth_headers(access_token)

        try:
            response = self.session.post(f"{self.base_url}{path}", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def generate_qr_code_and_secret_for_2fa(self, access_token: str) -> Dict[str, Any]:
        """Generate QR code and secret for 2FA."""
        path = "/secret-keys/generateQRCodeAndSecretFor2FA"
        headers = self._get_auth_headers(access_token)

        try:
            response = self.session.post(f"{self.base_url}{path}", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def verify_qr_code_and_secret_for_2fa(
        self, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify QR code and secret for 2FA."""
        path = "/secret-keys/verifyQrCodeAndSecretFor2FA"
        access_token = params.pop("accessToken")
        headers = self._get_auth_headers(access_token)

        try:
            response = self.session.post(
                f"{self.base_url}{path}", json=params, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def list_of_two_fa_secrets(self, access_token: str) -> Dict[str, Any]:
        """List of 2FA secrets."""
        path = "/secret-keys/listOfTwoFASecrets"
        headers = self._get_auth_headers(access_token)

        try:
            response = self.session.get(f"{self.base_url}{path}", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def remove_two_fa_device(self, access_token: str, key: str) -> List[str]:
        """Remove 2FA device."""
        path = "/secret-keys/removeTwoFADevice"
        headers = self._get_auth_headers(access_token)

        try:
            response = self.session.delete(
                f"{self.base_url}{path}", params={"key": key}, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def disable_two_fa(self, access_token: str) -> bool:
        """Disable 2FA."""
        path = "/auth/disableTwoFA"
        headers = self._get_auth_headers(access_token)

        try:
            response = self.session.post(f"{self.base_url}{path}", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)

    def list_of_recovery_code(self, access_token: str) -> Dict[str, Any]:
        """List of recovery codes."""
        path = "/secret-keys/listOfRecoveryCode"
        headers = self._get_auth_headers(access_token)

        try:
            response = self.session.get(f"{self.base_url}{path}", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise self._handle_error(e)
