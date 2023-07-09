from datetime import timedelta

from django.shortcuts import render, redirect
from django.utils import timezone
from rest_framework.views import APIView, Response
from rest_framework import permissions, status, generics
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from decouple import config
from django.core.mail import send_mail

from .serializers import CreateUserSerializer, LoginSerializer, EditProfileSerializer, UserAvatarSerializer, \
    PremiumPlanSerializer

import json
import requests

from .models import User, OTP, Profile, PremiumPlan, SubscribedPremiumPlan
from rent.models import room
import random
from django.contrib.auth.decorators import login_required
from knox.views import LoginView, LogoutView
from knox.auth import TokenAuthentication
from knox.models import AuthToken


@method_decorator(csrf_exempt, name='dispatch')
class SendOTPphone(APIView):
    """
     provide phone  in json format to meet ur request as follow
    {
    "phone" : "8373733743"
   }

    """

    def send_otp(self, phone, otp, email):
        try:

            print("8" * 70)
            print("Ye Send OTP TO PHONE NUMBER CALL HUA HAI ")
            print('Account_sid: ', config('Account_sid'))
            Account_sid = config('Account_sid')

            print(Account_sid, "SID no")
            auth_token = config('auth_token')
            print(auth_token, "auth TOken ")
            client = Client(Account_sid, auth_token)
            print(Client)
            message = client.messages \
                .create(
                body="Your One Time Password For  Apnaashiyana.com is {} Please do not share your OTP with Any one ".format(
                    otp),
                to='+91{}'.format(phone),
                from_=config('from'),
            )
            print(message)
            print(message.sid)
            print("8" * 70)

        except TwilioRestException:
            send_mail("OTP from ApnaAashiyana to register is",
                      "Please do not share your OTP {key}".format(key=otp),
                      config("YOUR_EMAIL_ID"), [email])

        return

    def post(self, request, *args, **kwargs):
        data = request.body
        dict_data = json.loads(data)
        print(dict_data)

        phone_number = dict_data.get("phone")
        email = dict_data.get("email_address")

        print(phone_number)
        if phone_number:

            user = User.objects.filter(phone__iexact=phone_number)
            if user.exists():
                return Response({
                    'status': False,
                    'Detail': "Failed to enroll as phone number already taken "
                })
            else:
                key = SendOTP(phone_number)
                if key:
                    print(key)
                    old_otp = OTP.objects.filter(phone=phone_number)
                    if old_otp.exists():
                        old = old_otp.first()
                        count = old.count
                        print(count)
                        if count > 4:
                            return Response({
                                'status': False,
                                'Detail': 'OTP sending limit is crossed contact to customer care on 8340312640 '

                            })
                        else:
                            old.count = count + 1
                            old.otp = key
                            old.save()
                            self.send_otp(phone_number, key, email)
                            return Response({
                                "status": True,
                                "OTP": key,
                                "Detail": "OTP sent Successfully "

                            })

                    OTP.objects.create(
                        phone=phone_number,
                        otp=key,
                        count=1
                    )
                    self.send_otp(phone_number, key, email)
                    return Response({
                        "status": True,
                        "OTP": key,
                        "Detail": "OTP sent Successfully "

                    })
                else:
                    return Response({
                        'status': False,
                        'Detail': 'Something Went Wrong please contact customer support'

                    })


        else:
            return Response({
                'status': False,
                'Detail': 'Phone Number Not Given plz input valid phone number'

            })


def SendOTP(phone):
    if phone:
        key = random.randint(999, 9999)
        return key
    else:
        return False


class validateOTP(APIView):
    """
    if user has already recieved the otp then  redirect to set password for registration

    provide phone and OTP in jason format to meet ur request as follow
    {

    "phone" : "83737337434" ,
    "otp" : "4848"

    }
    """

    def post(self, request, *args, **kwargs):
        data = request.body
        data_dict = json.loads(data)
        phone = data_dict["phone"]
        sent_otp = data_dict["otp"]
        if phone and sent_otp:
            old = OTP.objects.filter(phone__iexact=phone)
            old = old.first()
            if str(sent_otp) == old.otp:
                old.validated = True
                old.save()
                return Response({
                    "status": True,
                    "Message ": "OTP Matched proceed for registration "

                })
            else:
                return Response({
                    "status": False,
                    "Message ": "OTP Not Matched Try Again with valid otp "

                })
        else:
            return Response({
                "status": False,
                "Message ": "Enter valid phone number in valid json format "

            })


