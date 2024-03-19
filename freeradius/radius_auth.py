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

def authenticate_radius_user(username, password, tenant_port):
    secret = 'testing123'
    host='radius'

    r = radius.Radius(secret, host=host, port=tenant_port)

    if r.authenticate(username, password):
        print("Authentication successful!")
    else:
        print(f"Authentication failed")
     
