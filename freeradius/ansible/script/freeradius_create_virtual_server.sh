#!/bin/bash

# Start port number
START_PORT=1812

# Check if port argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <tenant_port>"
    exit 1
fi

# Input port
TENANT_PORT=$1

# Calculate tenant IP based on provided port
# Starting from 1812 and incrementing by 1 for each port
IP_LAST_OCTET=$((TENANT_PORT - START_PORT + 1))
TENANT_IP="10.0.0.$IP_LAST_OCTET"

# Configuration file for FreeRADIUS virtual server
VIRTUAL_SERVER_CONF="/etc/freeradius/3.0/sites-available/tenant_$TENANT_IP"

# Create virtual server configuration
cat << EOF > "$VIRTUAL_SERVER_CONF"
server {
    listen {
        ipaddr = $TENANT_IP
        tenant_port = $TENANT_PORT
    }
    ...
    # Add more configurations as needed
}
EOF

# Enable virtual server
ln -s "$VIRTUAL_SERVER_CONF" "/etc/freeradius/3.0/sites-enabled/tenant_$TENANT_IP"

# Restart FreeRADIUS service to apply changes
systemctl restart freeradius

echo "FreeRADIUS virtual server for tenant $TENANT_IP created successfully on port $TENANT_PORT."
