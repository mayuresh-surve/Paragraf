from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer
from .throttles import RegistrationRateThrottle, LoginRateThrottle, RefreshTokenRateThrottle
from django.http import JsonResponse

# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    throttle_classes = [RegistrationRateThrottle]
    

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT token pair.
    Returns the access token in the response body and sets the refresh token in an HTTP-only cookie.
    """
    throttle_classes = [LoginRateThrottle]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data
        
        response = Response({"access": tokens["access"]}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='refresh_token',
            value=tokens["refresh"],
            httponly=True,
            secure=not settings.DEBUG,  
            samesite='Lax',
            max_age=14 * 24 * 60 * 60  # expires in 14 days
        )
        return response

class CustomTokenRefreshView(TokenRefreshView):
    """ 
    Custom view to refresh access tokens after retriving refresh token from HTTP-only cookie.
    Return the access token in response body
    """
    
    throttle_classes = [RefreshTokenRateThrottle]
    def post(self, request, *args, **kwargs):
        # Retrieve the refresh token from the cookie
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found. Please login again"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the data dictionary for the serializer
        serializer = self.get_serializer(data={'refresh': refresh_token})
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data
        
        # Optionally, update the cookie if a new refresh token is issued
        response = Response(tokens, status=status.HTTP_200_OK)
        response.set_cookie(
            key='refresh_token',
            value=tokens.get('refresh', refresh_token),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=14 * 24 * 60 * 60   # expires in 14 days
        )
        return response


class LogoutView(APIView):
    """
    Custom view to Logout user and blacklist it's token.
    Returns the HTTP 205 response after successful logout and clearing token from cookies.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Try to get the refresh token from the request data.
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                # By using cookies
                refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Clear the cookie
            response = Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie("refresh_token")
            return response

        except Exception as e:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


def health(request):
    return JsonResponse({"status": "ok"})
