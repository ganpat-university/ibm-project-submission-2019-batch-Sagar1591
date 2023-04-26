"""initial_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.homepage, name='homepage'),
    path('aboutus/', views.aboutus,name='aboutus'),
    path('login/', views.Login,name='login'),
    path('signup/', views.Signup,name='signup'),
    path('admin/', admin.site.urls),
    path('security/', views.security,name='security'),
    path('confidentiality/', views.confidentiality,name='confidentiality'),
    path('availability/', views.availability,name='availability'),
    path('integrity/', views.integrity,name='integrity'),
    path('blog/',views.blog,name='blog'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout,name='logout'),
    path('login-otp/',views.Login_otp,name='login-otp'),
    path('email-verification/<str:uidb64>/<str:token>/',views.email_verification, name='email-verification'),
    path('email-verification-sent/',views.email_verification_sent, name='email-verification-sent'),
    path('email-verification-success/',views.email_verification_success, name='email-verification-success'),
    path('email-verification-failed/',views.email_verification_failed, name='email-verification-failed'),

    #path('otp/',views.Otp,name='otp'),
]

    # path('login/<id>',view.proid),
