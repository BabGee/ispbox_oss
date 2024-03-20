import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from freeradius.utils import generate_random_string, generate_random_password

from freeradius.radius_auth import *

import bcrypt

class CreateFreeRADIUSVirtualServerView(APIView):
    playbook_path = 'freeradius/ansible/create_virtual_server.yml'

    def post(self, request):
        tenant_data = request.data.get('payload')

        if not tenant_data:
            return Response({'message': 'Error: Tenant data not found'}, status=status.HTTP_400_BAD_REQUEST)

        ip_address = tenant_data.get('ip_address')
        auth_port = tenant_data.get('freeradius_auth_port')
        acct_port = tenant_data.get('freeradius_acct_port')

        if not all([ip_address, auth_port, acct_port]):
            return Response({'message': 'Error: Incomplete tenant data'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            self._run_ansible_playbook(ip_address, auth_port, acct_port)
            return Response({'message': 'FreeRADIUS virtual server created successfully'}, status=status.HTTP_200_OK)
        except subprocess.CalledProcessError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _run_ansible_playbook(self, ip_address, auth_port, acct_port):
        ansible_command = [
            'ansible-playbook',
            self.playbook_path,
            '-i', 'localhost,',
            '--extra-vars', f'tenant_ip={ip_address} auth_port={auth_port} acct_port={acct_port}'
        ]
        subprocess.check_call(ansible_command)




class CreateUserInRadcheckView(APIView):
    """
    API endpoint to create a user in the radcheck file for a tenant upon payment confirmation.
    """

    def post(self, request, tenant_id=None):
        """
        Handle POST requests for creating a user.
        """
        if tenant_id is None:
            # Handle error or return appropriate response if tenant_id is missing
            return Response({'status': 'error', 'message': 'Missing tenant ID'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Extract username from request data (optional)
            username = request.data.get('username')
            # If username not provided, generate a unique one
            if not username:
                username = f"tenant_{tenant_id}_{generate_random_string(8)}"

            # Generate a strong, random password
            password = generate_random_password()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Create user record in separate radcheck file for the tenant
            create_user_in_radcheck_file(tenant_id, username, hashed_password)

            # Optionally, persist user information in your radcheck table if needed
            # user = User.objects.create(username=username, tenant_id=tenant_id, password=hashed_password)

            return Response({'status': 'success', 'message': 'User created successfully', 'username': username, 'password': password})
        except Exception as e:
            return Response({'status': 'error', 'message': f"Error creating user: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LoginWithFreeRADIUSView(APIView):
    """
    API endpoint for user login using FreeRADIUS authentication.
    """

    def post(self, request):
        """
        Handle POST requests for user login.
        """

        username = request.data.get('username')
        password = request.data.get('password')
        tenant_port = request.data.get('tenant_port')

        if not username or not password:
            return Response({'status': 'error', 'message': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print("HERE 1")
            auth_result = authenticate_radius_user(username, password, tenant_port)

            if auth_result.code == 'Access-Accept':
                # Successful authentication
                return Response({'status': 'success', 'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'status': 'error', 'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'status': 'error', 'message': f"Error authenticating user: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











# from django.http import JsonResponse
# from django.views import View
# from pyrad.client import Client
# from pyrad.dictionary import Dictionary
# from pyrad.packet import AccessRequest

# class RadiusAuthView(View):
#     def post(self, request):
#         # Get user credentials from request data
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # RADIUS server configuration
#         radius_server = "radius.example.com"
#         radius_secret = "radius_secret"

#         # Create a RADIUS client
#         radius_client = Client(server=radius_server, secret=radius_secret, dict=Dictionary("/path/to/dictionary"))

#         # Create an Access-Request packet
#         access_request = radius_client.CreateAuthPacket(code=1)
#         access_request["User-Name"] = username
#         access_request["User-Password"] = password

#         try:
#             # Send the Access-Request packet to the RADIUS server
#             radius_client.SendPacket(access_request)

#             # Wait for a response from the server
#             response = radius_client.ReceivePacket()

#             if response is not None:
#                 if response.code == 2:  # Access-Accept
#                     return JsonResponse({"authenticated": True})
#                 elif response.code == 3:  # Access-Reject
#                     return JsonResponse({"authenticated": False, "message": response.get_reply_message()})
#                 else:
#                     return JsonResponse({"error": "Unexpected response code: " + str(response.code)})
#             else:
#                 return JsonResponse({"error": "No response received from RADIUS server"})

#         except Exception as e:
#             return JsonResponse({"error": "Error occurred during authentication: " + str(e)})



