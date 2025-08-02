from django.urls import path

from . import views
from croprecommendation import views as vw

urlpatterns = [
    path('',views.home,name='home'),
    path('userreg/',views.userreg,name='userreg'),
    path('insertuser/',views.insertuser,name='insertuser'),
    path('login/',views.login,name='login'),
    path('login_check/',views.login_check,name='login_check'),
    path('verify_otp/', views.otp_verify, name='verify_otp'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('imageinput/',views.getImage, name='function for image'),
    path('disease_result/',views.getImage, name='Disease display'),
    path("show_remedy/", views.show_remedy, name="show_remedy"),
    path("commodities/",views.get_commodities,name="Get commodities input from user"),
    path("commodities/handle_commodities/",views.handle_selected_commodities,name="Get commodities from html file"),
    path('visualize/',views.price_visualization,name='visualization'),
    path('crop_recommendation/',vw.map,name='crop_recommendation'),
    path('save_data/',vw.save_data,name='save')
]
