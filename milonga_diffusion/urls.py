from django.urls import path

from . import views

urlpatterns = [
    path('', views.build_a_reactor, name='build_a_reactor'),
    path('send_geo/', views.grab_geo, name='send_geo'),
    # path('button/', views.button, name='button')
]