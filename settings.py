version = 1

name = "Rising Scimitar"
safe_name = "RisingScimitar"
map_name = "Takistan"

mish = safe_name + '.' + map_name
mish_core = safe_name + '_core.' + map_name
mish_3d = safe_name + '_3dbase.' + map_name
mish_test = 'test.' + map_name
def mish_versioned():
	return "%sv%d.%s" % (safe_name, version, map_name)
try:
    from local_settings import *
except ImportError:
    pass

###############################################################################
# Create a file in this folder called local_settings.py and paste the following
# into it.  Change the path so that it points to your A3 profile folder.
#
# profile_folder = r'C:\Users\sux\Documents\Arma 3 - Other Profiles\Moore'
#
# Make sure to uncomment the line as well. duh
###############################################################################

missions_folder = profile_folder + r'\missions'
mpmissions_folder = profile_folder + r'\mpmissions'
