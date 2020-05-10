from django.db import models

class Thing(models.Model):
    name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)
    class_id = models.IntegerField(default=0) # Liquid, solid, etc. To decide icon
    net_weight = models.IntegerField(default=0) # Net weight
    autobuy_enable = models.BooleanField(default=True)
    autobuy_url = models.CharField(max_length=500)
    device_mac = models.CharField(max_length=100)
    owned_by = models.IntegerField(default=0)
    power = models.IntegerField(default=80)
    status = models.CharField(max_length=200)
    def __str__(self):
        return "%s(%s:%s)" % (self.name, self.id, self.owned_by)

class User(models.Model):
    nick_name = models.CharField(max_length=100)
    login_name = models.CharField(max_length=100)
    login_password = models.CharField(max_length=200)
    def __str__(self):
        return "%s (%s:%s)" % (self.nick_name, self.id, self.login_name)

class PaymentMethod(models.Model):
    user_id = models.IntegerField(default=0)
    card_number = models.CharField(max_length=32)
    card_valid = models.CharField(max_length=16)
    card_name = models.CharField(max_length=128)
    card_cvv = models.CharField(max_length=16)
    phone = models.CharField(max_length=64)