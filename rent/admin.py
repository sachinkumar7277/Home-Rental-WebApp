from django.contrib import admin
from .models import room,District,State,Locations,Temporary,City,Gallerys,Reg_Mess_Restaurent,Temp_Reg_Mess_Restaurent
from django.contrib.admin.options import ModelAdmin
#
# class ProfileAdmin(ModelAdmin):
#     list_display = ['name','state','city','pin_no','phone_no']
#     search_fields = ['name','phone_no','pin_no','city']
#
# admin.site.register(Profile,ProfileAdmin)

class roomAdmin(ModelAdmin):
    list_display = ['id','Owner_Name','city','House_address','phone_no']
    search_fields = ['Owner_Name','city','House_address','phone_no']

admin.site.register(room,roomAdmin)


class TemporaryAdmin(ModelAdmin):
    list_display = ['id','Owner_Name','state','district','city','House_address','phone_no']
    search_fields = ['Owner_Name','city','House_address','phone_no']

admin.site.register(Temporary,TemporaryAdmin)


class StateAdmin(ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']

admin.site.register(State,StateAdmin)

class DistrictAdmin(ModelAdmin):
    list_display = ['id','name','state']
    search_fields = ['name','state']

admin.site.register(District,DistrictAdmin)


class LocationsAdmin(ModelAdmin):
    list_display = ['id','name','city']
    search_fields = ['name','city']

admin.site.register(Locations,LocationsAdmin)



class CityAdmin(ModelAdmin):
    list_display = ['id','name','dist']
    search_fields = ['name','dist']

admin.site.register(City,CityAdmin)
# Register your models here.




class Reg_Mess_RestaurentAdmin(ModelAdmin):
    list_display = ['Mess_Owner_name','Mess_name','city','Mess_address','phone_no']
    search_fields = ['Mess_Owner_name','city','Mess_address','phone_no']

admin.site.register(Reg_Mess_Restaurent,Reg_Mess_RestaurentAdmin)

class Temp_Reg_Mess_RestaurentAdmin(ModelAdmin):
    list_display = ['Mess_Owner_name','Mess_name','city','Mess_address','phone_no']
    search_fields = ['Mess_Owner_name','city','Mess_address','phone_no']

admin.site.register(Temp_Reg_Mess_Restaurent,Temp_Reg_Mess_RestaurentAdmin)


admin.site.register(Gallerys)