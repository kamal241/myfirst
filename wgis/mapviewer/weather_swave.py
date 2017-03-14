import pygrib
import numpy as np
import math
import json
from decimal import *
import os
import datetime

def get_swave_data(lt1, lt2, ln1, ln2, t):
	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']

	shwws_all, mpwws_all, dirpws_all, perpws_all, swhs_all  = [], [], [], [], []
	dsw1_all, hsw1_all, tsw1_all = [], [], []
	dsw2_all, hsw2_all, tsw2_all = [], [], []
	start = 0
	grib = os.path.join(dls_path,'dls-data','WW3','%s/%s/gwes00.glo_30m.t%02dz.grib2' % (t[:8],t[8:11],int(t[8:11])))	
	if not os.path.exists(grib):
		hrs6 = datetime.timedelta(hours=-6)
		dt = datetime.datetime.strptime(t,'%Y%m%d%H')
		t = datetime.datetime.strftime(dt+hrs6,'%Y%m%d%H')
		print "Using DTM " + t
		grib = os.path.join(dls_path,'dls-data','WW3','%s/%s/gwes00.glo_30m.t%02dz.grib2' % (t[:8],t[8:11],int(t[8:11])))
		start = 6
#	grbs = pygrib.open(grib)
	grbs=pygrib.index(grib,'shortName')
#	grbs.seek(0)
	limit = 8
	#for msg in grbs[140:180]:
	#	print dir(msg)
	#	print msg.shortName, msg#.name, msg.typeOfLevel, msg.level, msg.validDate, msg.messagenumber 
	shwws = grbs.select(shortName="shww")
	for shww in shwws[start:start+limit]:	
		shww_data, lats, lons = shww.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		shwws_all.append(shww_data)
	shwwd = np.dstack((shwws_all))

	mpwws = grbs.select(shortName="mpww")
	for mpww in mpwws[start:start+limit]:	
		mpww_data, lats, lons = mpww.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		mpwws_all.append(mpww_data)
	mpwwd = np.dstack((mpwws_all))

        dirpws = grbs.select(shortName="dirpw")
        for dirpw in dirpws[start:start+limit]:
                dirpws_data, lats, lons = dirpw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
                dirpws_all.append(dirpws_data)
        dirpwsd = np.dstack((dirpws_all))

        perpws = grbs.select(shortName="perpw")
        for perpw in perpws[start:start+limit]:
                perpws_data, lats, lons = perpw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
                perpws_all.append(perpws_data)
        perpwsd = np.dstack((perpws_all))

        swhs = grbs.select(shortName="swh")
        for shw in swhs[start:start+limit]:
                swhs_data, lats, lons = shw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
                swhs_all.append(swhs_data)
        swhsd = np.dstack((swhs_all))

	grbs=pygrib.index(grib,'shortName','nameOfFirstFixedSurface','level')	

	dsw1s = grbs.select(shortName="swdir",nameOfFirstFixedSurface="241",level=1)
	for dsw in dsw1s[start:start+limit]:
		dsw1_data, lats, lons = dsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		dsw1_all.append(dsw1_data)
	dsw1d = np.dstack((dsw1_all))
	
	hsw1s = grbs.select(shortName="swell",nameOfFirstFixedSurface="241",level=1)
	for hsw in hsw1s[start:start+limit]:
		hsw1_data, lats, lons = hsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		hsw1_all.append(hsw1_data)
	hsw1d = np.dstack((hsw1_all))

	tsw1s = grbs.select(shortName="swper",nameOfFirstFixedSurface="241",level=1)
	for tsw in tsw1s[start:start+limit]:
		tsw1_data, lats, lons = tsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		tsw1_all.append(tsw1_data)
	tsw1d = np.dstack((tsw1_all))

	dsw2s = grbs.select(shortName="swdir",nameOfFirstFixedSurface="241",level=2)
	for dsw in dsw2s[:limit]:
		dsw2_data, lats, lons = dsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		dsw2_all.append(dsw2_data)
	dsw2d = np.dstack((dsw2_all))
	
	hsw2s = grbs.select(shortName="swell",nameOfFirstFixedSurface="241",level=2)
	for hsw in hsw2s[start:start+limit]:
		hsw2_data, lats, lons = hsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		hsw2_all.append(hsw2_data)
	hsw2d = np.dstack((hsw2_all))

	tsw2s = grbs.select(shortName="swper",nameOfFirstFixedSurface="241",level=2)
	for tsw in tsw2s[start:start+limit]:
		tsw2_data, lats, lons = tsw.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		tsw2_all.append(tsw2_data)
	tsw2d = np.dstack((tsw2_all))

	
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
	import itertools
	swavedata_properties = [ [{"swave":{"shwws": [float(Decimal("%.2f" % e)) for e in dsh.tolist()], "mpww": [float(Decimal("%.2f" % e)) for e in dmp.tolist()], "dirpws": [float(Decimal("%.2f" % e)) for e in ddr.tolist()], "perpws": [float(Decimal("%.2f" % e)) for e in dpr.tolist()], "swhs": [float(Decimal("%.2f" % e)) for e in dsw.tolist()], "dsw1": [float(Decimal("%.2f" % e)) for e in dsw1de.tolist()], "hsw1": [float(Decimal("%.2f" % e)) for e in hsw1de.tolist()], "tsw1": [float(Decimal("%.2f" % e)) for e in tsw1de.tolist()], "dsw2": [float(Decimal("%.2f" % e)) for e in dsw2de.tolist()], "hsw2": [float(Decimal("%.2f" % e)) for e in hsw2de.tolist()], "tsw2": [float(Decimal("%.2f" % e)) for e in tsw2de.tolist()] }} for (dsh,dmp,ddr,dpr,dsw,dsw1de,hsw1de,tsw1de,dsw2de,hsw2de,tsw2de) in itertools.izip(dshwwi,dmpwwi,ddirpwsdi,dperpwsdi,dswhsdi,dsw1di,hsw1di,tsw1di,dsw2di,hsw2di,tsw2di)]  for dshwwi,dmpwwi,ddirpwsdi,dperpwsdi,dswhsdi,dsw1di,hsw1di,tsw1di,dsw2di,hsw2di,tsw2di in itertools.izip(shwwd,mpwwd,dirpwsd,perpwsd,swhsd,dsw1d, hsw1d, tsw1d, dsw2d, hsw2d, tsw2d) ]
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

