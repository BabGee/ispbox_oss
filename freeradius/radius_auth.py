import radius

from tenant.models import *


from django.contrib import messages

def authenticate_radius_user(username, password, tenant_port):
    host='localhost' # change on production
    secret ='testing123' # change for production server

    r = radius.Radius(secret, host=host, port=tenant_port)

    if r.authenticate(username, password):
        print("Authentication successful!")
        return messages.SUCCESS
    else:
        print(f"Authentication failed")   
        return messages.ERROR     



def create_user_in_radcheck_file(tenant_id, username, hashed_password):
    """
    Creates a user record in a separate radcheck file for the given tenant.

    Args:
        tenant_id (int): The ID of the tenant.
        username (str): The username for the user.
        hashed_password (str): The hashed password for the user (e.g., bcrypt hash). Clear-Text Password can also be saved in this case(FreeRadius)
    """
    tenant = Tenant.objects.get(id=tenant_id)
    tenant_port=TenantPortAssignment.objects.get(tenant=tenant).port

    radcheck_file_path = f"/home/babgee/projects/SYK/django-oss/ispbox_oss/tenant_auth_files/tenant_{tenant_port}_auth.txt"

    try:
        # Open the file in append mode to add new user records
        with open(radcheck_file_path, "a") as file:
            # Write user data in a format compatible with your FreeRADIUS configuration
            # (usually username, password separated by a space)
            # file.write(f"{username} {hashed_password}\n")
            file.write(f"{username} {hashed_password}\n")

    except OSError as e:
        print(f"Error creating user in radcheck file: {e}")
       
     
