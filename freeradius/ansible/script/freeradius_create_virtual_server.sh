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
server tenant_$AUTH_PORT {
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
    authorize {
	#
	#  Take a User-Name, and perform some checks on it, for spaces and other
	#  invalid characters.  If the User-Name appears invalid, reject the
	#  request.
	#
	#  See policy.d/filter for the definition of the filter_username policy.
	#
	filter_username

	#
	#  The preprocess module takes care of sanitizing some bizarre
	#  attributes in the request, and turning them into attributes
	#  which are more standard.
	#
	#  It takes care of processing the 'raddb/hints' and the
	#  'raddb/huntgroups' files.
	preprocess

	#  If you intend to use CUI and you require that the Operator-Name
	#  be set for CUI generation and you want to generate CUI also
	#  for your local clients then uncomment the operator-name
	#  below and set the operator-name for your clients in clients.conf
#       operator-name

	#
	#  If you want to generate CUI for some clients that do not
	#  send proper CUI requests, then uncomment the
	#  cui below and set "add_cui = yes" for these clients in clients.conf
#       cui

	#
	#  If you want to have a log of authentication requests,
	#  un-comment the following line, and the 'detail auth_log'
	#  section, above.
#	auth_log

	#
	#  The chap module will set 'Auth-Type := CHAP' if we are
	#  handling a CHAP request and Auth-Type has not already been set
	chap

	#
	#  If the users are logging in with an MS-CHAP-Challenge
	#  attribute for authentication, the mschap module will find
	#  the MS-CHAP-Challenge attribute, and add 'Auth-Type := MS-CHAP'
	#  to the request, which will cause the server to then use
	#  the mschap module for authentication.
	mschap

	#
	#  If you have a Cisco SIP server authenticating against
	#  FreeRADIUS, uncomment the following line, and the 'digest'
	#  line in the 'authenticate' section.
	digest

	#
	#  The WiMAX specification says that the Calling-Station-Id
	#  is 6 octets of the MAC.  This definition conflicts with
	#  RFC 3580, and all common RADIUS practices.  Un-commenting
	#  the "wimax" module here means that it will fix the
	#  Calling-Station-Id attribute to the normal format as
	#  specified in RFC 3580 Section 3.21
#	wimax

	#
	#  Look for IPASS style 'realm/', and if not found, look for
	#  '@realm', and decide whether or not to proxy, based on
	#  that.
#	IPASS

	#
	#  If you are using multiple kinds of realms, you probably
	#  want to set "ignore_null = yes" for all of them.
	#  Otherwise, when the first style of realm doesn't match,
	#  the other styles won't be checked.
	#
	suffix
#	ntdomain

	#
	#  This module takes care of EAP-MD5, EAP-TLS, and EAP-LEAP
	#  authentication.
	#
	#  It also sets the EAP-Type attribute in the request
	#  attribute list to the EAP type from the packet.
	#
	#  As of 2.0, the EAP module returns "ok" in the authorize stage
	#  for TTLS and PEAP.  In 1.x, it never returned "ok" here, so
	#  this change is compatible with older configurations.
	#
	#  The example below uses module failover to avoid querying all
	#  of the following modules if the EAP module returns "ok".
	#  Therefore, your LDAP and/or SQL servers will not be queried
	#  for the many packets that go back and forth to set up TTLS
	#  or PEAP.  The load on those servers will therefore be reduced.
	#
	eap {
		ok = return
	}

	#
	#  Pull crypt'd passwords from /etc/passwd or /etc/shadow,
	#  using the system API's to get the password.  If you want
	#  to read /etc/passwd or /etc/shadow directly, see the
	#  passwd module in radiusd.conf.
	#
#	unix

	#
	#  Read the 'users' file
	files

	#
	#  Look in an SQL database.  The schema of the database
	#  is meant to mirror the "users" file.
	#
	#  See "Authorization Queries" in sql.conf
	-sql

	#
	#  If you are using /etc/smbpasswd, and are also doing
	#  mschap authentication, the un-comment this line, and
	#  configure the 'smbpasswd' module.
#	smbpasswd

	#
	#  The ldap module reads passwords from the LDAP database.
	-ldap

	#
	#  Enforce daily limits on time spent logged in.
#	daily

	#
	expiration
	logintime

	#
	#  If no other module has claimed responsibility for
	#  authentication, then try to use PAP.  This allows the
	#  other modules listed above to add a "known good" password
	#  to the request, and to do nothing else.  The PAP module
	#  will then see that password, and use it to do PAP
	#  authentication.
	#
	#  This module should be listed last, so that the other modules
	#  get a chance to set Auth-Type for themselves.
	#
	pap

	#
	#  If "status_server = yes", then Status-Server messages are passed
	#  through the following section, and ONLY the following section.
	#  This permits you to do DB queries, for example.  If the modules
	#  listed here return "fail", then NO response is sent.
	#
#	Autz-Type Status-Server {
#
#	}
}


#  Authentication.
#
#
#  This section lists which modules are available for authentication.
#  Note that it does NOT mean 'try each module in order'.  It means
#  that a module from the 'authorize' section adds a configuration
#  attribute 'Auth-Type := FOO'.  That authentication type is then
#  used to pick the appropriate module from the list below.
#

#  In general, you SHOULD NOT set the Auth-Type attribute.  The server
#  will figure it out on its own, and will do the right thing.  The
#  most common side effect of erroneously setting the Auth-Type
#  attribute is that one authentication method will work, but the
#  others will not.
#
#  The common reasons to set the Auth-Type attribute by hand
#  is to either forcibly reject the user (Auth-Type := Reject),
#  or to or forcibly accept the user (Auth-Type := Accept).
#
#  Note that Auth-Type := Accept will NOT work with EAP.
#
#  Please do not put "unlang" configurations into the "authenticate"
#  section.  Put them in the "post-auth" section instead.  That's what
#  the post-auth section is for.
#
authenticate {
	#
	#  PAP authentication, when a back-end database listed
	#  in the 'authorize' section supplies a password.  The
	#  password can be clear-text, or encrypted.
	Auth-Type PAP {
		pap
	}

	#
	#  Most people want CHAP authentication
	#  A back-end database listed in the 'authorize' section
	#  MUST supply a CLEAR TEXT password.  Encrypted passwords
	#  won't work.
	Auth-Type CHAP {
		chap
	}

	#
	#  MSCHAP authentication.
	Auth-Type MS-CHAP {
		mschap
	}

	#
	#  If you have a Cisco SIP server authenticating against
	#  FreeRADIUS, uncomment the following line, and the 'digest'
	#  line in the 'authorize' section.
	digest

	#
	#  Pluggable Authentication Modules.
#	pam

	#  Uncomment it if you want to use ldap for authentication
	#
	#  Note that this means "check plain-text password against
	#  the ldap database", which means that EAP won't work,
	#  as it does not supply a plain-text password.
	#
	#  We do NOT recommend using this.  LDAP servers are databases.
	#  They are NOT authentication servers.  FreeRADIUS is an
	#  authentication server, and knows what to do with authentication.
	#  LDAP servers do not.
	#
#	Auth-Type LDAP {
#		ldap
#	}

	#
	#  Allow EAP authentication.
	eap

	#
	#  The older configurations sent a number of attributes in
	#  Access-Challenge packets, which wasn't strictly correct.
	#  If you want to filter out these attributes, uncomment
	#  the following lines.
	#
#	Auth-Type eap {
#		eap {
#			handled = 1
#		}
#		if (handled && (Response-Packet-Type == Access-Challenge)) {
#			attr_filter.access_challenge.post-auth
#			handled  # override the "updated" code from attr_filter
#		}
#	}
}


#
#  Pre-accounting.  Decide which accounting type to use.
#
preacct {
	preprocess

	#
	#  Merge Acct-[Input|Output]-Gigawords and Acct-[Input-Output]-Octets
	#  into a single 64bit counter Acct-[Input|Output]-Octets64.
	#
#	acct_counters64

	#
	#  Session start times are *implied* in RADIUS.
	#  The NAS never sends a "start time".  Instead, it sends
	#  a start packet, *possibly* with an Acct-Delay-Time.
	#  The server is supposed to conclude that the start time
	#  was "Acct-Delay-Time" seconds in the past.
	#
	#  The code below creates an explicit start time, which can
	#  then be used in other modules.  It will be *mostly* correct.
	#  Any errors are due to the 1-second resolution of RADIUS,
	#  and the possibility that the time on the NAS may be off.
	#
	#  The start time is: NOW - delay - session_length
	#

#	update request {
#	  	FreeRADIUS-Acct-Session-Start-Time = "%{expr: %l - %{%{Acct-Session-Time}:-0} - %{%{Acct-Delay-Time}:-0}}"
#	}


	#
	#  Ensure that we have a semi-unique identifier for every
	#  request, and many NAS boxes are broken.
	acct_unique

	#
	#  Look for IPASS-style 'realm/', and if not found, look for
	#  '@realm', and decide whether or not to proxy, based on
	#  that.
	#
	#  Accounting requests are generally proxied to the same
	#  home server as authentication requests.
#	IPASS
	suffix
#	ntdomain

	#
	#  Read the 'acct_users' file
	files
}

#
#  Accounting.  Log the accounting data.
#
accounting {
	#  Update accounting packet by adding the CUI attribute
	#  recorded from the corresponding Access-Accept
	#  use it only if your NAS boxes do not support CUI themselves
#       cui
	#
	#  Create a 'detail'ed log of the packets.
	#  Note that accounting requests which are proxied
	#  are also logged in the detail file.
	detail
#	daily

	#  Update the wtmp file
	#
	#  If you don't use "radlast", you can delete this line.
	unix

	#
	#  For Simultaneous-Use tracking.
	#
	#  Due to packet losses in the network, the data here
	#  may be incorrect.  There is little we can do about it.
#	radutmp
#	sradutmp

	#  Return an address to the IP Pool when we see a stop record.
#	main_pool

	#
	#  Log traffic to an SQL database.
	#
	#  See "Accounting queries" in sql.conf
	-sql

	#
	#  If you receive stop packets with zero session length,
	#  they will NOT be logged in the database.  The SQL module
	#  will print a message (only in debugging mode), and will
	#  return "noop".
	#
	#  You can ignore these packets by uncommenting the following
	#  three lines.  Otherwise, the server will not respond to the
	#  accounting request, and the NAS will retransmit.
	#
#	if (noop) {
#		ok
#	}

	#
	#  Instead of sending the query to the SQL server,
	#  write it into a log file.
	#
#	sql_log

	#  Cisco VoIP specific bulk accounting
#	pgsql-voip

	# For Exec-Program and Exec-Program-Wait
	exec

	#  Filter attributes from the accounting response.
	attr_filter.accounting_response

	#
	#  See "Autz-Type Status-Server" for how this works.
	#
#	Acct-Type Status-Server {
#
#	}
}


#  Session database, used for checking Simultaneous-Use. Either the radutmp
#  or rlm_sql module can handle this.
#  The rlm_sql module is *much* faster
session {
#	radutmp

	#
	#  See "Simultaneous Use Checking Queries" in sql.conf
#	sql
}


#  Post-Authentication
#  Once we KNOW that the user has been authenticated, there are
#  additional steps we can take.
post-auth {
	#  Get an address from the IP Pool.
#	main_pool


	#  Create the CUI value and add the attribute to Access-Accept.
	#  Uncomment the line below if *returning* the CUI.
#       cui

	#
	#  If you want to have a log of authentication replies,
	#  un-comment the following line, and enable the
	#  'detail reply_log' module.
#	reply_log

	#
	#  After authenticating the user, do another SQL query.
	#
	#  See "Authentication Logging Queries" in sql.conf
	-sql

	#
	#  Instead of sending the query to the SQL server,
	#  write it into a log file.
	#
#	sql_log

	#
	#  Un-comment the following if you want to modify the user's object
	#  in LDAP after a successful login.
	#
#	ldap

	# For Exec-Program and Exec-Program-Wait
	exec

	#
	#  Calculate the various WiMAX keys.  In order for this to work,
	#  you will need to define the WiMAX NAI, usually via
	#
	#	update request {
	#	       WiMAX-MN-NAI = "%{User-Name}"
	#	}
	#
	#  If you want various keys to be calculated, you will need to
	#  update the reply with "template" values.  The module will see
	#  this, and replace the template values with the correct ones
	#  taken from the cryptographic calculations.  e.g.
	#
	# 	update reply {
	#		WiMAX-FA-RK-Key = 0x00
	#		WiMAX-MSK = "%{EAP-MSK}"
	#	}
	#
	#  You may want to delete the MS-MPPE-*-Keys from the reply,
	#  as some WiMAX clients behave badly when those attributes
	#  are included.  See "raddb/modules/wimax", configuration
	#  entry "delete_mppe_keys" for more information.
	#
#	wimax


	#  If there is a client certificate (EAP-TLS, sometimes PEAP
	#  and TTLS), then some attributes are filled out after the
	#  certificate verification has been performed.  These fields
	#  MAY be available during the authentication, or they may be
	#  available only in the "post-auth" section.
	#
	#  The first set of attributes contains information about the
	#  issuing certificate which is being used.  The second
	#  contains information about the client certificate (if
	#  available).
#
#	update reply {
#	       Reply-Message += "%{TLS-Cert-Serial}"
#	       Reply-Message += "%{TLS-Cert-Expiration}"
#	       Reply-Message += "%{TLS-Cert-Subject}"
#	       Reply-Message += "%{TLS-Cert-Issuer}"
#	       Reply-Message += "%{TLS-Cert-Common-Name}"
#	       Reply-Message += "%{TLS-Cert-Subject-Alt-Name-Email}"
#
#	       Reply-Message += "%{TLS-Client-Cert-Serial}"
#	       Reply-Message += "%{TLS-Client-Cert-Expiration}"
#	       Reply-Message += "%{TLS-Client-Cert-Subject}"
#	       Reply-Message += "%{TLS-Client-Cert-Issuer}"
#	       Reply-Message += "%{TLS-Client-Cert-Common-Name}"
#	       Reply-Message += "%{TLS-Client-Cert-Subject-Alt-Name-Email}"
#	}

	#  Insert class attribute (with unique value) into response,
	#  aids matching auth and acct records, and protects against duplicate
	#  Acct-Session-Id. Note: Only works if the NAS has implemented
	#  RFC 2865 behaviour for the class attribute, AND if the NAS
	#  supports long Class attributes.  Many older or cheap NASes
	#  only support 16-octet Class attributes.
#	insert_acct_class

	#  MacSEC requires the use of EAP-Key-Name.  However, we don't
	#  want to send it for all EAP sessions.  Therefore, the EAP
	#  modules put required data into the EAP-Session-Id attribute.
	#  This attribute is never put into a request or reply packet.
	#
	#  Uncomment the next few lines to copy the required data into
	#  the EAP-Key-Name attribute
#	if (reply:EAP-Session-Id) {
#		update reply {
#			EAP-Key-Name := "%{reply:EAP-Session-Id}"
#		}
#	}

	#  Remove reply message if the response contains an EAP-Message
	remove_reply_message_if_eap

	#
	#  Access-Reject packets are sent through the REJECT sub-section of the
	#  post-auth section.
	#
	#  Add the ldap module name (or instance) if you have set
	#  'edir_account_policy_check = yes' in the ldap module configuration
	#
	Post-Auth-Type REJECT {
		# log failed authentications in SQL, too.
		-sql
		attr_filter.access_reject

		# Insert EAP-Failure message if the request was
		# rejected by policy instead of because of an
		# authentication failure
		eap

		#  Remove reply message if the response contains an EAP-Message
		remove_reply_message_if_eap
	}
}

#
#  When the server decides to proxy a request to a home server,
#  the proxied request is first passed through the pre-proxy
#  stage.  This stage can re-write the request, or decide to
#  cancel the proxy.
#
#  Only a few modules currently have this method.
#
pre-proxy {
	# Before proxing the request add an Operator-Name attribute identifying
	# if the operator-name is found for this client.
	# No need to uncomment this if you have already enabled this in
	# the authorize section.
#       operator-name

	#  The client requests the CUI by sending a CUI attribute
	#  containing one zero byte.
	#  Uncomment the line below if *requesting* the CUI.
#       cui

	#  Uncomment the following line if you want to change attributes
	#  as defined in the preproxy_users file.
#	files

	#  Uncomment the following line if you want to filter requests
	#  sent to remote servers based on the rules defined in the
	#  'attrs.pre-proxy' file.
#	attr_filter.pre-proxy

	#  If you want to have a log of packets proxied to a home
	#  server, un-comment the following line, and the
	#  'detail pre_proxy_log' section, above.
#	pre_proxy_log
}

#
#  When the server receives a reply to a request it proxied
#  to a home server, the request may be massaged here, in the
#  post-proxy stage.
#
post-proxy {

	#  If you want to have a log of replies from a home server,
	#  un-comment the following line, and the 'detail post_proxy_log'
	#  section, above.
#	post_proxy_log

	#  Uncomment the following line if you want to filter replies from
	#  remote proxies based on the rules defined in the 'attrs' file.
#	attr_filter.post-proxy

	#
	#  If you are proxying LEAP, you MUST configure the EAP
	#  module, and you MUST list it here, in the post-proxy
	#  stage.
	#
	#  You MUST also use the 'nostrip' option in the 'realm'
	#  configuration.  Otherwise, the User-Name attribute
	#  in the proxied request will not match the user name
	#  hidden inside of the EAP packet, and the end server will
	#  reject the EAP request.
	#
	eap

	#
	#  If the server tries to proxy a request and fails, then the
	#  request is processed through the modules in this section.
	#
	#  The main use of this section is to permit robust proxying
	#  of accounting packets.  The server can be configured to
	#  proxy accounting packets as part of normal processing.
	#  Then, if the home server goes down, accounting packets can
	#  be logged to a local "detail" file, for processing with
	#  radrelay.  When the home server comes back up, radrelay
	#  will read the detail file, and send the packets to the
	#  home server.
	#
	#  With this configuration, the server always responds to
	#  Accounting-Requests from the NAS, but only writes
	#  accounting packets to disk if the home server is down.
	#
#	Post-Proxy-Type Fail {
#			detail
#	}
}
}      
EOF

# Enable virtual server
sudo ln -s "$VIRTUAL_SERVER_CONF" "/etc/freeradius/3.0/sites-enabled/tenant_$AUTH_PORT"

# Restart FreeRADIUS service to apply changes
sudo systemctl restart freeradius

echo "FreeRADIUS virtual server for tenant $TENANT_IP created successfully on Auth port $AUTH_PORT and Account port $ACCT_PORT."
