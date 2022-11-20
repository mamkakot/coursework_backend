from django.db import models
from django.utils.translation import gettext_lazy as _


class Room(models.Model):
    name = models.CharField(max_length=250)


class Chore(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField('date created')

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
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
