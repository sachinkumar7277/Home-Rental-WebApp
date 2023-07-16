from datetime import timedelta, datetime

from django.db import models
from django.utils import timezone
from django.db.models.deletion import CASCADE, PROTECT
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils.text import slugify


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, phone, email, date_of_birth, username, password):
        if not phone:
            raise ValueError("User must have phone number ")
        if password is None:
            raise ValueError("Password can not be None ")
        user = self.model(
            phone=phone,
            email=email,
            date_of_birth=date_of_birth,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, password, email, username, date_of_birth):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            phone,
            email,
            password,
            username,
            date_of_birth

        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, date_of_birth, username, password=None):
        user = self.create_user(
            phone=phone,
            email=email,
            password=password,
            date_of_birth=date_of_birth,
            username=username,

        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    phone = models.CharField('Phone', validators=[phone_regex], max_length=10, unique=True, null=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=100, null=False, blank=False)
    date_of_join = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'date_of_birth', 'username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    """ 
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin   """


class OTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$')
    phone = models.CharField('phone', validators=[phone_regex], max_length=10, null=False, blank=False, unique=True)
    otp = models.CharField(max_length=5, null=True, blank=True)
    Sent_time = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(null=True, help_text="Number of OTP sent", blank=True)
    validated = models.BooleanField(default=False)

    def __str__(self):
        return self.otp + "is Your OTP --->" + self.phone


class Profile(models.Model):
    Fullname = models.CharField(max_length=100, null=True, blank=True)
    Email = models.EmailField(max_length=100, unique=True, null=True)
    date_of_birth = models.DateField()
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    address = models.TextField(null=True)
    pin_no = models.IntegerField(null=True)
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True, blank=True)
    Profile_pic = models.ImageField(upload_to='Profilepic', null=True, blank=True, max_length=255)
    premium = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.user, self.Fullname)

    @property
    def is_premium_active(self):
        current_datetime = datetime.now()
        subscribed_plan = self.premium_subscribed_profile.filter(end_date__gte=current_datetime).first()
        return subscribed_plan is not None

    @property
    def profile_picURL(self):
        try:
            url = self.Profile_pic.url
        except:
            url = ''
        return url


class ServiceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    service_type_for_url = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate the service type for URL by slugifying the name
        self.service_type_for_url = slugify(self.name)

        super().save(*args, **kwargs)



class PremiumPlan(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    Amount = models.IntegerField(null=False)
    duration = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name


class SubscribedPremiumPlan(models.Model):
    premium_plan = models.ForeignKey(to=PremiumPlan, on_delete=PROTECT)
    profile = models.ForeignKey(to=Profile, on_delete=CASCADE, related_name="premium_subscribed_profile")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=None, null=True)
    is_premium_active = models.BooleanField(default=False)

    def __str__(self):
        return self.premium_plan.name


class ServiceProvider(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.service_type.name


# demo to upload image  using Put request


# myproject/apps/accounts/models.py
import os
import sys
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"users/{instance.pk}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


class ImageFieldUpload(models.Model):
    # …
    avatar = models.ImageField(_("Avatar"), upload_to=upload_to, blank=True)
