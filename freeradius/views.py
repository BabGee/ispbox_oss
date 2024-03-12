import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CreateFreeRADIUSVirtualServerView(APIView):
    def post(self, request):
        tenant_ip = request.data.get('tenant_ip')
        tenant_port = request.data.get('tenant_port')

        # Call Ansible playbook to create FreeRADIUS virtual server
        ansible_command = [
        'ansible-playbook',
        'freeradius/ansible/create_virtual_server.yml',
        '-i', 'localhost,',
        '--extra-vars', f'tenant_ip={tenant_ip} tenant_port={tenant_port}'
        ]

        try:
            subprocess.check_call(ansible_command)
            return Response({'message': 'FreeRADIUS virtual server created successfully'}, status=status.HTTP_200_OK)
        except subprocess.CalledProcessError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)