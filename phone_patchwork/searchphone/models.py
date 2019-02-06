from django.db import models

class Student(models.Model):
    login = models.CharField(max_length=20, unique=True)
    id_42 = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True )
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mail = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.CharField(max_length=250, blank=True, null=True)
    detail_url = models.CharField(max_length=250, unique=True, blank=True, null=True)
    intra_url = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.login

