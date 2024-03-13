import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
