from django.urls import path

from . import views  #引入视图

urlpatterns = [
    #path('loginCheck',views.loginCheck ,name='loginCheck'),
    path('freeRoomList', views.freeRoomList, name='freeRoomList'),
    path('openRoom', views.openRoom, name='openRoom'),
    path('closeRoom', views.closeRoom, name='closeRoom'),
    path('getBill', views.getBill, name='getBill'),
    path('getDetail', views.getDetail, name='getDetail'),
    path('getRoomsData', views.getRoomsData, name='getRoomsData'),
    #path('openRoom',views.openRoom,name='openRoom'),
    #path('')

    path('getReporter', views.getReporter, name='getReporter'),
]


