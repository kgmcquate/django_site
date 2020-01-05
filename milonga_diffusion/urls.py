from django.urls import path

from . import views

urlpatterns = [
    path('', views.reactor_sim, name='reactor_sim'),
    path('send_geo/', views.grab_geo, name='send_geo'),
    # path('button/', views.button, name='button')
]