from django.contrib import admin
from user.models import *



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tenant', 'access_level', 'status') 
    list_filter = ('user','tenant', 'access_level', 'status')  

admin.site.register(Profile, ProfileAdmin)

class ProfileStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')   

admin.site.register(ProfileStatus, ProfileStatusAdmin)

class AccessLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  

admin.site.register(AccessLevel, AccessLevelAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number') 
    list_filter = ('first_name','last_name', 'email', 'phone_number')  

admin.site.register(User, UserAdmin)


