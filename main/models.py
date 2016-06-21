# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Member(models.Model):
	name = models.CharField(max_length=10, unique=True)
	phone_number = models.CharField(max_length=13)

	def __unicode__(self):
		return u'''%s (%s)''' % (self.name, self.phone_number)


class Schedule(models.Model):
	SUNDAY = 0
	MONDAY = 1
	THUSDAY = 2
	WEDNESDAY = 3
	THURSDAY = 4
	FRIDAY = 5
	SATURDAY = 6
	WEEK_DAY = (
		(SUNDAY, '일요일'),
		(MONDAY, '월요일'),
		(THUSDAY, '화요일'),
		(WEDNESDAY, '수요일'),
		(THURSDAY, '목요일'),
		(FRIDAY, '금요일'),
		(SATURDAY, '토요일'),
	)
	member = models.ForeignKey(Member)
	week_day = models.IntegerField(default=0, choices=WEEK_DAY)
	start_time = models.IntegerField(
		default=0,
		validators=[
            MaxValueValidator(86399),
            MinValueValidator(0)
        ]
	)
	end_time = models.IntegerField(
		default=0,
		validators=[
            MaxValueValidator(86399),
            MinValueValidator(0)
        ]
	)
	place = models.CharField(max_length=30)

	@property
	def start_time_display(self):
		return '%02d:%02d:%02d' % (self.start_time / 3600, self.start_time % 3600 / 60, self.start_time % 60)


	@property
	def end_time_display(self):
		return '%02d:%02d:%02d' % (self.end_time / 3600, self.end_time % 3600 / 60, self.end_time % 60)

	def __unicode__(self):
		return u'''%s has schedule at %s %s (%d ~ %d)''' % (self.member.name, self.place, self.get_week_day_display(), self.start_time, self.end_time)



