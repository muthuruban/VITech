from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Departments(models.Model):
    dept_number = models.IntegerField(null=False)
    dept_name = models.CharField(max_length=10, null=False)
    no_faculty = models.IntegerField(default=0)
    no_journals = models.IntegerField(default=0)

    def __str__(self):
        return self.dept_name


class Staff(AbstractUser):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    mail_id = models.EmailField(max_length=40)
    phone_number = models.CharField(max_length=10)
    dept_name = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True, related_name='staff_members')
    staff_id = models.CharField(max_length=20)
    date_joined = models.DateField()

class Journals(models.Model):
    title = models.CharField(max_length=50)
    issn_no = models.IntegerField()
    publisher = models.CharField(max_length=40)
    staff_name = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name='journals')
    name_journal = models.CharField(max_length=50)
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True, related_name='journals')

    def __str__(self):
        return self.title
