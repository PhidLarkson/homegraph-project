from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created and instance.is_host:
        group = Group.objects.get(name="Host")
        instance.groups.add(group)
    elif created and not instance.is_host:
        group = Group.objects.get(name="Guest")
        instance.groups.add(group)