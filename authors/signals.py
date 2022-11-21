import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from authors.models import Profile

User = get_user_model()


def delete_cover_profile(instance):
    try:
        os.remove(instance.cover_profile.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(author=instance)
        profile.save()


@receiver(pre_delete, sender=Profile)
def profile_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Profile.objects.get(pk=instance.pk)

    if old_instance:
        delete_cover_profile(old_instance)


@receiver(pre_save, sender=Profile)
def profile_cover_update(sender, instance, *args, **kwargs):
    old_instance = Profile.objects.get(pk=instance.pk)

    if not old_instance:
        return
    is_new_cover = old_instance.cover_profile != instance.cover_profile

    if is_new_cover:
        delete_cover_profile(old_instance)
