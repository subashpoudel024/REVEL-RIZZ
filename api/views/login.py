from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(TokenObtainPairView):
    """
    JWT login endpoint
    """
    pass