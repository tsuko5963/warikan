from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator\
    ,MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.

class HistoryModel(models.Model):
    date = models.DateField(default=timezone.now)
    time = models.CharField(default = "18:00",
        max_length = 5)
    numMyside = models.IntegerField(default = 1,
        validators = [MinValueValidator(1),MaxValueValidator(99)],
        )
    numOtherside = models.IntegerField(default = 1,
        validators = [MinValueValidator(1),MaxValueValidator(99)],
        )
    amount = models.IntegerField(default = 0)
    ratio = models.IntegerField(default = 50,
        validators = [MinValueValidator(0),MaxValueValidator(100)],
        )
    amountMyside = models.IntegerField(default = 0)
    amountOtherside = models.IntegerField(default = 0)
    charge = models.IntegerField(default = 0)
    remarks = models.TextField(default = "", max_length = 400)
    username = models.CharField(default = "", max_length = 15)
    user_id = models.IntegerField(default = 0)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d') + ' ' + self.time

class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    jaspay = models.CharField(max_length = 10, validators = [MinLengthValidator(10)])

    def __str__(self):
        return self.user.username
