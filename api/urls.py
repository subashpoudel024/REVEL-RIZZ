from django.urls import path
from . import views

urlpatterns = [
    path('reply-generator/', views.generate_reply),
    path('pickup-line-generator/', views.generate_pickup_line),
    path('looks-analyzer/', views.analyze_looks)

]