from django.shortcuts import get_object_or_404, render, redirect
from .models import Ride, UserEx, Vehicle, Sharer
from django.utils import timezone
from django.contrib.auth.models import User
from . import forms
from django.contrib import messages, auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q


@login_required
def dashboard(request):
    user = request.user
    #user_ex = UserEx.objects.get_or_create(user=request.user)
    context = {}
    context = {'user_name':user.username}
    return render(request, 'ride/dashboard.html', context)

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/ride/dashboard/')
        else:
            messages.info(request, 'user is not exist or wrong password!')
            return render(request, 'ride/login.html', locals())
    else:
        return render(request, 'ride/login.html')

        
def register(request):
    if request.method=="POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'user exist!')
                return render(request, 'ride/register.html', locals())
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'email exist!')
                    return render(request, 'ride/register.html', locals())
                else: 
                    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,last_name=last_name)
                    user.save()
                    user_ex = UserEx.objects.create(user=user)
                    user_ex.save()
                    messages.success(request, 'Registration successful!')
                    return render(request, 'ride/login.html', locals())

        else:
            messages.info(request, 'password not same!')
            return render(request, 'ride/register.html', locals())
    else:
        return render(request, 'ride/register.html')


@login_required  
def logout(request):
    auth.logout(request)
    return redirect('/ride/')

@login_required
def userProfile(request):
    # context = {}
    # user = request.user
    # if UserEx.objects.filter(user=request.user).exists():
    #     is_driver = user.userex.is_driver
    # else:
    #     user_ex = UserEx.objects.create(user=request.user)
    #     is_driver = user_ex.is_driver
        
    # if request.method == 'POST':

    #     context = {'user_name':user.username, 'user_email':user.email, 'is_driver':is_driver, 'last_name':user.last_name, 'first_name': user.first_name}
    #     #password_old = request.POST['password1']
    #     password_old = request.POST['password1']
    #     if auth.authenticate(username=request.user.username, password=password_old) is None:
    #         messages.info(request, 'Wrong user old password!')
    #         return render(request, 'ride/profile.html', context)
    #     password_new1 = request.POST['password2']
    #     password_new2 = request.POST['password3']
    #     if password_new1 != password_new2:
    #         messages.info(request, 'Two password is not the same!')
    #         return render(request, 'ride/profile.html', context) 
    #     # email = profile_form.cleaned_data.get('email')
    #     user.set_password(password_new1)
    #     # user.email = email
    #     user.save()
    #     messages.info(request, 'Changes saved!')
    #     return render(request, 'ride/profile.html', context)

    # context = {'user_name':user.username, 'user_email':user.email, 'is_driver':is_driver, 'last_name':user.last_name, 'first_name': user.first_name}
    # return render(request, 'ride/profile.html', context)
    context = {}
    user = request.user
    if UserEx.objects.filter(user=request.user).exists():
        is_driver = user.userex.is_driver
    else:
        user_ex = UserEx.objects.create(user=request.user)
        is_driver = user_ex.is_driver
        
    if request.method == 'POST':
        profile_form = forms.UserProfileForm(request.POST)
        context = {'user_name':user.username, 'user_email':user.email, 'is_driver':is_driver, 'last_name':user.last_name, 'first_name': user.first_name}
        if profile_form.is_valid():
            password_old = profile_form.cleaned_data.get('password1')
            password_new1 = profile_form.cleaned_data.get('password2')
            password_new2 = profile_form.cleaned_data.get('password3')
            email = profile_form.cleaned_data.get('email')
            if password_old != '' and (password_new1 == '' or password_new2 == ''):
                messages.info(request, 'Please input new password!')
                return render(request, 'ride/profile.html', context)
            if password_old == '' and (password_new1 != '' or password_new2 != ''):
                messages.info(request, 'Please input old password!')
                return render(request, 'ride/profile.html', context)
            if password_old != '' and password_new1 != '' and password_new2 != '':
                if auth.authenticate(username=request.user.username, password=password_old) is None:
                    messages.info(request, 'Wrong user old password!')
                    return render(request, 'ride/profile.html', context)

                if password_new1 != password_new2:
                    messages.info(request, 'Two password is not the same!')
                    return render(request, 'ride/profile.html', context)
                user.set_password(password_new1)
                 
                if email != '':    
                    if User.objects.filter(Q(email=email) & ~Q(username=request.user.username)).exists():
                        messages.info(request, 'The email address is used, please use another one!')
                        return render(request, 'ride/profile.html', context) 
                    user.email = email
                    context['user_email'] = email
            if password_old == '' and password_new1 == '' and password_new2 == '':        
                if email != '':    
                    if User.objects.filter(Q(email=email) & ~Q(username=request.user.username)).exists():
                        messages.info(request, 'The email address is used, please use another one!')
                        return render(request, 'ride/profile.html', context) 
                    user.email = email
                    context['user_email'] = email
            user.save()
            messages.info(request, 'Changes saved!')
            return render(request, 'ride/profile.html', context)
        else:
            messages.info(request, 'One your input is invalid, maybe the email do not include .com !')
            return render(request, 'ride/profile.html', context)
    # else:
    profile_form = forms.UserProfileForm()
    context = {'user_name':user.username, 'user_email':user.email, 'is_driver':is_driver, 'last_name':user.last_name, 'first_name': user.first_name}
    return render(request, 'ride/profile.html', context)

 
