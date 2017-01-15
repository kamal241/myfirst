import pygrib
import numpy as np
import math
import json
from decimal import *
import os

def get_swave_data(lt1, lt2, ln1, ln2, t):
	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']

	shwws_all, mpwws_all, dirpws_all, perpws_all, swhs_all  = [], [], [], [], []
	dsw1_all, hsw1_all, tsw1_all = [], [], []
	dsw2_all, hsw2_all, tsw2_all = [], [], []

	grib = os.path.join(dls_path,'dls-data','WW3','%s/%s/gwes00.glo_30m.t%02dz.grib2' % (t[:8],t[8:11],int(t[8:11])))	
	grbs = pygrib.open(grib)
	grbs.seek(0)

	#for msg in grbs[140:180]:
	#	print dir(msg)
	#	print msg.shortName, msg#.name, msg.typeOfLevel, msg.level, msg.validDate, msg.messagenumber 
	shwws = grbs.select(shortName="shww")
	for shww in shwws[:4]:	
		shww_data, lats, lons = shww.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		shwws_all.append(shww_data)
	shwwd = np.dstack((shwws_all))

	mpwws = grbs.select(shortName="mpww")
	for mpww in mpwws[:4]:	
		mpww_data, lats, lons = mpww.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		mpwws_all.append(mpww_data)
	mpwwd = np.dstack((mpwws_all))
	
	dsw1s = grbs.select(shortName="swdir",nameOfFirstFixedSurface="241",level=1)
	for dsw in dsw1s[:4]:
		dsw1_data, lats, lons = dsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		dsw1_all.append(dsw1_data)
	dsw1d = np.dstack((dsw1_all))
	
	hsw1s = grbs.select(shortName="swell",nameOfFirstFixedSurface="241",level=1)
	for hsw in hsw1s[:4]:
		hsw1_data, lats, lons = hsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		hsw1_all.append(hsw1_data)
	hsw1d = np.dstack((hsw1_all))

	tsw1s = grbs.select(shortName="swper",nameOfFirstFixedSurface="241",level=1)
	for tsw in tsw1s[:4]:
		tsw1_data, lats, lons = tsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		tsw1_all.append(tsw1_data)
	tsw1d = np.dstack((tsw1_all))

	dsw2s = grbs.select(shortName="swdir",nameOfFirstFixedSurface="241",level=1)
	for dsw in dsw2s[:4]:
		dsw2_data, lats, lons = dsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		dsw2_all.append(dsw2_data)
	dsw2d = np.dstack((dsw2_all))
	
	hsw2s = grbs.select(shortName="swell",nameOfFirstFixedSurface="241",level=1)
	for hsw in hsw2s[:4]:
		hsw2_data, lats, lons = hsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		hsw2_all.append(hsw2_data)
	hsw2d = np.dstack((hsw2_all))

	tsw2s = grbs.select(shortName="swper",nameOfFirstFixedSurface="241",level=1)
	for tsw in tsw2s[:4]:
		tsw2_data, lats, lons = tsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		tsw2_all.append(tsw2_data)
	tsw2d = np.dstack((tsw2_all))

	dirpws = grbs.select(shortName="dirpw")
	for dirpw in dirpws[:4]:	
		dirpws_data, lats, lons = dirpw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		dirpws_all.append(dirpws_data)
	dirpwsd = np.dstack((dirpws_all))

	perpws = grbs.select(shortName="perpw")
	for perpw in perpws[:4]:	
		perpws_data, lats, lons = perpw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		perpws_all.append(perpws_data)
	perpwsd = np.dstack((dirpws_all))

	swhs = grbs.select(shortName="swh")
	for shw in swhs[:4]:	
		swhs_data, lats, lons = shw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		swhs_all.append(swhs_data)	
	swhsd = np.dstack((swhs_all))
	
	"""
	for shww in shwws:
		print shww.shortName, shww.name, shww.typeOfLevel, shww.level, shww.validDate, shww.messagenumber 
		break
	#for mpww in mpwws:
	#	print mpww.shortName, mpww.name, mpww.typeOfLevel, mpww.level, mpww.validDate, mpww.messagenumber 

	#dsw1 = grbs.select(shortName="swdir",nameOfFirstFixedSurface="241",level=1)
	
	print shwws_data.lats
	print shwws_data.lons
	print shwws_data.data
	"""
	#print shwwd[0]
	swavedata_properties = [ [{"swave":{"shwws": [float(Decimal("%.2f" % e)) for e in dsh.tolist()], "mpww": [float(Decimal("%.2f" % e)) for e in dmp.tolist()], "dirpws": [float(Decimal("%.2f" % e)) for e in ddr.tolist()], "perpws": [float(Decimal("%.2f" % e)) for e in dpr.tolist()], "swhs": [float(Decimal("%.2f" % e)) for e in dsw.tolist()], "dsw1": [float(Decimal("%.2f" % e)) for e in dsw1de.tolist()], "hsw1": [float(Decimal("%.2f" % e)) for e in hsw1de.tolist()], "tsw1": [float(Decimal("%.2f" % e)) for e in tsw1de.tolist()], "dsw2": [float(Decimal("%.2f" % e)) for e in dsw2de.tolist()], "hsw2": [float(Decimal("%.2f" % e)) for e in hsw2de.tolist()], "tsw2": [float(Decimal("%.2f" % e)) for e in tsw2de.tolist()] }} for (dsh,dmp,ddr,dpr,dsw,dsw1de,hsw1de,tsw1de,dsw2de,hsw2de,tsw2de) in zip(dshwwi,dmpwwi,ddirpwsdi,dperpwsdi,dswhsdi,dsw1di,hsw1di,tsw1di,dsw2di,hsw2di,tsw2di)]  for dshwwi,dmpwwi,ddirpwsdi,dperpwsdi,dswhsdi,dsw1di,hsw1di,tsw1di,dsw2di,hsw2di,tsw2di in zip(shwwd,mpwwd,dirpwsd,perpwsd,swhsd,dsw1d, hsw1d, tsw1d, dsw2d, hsw2d, tsw2d) ]
	swave_all = np.dstack((lons, lats, swavedata_properties))
	features = [ {"type": "Feature", "geometry": {"type": "Point", "coordinates" : [ln, lt]}, "properties": { "shwws" : sw['swave']['shwws'], "mpww" : sw['swave']['mpww'], "dirpws" : sw['swave']['dirpws'], "perpws" : sw['swave']['perpws'], "swhs" : sw['swave']['swhs'], "dsw1" : sw['swave']['dsw1'], "hsw1" : sw['swave']['hsw1'], "tsw1" : sw['swave']['tsw1'], "dsw2" : sw['swave']['dsw2'], "hsw2" : sw['swave']['hsw2'], "tsw2" : sw['swave']['tsw2']} }  for dswave in swave_all for ln,lt,sw in dswave ]

	f_coll = {"type": "FeatureCollection", "features": features }
	return json.dumps(f_coll)
	


if __name__ == "__main__":
	lt1, lt2, ln1, ln2 = 20,25,335,340
	wjson_data = get_swave_data(lt1, lt2, ln1, ln2, "2016112200")
#	print wjson_data
	with open('swave.geojson','w') as wf:
		wf.write(wjson_data)

