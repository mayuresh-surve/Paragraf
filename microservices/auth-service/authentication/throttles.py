from rest_framework.throttling import SimpleRateThrottle

class LoginRateThrottle(SimpleRateThrottle):
    scope = 'login'

    def get_cache_key(self, request, view):
        # Use the IP address for anonymous users or user id for authenticated users.
        return self.get_ident(request)

class RegistrationRateThrottle(SimpleRateThrottle):
    scope = 'registration'

    def get_cache_key(self, request, view):
        # Use the IP address as the key.
        return self.get_ident(request)
    

class RefreshTokenRateThrottle(SimpleRateThrottle):
    scope = 'refresh_token'
    
    def get_cache_key(self, request, view):
        return self.get_ident(request)