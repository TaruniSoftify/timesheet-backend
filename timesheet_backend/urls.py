"""
URL configuration for timesheet_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from django.http import HttpResponse 
from timesheet.views import ProjectViewSet, TimeEntryViewSet, ApprovalViewSet, CountryViewSet, ClientViewSet, TimeCardViewSet, TeamTimecardViewSet, NotificationViewSet, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 


router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'approvals', ApprovalViewSet)
router.register(r'timeentries', TimeEntryViewSet, basename='timeentry')
# router.register(r'countries', CountryViewSet)
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'clients', ClientViewSet)
# router.register(r'timecards', TimeCardViewSet)
router.register(r'timecards', TimeCardViewSet, basename='timecard')
router.register(r'team-timecards', TeamTimecardViewSet, basename='team-timecards')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'users', UserViewSet, basename='user')




def home(request):
    return HttpResponse("Django backend is running")


from timesheet.views import ProjectViewSet, TimeEntryViewSet, ApprovalViewSet, CountryViewSet, ClientViewSet, TimeCardViewSet, TeamTimecardViewSet, NotificationViewSet, current_user, debug_users

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/current_user/', current_user, name='current_user'),
    path('api/debug-users/', debug_users, name='debug_users'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

