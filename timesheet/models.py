from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ROLE_CHOICES = [
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('Admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"



# class Country(models.Model): 
#     name = models.CharField(max_length=100) 
    
#     def __str__(self): 
#         return self.name 

class Country(models.Model): 
    name = CountryField(blank_label='(select country)') 
    
    def __str__(self): 
        return str(self.name)

class Client(models.Model): 
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True) 
    
    def __str__(self): 
        return self.name

# class Project(models.Model):
#     name = models.CharField(max_length=100)
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, null=True, blank=True)
    client = models.CharField(max_length=100)
    compliance_rules = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TimeEntry(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    task = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee.username} - {self.date}"

class Approval(models.Model):
    time_entry = models.ForeignKey(TimeEntry, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="approvals")
    status = models.CharField(max_length=20, choices=[("Pending","Pending"),("Approved","Approved"),("Rejected","Rejected")])
    comments = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


# class TimeCard(models.Model):
#     employee = models.ForeignKey(User, on_delete=models.CASCADE)
#     period_start = models.DateField()
#     period_end = models.DateField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.employee.username} - {self.period_start} to {self.period_end}"

class TimeCard(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=50, blank=True, default="Draft")   # NEW
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # NEW
    submission_date = models.DateField(blank=True, null=True)  # NEW
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.period_start} to {self.period_end}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username}: {self.message}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ROLE_CHOICES = [
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('Admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')
    department = models.CharField(max_length=100, blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_employees')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
