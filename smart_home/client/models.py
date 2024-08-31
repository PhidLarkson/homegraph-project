from django.db import models
from .extensions.switches import *
from .extensions.rooms import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission, Group
from django.urls import reverse
from django.utils.text import slugify

# actuator setup model
class SerialConfigurationObjectA(models.Model):                         # for the actuators
    serial_port = models.CharField(default='/dev/ttyUSB0', max_length=100, blank=True)
    serial_baudrate = models.IntegerField(default=9600, editable=True)
    connection_timeout = models.IntegerField(default=30, editable=True)
    config_id = models.IntegerField(default=8, primary_key=True, editable=True)

# sensor setup model
class SerialConfigurationObjectB(models.Model):                         # for the sensors
    serial_port = '/dev/ttyUSB0'
    serial_baudrate = models.IntegerField(default=9600, editable=True)
    connection_timeout = models.IntegerField(default=30, editable=True)
    config_id = models.IntegerField(default=8, primary_key=True, editable=True)


# client user object model  
class OperatorID(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    id = models.IntegerField(primary_key=True, editable=True)
    theme = models.CharField(default='#fffff', max_length=20)

    def __str__(self):
        return self.user.username 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        OperatorID.objects.create(user=instance)


# smart home records >> user manual + technical manual
class Room(models.Model):
    service_name = models.TextField()
    switch_name = models.TextField(max_length=20)
    is_automated = models.BooleanField(default='False')
    

# more less the actuators
class RoomObjectIdentifiers(models.Model):
    service_room = models.CharField(
            max_length=20,
            choices = room_id_tags,
            default = '1'
        )
    switch_type = models.CharField(
            max_length=20,
            choices = alternatives,
            default = '1'
        )
    id = models.IntegerField(primary_key=True, editable=True)
    room_operator = models.ForeignKey(User, on_delete= models.CASCADE)
    roomObject_name = models.CharField(max_length=200, unique=True)
    interaction_count = models.IntegerField(default=0, editable=True)
    interaction_key = models.CharField(max_length=100, blank=True)                        # non-editable key similar to Schar included for added security
    pinned_room_object = models.BooleanField(default=False)
    room_marker = models.IntegerField(default=0, editable=True)     # to arranged room cards in the order of the values in a descending order
    guest = models.BooleanField(default=True)
    color = models.CharField(default='#fffff', max_length=20)
    config_id = models.IntegerField(default=8, editable=True)

    class Meta:
        ordering = ['-room_marker']
                                        
    def __str__(self):
        return self.roomObject_name   
   

# records of operation
class DataSensorObjects(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.CharField(max_length=100, blank=True)
    room_states = models.CharField(max_length=100, blank=True)
    power_reading = models.TextField(max_length=20)
    weather_reading = models.CharField(max_length=100, blank=True)
    sensor_reading = models.CharField(max_length=100, blank=True)
    is_automated = models.BooleanField(default='False')
    config_id = models.IntegerField(primary_key=True, editable=True, default=0)

    def __str__(self):
        return f"SensorData - Value: {self.room_states}, Timestamp: {self.timestamp}"






class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='task_images/', blank=True, null=True)
    url = models.URLField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    proof_of_work_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    def can_be_edited(self):
        return not self.is_completed

    def can_be_completed(self,user):
                return not self.is_completed and self.created_by != user

