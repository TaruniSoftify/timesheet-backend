from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .models import Project, TimeEntry, Approval, Country, Client, TimeCard, UserProfile, Notification
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ProjectSerializer, TimeEntrySerializer, ApprovalSerializer, CountrySerializer, ClientSerializer, TimeCardSerializer, UserSerializer, TeamTimecardSerializer, NotificationSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# class TimeEntryViewSet(viewsets.ModelViewSet):
#     queryset = TimeEntry.objects.all()
#     serializer_class = TimeEntrySerializer


class TimeEntryViewSet(viewsets.ModelViewSet):
    serializer_class = TimeEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ONLY return data of logged-in user and eagerly load foreign keys
        return TimeEntry.objects.filter(employee=self.request.user).select_related('project', 'project__client')

    def perform_create(self, serializer):
        # Automatically attach logged-in user
        serializer.save(employee=self.request.user)

class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class CountryViewSet(ModelViewSet): 
    queryset = Country.objects.all() 
    serializer_class = CountrySerializer 

class ClientViewSet(ModelViewSet): 
    queryset = Client.objects.all() 
    serializer_class = ClientSerializer 

# class TimeCardViewSet(ModelViewSet): 
#     queryset = TimeCard.objects.all() 
#     serializer_class = TimeCardSerializer 
#     permission_classes = [IsAuthenticated] 

#     def get_queryset(self): 
#         return TimeCard.objects.filter(employee=self.request.user)

#     def perform_create(self, serializer):
#         # Attach the logged-in user to the timecard
#         serializer.save(employee=self.request.user)


        
class TimeCardViewSet(ModelViewSet):
    queryset = TimeCard.objects.all()
    serializer_class = TimeCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show timecards for the logged-in user
        return TimeCard.objects.filter(employee=self.request.user).prefetch_related('entries')

    def perform_create(self, serializer):
        # Attach the logged-in user when creating
        serializer.save(employee=self.request.user)

class TeamTimecardViewSet(viewsets.ModelViewSet):
    serializer_class = TeamTimecardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Only Managers and Admins should see this
        if not hasattr(user, 'profile') or user.profile.role == 'Employee':
            return TimeCard.objects.none()
        
        # Optimize DB queries with select_related and prefetch_related to fix N+1
        base_qs = TimeCard.objects.select_related('employee', 'employee__profile').prefetch_related('entries', 'entries__project', 'entries__project__client')
        
        # Admins see everything
        if user.profile.role == 'Admin':
            return base_qs.exclude(status='Draft', total_hours=0).order_by('-created_at')
            
        # Managers ONLY see employees explicitly assigned to them in the database
        return base_qs.filter(employee__profile__manager=user).exclude(status='Draft').order_by('-created_at')

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def debug_users(request):
    profiles = UserProfile.objects.all()
    user_data = []
    for p in profiles:
        user_data.append({
            "username": p.user.username,
            "role": p.role,
            "department": p.department,
            "manager": p.manager.username if p.manager else "None"
        })
        
    timecards = TimeCard.objects.all()
    tc_data = []
    for t in timecards:
        tc_data.append({
            "id": t.id,
            "employee": t.employee.username,
            "status": t.status,
            "total_hours": float(t.total_hours)
        })
        
    return JsonResponse({"users": user_data, "timecards": tc_data})

from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('profile', 'profile__manager').order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] # Or IsAdminUser if strict

    def get_queryset(self):
        # Optimize DB queries with select_related to fix N+1
        return User.objects.select_related('profile', 'profile__manager').order_by('-date_joined')

    def perform_create(self, serializer):
        # Allow the UserSerializer to cascade create the profile using the nested payload
        user = serializer.save()
        
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
        
        # Grab nested profile data from the frontend payload
        profile_data = self.request.data.get('profile', {})
        role = profile_data.get('role', 'Employee')
        department = profile_data.get('department', '')
        manager_name = profile_data.get('manager_name', None)
        
        # Check if profile exists (signals might have created it)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.department = department
        
        if manager_name:
            try:
                manager_user = User.objects.get(username=manager_name)
                profile.manager = manager_user
            except User.DoesNotExist:
                profile.manager = None
        else:
            profile.manager = None
            
        profile.save()

    def perform_update(self, serializer):
        user = serializer.save()
        
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
            
        profile_data = self.request.data.get('profile', {})
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = profile_data.get('role', profile.role)
            profile.department = profile_data.get('department', profile.department)
            
            if 'manager_name' in profile_data:
                manager_name = profile_data.get('manager_name')
                if manager_name:
                    try:
                        manager_user = User.objects.get(username=manager_name)
                        profile.manager = manager_user
                    except User.DoesNotExist:
                        profile.manager = None
                else:
                    profile.manager = None
                    
            profile.save()

    def perform_destroy(self, instance):
        # Django automatically cascades UserProfile deletion
        instance.delete()

