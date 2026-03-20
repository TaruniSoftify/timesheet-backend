from django.contrib import admin
from .models import Project, TimeEntry, Approval, Country, Client, TimeCard, UserProfile

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'client')
    search_fields = ('name', 'code', 'client')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'manager')
    list_filter = ('role', 'department')

admin.site.register(Project, ProjectAdmin)
admin.site.register(TimeEntry)
admin.site.register(Approval)
admin.site.register(Country)
admin.site.register(Client)
admin.site.register(TimeCard)
admin.site.register(UserProfile, UserProfileAdmin)

