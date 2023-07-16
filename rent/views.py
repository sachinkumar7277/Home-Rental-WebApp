from decouple import config
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import room, State, District, Locations, Temporary, City, Gallerys, Reg_Mess_Restaurent, \
    Temp_Reg_Mess_Restaurent
import json
import requests
from accounts.models import Profile, SubscribedPremiumPlan, ServiceType, ServiceProvider
from django.core.mail import send_mail
from .serializers import RoomUploadUSerializer, RoomUpdateUSerializer, RoomMediaFileUpdateSerializer, RoomSerializer
# from .forms import roomForm
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .regexutils import extract_value_from_source


def index(request):
    base_url = "{0}://{1}".format(request.scheme, request.get_host(), request.path)
    print(base_url)
    state = State.objects.all()
    if request.method == 'POST':

        state_id = request.POST.get("state")
        state = State.objects.get(id=state_id)
        dist_id = request.POST.get("district")
        dist = District.objects.get(id=dist_id)
        city_id = request.POST.get("city")
        city = City.objects.get(id=city_id)
        location_id = request.POST.get("location")
        location = Locations.objects.get(id=location_id)
        AllowedFor = request.POST.get("selectFor")
        House_type = request.POST.get("House_type")

        SearchedObject = room.objects.filter(
            Q(state__icontains=state.name) and Q(AllowedFor__icontains=AllowedFor) and Q(
                House_type__icontains=House_type) and Q(district__icontains=dist.name) and Q(
                city__icontains=city.name) and Q(location__icontains=location.name))
        search = SearchedObject.filter(Active=True, Premium=True)
        recomend = room.objects.filter(city=city.name)
        recomend = recomend.filter(Active=True, Premium=True)
        if SearchedObject is None:
            messages.info(request, 'No Result Found As of Now')
            return redirect('/')
        return render(request, 'SearchResult.html', {'SearchResult': search, 'Reco': recomend})
    state = State.objects.all()

    Restaurents = Reg_Mess_Restaurent.objects.all()

    gallery = Gallerys.objects.all()

    # Room = room.objects.filter(Premium = True,Active = True)
    END_POINT = "/rent/GetRoomData"
    respo = requests.get(base_url + END_POINT)

    return render(request, 'index11.html',
                  {'RoomDetail': respo.json()['results'], 'state': state, 'gallery': gallery, 'Resto': Restaurents})


# Create your views here.

def loginpage(request):
    Render_to = str(request.GET['next'])
    print(Render_to)

    return render(request, 'loginPage.html', {'Render_to': Render_to})


def About(request):
    return render(request, 'about.html')


def services(request):
    service_list = ServiceType.objects.all()
    return render(request, 'serviceListing.html', {'service_list': service_list})

@login_required(login_url='/rent/loginPage')
def service_providers(request, service_type):
    service_providers_list = ServiceProvider.objects.filter(service_type__service_type_for_url=service_type)
    return render(request, 'serviceProvidersList.html',
                  {'service_providers': service_providers_list,'service_type':service_type}
                  )


def ContactUs(request):
    return render(request, 'contact.html')


def Districts(request):
    state_id = request.GET.get('state')
    # print("selected state is ",state_id)
    dist = District.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'load_country.html', {'dists': dist})


def city(request):
    dist_id = request.GET.get('dist')
    # print("selected district is yahi hai ",dist_id)
    dist = City.objects.filter(dist_id=dist_id).order_by('name')
    return render(request, 'load_country.html', {'dists': dist})


def locations(request):
    city_id = request.GET.get('city')
    # print("selected city is yahi hai ",city_id)
    dist = Locations.objects.filter(city_id=city_id).order_by('name')
    return render(request, 'load_country.html', {'dists': dist})


@login_required(login_url='/rent/loginPage')
def UploadHouseDetail(request):
    profile = request.user.profile
    is_rental_service_subscribed = SubscribedPremiumPlan.objects.filter(
        profile=profile,
        premium_plan__service_type__name="Rental"
    ).exists()

    if is_rental_service_subscribed and profile.is_premium_active:
        state = State.objects.all()
        context = {'state': state}
        return render(request, 'FormUpload.html', context)

    else:
        return redirect('/')


@login_required(login_url='/rent/loginPage')
def HouseDetail(request, pk):
    Room = room.objects.filter(id=pk)
    return render(request, 'property-single.html', {'Detail': Room})


def Allmess(request):
    state = State.objects.all()
    return render(request, 'All_mess.html', {'state': state})


@login_required(login_url='/rent/loginPage')
def Single_view_mess(request, pk):
    MessDetail = Reg_Mess_Restaurent.objects.filter(id=pk)

    return render(request, 'mess_single.html', {'Details': MessDetail})


