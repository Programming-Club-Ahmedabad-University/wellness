from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from multiselectfield import MultiSelectField

from AhdUni.settings import SCREENING_TEST_GAP

GENDER_CHOICES = (
    ("1", "male"),
    ("2", "female"),
    ("3", "rather not say"),
)
CATEGORY_SG = (
    ('<5', '<5'),
    ('5-10', '5-10'),
    ('10-15', '10-15'),
    ('15-25', '15-25')
)
CATEGORY_WP = (
    ('Exercise at home', 'Exercise at home'),
    ('Gyming', 'Gyming'),
    ('Cycling', 'Cycling'),
    ('Walk', 'Walk'),
    ('Yoga', 'Yoga'),
    ('Zumba', 'Zumba')
)
CATEGORY_REASON = (
    ('Peer', 'Peer'),
    ('Social', 'Social'),
    ('Self', 'Self'),
    ('Family', 'Family'),
    ('Group', 'Group'),
)
CATEGORY_MED = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)
CATEGORY_JUNK = (
    ('Daily', 'Daily'),
    ('Every alternate day', 'Every alternate day'),
    ('twice a week', 'twice a week'),
    ('once a week', 'once a week'),
    ('once a month', 'once a month'),
)
CATEGORY_MC = (
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('6+', '6+'),
)


class AccountManager(BaseUserManager):

    def create_user(self, email, enrollment_number=None, password=None,
                    full_name=None, contact_number=None,
                    programme=None, gender=None, is_active=True,
                    staff=False, is_superuser=False, is_activated=False):

        user = self.model(
            full_name=full_name,
            email=self.normalize_email(email),
            enrollment_number=enrollment_number,
            contact_number=contact_number,
            programme=programme,
            gender=gender
        )

        user.set_password(password)
        user.is_active = is_active
        user.staff = staff
        user.is_superuser = is_superuser
        user.is_activated = is_activated
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            staff=True,
            is_activated=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            staff=True,
            is_superuser=True,
            is_activated=True
        )
        return user


class Account(AbstractBaseUser):

    # custom_fields
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True)
    enrollment_number = models.IntegerField(null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True)
    programme = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES,
                              null=True, blank=True)
    last_weekly_update = models.DateTimeField(null=True, blank=True)
    last_daily_update = models.DateTimeField(null=True, blank=True)
    last_screening_date = models.DateTimeField(null=True, blank=True)
    last_screening_number = models.IntegerField(default=1)
    has_updated_profile = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    # required_fields
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = AccountManager()

    def __str__(self):
        return self.full_name or "No name"

    # required functions
    @property
    def is_staff(self):
        return self.staff

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    # custom functions

    # To increment the number of screening tests
    def set_screening_number(self):
        self.last_screening_number += 1
        self.save()

    # Returns all the given answers of current test
    def get_answered_questions(self):
        answered_questions = list()
        answers = self.answers.filter(
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
            return (True if current_time - self.last_screening_date >=
                    timedelta(days=SCREENING_TEST_GAP)
                    else False)    


class UserDetails(models.Model):

    age = models.IntegerField()
    height = models.IntegerField()
    current_weight = models.IntegerField()
    set_goal = models.CharField(max_length=200, choices=CATEGORY_SG)
    workout_patterns = MultiSelectField(choices=CATEGORY_WP)
    daily_water = models.IntegerField()
    # current_diet
    reason = MultiSelectField(max_length=200, choices=CATEGORY_REASON)
    ongoing_med = models.CharField(max_length=200, choices=CATEGORY_MED)
    ongoing_med_reason = models.CharField(max_length=200, null=True, 
                                          blank=True)
    menstural_cycle = models.CharField(max_length=200, choices=CATEGORY_MC, 
                                       null=True, blank=True)
    hours_sleep = models.IntegerField()
    smoking = models.IntegerField()  # how many times a day
    alcohol = models.IntegerField()  # how many times a month
    junkfood = models.CharField(max_length=200, choices=CATEGORY_JUNK)

    user = models.ForeignKey(
        Account, related_name='details', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.full_name
