from django.db import models

# Create your models here.

class Remedy(models.Model):
    # (Disease Name, Disease Type, Disease Cause, Remedy)
    dname = models.CharField(max_length=100)
    dtype = models.CharField(max_length=100)
    dcause = models.CharField(max_length=200)
    dremedy = models.CharField(max_length=200)

    class Meta:
        db_table = "remedy"

class User(models.Model):
    #(uname,upass,id,uemail)
    uname=models.CharField(max_length=30)
    upass=models.CharField(max_length=25,default='')
    uemail=models.EmailField()

    def __str__(self):
        return self.uname
    
    class Meta:
        db_table = "user"