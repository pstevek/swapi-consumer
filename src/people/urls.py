from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:person_id>', views.person),
    path('votes', views.votes)
]