#!/usr/local/bin/python3

# author: jason mueller
# created: 2018-12-26
# last modified: 2018-01-26

# purpose:
# common functions I have used over the years when Python scripting against 
# networking equipment
# original dates are lost to time, so added dates when added to this module

# usage:
# use at your own risk
# there are no explicit or implied warranties or guarantees

# python version: 3.7.2


import socket


# is_ipv4_format
# verify supplied string is valid IPv4 address format
#   All IPv4 addresses from 0.0.0.0 through 255.255.255.255 are true
# returns: True or False
# created: 2019-01-05
# last modified: 2019-01-26
def is_ipv4_format(candidate):
    is_ipv4 = True            

    try:
        octets = list(map(int, candidate.split('.')))

        # verify IP address contains four components
        if len(octets) != 4:
            is_ipv4 = False

        # verify values are integer versions of binary octets in candidate IP
        else:
            for octet in octets:
                if (octet < 0 or octet > 255):
                    is_ipv4 = False
    except:
        is_ipv4 = False
        
    return is_ipv4



# verify a supplied string can be used as a valid IPv4 subnet mask
#   can verify cidr-based mask
#   or decimal mask of four octets
# returns: True or False
# created: 2018-12-29
# last modified: 2019-01-27
def valid_ipv4_mask(candidate):
    valid_mask = True
    
    # list of decimal octet values with contiguous set of binary ones
    valid_octets = [0, 128, 192, 224, 240, 248, 252, 254, 255]
    
    try:
        # create list of integers from provided mask string
        mask_components = list(map(int, candidate.split('.')))
        
        # verify number of bits in cidr-style mask
        if len(mask_components) == 1:
            if (mask_components[0] < 0 or mask_components[0] > 32):
                valid_mask = False
        
        # verify octets in a decimal style mask
        elif len(mask_components) == 4:        
            # verify individual octet allowed value (contiguous ones within octet)
            for octet in mask_components:
                invalid_octet = True
                if octet in valid_octets:
                    invalid_octet = False
                if invalid_octet:
                    valid_mask = False

            # verify contiguous ones for the entire decimal mask
            if valid_mask:
                if (mask_components[0] < 255):
                    if (mask_components[1] > 0 or mask_components[2] > 0 
                        or mask_components[3] > 0):
                        valid_mask = False
                if (mask_components[0] == 255 and mask_components[1] < 255):
                    if (mask_components[2] > 0 or mask_components[3] > 0):
                        valid_mask = False
                if (mask_components[0] == 255 and mask_components[1] == 255
                    and mask_components[2] < 255):
                    if (mask_components[3] > 0):
                        valid_mask = False

        else:
            valid_mask = False

    except:
        valid_mask = False

    return valid_mask



# convert cidr bit length mask to ipv4 decimal mask (input can be string or int)
# returns: decimal mask string or None
# created: 2019-01-05
# last modified: 2019-01-05
def cidr_to_dec_mask(cidr_mask):

    # dictionary of cidr bits : decimal mask relationships
    cidr_to_dec = {
        0:'0.0.0.0',1:'128.0.0.0',2:'192.0.0.0',3:'224.0.0.0',4:'240.0.0.0',
        5:'248.0.0.0',6:'252.0.0.0',7:'254.0.0.0',8:'255.0.0.0',
        9:'255.128.0.0',10:'255.192.0.0',11:'255.224.0.0',12:'255.240.0.0',
        13:'255.248.0.0',14:'255.252.0.0',15:'255.254.0.0',16:'255.255.0.0',
        17:'255.255.128.0',18:'255.255.192.0',19:'255.255.224.0',20:'255.255.240.0',
        21:'255.255.248.0',22:'255.255.252.0',23:'255.255.254.0',24:'255.255.255.0',
        25:'255.255.255.128',26:'255.255.255.192',27:'255.255.255.224',28:'255.255.255.240',
        29:'255.255.255.248',30:'255.255.255.252',31:'255.255.255.254',32:'255.255.255.255'
        }
    
    try:
        dec_mask = cidr_to_dec[int(cidr_mask)]

    except:
        dec_mask = None
    
    return dec_mask



