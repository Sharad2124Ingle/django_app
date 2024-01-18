from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_staff= models.BooleanField('Is admin', default=False)
    is_employee = models.BooleanField('Is employee', default=True)



class Record(models.Model):
    myuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myuser_records')
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=10) 
    mall_id = models.CharField(max_length=15) 

    def __str__(self):
        return f"Record ID: {self.id}, myuser: {self.myuser}"
        #return self.user.username

    def save(self, *args, **kwargs):
        if self.myuser:  # Make sure myuser is set before saving
            user_email = self.myuser.email
            self.email = user_email  # Populate the email field with the user's email
            user_phone = self.myuser.phone
            #self.phone = user_phone
            if not self.phone:
                self.phone = user_phone 
            # Update related User instance's first_name and last_name
            self.myuser.first_name = self.first_name
            self.myuser.last_name = self.last_name
            self.myuser.save()

        super().save(*args, **kwargs)