# @login_required(redirect_field_name='RegisterMess',login_url='/rent/loginPage')
@login_required(login_url='/rent/loginPage')
def RegisterMess(request):
    state = State.objects.all()
    if request.method == 'POST':
        user = request.user.profile
        Ownername = request.POST.get('Ownername')
        Messname = request.POST.get('Messname')
        phone = request.POST.get('phone')
        MessAdress = request.POST.get('MessAdress')
        landmark = request.POST.get('landmark')
        state_Id = request.POST.get('programming')
        statee = State.objects.get(id=state_Id)
        dist_Id = request.POST.get('courses')
        dist = District.objects.get(id=dist_Id)
        city_Id = request.POST.get('city')
        city = City.objects.get(id=city_Id)
        location_Id = request.POST.get('location')
        location = Locations.objects.get(id=location_Id)
        pincode = request.POST.get('pincode')
        Mess_image = request.FILES.get('Mess_image')

        MessDescription = request.POST.get('MessDescription')

        Messlink = request.POST.get('Messlink')
        Messmap = request.POST.get('Messmap')

        Messmap1 = Messmap[13:271]

        # print(Housemap1)
        # print("length of map code hai tera",len(Housemap1))

        Temp_Reg_Mess_Restaurent.objects.create(user=user, Mess_Owner_name=Ownername, Mess_name=Messname,
                                                Mess_address=MessAdress,
                                                Landmark=landmark, Mess_Location_link=Messlink,
                                                Mess_Location_map_Code=Messmap1,
                                                Mess_description=MessDescription,
                                                state=statee.name, city=city.name,
                                                district=dist.name, location=location.name, pin_no=pincode,
                                                phone_no=phone,
                                                Mess_img=Mess_image
                                                ).save()
        return redirect('/')

    context = {'state': state}
    return render(request, 'RegisterMess.html', context)


@login_required()
def AllProperty(request):
    Room = room.objects.all().filter(Premium=True, Active=True)

    return render(request, 'property-grid.html', {'rooms': Room})


def PropertyDetail(request):
    return render(request, 'property-single.html')


@login_required(login_url='/rent/loginPage')
def ValidationPage(request):
    if request.user.is_admin:
        val = Temporary.objects.all().order_by("-id")
        messval = Temp_Reg_Mess_Restaurent.objects.all().order_by("-id")
        return render(request, 'Validate.html', {'Forvalidate': val, 'ForvalidateMess': messval})
    else:
        return HttpResponse('<h1>Access - Denied </h1>')


@login_required(login_url='/rent/loginPage')
def Validate(request, pk):
    if request.user.is_admin:

        getvalue = Temporary.objects.filter(id=pk)
        for i in getvalue:
            room.objects.create(user=i.user, Owner_Name=i.Owner_Name, House_address=i.House_address,
                                Landmark=i.Landmark,
                                House_Location_link=i.House_Location_link, House_Location_map=i.House_Location_map,
                                House_type=i.House_type, House_description=i.House_description, AllowedFor=i.AllowedFor,
                                state=i.state, city=i.city, location=i.location, Owner_pic=i.Owner_pic,
                                district=i.district, pin_no=i.pin_no, phone_no=i.phone_no,
                                Building_img1=i.Building_img1,
                                Room_img1=i.Room_img1,
                                Room_img2=i.Room_img2, Room_img3=i.Room_img3, House_video=i.House_video,
                                Alt_phone_no=i.Alt_phone_no, Price=i.Price, Premium=i.Premium, Active=True).save()

        Temporary.objects.filter(id=pk).delete()
    return HttpResponse("<h1>Validated </h1>")


@login_required(login_url='/rent/loginPage')
def ValidateMess(request, pk):
    if request.user.is_admin:

        getvalue = Temp_Reg_Mess_Restaurent.objects.filter(id=pk)

        for i in getvalue:
            Reg_Mess_Restaurent.objects.create(user=i.user, Mess_Owner_name=i.Mess_Owner_name, Mess_name=i.Mess_name,
                                               Mess_address=i.Mess_address,
                                               Landmark=i.Landmark, Mess_Location_link=i.Mess_Location_link,
                                               Mess_Location_map_Code=i.Mess_Location_map_Code,
                                               Mess_description=i.Mess_description,
                                               state=i.state, city=i.city,
                                               district=i.district, location=i.location, pin_no=i.pin_no,
                                               phone_no=i.phone_no,
                                               Mess_img=i.Mess_img
                                               ).save()

        Temp_Reg_Mess_Restaurent.objects.filter(id=pk).delete()
    return HttpResponse("<h1>Validated </h1>")


@login_required(login_url='/rent/loginPage')
def deletePostValidation(request, pk):
    Temporary.objects.filter(id=pk).delete()
    return HttpResponse("<h> Deleted the Post </h1>")


@login_required(login_url='/rent/loginPage')
def deleteMessPostValidation(request, pk):
    Temp_Reg_Mess_Restaurent.objects.filter(id=pk).delete()
    return HttpResponse("<h> Deleted the Post </h1>")


