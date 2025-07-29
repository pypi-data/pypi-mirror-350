from ardhi_framework.mfa.fingerprint import AuthenticateFingerprint
from ardhi_framework.mfa.otps import OTPAuthentication
from ardhi_framework.mfa.signatures import AuthenticateSignature


class RequestVerification(OTPAuthentication, AuthenticateFingerprint, AuthenticateSignature):

    def __init__(self):
        self.user_id = 'logged_in_user'
        self.application_instance = None
        super().__init__(self.application_instance, self.user_id)

    def authenticate(self, u_id: str, type: str):
        if type == 'OTP':
            return self.verify_otp()

    def is_authenticated(self, u_id=None):
        """Uses logged in user, or passes user id"""
        if u_id:
            self.user_id = u_id
        return self.is_verified() and (self.has_fingerprint() or self.has_signature())


