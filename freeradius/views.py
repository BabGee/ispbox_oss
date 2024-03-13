import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CreateFreeRADIUSVirtualServerView(APIView):
    def post(self, request, tenant_data=None):
                print(request.data)
                if request.data:
                     tenant_data = request.data.get('tenant_data')
                print(f'Tenant DATA: {tenant_data}')
                if tenant_data:
                    tenant_ip = tenant_data['ip_address']
                    auth_port = tenant_data['freeradius_auth_port']
                    acct_port = tenant_data['freeradius_acct_port']        

                    # Call Ansible playbook to create FreeRADIUS virtual server
                    ansible_command = [
                    'ansible-playbook',
                    'freeradius/ansible/create_virtual_server.yml',
                    '-i', 'localhost,',
                    '--extra-vars', f'tenant_ip={tenant_ip} auth_port={auth_port} acct_port={acct_port}'
                    ]
                    try:
                        subprocess.check_call(ansible_command)
                        return Response({'message': 'FreeRADIUS virtual server created successfully'}, status=status.HTTP_200_OK)
                    except subprocess.CalledProcessError as e:
                        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                    
                    
                else:
                    # Handle missing data
                    return Response({'message': 'Error: Tenant data not found'}, status=400) 
                   