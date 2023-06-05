from whoishere.views import QRView, CheckinView, SuccessView, SplashView, AttendancePollList, AttendancePollCreate, CheckinList
"""
URL configuration for whoishere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

urlpatterns = [
    path('success/', SuccessView.as_view()),
    path('checkins/', CheckinList.as_view()),
    path('checkin/<slug:slug>/', CheckinView.as_view(), name="checkin-view"),
    path('attendance-polls/', AttendancePollList.as_view()),
    path('qr/<slug:slug>', QRView.as_view()),
    path('create-poll/', AttendancePollCreate.as_view()),
    path('admin/', admin.site.urls),
    path('', SplashView.as_view())
]
