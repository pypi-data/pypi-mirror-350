from ardhi_framework.mfa.base_mfa import AuthBase

class AuthenticateFingerprint(AuthBase):

    def has_fingerprint(self):
        """Filter signatures by is fingerprinted"""
        return self.application_instance.fingerprints.filter(user_id=self.user_id).exists()