@login_required 
def ride_request(request):
    ride = Ride()
    context={'username':request.user.username}
    if request.method == 'POST':
        rideform = forms.RideRequestForm(request.POST)
        if rideform.is_valid():
            destination = rideform.cleaned_data['destination']
            arrival_time = rideform.cleaned_data['arrival_time']
            is_share = request.POST["is_share"]
            if arrival_time < timezone.now():
                messages.info(request, 'arrival time is invalid!')
                return render(request,'ride/rideReq.html', context)
            passenger_number = rideform.cleaned_data['passenger_number']
            if passenger_number < 1 or passenger_number > 20:
                messages.info(request, 'Passenger at least 1 or at most 20!')
                return render(request, 'ride/rideReq.html') 
            special_request = rideform.cleaned_data['special_request']
            vehicle_required = rideform.cleaned_data['vehicle_type']
            
            ride.owner = request.user
            ride.destination = destination
            ride.arrival_time = arrival_time
            ride.passenger_number = passenger_number
            ride.total_number = passenger_number
            ride.special_request = special_request
            ride.vehicle_required = vehicle_required

            if is_share == "False":
                ride.is_share = False
            else:
                ride.is_share = True
            ride.status = 'open'
            ride.save()
            messages.info(request, 'Ride request submitted!')
            return render(request, 'ride/rideReq.html', context)
        return render(request, 'ride/rideReq.html', context)
    rideform = forms.RideRequestForm()
    return render(request, 'ride/rideReq.html', context)

@login_required
def shareFilter(request):
    if request.method=='POST':
        destination = request.POST['destination']
        e_arrival = request.POST['earliest_arrival']
        l_arrival = request.POST['latest_arrival']
        passenger_num = request.POST['passenger_number']
        #ride_list = Ride.objects.filter(status='open', is_share=True, arrival_time__range=(e_arrival, l_arrival))
        ride_list = Ride.objects.filter(Q(status='open')& Q(is_share=True) & Q(arrival_time__range=(e_arrival, l_arrival)) & ~Q(owner=request.user) & ~Q(driver=request.user) & ~Q(sharers=request.user))
        results_list = []
        for ride in ride_list:
            if ride.destination == destination:
                #total_num = int(passenger_num) + ride.passenger_number
                total_num = int(passenger_num) + ride.total_number
                if total_num <= 20:
                    results_list.append(ride)
        context = {'ride_list':results_list, 'sharer_num':passenger_num}
        messages.info(request, 'results are shown below:')
        context['list_len'] = len(results_list)
        return render(request, 'ride/shareFilter.html', context)
    return render(request, 'ride/shareFilter.html')


