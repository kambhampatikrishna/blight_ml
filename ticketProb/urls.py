from django.urls import path
from . import views

urlpatterns = [
  
    path('ticket/', views.ticketId, name = 'ticketId')
]