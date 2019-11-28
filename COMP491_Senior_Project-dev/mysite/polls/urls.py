from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index),
    path('info', views.show_info),
    path('record', views.recordAndDraw),
    path('draw_objects', views.draw_objects),
    path('start_demo', views.start_demo),
]
