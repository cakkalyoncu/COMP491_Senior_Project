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
    path('goLeft_en', views.goLeft_en),
    path('fly_en', views.fly_en),
    path('goRight_en', views.goRight_en),
    path('ascend_en', views.ascend_en),
    path('write_code', views.write_code),
    path('write_code_en', views.write_code_en),
    path('save_page', views.save_page),
    path('save_page_en', views.save_page_en),
    path('start_demo_en', views.start_demo_en),
    path('index_en', views.index_en),
    path('custom_action_en', views.custom_action_en),
    path('show_info_en', views.show_info_en),
    path('record_en', views.recordAndDraw_en),
    path('draw_text', views.draw_text),
]
