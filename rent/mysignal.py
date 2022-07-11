# from django.dispatch.dispatcher import receiver
# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from rent.models import Profile
# @receiver(post_save,sender =User)
# def save_profile(sender,instance,created,**kwargs):
#     if created:
#         Profile.objects.create(user = instance,name = instance.username)

