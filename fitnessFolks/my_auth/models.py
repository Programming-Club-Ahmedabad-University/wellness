from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User

from multiselectfield import MultiSelectField


GENDER = (
	("1", "male"),
	("2", "female"),
	("3", "rather not say"),
)
GOAL = (

	('<5', '<5'),
	('5-10', '5-10'),
	('10-15', '10-15'),
	('15-25', '15-25')
)
WORKOUT = (
	('Exercise at home', 'Exercise at home'),
	('Gyming', 'Gyming'),
	('Cycling', 'Cycling'),
	('Walk', 'Walk'),
	('Yoga', 'Yoga'),
	('Zumba', 'Zumba')
)
REASON = (
	('Peer', 'Peer'),
	('Social', 'Social'),
	('Self', 'Self'),
	('Family', 'Family'),
	('Group', 'Group'),
)
MEDICINES = (
	('Yes', 'Yes'),
	('No', 'No'),
)
JUNK = (
	('Daily', 'Daily'),
	('Every alternate day', 'Every alternate day'),
	('twice a week', 'twice a week'),
	('once a week', 'once a week'),
	('once a month', 'once a month'),
)
MENSTRUAL_CYCLE = (
	('2', '2'),
	('3', '3'),
	('4', '4'),
	('5', '5'),
	('6', '6'),
	('6+', '6+'),
)

SCREENING_TEST_GAP = 1


class ExtraDetails(models.Model):
	last_weekly_update 		= models.DateTimeField(null=True, blank=True)
	last_daily_update 		= models.DateTimeField(null=True, blank=True)
	last_screening_date 	= models.DateTimeField(null=True, blank=True)
	last_screening_number 	= models.IntegerField(default=1)
	updated_profile 		= models.BooleanField(default=False)
	user 					= models.OneToOneField(User,
										related_name='extra_details',
										null=True, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.user.first_name}_extra_details"
	
	def set_screening_number(self):
		self.last_screening_number += 1
		self.save()

	# Returns all the given answers of current test
	def get_answered_questions(self):
		answered_questions = list()
		answers = self.user.answers.filter(
			answer_test=self.last_screening_number)
		for answer in answers:
			answered_questions.append(answer.answer_number)
		return answered_questions

	# To check if the test is available for the user
	def is_test_active(self):
		if self.last_screening_date is None:
			return True
		else:
			current_time = datetime.now(tz=self.last_screening_date.tzinfo)
			return (True 
				if (current_time - self.last_screening_date >= 
					timedelta(days=SCREENING_TEST_GAP))
				else False)


class UserDetails(models.Model):

	gender 				= models.CharField(max_length=200, choices=GENDER)
	birthdate 			= models.DateField()
	height 				= models.IntegerField()
	weight 				= models.IntegerField()
	goal 				= models.CharField(max_length=200, choices=GOAL)
	workout_pattern 	= MultiSelectField(choices=WORKOUT)
	water_consumption 	= models.IntegerField()
	reason 				= MultiSelectField(max_length=200, choices=REASON)
	med 				= models.CharField(max_length=200, choices=MEDICINES)
	med_reason 			= models.CharField(max_length=200, null=True,
										  blank=True)
	menstural_cycle 	= models.CharField(max_length=200, 
										choices=MENSTRUAL_CYCLE,
										   null=True, blank=True)
	sleep 				= models.IntegerField()
	smoking 			= models.IntegerField()
	junkfood 			= models.CharField(max_length=200, choices=JUNK)

	user 				= models.OneToOneField(User, related_name='details', 
										null=True, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.user.first_name}_details"
