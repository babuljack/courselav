from django.urls import path
from . import views
from .extraforms import CourseInlineForm
from django.urls import re_path as url
from django.views.static import serve 
from django.conf import settings
urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('',views.Home),
    path('courseview/<str:slug>',views.CourseView,name="courseview"),
    path('signup',views.SignUp,name="signup"),
    path('login',views.loginUser,name="login"),
    path('logout',views.LogoutUser,name="logout"),
    path('profile',views.Profile,name="profile"),
    path('upload',views.UploadCourse,name="upload"),
    path('inline',CourseInlineForm.as_view(),name='inline'),
    path('check-out/<str:slug>',views.CheckOut,name='check-out'),
    path('mycourse',views.Mycourse,name="mycourse"),
    path('verify_payment',views.verifyPayment,name='verify_payment')
]