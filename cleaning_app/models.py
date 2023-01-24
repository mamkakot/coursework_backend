from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Family(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name)


class Room(models.Model):
    name = models.CharField(max_length=250)
    color = models.CharField(max_length=25)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='familys_rooms')

    def __str__(self):
        return str(self.name)


class Slave(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='familys_slaves', null=True)
    is_admin = models.BooleanField(null=True)

    def __str__(self):
        return self.user.__str__()


class Chore(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField('date done', null=True)
    period = models.PositiveIntegerField('period count', null=True)

    class PeriodChoices(models.TextChoices):
        DAY = 'D', _('days')
        WEEK = 'W', _('weeks')
        MONTH = 'M', _('months')
        YEAR = 'Y', _('years')
        ONCE = 'O', _('once')

    period_type = models.CharField(
        max_length=1,
        choices=PeriodChoices.choices,
        default=PeriodChoices.WEEK,
    )

    class EffortChoices(models.TextChoices):
        EASY = 'E', _('Easy')
        NORMAL = 'N', _('Normal')
        HARD = 'H', _('Hard')

    effort = models.CharField(
        max_length=1,
        choices=EffortChoices.choices,
        default=EffortChoices.NORMAL,
    )

    status = models.BooleanField('chore status')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rooms_chores')
    slave = models.ForeignKey(Slave, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Invite(models.Model):
    sender = models.ForeignKey(Slave, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Slave, on_delete=models.CASCADE, related_name='receiver')
    is_join_request = models.BooleanField(default=False, null=True)
    is_accepted = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.sender.__str__()
