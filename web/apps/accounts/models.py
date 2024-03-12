from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models import OneToOneField

from conf import GROUP_SUPERVISORS, GROUP_GATE_MANAGERS, GROUP_CHECK_IN_MANAGERS

class User(AbstractUser):
    phone_number = models.CharField(blank=True, null=True, max_length=20)
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)


class Supervisor(models.Model):
    user = OneToOneField(
        User, on_delete=models.CASCADE, related_name=GROUP_SUPERVISORS,
    )


class CheckInManager(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name=GROUP_CHECK_IN_MANAGERS,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        check_in_managers, _ = Group.objects.get_or_create(
            name='check_in_managers'
        )
        self.user.groups.add(check_in_managers)


class GateManager(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name=GROUP_GATE_MANAGERS,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        gate_managers, _ = Group.objects.get_or_create(
            name='gate_managers'
        )
        self.user.groups.add(gate_managers)
