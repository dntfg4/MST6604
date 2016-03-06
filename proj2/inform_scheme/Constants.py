'''Location Management Constants:
        This contains the MS, Tree, and Node classes for the algorithms.

'''

__author__ = 'James Soehlke and David Taylor'
__version__ = '$Revision: 1.0 $'[11:-2]
__date__ = '$Date: 2016/02/17 12:00:00 $'
__copyright__ = '2016 James Soehlke and David N. Taylor'
__license__ = 'Python'


# These are constants that are being used
POINTER = "pointer"
VALUE = "value"
FORWARDING_P = "forwarding_p"
FORWARDING_V = "forwarding_v"
FORWARDING_P_FORWARD = "forwarding_p_forward"
FORWARDING_P_REVERSE = "forwarding_p_reverse"
MOBILE_STATION = "mobile station"
LOCATION = "location"
REPLICATION = "replication"
REPLICATION_P = "replication_p"
REPLICATION_V = "replication_v"

algorithm_list = [POINTER]
location_list = [FORWARDING_P_FORWARD, FORWARDING_P_REVERSE, REPLICATION]
location_list[len(location_list):] = algorithm_list
