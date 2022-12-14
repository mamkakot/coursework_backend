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
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='familys_slaves')

    def __str__(self):
        return self.user.__str__()


class Chore(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField('date done', null=True)

    class PeriodChoices(models.TextChoices):
        DAY = 'D', _('Once a day')
        WEEK = 'W', _('Once a week')
        MONTH = 'M', _('Once a month')
        YEAR = 'Y', _('Once a year')
        ONCE = 'O', _('Once')
        CUSTOM = 'C', _('Custom')

    period = models.CharField(
        max_length=1,
        choices=PeriodChoices.choices,
        default=PeriodChoices.WEEK,
    )

    class ConditionChoices(models.TextChoices):
        AWFUL = 'A', _('Awful')
        BAD = 'B', _('Bad')
        NORMAL = 'N', _('Normal')
        GOOD = 'G', _('Good')
        EXCELLENT = 'E', _("Excellent")

    condition = models.CharField(
        max_length=1,
        choices=ConditionChoices.choices,
        default=ConditionChoices.NORMAL,
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
