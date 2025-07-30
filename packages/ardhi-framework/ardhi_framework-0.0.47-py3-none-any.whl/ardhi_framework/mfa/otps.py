from registration_shared_service.otp import GenerateOTP, VerifyOTP
from registration_shared_service.utils import GetUser
from ardhi_framework.exceptions import UnauthorizedActorError, MicroserviceCommunicationError
from ardhi_framework.mfa.base_mfa import AuthBase


class OTPAuthentication(AuthBase):
    """OTP by message and email"""

    def __init__(self, request, instance, user_id):
        super().__init__(instance, user_id)
        self.otp_inst = self.application_instance.otps.filter(user_id=self.user_id).first()
        self.request = request

    def has_otp(self):
        """check otp"""
        return bool(self.otp_inst)

    def is_verified(self):
        return self.has_otp() and self.otp_inst.verified == True

    def verify_otp(self, code=None):
        """
        Verify the otp requested
        Args:
            code: int
        """
        if not self.has_otp():
            raise UnauthorizedActorError('Unauthorized')
        if self.is_verified():
            return
        if not code:
            raise UnauthorizedActorError('Invalid verification code')
        otp_res = VerifyOTP(
            user=self.user_id,
            otpcode=code,
            module=None,
            headers=self.request.headers
        ).verify_otp()
        if otp_res:
            self.otp_inst.verified = True
            self.otp_inst.save()
        else:
            raise UnauthorizedActorError('Invalid Verification details.')

    def request_otp(self):
        """Get otp value"""
        if not self.has_otp():
            self.otp_inst = self.application_instance.otps.create(user_id=self.user_id, verified=False)
        # generate otp
        otp_res = GetUser(
            headers=self.request.headers,
            user_field=self.user_id
        ).get_otp_response()
        if not otp_res:
            raise MicroserviceCommunicationError(None, 'verification service.')







