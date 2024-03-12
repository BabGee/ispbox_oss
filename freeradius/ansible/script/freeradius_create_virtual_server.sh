#!/bin/bash

# Start port number
START_PORT=1812

# Check if tenant IP and port arguments are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: sudo $0 <tenant_ip> <tenant_port>"
    exit 1
fi

# Tenant IP and port from command line arguments
TENANT_IP="$1"
TENANT_PORT="$2"

# Configuration file for FreeRADIUS virtual server
VIRTUAL_SERVER_CONF="/etc/freeradius/3.0/sites-available/tenant_$TENANT_PORT"

# Create virtual server configuration
sudo tee "$VIRTUAL_SERVER_CONF" > /dev/null <<EOF
server {
    listen {
        ipaddr = $TENANT_IP
        port = $TENANT_PORT
        type = auth
    }

    listen {
        ipaddr = $TENANT_IP
        port = $((TENANT_PORT + 1))
        type = acct
    }
    ...
    # Add more configurations
}
EOF

# Enable virtual server
sudo ln -s "$VIRTUAL_SERVER_CONF" "/etc/freeradius/3.0/sites-enabled/tenant_$TENANT_PORT"

# Restart FreeRADIUS service to apply changes
sudo systemctl restart freeradius

echo "FreeRADIUS virtual server for tenant $TENANT_IP created successfully on port $TENANT_PORT."
