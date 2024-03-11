from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# from tenant.models import *


User = get_user_model()

class TenantSignUpForm(UserCreationForm):
	first_name = forms.CharField(
		max_length=50,
		min_length=4,
		required=True,
		widget=forms.TextInput(
				attrs={
					'placeholder': 'First Name',
					'class': 'form-control'
				}
			)
		)
	last_name = forms.CharField(
		max_length=30,
		required=True,
		widget=forms.TextInput(
				attrs={
					'placeholder': 'Last Name',
					'class': 'form-control'
				}
			)
		)
		
	email = forms.EmailField(
		max_length=254,
		widget=forms.EmailInput(
			attrs={
				'placeholder': 'Email',
				'class': 'form-control'
			}
		)
	)
	phone_number = forms.RegexField(regex='^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', max_length=13)

	tenant_name = forms.CharField(
		max_length=30,
		required=True,
		widget=forms.TextInput(
				attrs={
					'placeholder': 'Business Name',
					'class': 'form-control'
				}
			)
		)	
	
	tenant_location = forms.CharField(
		max_length=30,
		required=True,
		widget=forms.TextInput(
				attrs={
					'placeholder': 'Business Location',
					'class': 'form-control'
				}
			)
		)	
	
	password1 = forms.CharField(
		label='Password',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				'placeholder': 'Password',
				'class': 'form-control'
			}
		)
	)

	password2 = forms.CharField(
		label='Confirm Password',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				'placeholder': 'Confirm Password',
				'class': 'form-control'
			}
		)
	)
	
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ('username','first_name','last_name','phone_number','email','tenant_name', 'tenant_location','password1', 'password2',)

	
# class CustomerSignUpForm(UserCreationForm):
# 	first_name = forms.CharField(
# 		max_length=50,
# 		min_length=4,
# 		required=True,
# 		widget=forms.TextInput(
# 				attrs={
# 					'placeholder': 'First Name',
# 					'class': 'form-control'
# 				}
# 			)
# 		)
# 	last_name = forms.CharField(
# 		max_length=30,
# 		required=True,
# 		widget=forms.TextInput(
# 				attrs={
# 					'placeholder': 'Last Name',
# 					'class': 'form-control'
# 				}
# 			)
# 		)
# 	email = forms.EmailField()
# 	phone_number = forms.RegexField(regex='^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', max_length=13)
# 	tenant = forms.ModelChoiceField(queryset=Tenant.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
# 	password1 = forms.CharField(
# 		label='Password',
# 		max_length=30,
# 		min_length=8,
# 		required=True,
# 		widget=forms.PasswordInput(
# 			attrs={
# 				'placeholder': 'Password',
# 				'class': 'form-control'
# 			}
# 		)
# 	)

# 	password2 = forms.CharField(
# 		label='Confirm Password',
# 		max_length=30,
# 		min_length=8,
# 		required=True,
# 		widget=forms.PasswordInput(
# 			attrs={
# 				'placeholder': 'Confirm Password',
# 				'class': 'form-control'
# 			}
# 		)
# 	)


# 	class Meta(UserCreationForm.Meta):
# 		model = User
# 		fields = ['username','first_name','last_name','tenant','email', 'location','password1', 'password2']
			

