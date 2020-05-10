from django.db import models

class Thing(models.Model):
    name = models.CharField(max_length=100, default="unnamed")
    weight = models.IntegerField(default=0)
    net_weight = models.IntegerField(default=0)
    watch_dog = models.IntegerField(default=0)
    phone = models.CharField(max_length=100, default="0")
    clear_time = models.IntegerField(default=0)
    def __str__(self):
        return "%s: %sg" % (self.name, self.weight)