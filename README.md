# net_eng
Python module with common network engineering functions used when scripting.

There are no explicit or implied guarantees or warranties with this module.
See required Python modules below.

-----
Functions provided:

is_ipv4_format: 
verifies a supplied IPv4 address is a decimal representation of four decimal octets.
returns True or False

valid_ipv4_mask:
verifies supplied IPv4 mask value is valid (both cidr and decimal-based masks).
returns True or False

cidr_to_dec_mask:
converts an IPv4 cidr mask integer to an IPv4 decimal mask
returns string representation of IPv4 decimal mask

valid_ipv4_unicast:
verifies a supplied IPv4 address is a valid IPv4 unicast destination address.
returns True or False

is_ipv4_mcast
verifies a supplied IPv4 address is a valid IPv4 multicast destination address.
returns True or False

is_ipv4_range:
verifies a supplied start and end IPv4 address pair is a valid unicast destination range.
returns True or False

dns_resolves:
verifies DNS resolves to an IP address for a provided DNS name.
returns True or False

enable_default:
receives a string value. any value provided that does not equal 'disable' is set to 'enable'.
returns string of 'disable' or 'enable'

disable_default:
receives a string value. any value provided that does not equal 'enable' is set to 'disable'.
returns string of 'disable' or 'enable'


-----
Required Python modules:
socket

