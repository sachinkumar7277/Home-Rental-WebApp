from django.urls import path
from django.views.generic.base import RedirectView
from rent import views


urlpatterns = [

    path('home/', views.index),
    path('loginPage',views.loginpage),

    path('about/', views.About),

    path('service-providers/<str:service_type>/', views.service_providers),

    path('services/', views.services),

    path('contact/', views.ContactUs),

    path('Single_view_mess/<int:pk>', views.Single_view_mess),

    path('propertyDetail/', views.PropertyDetail),

    path('allproperty/', views.AllProperty),

    path('allmess/', views.Allmess),

    path('load-dists/',views.Districts, name='ajax_load_dists'),

    path('load-city/',views.city, name='ajax_load_city'),

    path('load-location/',views.locations, name='ajax_load_locations'),

    # path('mypost/', views.mypost),

    path('ActivateThisRoom/',views.PostActivation.as_view()),
    path('DeactivateThisRoom/',views.PostDeactivation.as_view()),

    path('validationpage/', views.ValidationPage),

    path('Validate/<int:pk>', views.Validate),
    path('ValidateMess/<int:pk>', views.ValidateMess),

    path('DeletePost/<int:pk>', views.DeletePost),

    path('deletePostvalidation/<int:pk>', views.deletePostValidation),
    path('deleteMessPostvalidation/<int:pk>', views.deletePostValidation),

    # path('apii/<int:id>/', views.JsonCBV.as_view()),

    path('Detail/<int:pk>', views.HouseDetail),

    path('RegisterMess/', views.RegisterMess,name = 'RegisterMess'),

    path('UploadHouseDetail/', views.UploadHouseDetail),
    path('UploadRoom', views.UploadRoomsViewSet.as_view({'post':'create'})),
    path('PartialUpdateRoom', views.UploadRoomsViewSet.as_view({'patch':'partial_update'})),
    path('UpdateThisRoom/<int:pk>', views.UpdateRooms),
    path('UpdateRoomMediaFile', views.RoomMediaFileUpdate.as_view({'patch':'partial_update'})),
    # path('searchRoom',views.searchRoomAPI.as_view()),
    # path('UploadRoom', views.UploadRoomsViewSet.as_view({'post': 'create'})),
    path('GetRoomData', views.RoomDataViewSet.as_view()),

    path('', RedirectView.as_view(url='home/'))

]