# valid_ipv4_unicast
# purpose: verify supplied string is a valid IPv4 unicast *destination* address
#   verifies address is not in some reserved ranges not common in production or testing
#   comment or uncomment preferred reserved address checks per your preference
# returns: True or False
# created: 2018-12-28
# last modified: 2019-01-27
def valid_ipv4_unicast(candidate):
    valid_unicast = True            

    try:
        octets = list(map(int, candidate.split('.')))
        # verify supplied string conforms to IPv4 format

        valid_unicast = is_ipv4_format(candidate)

        # octet value checks
        if valid_unicast:
            # verify first octet is not multicast or experimental (also catches broadcast)
            if (octets[0] > 223):
                valid_unicast = False

            # select reserved address checks follow
            # comment or uncomment as you see fit
            
            # verify not "host on this network"; only valid as source (RFC 1122)
            if octets[0] == 0:
                valid_unicast = False
            
            # verify not loopback (RFC 1122); sometimes used in testing
            #if octets[0] == 127:
            #    valid_unicast = False
            
            # verify not self-assigned IP (RFC 3927)
            if (octets[0] == 169 and octets[1] == 254):
                valid_unicast = False

            # verify not reserved space for IETF protocol assignment (RFC 6890)
            if (octets[0] == 192 and octets[1] == 0 and octets[2] == 0):
                valid_unicast = False                
            
            # verify not automatic multicast tunneling (RFC 7450)
            if (octets[0] == 192 and octets[1] == 52 and octets[2] == 193):
                valid_unicast = False                
            
            # verify not AS 112 DNS redirection (RFC 7535)
            if (octets[0] == 192 and octets[1] == 31 and octets[2] == 196):
                valid_unicast = False                

            # verify not AS 112 DNS service (RFC 7534)
            if (octets[0] == 192 and octets[1] == 175 and octets[2] == 48):
                valid_unicast = False                
            
            # verify not 6to4 relay anycast (RFC 3068)
            if (octets[0] == 192 and octets[1] == 88 and octets[2] == 99):
                valid_unicast = False                
            
    except:
        valid_unicast = False

    return valid_unicast



# is_ipv4_mcast
# verify supplied string is valid IPv4 multicast address
# returns: True or False
# created: 2019-01-26
# last modified: 2019-01-27
def is_ipv4_mcast(candidate):
    is_mcast = True            

    try:
        # verify supplied string conforms to IPv4 format
        is_mcast = is_ipv4_format(candidate)

        if is_mcast:
            octets = list(map(int, candidate.split('.')))

            # verify first octet valid multicast value
            if (octets[0] < 224 or octets[0] > 239):
                    is_mcast = False
    except:
        is_mcast = False
        
    return is_mcast



# is_ipv4_range
# verify supplied start and end IPv4 addresses are a valid range of unicast IP addresses
#   note: there is no check if the range crosses reserved address space
# returns: True or False
# created: 2019-01-07
# last modified: 2019-01-26
def is_ipv4_range(start_ip, end_ip):
    valid_range = False
    
    try:
        start_valid = valid_ipv4_unicast(start_ip)
        end_valid = valid_ipv4_unicast(end_ip)
                
        if (start_valid == True and end_valid == True):
            start_octets = list(map(int, start_ip.split('.')))
            end_octets = list(map(int, end_ip.split('.')))

            # evalutate octet values as means to validate range
            if (end_octets == start_octets):
                valid_range = True

            elif (end_octets[0:3] == start_octets[0:3] and
                  end_octets[3] > start_octets[3]):
                valid_range = True

            elif (end_octets[0:2] == start_octets[0:2] and
                  end_octets[2] > start_octets[2]):
                valid_range = True

            elif (end_octets[0] == start_octets[0] and
                  end_octets[1] > start_octets[1]):
                valid_range = True

            elif (end_octets[0] > start_octets[0]):
                valid_range = True

    except:
        return False
    
    return valid_range



# verify the supplied string has a valid DNS hostname associated with it
# returns: True or False
# created: 12/26/18
# last modified: 12/26/18
def dns_resolves(hostname):
    dns_resolves = True
    
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        dns_resolves = False
    
    return dns_resolves



# verify 'enable'/'disable' toggle value
#   all invalid values will result in 'enable'
# returns: 'enable' or 'disable' string
# created: 2019-01-06
# last modified: 2019-01-06
def enable_default(toggle):
    try:
        toggle = toggle.lower()
        if toggle != 'disable':
            toggle = 'enable'
    except:
        toggle = 'enable'
    return toggle



# verify 'enable'/'disable' toggle value
#   all invalid values will result in 'disable'
# returns: 'enable' or 'disable' string
# created: 2019-01-06
# last modified: 2019-01-06
def disable_default(toggle):
    try:
        toggle = toggle.lower()
        if toggle != 'enable':
            toggle = 'disable'
    except:
        toggle = 'disable'
    return toggle
