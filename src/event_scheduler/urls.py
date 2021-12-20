from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django_rest_passwordreset.views import ResetPasswordValidateTokenViewSet, ResetPasswordConfirmViewSet, \
    ResetPasswordRequestTokenViewSet

from event_scheduler import views
from django.contrib.auth import views as auth_views
from djreservation import urls as djreservation_urls
from django.conf.urls import url
from django.urls import path, re_path, include
from .views import reservation_create_view, reservation_detail_view, reservation_list_view, reservation_update_view, reservation_delete_view,user_create_view,user_login_view,user_logout

app_name = 'event_scheduler'
router = DefaultRouter()

router.register('profile',views.UserProfileViewSet)
router.register('booking',views.UserBookingItemViewSet)
router.register('meetingroom',views.RoomViewSet)
router.register(
    r'passwordreset/validate_token',
    ResetPasswordValidateTokenViewSet,
    basename='reset-password-validate'
)
router.register(
    r'passwordreset/confirm',
    ResetPasswordConfirmViewSet,
    basename='reset-password-confirm'
)
router.register(
    r'passwordreset',
    ResetPasswordRequestTokenViewSet,
    basename='reset-password-request'
)
urlpatterns = [
    path('', reservation_list_view, name='reservation-list'),
    path('<int:id>/', reservation_detail_view, name='BookingItem-details'),
    path('<int:id>/update/',
         reservation_update_view, name='reservation-update'),
    path('<int:id>/delete/',
         reservation_delete_view, name='reservation-delete'),
    path('create/', reservation_create_view, name='reservation-create'),
    path('create_user/', user_create_view, name='user-create'),
    path('login/', user_login_view, name='user_login_view'),
    path('logout/', user_logout, name='logout'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('django.contrib.auth.urls')),
    
] 