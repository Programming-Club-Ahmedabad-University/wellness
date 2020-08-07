from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

DEFAULT_TIME = datetime(2020, 6, 13, 16, 0, 0)


class AccountManager(BaseUserManager):

    def create_user(self, enrollment_number, email, password=None,
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

    def create_staffuser(self, enrollment_number, email, password=None):
        user = self.create_user(
            enrollment_number,
            email,
            password=password,
            staff=True,
            is_activated=True
        )
        return user

    def create_superuser(self, enrollment_number, email, password=None):
        user = self.create_user(
            enrollment_number,
            email,
            password=password,
            staff=True,
            is_superuser=True,
            is_activated=True
        )
        return user

gender_choices =( 
    ("1", "male"), 
    ("2", "female"), 
    ("3", "rather not say"), 
) 

class Account(AbstractBaseUser):
    # custom_fields
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True)
    # enrollment_number = models.CharField(max_length=20, unique=True)
    # contact_number = models.IntegerField(unique=True, null=True, blank=True)
    enrollment_number = models.CharField(max_length=20)
    contact_number = models.IntegerField(null=True, blank=True)
    programme = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=gender_choices, null=True, blank=True)
    # required_fields
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['enrollment_number']

    objects = AccountManager()

    def __str__(self):
        return self.enrollment_number

    @property
    def is_staff(self):
        return self.staff

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class User_Details(models.Model):
    CATEGORY_SG = (
        ('<5','<5'),
        ('5-10','5-10'),
        ('10-15','10-15'),
        ('15-25','15-25')
    )
    CATEGORY_WP = (
        ('Exercise at home','Exercise at home'),
        ('Gyming','Gyming'),
        ('Cycling','Cycling'),
        ('Walk','Walk'),
        ('Yoga','Yoga'),
        ('Zumba','Zumba')
    )

    CATEGORY_WI = (
        ('2','2'),
        ('4','4'),
        ('6','6'),
        ('8','8'),
        ('10','10'),
    )
    
    CATEGORY_REASON = (
        ('Peer','Peer'),
        ('Social','Social'),
        ('Self','Self'),
        ('Family','Family'),
        ('Group','Group'),
    )

    CATEGORY_MED = (
        ('Yes','Yes'),
        ('No','No'),
    )

    CATEGORY_JUNK = (
        ('Daily','Daily'),
        ('Every alternate day','Every alternate day'),
        ('twice a week','twice a week'),
        ('once a week','once a week'),
        ('once a month','once a month'),
    )
    age             = models.IntegerField()
    height          = models.IntegerField()
    current_weight  = models.IntegerField()
    set_goal        = models.CharField(max_length=200, choices=CATEGORY_SG)
    workout_patterns= models.CharField(max_length=200,choices=CATEGORY_WP)
    daily_water     = models.CharField(max_length=200, choices=CATEGORY_WI)
    reason          = models.CharField(max_length=200, choices=CATEGORY_REASON)
    ongoing_med     = models.CharField(max_length=200, choices=CATEGORY_MED)
    ongoing_med_reason = models.CharField(max_length=200,null=True)
    menstural_cycle = models.CharField(max_length=200 , null=True)
    hours_sleep     = models.IntegerField()
    smoking         = models.IntegerField()   #how many times a day
    alcohol         = models.IntegerField() #how many times a month
    junkfood        = models.CharField(max_length=200,choices=CATEGORY_JUNK)


    user = models.ForeignKey(Account,related_name='details', null=True, on_delete = models.SET_NULL)
