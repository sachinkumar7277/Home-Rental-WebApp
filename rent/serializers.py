from rest_framework import serializers

from rest_framework.authentication import authenticate
from .models import room,Temporary
class RoomUploadUSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temporary
        fields = '__all__'


    def create(self, validated_data):
        Room_created = Temporary.objects.create(**validated_data)

        return Room_created

class RoomUpdateUSerializer(serializers.ModelSerializer):
    class Meta:
        model = room
        fields = ['Owner_Name','House_address','House_description','AllowedFor','House_type','phone_no','Price',
                  'Landmark','Alt_phone_no','House_Location_map','House_Location_link']
        extra_kwargs = {'user': {'read_only': True} }

    def partial_update(self, instance, validated_data):
        print(validated_data, "ye validated data hai avatar se ")

        instance.Owner_Name = validated_data.get('Owner_Name', instance.Owner_Name)
        instance.House_address = validated_data.get('House_address', instance.House_address)
        instance.Landmark = validated_data.get('Landmark', instance.Landmark)
        instance.Alt_phone_no = validated_data.get('Alt_phone_no', instance.Alt_phone_no)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.Price = validated_data.get('Price', instance.Price)
        instance.House_type = validated_data.get('House_type', instance.House_type)
        instance.AllowedFor = validated_data.get('AllowedFor', instance.AllowedFor)
        instance.House_description = validated_data.get('House_description', instance.House_description)
        instance.House_Location_map = validated_data.get('House_Location_map', instance.House_Location_map)
        instance.House_Location_link = validated_data.get('House_Location_link', instance.House_Location_link)


        instance.save()
        print(instance)
        return instance



class RoomMediaFileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = room
        fields = ['House_video','Building_img1','Room_img1','Room_img2','Room_img3']
    def partial_update(self, instance, validated_data):
        print(validated_data, "ye validated data hai Room media file se aaya hai se ")

        instance.House_video = validated_data.get('House_video', instance.House_video)
        instance.Building_img1 = validated_data.get('Building_img1', instance.Building_img1)
        instance.Room_img1 = validated_data.get('Room_img1', instance.Room_img1)
        instance.Room_img2 = validated_data.get('Room_img2', instance.Room_img2)
        instance.Room_img3 = validated_data.get('Room_img3', instance.Room_img3)
        print(instance.Building_img1,instance.Room_img3,instance.House_video)

        instance.save()
        print(instance)
        return instance


class RoomSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temporary
        fields = ['state','city','district','locaton','AllowedFor','House_type']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = room
        fields = '__all__'
