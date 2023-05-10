from django.urls import path
from . import views

app_name = 'ride'
urlpatterns = [
    path('', views.login, name='login'),
    #path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.userProfile, name='profile'),
    path('rideReq/', views.ride_request, name='ride_request'),
    path('user_rideInfo/', views.user_rideInfo, name='user_rideInfo'),
    path('driver_reg/', views.driver_reg, name='driver_reg'),
    path('driverHome/', views.driverHome, name='driverHome'),
    path('driver_quit/', views.driver_quit, name='driver_quit'),
    path('vehicle_edit/', views.vehicle_edit, name='vehicle_edit'),
    path('user_rideEdit/<int:ride_id>/', views.user_rideEdit, name='user_rideEdit'),
    path('d_search_ride/', views.driver_search_ride),
    path('ride_detail/<int:ride_id>/', views.ride_detail),
    path('shareFilter/', views.shareFilter),
    #path('shareReq/', views.shareReq),
    path('shareDetail/<int:ride_id>/', views.share_detail),
    path('driver_ride/', views.driver_ride),
    path('driver_rideEdit/<int:ride_id>/', views.driver_rideEdit),
    path('driverConfirm/<int:ride_id>/', views.driverConfirm),
    path('driver_rideCancel/', views.driver_rideCancel),
    path('ride_shareCancel/<int:ride_id>/', views.shareCancel),
    path('ownerCancel/', views.ownerCancel),
    
    # path('ride/orders/', views.rideOrder, name='rideOrder'),
    #path(''),
    #path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
]