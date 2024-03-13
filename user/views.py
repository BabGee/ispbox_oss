from django.shortcuts import render, redirect

from . import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# from django.views.generic import CreateView
#from django.views.generic import View

from django.contrib.auth import get_user_model, logout

from django.contrib.auth import login, authenticate

from user.models import *
from tenant.models import *

from django.contrib.auth.forms import AuthenticationForm   

from django.db import transaction

from freeradius.views import *

User = get_user_model()

def tenant_signup_view(request):
	if request.method == 'POST':
		tenant_data = {}
		tenant_data['ip_address'] = '127.0.0.1'
		form = forms.TenantSignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.first_name = form.cleaned_data.get('first_name')
			user.last_name = form.cleaned_data.get('last_name')
			user.email = form.cleaned_data.get('email')
			user.phone_number = form.cleaned_data.get('phone_number')
			user.save()

			tenant_name = form.cleaned_data.get('tenant_name')
			tenant_location = form.cleaned_data.get('tenant_location')
			tenant = Tenant.objects.create(name=tenant_name, location=tenant_location)
			tenant.status = TenantStatus.objects.get(name="ACTIVE")
			tenant.save()
			# update Profile with Tenant, access level, status
			profile = Profile.objects.get(user=user)
			profile.tenant = tenant
			profile.access_level = AccessLevel.objects.get(name='ADMINISTRATOR')
			profile.status = ProfileStatus.objects.get(name='ACTIVATED')
			profile.save()

			with transaction.atomic():
				# Find two consecutive available ports
				available_ports = Port.objects.filter(is_allocated=False).order_by('port_number')[:2]

				if available_ports.count() == 2:
					assigned_ports = []
					for port in available_ports:
						port.is_allocated = True
						port.save()
						assigned_ports.append(port.port_number)

						# Assign specific purpose (optional)
						if port.port_number == assigned_ports[0]:
							tenant_data['freeradius_auth_port'] = port.port_number
						else:
							tenant_data['freeradius_acct_port'] = port.port_number

					TenantPortAssignment.objects.create(
						tenant=tenant, 
						port=available_ports[0]  # Assign first port to the main relationship
					)
					# Call CreateFreeRADIUSVirtualServerView with tenant_data
					view = CreateFreeRADIUSVirtualServerView()
					response = view.dispatch(request=request, tenant_data=tenant_data)
					print(f'RESPONSE AFTER ANSIBLE: {response.status_code}')

					# Handle the response from CreateFreeRADIUSVirtualServerView
					if response.status_code == 200:
						print("Success Ansible Automation")
						pass
					else:
						print("Failed Ansible Automation")
						pass

			#login user
			login(request, user)
			return redirect('index')

	else:
		form = forms.TenantSignUpForm()

	context = {
		'form':form
	}

	return render(request, 'user/tenant_register.html', context)			


# def customer_signup_view(request):
# 	if request.method == 'POST':
# 		form = forms.CustomerSighUpForm(request.POST)
# 		if form.is_valid():
# 			user = form.save(commit=False)
# 			user.is_farmer = True
# 			user.first_name = form.cleaned_data.get('first_name')
# 			user.last_name = form.cleaned_data.get('last_name')
# 			user.email = form.cleaned_data.get('email')
# 			user.phone_number = form.cleaned_data.get('phone_number')
# 			user.save()
# 			farmer = Farmer.objects.create(user=user)
# 			farmer.farm_name = form.cleaned_data.get('farm_name')
# 			farmer.location = form.cleaned_data.get('location')
# 			farmer.save()
# 			username = form.cleaned_data.get('username')
# 			messages.success(request, f'Account created for {username}. You can now login')
# 			return redirect('farmer-login')

# 	else:
# 		form = forms.FarmerSignUpForm()

# 	context = {
# 		'form':form
# 	}

# 	return render(request, 'user/farmerregister.html', context)



		

def tenant_login(request):
	form = AuthenticationForm()
	if request.method == 'POST':  
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_authenticated:
				login(request, user)
				return redirect('index') # TEnant Portal
			# elif user.is_authenticated and user.is_farmer:
			# 	messages.warning(request, 'Kindly login as farmer')
			# 	return redirect('farmer-login')
			# elif user.is_authenticated and user.is_student:
			# 	messages.warning(request, 'Kindly login as student')
			# 	return redirect('student-login')
				    
		else:
			messages.error(request, 'invalid Credentials')
    
	return render(request, 'user/tenant_login.html', {'form':form})

# def customer_login(request):
# 	form = AuthenticationForm()
# 	if request.method == 'POST':  
# 		username = request.POST['username']
# 		password = request.POST['password']
# 		user = authenticate(username=username, password=password)
# 		if user is not None:
# 			if user.is_authenticated and user.is_farmer:
# 				login(request, user)
# 				return redirect('farmer-portal')
# 			elif user.is_authenticated and user.is_vet_officer:
# 				messages.warning(request, 'Kindly login as Vet Officer')
# 				return redirect('vet-login')
# 			# elif user.is_authenticated and user.is_student:
# 			# 	messages.warning(request, 'Kindly login as student')
# 			# 	return redirect('student-login')
				    
# 		else:
#  			messages.error(request, 'invalid Credentials')
    
# 	return render(request, 'user/farmerlogin.html', {'form':form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('landing_page')