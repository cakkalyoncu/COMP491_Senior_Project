from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index),
    path('info', views.show_info),
    path('record', views.recordAndDraw),
    path('draw_objects', views.draw_objects),
    path('start_demo', views.start_demo),
    path('custom_action', views.custom_action),
    path('goLeft', views.goLeft),
    path('fly', views.fly),
    path('goRight', views.goRight),
    path('ascend', views.ascend),
    path('write_code', views.write_code),
]
