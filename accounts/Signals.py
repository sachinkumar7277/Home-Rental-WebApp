from django.dispatch import receiver
from django.urls import reverse

from django.db.models.signals import post_save, pre_delete,pre_save
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

from .models import User
from .models import Profile
@receiver(post_save,sender =User)
def save_profile(sender,instance,created,**kwargs):
    if created:
        print("New User Created Now")
        Profile.objects.create(phone_no = instance.phone , user = instance,Fullname = instance.username,Email = instance.email,date_of_birth = instance.date_of_birth)





@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "http://127.0.0.1:8000/api/password-reset-confirmation/{}".format(reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )