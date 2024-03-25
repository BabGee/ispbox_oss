# from radius import RadiusClient

# def authenticate_radius_user(username, password, tenant_port):
#     # Replace with your FreeRADIUS server details
#     server_address = "127.0.0.1:8000"
#     server_secret = "testing123"

#     # Create a RadiusClient instance
#     client = RadiusClient(server_address, server_secret, auth_port=tenant_port)  # Tenant RADIUS auth port

#     # Build the authentication request packet
#     auth_packet = client.auth_packet(
#         code=client.CODE_ACCESS_REQUEST,
#         User_Name=username,
#         NAS_Port=tenant_port  # Include tenant's port
#     )

#     # Send the authentication request and receive the response
#     response = client.send(auth_packet)

#     # Check the response code for success
#     if response.code == client.CODE_ACCESS_ACCEPT:
#         print("Authentication successful!")
#     else:
#         print(f"Authentication failed: Code {response.code}")


import radius

import os
from tenant.models import *


from django.contrib import messages

# def authenticate_radius_user(username, password, tenant_port):
#     secret = 'testing123'
#     host='localhost'
#     print("HERE 2")

#     r = radius.Radius(secret, host=host, port=tenant_port)
#     print(f"HERE 3: {r}")

#     if r.authenticate(username, password):
#         print("HERE 4")
#         print("Authentication successful!")
#     else:
#         print("HERE 5")
#         print(f"Authentication failed")

def authenticate_radius_user(username, password, tenant_port):
    host='localhost'
    secret ='testing123'
    print("HERE 2")

    r = radius.Radius(secret, host=host, port=tenant_port)
    print(f"HERE 3: {r}")

    if r.authenticate(username, password):
        print("HERE 4")
        print("Authentication successful!")
        return messages.SUCCESS
    else:
        print("HERE 5")
        print(f"Authentication failed")   
        return messages.ERROR     



def create_user_in_radcheck_file(tenant_id, username, hashed_password):
    """
    Creates a user record in a separate radcheck file for the given tenant.

    Args:
        tenant_id (int): The ID of the tenant.
        username (str): The username for the user.
        hashed_password (str): The hashed password for the user (e.g., bcrypt hash).
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
       
     
