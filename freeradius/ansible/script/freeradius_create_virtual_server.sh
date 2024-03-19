#!/bin/bash

# Check if tenant IP and both ports arguments are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: sudo $0 <tenant_ip> <auth_port> <acct_port>"
    exit 1
fi

# Tenant IP and port from command line arguments
TENANT_IP="$1"
AUTH_PORT="$2"
ACCT_PORT="$3"

# Configuration file for FreeRADIUS virtual server
VIRTUAL_SERVER_CONF="/etc/freeradius/3.0/sites-available/tenant_$AUTH_PORT"

# Create virtual server configuration
sudo tee "$VIRTUAL_SERVER_CONF" > /dev/null <<EOF
server {
    listen {
        ipaddr = $TENANT_IP
        port = $AUTH_PORT
        type = auth
    }

    listen {
        ipaddr = $TENANT_IP
        port = $ACCT_PORT
        type = acct
    }
    client {
        file = /etc/freeradius/3.0/radcheckfiles/tenant_$AUTH_PORT.txt
        
    }
}
EOF

# Enable virtual server
sudo ln -s "$VIRTUAL_SERVER_CONF" "/etc/freeradius/3.0/sites-enabled/tenant_$AUTH_PORT"

# Restart FreeRADIUS service to apply changes
sudo systemctl restart freeradius

echo "FreeRADIUS virtual server for tenant $TENANT_IP created successfully on Auth port $AUTH_PORT and Account port $ACCT_PORT."
