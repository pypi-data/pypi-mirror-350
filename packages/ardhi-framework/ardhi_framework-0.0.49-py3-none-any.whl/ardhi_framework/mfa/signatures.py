from ardhi_framework.mfa.base_mfa import AuthBase


class AuthenticateSignature(AuthBase):

    def has_signature(self):
        """Filter signatures by is fingerprinted"""
        return self.application_instance.signatures.filter(user_id=self.user_id).exists()
