from rest_framework.authentication import TokenAuthentication


class InterserviceToolAuthentication(TokenAuthentication):
    """
    This is for interservice calls, such as microservice calls. Service to service calls can be authenticated differently
    """
    keyword = 'Bearer'


class GeneralAuthentication(TokenAuthentication):
    """
    Authentication for web calls. Restrict to come from ardhi endpoints, in 'settings.ALLOWED_HOSTS'
    """
    keyword = 'Token'