class Register(APIView):
    """
     provide phone and password in json format to meet ur request as follow
    {

    "phone" : "8737337434",
    "password"   : "Sanjf38339@",
    "email" : "sajjff27636@gmail.com",
    "DOB"   :  "1998-12-30",
    "username" : "sachin"

    }

    """

    def post(self, request, *args, **kwargs):
        print("Register call hua hai ")
        data = json.loads(request.body)
        phone = data["phone"]
        password = data["password"]
        print(data, "register form se aaya hai ")
        if phone and password:
            old = OTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                if old.validated:
                    temp_data = {
                        "phone": data['phone'],
                        "password": data['password'],
                        "email": data['email'],
                        "date_of_birth": data['DOB'],
                        "username": data["username"]

                    }
                    serializer = CreateUserSerializer(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    old.delete()
                    return Response({
                        "status": True,
                        "message": "Account created",
                        "token": AuthToken.objects.create(user)[1]
                    })
                else:
                    return Response({
                        "status": False,
                        "message": "Account not created First verify ur phone"
                    })
            else:

                return Response({
                    "status": False,
                    "message": "Account not created First verify ur phone"
                })
        else:
            return Response({
                "status": False,
                "message": "Enter valid phone or password in json format"
            })


class LoginAPI(LoginView):
    """
     provide phone and password in json format to meet ur login request as follow
    {

    "phone" : "8737337434",
    "password"   : "Sanjf38339@"
    }
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = request.body
        data = json.loads(data)
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        res = super().post(request, format=None)
        print(res.data)
        print(super().post(request, format=None), "ye super method wala ha")
        if user.is_authenticated:
            print("user is logged in ")
            return Response({
                'status': True,
                'token': res.data['token']
            })


        else:

            return Response({'status': False})


@method_decorator(login_required, name="dispatch")
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = json.loads(request.body)
        print(data, "cOMING FROM CHANGE PASSW FORM")
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required, name="dispatch")
class EditProfile(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, format=None):

        data = request.body

        data = json.loads(data)

        # print(type(data['Profile_pic']))
        queryset = Profile.objects.get(id=data['id'])
        serializer = EditProfileSerializer(queryset, data=data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "UpdatedData": serializer.validated_data,
                'status': True,
                "msg": "Data successfully updated"

            })
        else:
            return Response({
                "msg": "something went wrong",
                "status": False
            })


def logoutview(request):
    logout(request)
    return redirect('/')


@login_required()
def ProfileView(request):
    user = Profile.objects.filter(id=request.user.profile.id)
    context = {'data': room.objects.all().filter(user=request.user.profile).order_by("-id"),
               'users': user
               }
    return render(request, 'UserProfile.html', context)


@login_required()
def UpdateProfileView(request):
    user = Profile.objects.filter(id=request.user.profile.id)
    date_of_birth = None
    for i in user:
        date_of_birth = i.date_of_birth.strftime("%Y-%m-%d")
    return render(request, 'UpdateProfile.html', {'users': user, 'date_of_birth': date_of_birth})


# FOR IMAGEFIELD UPLOAD CHECK
@method_decorator(login_required, name="dispatch")
class UserAvatarUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, format=None):
        # print("Avtar se AAYA HAI ")
        user = Profile.objects.get(id=request.data.get('id'))
        serializer = UserAvatarSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({

                'status': True,
                "msg": "Data successfully updated"

            })
        else:
            return Response({
                "msg": "something went wrong",
                "status": False
            })


class goToResetPass(APIView):
    def post(self, request, format=None):
        data = request.body

        data = json.loads(data)
        try:

            user = User.objects.filter(email=data['email'])
        except:
            return Response({
                "status": False,
                "msg": "User with this email id is not valid "
            })
        if user.exists():
            BASE_URL = "{0}://{1}/api/".format(request.scheme, request.get_host(), request.path)
            # BASE_URL = "http://127.0.0.1:8000/api/"
            END_POINT = "password_reset/"
            respo = requests.post(BASE_URL + END_POINT, data=data)
            print(respo)
            print("User exist but : ", )
            if respo.status_code == 200:

                return Response({

                    "status": True,
                    'msg': 'Reset password link has been sent to your email'
                })
            else:
                return Response({
                    "status": False,
                    "msg": "User exist  with this email id is unable to process this time "
                })


def ConfirmResetPass(request, token):
    print("This cam from email link when you clicked on email link  ", token)

    return render(request, 'resetpassword.html', {'token': token})


class ConfirmPassreset(APIView):

    def post(self, request, token, format=None):
        data = request.body
        print("i was called from  confirm Pass Reset")
        data = json.loads(data)

        print(data['password'])
        data['token'] = token
        print(data, "Conform pass se aaya hu SS")

        BASE_URL = "{0}://{1}/api/".format(request.scheme, request.get_host(), request.path)
        # BASE_URL = "http://127.0.0.1:8000/api/"
        END_POINT = "password_reset/confirm/{}".format(token)
        respo = requests.post(BASE_URL + END_POINT, data=data)
        print(respo.json(), "Ye e ConfirmPassreset", respo.status_code)
        if respo.status_code == 200:

            return Response({

                "status": True,
                'msg': 'Password reset successful!'
            })
        else:
            return Response({
                "status": False,
                "msg": respo.json()
            })


class GetPremiumPlan(APIView):
    def get(self, request, format=None):
        plans = PremiumPlan.objects.all()
        serializer = PremiumPlanSerializer(plans, many=True)
        return Response(serializer.data)


def ShowPremiumPlan(request):
    plans = PremiumPlan.objects.all()
    return render(request, 'premiumplan.html', {'plans': plans})


class AddPremiumMembership(APIView):
    def put(self, request, format=None):
        print("Ander aaya hai Premium membership")
        data = request.body

        data = json.loads(data)
        print(data)
        plan = PremiumPlan.objects.get(id=data['planId'])
        profile = Profile.objects.get(id=data['id'])
        duration = plan.duration  # Assuming duration is in days
        current_datetime = timezone.now()
        end_date = current_datetime + timedelta(days=duration)

        subscribed_plan = SubscribedPremiumPlan.objects.create(
            premium_plan=plan,
            profile=profile,
            start_date=current_datetime,
            end_date=end_date,
            is_premium_active=True
        )
        profile.premium = True
        profile.save()
        return Response({
            'status': True,
            "msg": "Premium Added successfully"

        })


class ContactUs(APIView):
    def post(self, request, format=None):
        data = request.body
        data = json.loads(data)
        send_mail(data['subject'], "Hi  This is " + data['name'] + '   ' + data['message'],
                  config("YOUR_EMAIL_ID"), [data['email']])
        return Response({
            'status': True,
            "msg": "Data successfully updated"

        })
