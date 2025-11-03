


from django.urls import path
from .views import reply_generator , pickup_line_generator , looks_analyzer, register, login

urlpatterns = [
    path('register/', register.register, name="register"),
    path('login/', login.LoginView.as_view(), name='login'),
    path('pickup-line-generator/', pickup_line_generator.generate_pickup_line, name='pickup-line'),
    path('reply-generator/', reply_generator.generate_reply, name='reply-generator'),
    path('looks-analyzer/', looks_analyzer.analyze_looks, name='looks-analyzer'),
]
