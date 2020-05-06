from django.db import models

class thing(models.Model):
    name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)
    class_id = models.IntegerField(default=0) # Liquid, solid, etc. To decide icon
    thing_id = models.IntegerField(default=0) # Query this thing. To assign to user
    net_weight = models.IntegerField(default=0) # Net weight
    autobuy_enable = models.BooleanField(default=True)
    autobuy_url = models.CharField(max_length=500)
    device_mac = models.CharField(max_length=100)
    power = models.IntegerField(default=80)
    status = models.CharField(max_length=200)

class user(models.Model):
    id = models.IntegerField(default=0,primary_key=True)
    nick_name = models.CharField(max_length=100)
    login_name = models.CharField(max_length=100)
    login_password = models.CharField(max_length=200)

class paymentMethod(models.Model):
    user_id = models.IntegerField(default=0)
    card_number = models.CharField(max_length=32)
    card_valid = models.CharField(max_length=16)
    card_name = models.CharField(max_length=128)
    card_cvv = models.CharField(max_length=16)
    phone = models.CharField(max_length=64)