@login_required
def share_detail(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    num = request.GET["party_num"]
    if request.method == 'POST':
        ride.sharers.add(request.user)
        ride.total_number = ride.total_number + int(num)
        sharer_e = Sharer.objects.create(user=request.user, ride=ride)
        sharer_e.party_number = num
        sharer_e.save()
        ride.save()
        # if ride.sharers.all() is not None:
        messages.info(request, 'Join Successfully!')
        return redirect('/ride/shareFilter')
    return render(request, 'ride/shareDetail.html', {'ride':ride, 'sharer_num':num})

@login_required
def user_rideInfo(request):
    owner_open_list = Ride.objects.filter(Q(owner=request.user) & Q(status='open') & ~Q(driver=request.user) & ~Q(sharers=request.user))
    owner_confirmed_list = Ride.objects.filter(Q(owner=request.user) & Q(status='confirmed') & ~Q(driver=request.user) & ~Q(sharers=request.user))
    owner_completed_list = Ride.objects.filter(Q(owner=request.user) & Q(status='completed') & ~Q(driver=request.user) & ~Q(sharers=request.user))
    sharer_open_list = Ride.objects.filter(Q(sharers=request.user) & Q(status='open') & ~Q(owner=request.user) & ~Q(driver=request.user))
    sharer_confirmed_list = Ride.objects.filter(Q(sharers=request.user) & Q(status='confirmed') & ~Q(owner=request.user) & ~Q(driver=request.user))
    sharer_completed_list = Ride.objects.filter(Q(sharers=request.user) & Q(status='completed') & ~Q(owner=request.user) & ~Q(driver=request.user))
    context = {'user':request.user,'owner_open_list':owner_open_list, 'owner_confirmed_list':owner_confirmed_list, 'owner_completed_list':owner_completed_list, 'sharer_open_list':sharer_open_list, 'sharer_confirmed_list':sharer_confirmed_list, 'sharer_completed_list':sharer_completed_list}
    # share_list_len_list = []
    # for ride in owner_open_list:
    #     share = Sharer.objects.filter(ride=ride)
    #     share_list_len_list.append(len(share))
    # context['share_list'] = share_list_len_list
    #context['share_list'] = Sharer.objects.filter(Q(ride=ride) & ~Q(user=request.user))
    return render(request, 'ride/user_rideInfo.html', context)

@login_required
def user_rideEdit(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    context = {'user':request.user,'ride': ride, 'ride_id': ride_id, 'share_list': Sharer.objects.filter(user=request.user, ride=ride)}
    
    if request.method == 'POST':
        rideEditform = forms.RideEditForm(request.POST)
        if rideEditform.is_valid():
            destination = rideEditform.cleaned_data['destination']
            arrival_time = rideEditform.cleaned_data['arrival_time']
            # destination = request.POST['destination']
            # arrival_time = request.POST['arrival_time']
            # if arrival_time < str(timezone.now()):
            #     messages.info(request, 'arrival time is invalid!')
            #     return render(request,'ride/user_rideEdit.html', context)
            # passenger_number = request.POST['passenger_number']  
            passenger_number = rideEditform.cleaned_data['passenger_number']
            if passenger_number < 1:
                messages.info(request, 'Passenger at least 1!')
                return render(request, 'ride/user_rideEdit.html')  
            if ride.passenger_number - passenger_number + ride.total_number > 20:
                messages.info(request, 'Passenger number out of range! mini bus can hold at most 20!')
                return render(request, 'ride/user_rideEdit.html')
            # special_request = request.POST['special_request']
            special_request = rideEditform.cleaned_data['special_request']
            # vehicle_required = request.POST['vehicle_required'] 
            vehicle_required = rideEditform.cleaned_data['vehicle_required']
            
            ride.destination = destination
            ride.arrival_time = arrival_time
            ride.total_number = ride.total_number - ride.passenger_number + passenger_number
            ride.passenger_number = passenger_number
            ride.special_request = special_request
            ride.vehicle_required = vehicle_required
            ride.save()
            
            context['ride_id'] = ride_id
            context['destination'] = destination
            context['arrival_time'] = arrival_time
            context['vehicle_required'] = vehicle_required
            context['passenger_number'] = passenger_number
            context['special_request'] = special_request
            messages.info(request, 'Edit Successfully!')
            email_list = []
            email_list.append(ride.owner.email)
            for sharer in Sharer.objects.filter(Q(ride=ride) & ~Q(user=request.user)):
                email_list.append(sharer.user.email)    
            send_mail(
                subject='Notice of ride changes',
                message="hi, your order to " + ride.destination + " has been changed, please login to see the changes!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=email_list,
                fail_silently=False
            )
            return render(request, 'ride/user_rideEdit.html', context)
        messages.info(request, 'One of your input is invalid! Please check the time you choose!')
        return render(request, 'ride/user_rideEdit.html', context) 
    # context = {'ride_id':ride_id, 'destination':ride.destination, 'arrival_time':ride.arrival_time, 'vehicle_type': ride.vehicle_type, 'is_share': ride.is_share, 'passenger_number': ride.passenger_number, 'special_request': ride.special_request}
    rideEditform = forms.RideEditForm()
    return render(request, 'ride/user_rideEdit.html', context)



@login_required
def driverHome(request):
    user_ex = UserEx.objects.get(user=request.user)
    if user_ex.is_driver == "false":
        return redirect('/ride/driver_reg/')
    else:
        return render(request, 'ride/driverHome.html')
 

@login_required
def driver_reg(request):
    context = {}
    user_ex = UserEx.objects.get(user=request.user)
    if Vehicle.objects.filter(owner=request.user).exists():
        user_vehicle = Vehicle.objects.get(owner=request.user)
    else:
        user_vehicle = Vehicle.objects.create(owner=request.user)
    if request.method == 'POST':
        driver_form = forms.DriverRegisterForm(request.POST)
        if driver_form.is_valid():
            vehicle_type = driver_form .cleaned_data.get('vehicle_type')
            license_number = driver_form.cleaned_data.get('license_number')
            max_capacity = driver_form.cleaned_data.get('max_capacity')
            special_info = driver_form.cleaned_data.get('special_info')
            if max_capacity < 1:
                messages.info(request, 'Passenger at least 1!')
                return render(request, 'ride/driver_reg.html')
            if max_capacity > 20:
                messages.info(request, 'Capacity at most 20!')
                return render(request, 'ride/driver_reg.html')
            user_vehicle.vehicle_type =  vehicle_type
            for vehicle in Vehicle.objects.filter(license_number=license_number):
                if vehicle.owner.username != request.user.username:
                    messages.info(request, 'Others have used the same license number!')
                    return redirect('/ride/driverHome', context)
            user_vehicle.license_number =  license_number 
            user_vehicle.max_capacity =  max_capacity
            user_vehicle.special_info =  special_info
            user_ex.is_driver = "True"
            user_ex.save()
            user_vehicle.save()
            messages.info(request, 'successfully save the edit!')
            context = {'is_driver':user_ex.is_driver}
            return redirect('/ride/driverHome', context)
            #return render(request, 'ride/driverHome.html', context)
        
        return render(request, 'ride/driver_reg.html')
    #context = {'is_driver':user.is_driver, 'user_name':request.user.username}
    driver_form = forms.DriverRegisterForm()
    return render(request, 'ride/driver_reg.html')

@login_required
def driver_quit(request):
    if Ride.objects.filter(driver=request.user, status='confirmed').exists():
        messages.info(request, 'You cannot quit as you still have onging order!')
        return render(request, 'ride/driverHome.html')
        
    user_ex = UserEx.objects.get(user=request.user)
    user_ex.is_driver = "false"
    user_ex.save()
    user_vehicle = Vehicle.objects.get(owner=request.user)
    user_vehicle.delete()
    return redirect('/ride/driverHome/')

@login_required
def vehicle_edit(request):
    context = {}
    user = request.user
    user_vehicle = Vehicle.objects.get(owner=user)
    if request.method == 'POST':
        vehicle_form = forms.VehicleForm(request.POST)
        if vehicle_form.is_valid():
            context = {'user_name':user.username, 'vehicle_type':user_vehicle.vehicle_type, 'license_number': user_vehicle.license_number, 'max_capacity': user_vehicle.max_capacity, 'special_info': user_vehicle.special_info}
            vehicle_type = vehicle_form .cleaned_data.get('vehicle_type')
            license_number = vehicle_form.cleaned_data.get('license_number')
            max_capacity = vehicle_form.cleaned_data.get('max_capacity')
            special_info = vehicle_form.cleaned_data.get('special_info')
            if Vehicle.objects.filter(Q(license_number=license_number) & ~Q(owner=request.user)).exists():
                messages.info(request, 'Others have used the same license number!')
                return render(request, 'ride/vehicle_edit.html', context)
            if vehicle_type != '':
                user_vehicle.vehicle_type = vehicle_type
            if license_number != '':
                if max_capacity < 1:
                    messages.info(request, 'Passenger at least 1!')
                    return render(request, 'ride/vehicle_edit.html', context)
                if max_capacity > 20:
                    messages.info(request, 'It is impossible to hold more than 20!')
                    return render(request, 'ride/vehicle_edit.html', context)
                user_vehicle.license_number = license_number
            if max_capacity != '':
                user_vehicle.max_capacity = max_capacity
            user_vehicle.special_info = special_info
            user_vehicle.save()
            context = {'user_name':user.username, 'vehicle_type':user_vehicle.vehicle_type, 'license_number': user_vehicle.license_number, 'max_capacity': user_vehicle.max_capacity, 'special_info': user_vehicle.special_info}
            messages.info(request, 'Changes saved!')
            return render(request, 'ride/vehicle_edit.html', context)
        else:
            context = {'user_name':user.username, 'vehicle_type':user_vehicle.vehicle_type, 'license_number': user_vehicle.license_number, 'max_capacity': user_vehicle.max_capacity, 'special_info': user_vehicle.special_info}
            return render(request, 'ride/vehicle_edit.html')
    # else:
    vehicle_form = forms.VehicleForm()
    context = {'user_name':user.username, 'user_email':user.email, 'vehicle_type':user_vehicle.vehicle_type, 'license_number': user_vehicle.license_number, 'max_capacity': user_vehicle.max_capacity, 'special_info': user_vehicle.special_info}
    return render(request, 'ride/vehicle_edit.html', context) 

@login_required
def driver_search_ride(request):
    vehicle = Vehicle.objects.get(owner=request.user)
    curr_time = timezone.now()
    ride_list = list(Ride.objects.filter(Q(status='open') & ~Q(owner=request.user) & ~Q(sharers=request.user) & Q(arrival_time__gte=curr_time)))
    result_list = []
    for ride in ride_list:
        if ride.vehicle_required == '' or ride.vehicle_required == vehicle.vehicle_type:
            if ride.special_request == '' or ride.special_request == vehicle.special_info:
                if ride.total_number <= vehicle.max_capacity:
                    result_list.append(ride)
    return render(request, 'ride/driver_search_ride.html', {'ride_list': result_list})

@login_required
def driverConfirm(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    context = {'ride': ride, 'ride_id': ride_id}
    context['share_list'] = Sharer.objects.filter(Q(ride=ride) & ~Q(user=request.user))
    if request.method=="POST":
        user_vehicle = Vehicle.objects.get(owner=request.user)
        if ride.total_number > user_vehicle.max_capacity:
            messages.info(request, 'Out of capacity, cannot take order!')
            return render(request, 'ride/ride_detail.html', context)
        ride.status = 'confirmed'
        email_list = []
        email_list.append(ride.owner.email)
        for sharer in Sharer.objects.filter(Q(ride=ride) & ~Q(user=request.user)):
            email_list.append(sharer.user.email)    
        send_mail(
            subject='Notice of ride changes',
            message='One driver has picked your order! Please see your order detail in "My rides".',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list,
            fail_silently=False
        )
        
        ride.vehicle_type = user_vehicle.vehicle_type
        ride.driver = request.user
        ride.save()
        return redirect('/ride/d_search_ride/')
    return render(request, 'ride/driverConfirm.html', context)


@login_required
def ride_detail(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    context = {'ride': ride, 'ride_id': ride_id}
    context['share_list'] = Sharer.objects.filter(ride=ride)
    return render(request, 'ride/ride_detail.html', context)

@login_required
def driver_ride(request):
    user = request.user
    driver_confirmed_list = list(Ride.objects.filter(driver=user, status='confirmed'))
    driver_completed_list = list(Ride.objects.filter(driver=user, status='completed'))
    context={'driver_confirmed_list':driver_confirmed_list, 'driver_completed_list':driver_completed_list}
    return render(request, 'ride/driver_ride.html', context)

@login_required
def driver_rideEdit(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    share_list =  Sharer.objects.filter(ride=ride)
    context = {'ride':ride, 'ride_id':ride_id, 'share_list':share_list}
    if request.method=="POST":
        user_vehicle = Vehicle.objects.get(owner=request.user)
        if ride.passenger_number > user_vehicle.max_capacity:
            messages.info(request, 'Out of capacity, cannot take order!')
            return render(request, 'ride/ride_detail.html', context)
        ride.status = 'completed'
        ride.save()
        return redirect('/ride/driver_ride/')
    return render(request, 'ride/driver_rideEdit.html', context)

@login_required
def driver_rideCancel(request):
    ride_id = request.GET['ride']
    ride = Ride.objects.get(pk=ride_id)
    email_list = []
    email_list.append(ride.owner.email)
    for sharer in Sharer.objects.filter(Q(ride=ride) & ~Q(user=request.user)):
        email_list.append(sharer.user.email)    
    send_mail(
        subject='Notice of ride changes',
        message="hi, your order to " +  ride.destination + " has been cancelled, please login to see the changes!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email_list,
        fail_silently=False
    )
    ride.driver = None
    ride.vehicle_type = ride.vehicle_required
    ride.status = 'open'
    ride.save()
    return redirect('/ride/driver_ride/')
    
@login_required
def shareCancel(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    sharer_list = list(Sharer.objects.filter(ride=ride))
    ride.sharers.set(ride.sharers.exclude(Q(username=request.user.username)))
    for sharer in sharer_list:
        if sharer.user.username == request.user.username:
            ride.total_number = ride.total_number - sharer.party_number
            sharer.delete()
    ride.save()
    return redirect('/ride/user_rideInfo/')

@login_required
def ownerCancel(request):
    ride_id = request.GET['ride']
    ride = Ride.objects.get(pk=ride_id)
    ride.delete()
    return redirect('/ride/user_rideInfo/')