@login_required()
def DeletePost(request, pk):
    room.objects.filter(id=pk).delete()
    return render(request, 'index11.html')


@login_required()
def AddPremium(request):
    return render(request, 'index11.html')


#
# from django.core.serializers import serialize
#
# class JsonCBV(HttpResponseMixin,View):
#
#     def get(self,request,id,*args,**kwargs):
#         dataval = room.objects.all()
#         json_data = serialize('json',dataval,fields = ('state','city','House_type','House_address','Price'))
#
#         return self.render_to_Http_response(json_data)


@login_required(login_url='/rent/loginPage')
def UpdateRooms(request, pk):
    # state = State.objects.all()

    data = room.objects.filter(id=pk)
    obj = room.objects.get(id=pk)

    if request.user.id == obj.user.id:
        return render(request, 'UpdatePostRooms.html', {'data': data})
    return HttpResponse("404 BAD REQUEST You Are Not Authorized to Update this Post Invalid Auth Token")


# API FOR UPLOADING ROOMS

from rest_framework.views import APIView, Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, generics


@method_decorator(login_required, name='dispatch')
class RoomMediaFileUpdate(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser]

    def partial_update(self, request, pk=None):

        print(" Media file update k liye API CAll hua hai ")
        instance = room.objects.get(id=request.data.get('id'))

        Data = request.data
        print(Data, "Before pop operation")
        for key in list(Data):
            if Data[key] == 'undefined':
                print(Data[key], "loop k ander se")
                print(Data.pop(key))
        print(Data, "ye delete hone k baad aaya")

        serializer = RoomMediaFileUpdateSerializer(instance=instance, data=Data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.validated_data, "save hone k bad")
            return Response({

                'status': True,
                "msg": "Media File Updated  successfully "

            })
        else:
            print(serializer.validated_data, "save hone k bad")
            return Response({
                "msg": "something went wrong",
                "status": False
            })


@method_decorator(login_required, name='dispatch')
class UploadRoomsViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = room.objects.all(Premium=True, Active=True)
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pro = Profile.objects.get(id=int(request.data['user']))
        if pro.is_premium_active:
            print("yes Premium")
            request.data['Premium'] = True

        print("Room post upload k kliye rwana ho gya hai ")
        Housemap = request.data['House_Location_map']
        request.data['House_Location_map'] = extract_value_from_source(Housemap, "src")
        request.data['state'] = State.objects.get(id=int(request.data['state'])).name
        request.data['city'] = City.objects.get(id=int(request.data['city'])).name
        request.data['location'] = Locations.objects.get(id=int(request.data['location'])).name
        request.data['district'] = District.objects.get(id=int(request.data['district'])).name

        serializer = RoomUploadUSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            send_mail("Validate This Post  to upload ", "http://127.0.0.1:8000/rent/validationpage/",
                      config("YOUR_EMAIL_ID"), [config("YOUR_EMAIL_ID")])

            print("Room add ho gya data base me ")
            return Response({

                'status': True,
                "msg": "Data successfully created"

            })
        else:
            return Response({
                'status': False,
                "msg": "something went wrong",

            })

    def partial_update(self, request, pk=None):

        print("Update k liye aa gya hai dekho ")
        queryset = room.objects.get(id=request.data['id'])

        serializer = RoomUpdateUSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print("Room update ho gya hai in database")
            return Response({

                'status': True,
                "msg": "Data successfully updated"

            })
        else:
            return Response({
                'status': False,
                "msg": "something went wrong" + str(serializer.error_messages),

            })

    def destroy(self, request, pk=None):
        pass


class PostActivation(APIView):
    def post(self, request):
        data = request.body
        data = json.loads(data)

        obj = room.objects.get(id=data['id'])
        if data['user_id'] == obj.user.id:
            obj.Active = True
            obj.save()
            return Response({
                'status': True,
                'msg': 'Successfully Activated'
            })
        else:
            return Response({
                "status": False,
                "msg": 'Your are not Authorized to update this'
            })


class PostDeactivation(APIView):
    def post(self, request):
        data = request.body
        data = json.loads(data)

        obj = room.objects.get(id=data['id'])
        if data['user_id'] == obj.user.id:
            obj.Active = False
            obj.save()
            return Response({
                'status': True,
                'msg': 'Successfully Deactivated'
            })
        else:
            return Response({
                "status": False,
                "msg": 'Your are not Authorized to update this'
            })


class RoomDataViewSet(generics.ListAPIView):
    queryset = room.objects.filter(Premium=True, Active=True)
    serializer_class = RoomSerializer

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = RoomSerializer(queryset, many=True)
    #     print("ye tpe hai serializer data ka ",list(serializer.data))
    #     return Response(list(serializer.data))
