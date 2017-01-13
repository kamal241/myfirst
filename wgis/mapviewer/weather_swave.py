import pygrib
import numpy as np
import math
import json
from decimal import *
import os

def get_swave_data(lt1, lt2, ln1, ln2, t):
	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']

	
	grib = os.path.join(dls_path,'dls-data','WW3','%s/%s/gwes00.glo_30m.t%02dz.grib2' % (t[:8],t[8:11],int(t[8:11])))	
	grbs = pygrib.open(grib)
	grbs.seek(0)

	#for msg in grbs[140:180]:
	#	print dir(msg)
	#	print msg.shortName, msg#.name, msg.typeOfLevel, msg.level, msg.validDate, msg.messagenumber 
	"""
	shwws = grbs.select(shortName="shww")
	mpwws = grbs.select(shortName="mpww")
	dsw1 = grbs.select(shortName="swdir",nameOfFirstFixedSurface="241",level=1)
	hsw1 = grbs.select(shortName="swell",nameOfFirstFixedSurface="241",level=1)
	tsw1 = grbs.select(shortName="swper",nameOfFirstFixedSurface="241",level=1)
	dsw2 = grbs.select(shortName="swdir",nameOfFirstFixedSurface="241",level=2)
	hsw2 = grbs.select(shortName="swell",nameOfFirstFixedSurface="241",level=2)
	tsw2 = grbs.select(shortName="swper",nameOfFirstFixedSurface="241",level=2)
	dirpws = grbs.select(shortName="dirpw")
	perpws = grbs.select(shortName="perpw")
	swhs = grbs.select(shortName="swh")
	"""
#	for shww in shwws:
#		print shww.shortName, shww.name, shww.typeOfLevel, shww.level, shww.validDate, shww.messagenumber 
#		break
	#for mpww in mpwws:
	#	print mpww.shortName, mpww.name, mpww.typeOfLevel, mpww.level, mpww.validDate, mpww.messagenumber 

	#dsw1 = grbs.select(shortName="swdir",nameOfFirstFixedSurface="241",level=1)


if __name__ == "__main__":
	lt1, lt2, ln1, ln2 = 20,21,335,336
	wjson_data = get_swave_data(lt1, lt2, ln1, ln2, "2017011200")
