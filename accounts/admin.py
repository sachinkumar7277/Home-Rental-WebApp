from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User,OTP,Profile,PremiumPlan
from django.contrib.admin.options import ModelAdmin
from accounts.forms import UserCreationForm,UserChangeForm
# Register your models here.



class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'phone','username','is_admin','is_staff','date_of_join')
    list_filter = ('is_admin','phone')
    fieldsets = (
        (None, {'fields': ('phone','email', 'password')}),
        ('Permissions', {'fields': ('is_admin','is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone','email', 'password1', 'password2','username','is_admin','is_staff'),
        }),
    )
    search_fields = ('email','phone')
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


class OTPAdmin(ModelAdmin):
    list_display = ['phone','otp','count','Sent_time']
admin.site.register(OTP,OTPAdmin)



class ProfileAdmin(ModelAdmin):
    list_display = ['id','phone_no','Fullname','Email','address']
admin.site.register(Profile,ProfileAdmin)

class PremiumPlanAdmin(ModelAdmin):
    list_display = ['id','Amount','Validity']
admin.site.register(PremiumPlan,PremiumPlanAdmin)