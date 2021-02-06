# net_eng
__net_eng__ is a Python module with common network engineering functions used when scripting. Many functions are used to sanitize/validate input into a script.

There are no explicit or implied guarantees or warranties with this module.
See required Python modules below.

-----
## Functions provided:

1. __is_ipv4_format():__\
verifies a supplied string is a valid IPv4 decimal format.\
returns True or False

1. __valid_ipv4_mask():__\
verifies supplied IPv4 mask value is valid (both cidr and decimal-based masks).\
returns True or False

1. __cidr_to_dec_mask():__\
converts an IPv4 cidr mask (string or integer) to an IPv4 decimal mask.\
returns string representation of IPv4 decimal mask

1. __valid_ipv4_unicast():__\
verifies a supplied string is a valid IPv4 unicast destination address.\
returns True or False

1. __is_ipv4_mcast():__\
verifies a supplied string is a valid IPv4 multicast destination address.\
returns True or False

1. __is_ipv4_range():__\
verifies a supplied start and end IPv4 address pair is a valid unicast destination range.\
returns True or False

1. __ipv4_pool_size():__\
determines the number of IPs in an IP address range.\
returns integer of the number of IPs or False

1. __ipv4_to_dec():__\
converts an IP in dotted quad decimal format to its corresponding integer value.\
returns integer representation of IP address or False

1. __dec_to_ipv4():__\
converts an integer value to is corresponding IP dotted quad decimal format.\
returns string of standard IP representation or False

1. __is_unpriv_port():__\
verifies an integer is in the range 1024-65535.\
returns True or False

1. __dns_resolves:__\
verifies DNS resolves to an IP address for a provided DNS name.\
returns True or False

1. __enable_default:__\
takes provided string and sets any value that is not 'disable' to 'enable'.\
returns string of 'disable' or 'enable'

1. __disable_default:__\
takes provided string and sets any value that is not 'enable' to 'disable'.\
returns string of 'disable' or 'enable'


-----
## Required Python modules:
* socket

