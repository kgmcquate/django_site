from django.urls import path

from . import views

urlpatterns = [
    path('', views.reactor_sim, name='reactor_sim'),
    path('solve/', views.solve, name='solve'),
    # path('button/', views.button, name='button')
]