from django import forms
from .models import Ride


class RegisterForm(forms.Form):
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="last_name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="first_name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="password2", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={'class': 'form-control'}))


class UserProfileForm(forms.Form):
    password1 = forms.CharField(label="password_old", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    password2 = forms.CharField(label="password_new", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    password3 = forms.CharField(label="password_new again", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)
    #is_driver = forms.CharField(label="is_driver", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    
class RideRequestForm(forms.Form):
    destination = forms.CharField(label="destination", max_length=128)
    arrival_time = forms.DateTimeField(label="arrival_time")
    passenger_number = forms.IntegerField(label="passenger_number")
    #is_share = forms.BooleanField(label="is_share")
    special_request = forms.CharField(label="special_request", max_length=200, required=False)
    vehicle_type = forms.CharField(label="vehivle_type", required=False)    

class RideEditForm(forms.Form):
    destination = forms.CharField(label="destination", max_length=128)
    arrival_time = forms.DateTimeField(label="arrival_time")
    passenger_number = forms.IntegerField(label="passenger_number")
    #is_share = forms.BooleanField(label="is_share")
    special_request = forms.CharField(label="special_request", max_length=200, required=False)
    vehicle_required = forms.CharField(label="vehivle_required", required=False)


class DriverRegisterForm(forms.Form):
    #driver_name = forms.CharField(label="driver_name", max_length=128)
    vehicle_type = forms.CharField(label="vehicle_type", max_length=128)
    license_number = forms.CharField(label="license_number", max_length=128)
    max_capacity = forms.IntegerField(label="max_capacity")
    special_info = forms.CharField(label="special_info", max_length=128, required=False)
 
# class DriverForm(forms.Form):
#     driver = User
#     ride = Ride
#     class Meta:
#         model = Driver
#         fields = ['driver', 'ride']


class VehicleForm(forms.Form):
    vehicle_type = forms.CharField(label="vehicle_type", max_length=128, required=False)
    license_number = forms.CharField(label="license_number", max_length=128, required=False)
    max_capacity = forms.IntegerField(label="max_capacity", required=False)
    special_info = forms.CharField(label="special_info", max_length=128, required=False)