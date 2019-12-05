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
    path('save_page', views.save_page),
    path('start_demo_en', views.start_demo_en),
    path('index_en', views.index_en),
    path('custom_action_en', views.custom_action_en),
    path('show_info_en', views.show_info_en),
    path('record_en', views.recordAndDraw_en),
]
