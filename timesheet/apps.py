from django.apps import AppConfig
import sys

class TimesheetConfig(AppConfig):
    name = 'timesheet'

    def ready(self):
        # Auto-create the default admin profile on server launch if it doesn't exist
        if 'runserver' in sys.argv or any('gunicorn' in arg for arg in sys.argv):
            try:
                from django.contrib.auth.models import User
                from .models import UserProfile
                if not UserProfile.objects.filter(role='Admin').exists():
                    user, created = User.objects.get_or_create(username='Admin', defaults={'email': 'admin@softify.com'})
                    if created:
                        user.set_password('Admin@123')
                        user.is_superuser = True
                        user.save()
                    UserProfile.objects.get_or_create(user=user, defaults={'role': 'Admin'})
                    print("✅ Successfully generated default 'Admin' user with password 'Admin@123'.")
            except Exception:
                pass
