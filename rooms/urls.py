from django.urls import path
from . import views

app_name="rooms"

urlpatterns = [
    path("create/", views.CreateRoomView, name='create'),
    path('<int:pk>/update/',views.UpdateRoomView, name='update'),
    path('<int:pk>/',views.RoomDetail, name='detail'),
    path('search/', views.SearchView, name='search'),
    # path('search/room_result/',views.result, name='result'),
    # path('room_result/',views.result, name='result')

]