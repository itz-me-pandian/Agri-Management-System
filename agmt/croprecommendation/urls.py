from django.urls import path

from . import views

urlpatterns = [
    path('',views.map, name='map'),
    path('save_data/',views.save_data,name='save')
]