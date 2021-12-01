from django.urls import path
from .views import room_detail_view, room_list_view, room_update_view, room_delete_view, room_create_view


urlpatterns = [
    path('', room_list_view, name='room-list'),
    path('<int:room_number>/', room_detail_view, name='room-details'),
    path('<int:room_number>/update/',
         room_update_view, name='room-update'),
    path('<int:room_number>/delete/',
         room_delete_view, name='room-delete'),
    path('create/', room_create_view, name='room-create'),
]