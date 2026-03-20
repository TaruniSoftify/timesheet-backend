from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, TimeEntry, Approval, Country, Client, TimeCard, UserProfile, Notification

class UserProfileSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['role', 'department', 'manager_name']

    def get_manager_name(self, obj):
        if obj.manager:
            return obj.manager.username
        return None

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

# class ProjectSerializer(serializers.ModelSerializer): 
#     # Show names instead of IDs 
#     country = serializers.SlugRelatedField( slug_field="name", queryset=Country.objects.all() ) 
#     client = serializers.SlugRelatedField( slug_field="name", queryset=Client.objects.all() ) 
#     class Meta: 
#         model = Project 
#         fields = "__all__"

class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = '__all__'
        read_only_fields = ['employee']  # <-- JUST ADD THIS LINE HERE TOO

class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer): 
    code = serializers.SerializerMethodField() 
    full_name = serializers.SerializerMethodField() 
    class Meta: 
        model = Country
        fields = ["id", "code", "full_name"] 
    def get_code(self, obj): 
        # obj.name is a Country object from django-countries 
        return obj.name.code # ISO code like "IN" 
    def get_full_name(self, obj): 
        return obj.name.name # Full name like "India"
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class TimeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeCard
        fields = "__all__"
        read_only_fields = ['employee']  # <-- YOU JUST NEED TO ADD THIS ONE LINE


class TeamTimecardSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    employee_username = serializers.CharField(source='employee.username', read_only=True)
    employee_id = serializers.IntegerField(source='employee.id', read_only=True)
    department = serializers.CharField(source='employee.profile.department', read_only=True)
    entries = serializers.SerializerMethodField()

    class Meta:
        model = TimeCard
        fields = ['id', 'period_start', 'period_end', 'status', 'total_hours', 'submission_date', 'employee_id', 'employee_name', 'employee_username', 'department', 'entries']

    def get_employee_name(self, obj):
        name = obj.employee.get_full_name().strip()
        return name if name else obj.employee.username

    def get_entries(self, obj):
        # Fetch all TimeEntries for this employee within the TimeCard's date range
        entries = TimeEntry.objects.filter(
            employee=obj.employee,
            date__range=[obj.period_start, obj.period_end]
        )
        # We need task, date, hours, note, project name, client name
        return [{
            'id': e.id,
            'date': str(e.date) if e.date else '',
            'project': getattr(e.project, 'name', str(e.project)) if e.project else '',
            'client': getattr(getattr(e.project, 'client', ''), 'name', str(getattr(e.project, 'client', ''))) if e.project else '',
            'task': e.task,
            'hours': float(e.hours) if e.hours is not None else 0.0,
            'notes': e.notes
        } for e in entries]

