import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CreateFreeRADIUSVirtualServerView(APIView):
    def post(self, request):
        tenant_ip = request.data.get('tenant_ip')
        tenant_port = request.data.get('tenant_port')

        # Call Ansible playbook to create FreeRADIUS virtual server
        # ansible_command = [
        #     'ansible',
        #     'create_freeradius_virtual_server.yml',
        #     '--extra-vars', f'tenant_ip={tenant_ip} port={port}'
        # ]
        print("HERE 1")
        ansible_command = [
        'ansible-playbook',
        'freeradius/ansible/create_virtual_server.yml',
        '-i', 'localhost,',
        '--extra-vars', f'tenant_ip={tenant_ip} tenant_port={tenant_port}'
        ]
        print("HERE 2")
        # try:
        #     process = subprocess.Popen(ansible_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #     stdout, stderr = process.communicate()
        #     print("HERE 3")
        #     print(f'Process Code: {process.returncode}')        
        #     if process.returncode != 0:
        #         print("HERE 4")
        #         raise Exception(stderr.decode('utf-8'))        
        #     return Response({'message': 'FreeRADIUS virtual server created successfully'}, status=status.HTTP_200_OK)
        # except Exception as e:
        #     print("HERE 5")        
        #     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            subprocess.check_call(ansible_command)
        except subprocess.CalledProcessError as e:
            # Handle the error here
            print("An error occurred:")