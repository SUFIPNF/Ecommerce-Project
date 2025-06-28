from django.urls import path

from .import views
urlpatterns = [

    path('register/',views.register,name="register"),
    path('signin/',views.signin,name="signin"),
    path('signout/',views.signout,name="signout"),
    path('activate/<uidb64>/<token>/',views.activate,name="activate"),
    path('reset_pass/<uidb64>/<token>/',views.reset_pass,name="reset_pass"),
    path('new_pass/',views.new_pass,name="new_pass"),
    path('forgotpassword/',views.forgotpass,name="forgotpass"),
 
]