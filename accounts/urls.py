from django.urls import path
from django.conf.urls import include
from .views import SendOTPphone,validateOTP,Register,LoginAPI,ChangePasswordView,EditProfile,logoutview,\
    ProfileView,UpdateProfileView,UserAvatarUpload,goToResetPass,ConfirmResetPass,ConfirmPassreset,GetPremiumPlan,ShowPremiumPlan,AddPremiumMembership,ContactUs
urlpatterns = [
    path('validatePhone',SendOTPphone.as_view() ),
    path('validateOTP', validateOTP.as_view()),
    path('register',Register.as_view()),
    path('login',LoginAPI.as_view()),
    path('logout',logoutview),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('Editprofile', EditProfile.as_view(), name='Edit-profile'),
    path('goToResetPass', goToResetPass.as_view(), name='goToResetPass'),

    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password_reset/confirm/<str:token>', include('django_rest_passwordreset.urls', namespace='password_reset_confirm')),
    path('password-reset-confirmation/<str:token>',ConfirmResetPass),
    path('confirmation/<str:token>',ConfirmPassreset.as_view()),


    path('profile/view/', ProfileView),
    path('profile/update/', UpdateProfileView),
    path('AddPremium', AddPremiumMembership.as_view()),
    path('ShowPremiumPlans', ShowPremiumPlan),
    path('Contactus', ContactUs.as_view()),



    path("Imageupload", UserAvatarUpload.as_view(), name="rest_user_avatar_upload"),

]
