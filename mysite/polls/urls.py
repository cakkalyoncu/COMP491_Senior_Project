from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index', views.index),
    path('info', views.show_info),
    path('record', views.recordAndDraw),
    path('draw_objects', views.draw_objects),
    path('start_demo', views.start_demo),
    path('upload', views.upload),
    path('custom_action', views.custom_action),
    path('goLeft', views.goLeft),
    path('fly', views.fly),
    path('goRight', views.goRight),
    path('ascend', views.ascend),
    path('write_code', views.write_code),
]
