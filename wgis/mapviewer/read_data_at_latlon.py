import os
import pygrib
import math
import numpy

def read_latlon2idx(lat,lon, res):
	nlat = round(lat*(1/res))*res
	ltidx = (90 - nlat)/res 
	nlon = round(lon%360*(1/res))*res
	lnidx = nlon /res
	return nlat,nlon

def read_latlon2llidx(lat,lon, res,blat=90):
	nlat = round(lat*(1/res))*res
	ltidx = (blat - nlat)/res 
	nlon = round(lon%360*(1/res))*res
	lnidx = nlon /res
	return int(ltidx),int(lnidx)

def get_ww3_data_at_lat_lon_idx(lon, lat,dt, tm,hrsfcst):
	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']

	start = int(3/3)
	limit = int(hrsfcst/3)+1
	nlat,nlon = read_latlon2llidx(lat,lon,0.5,80)
	ww3_all = []
#	print nlat,nlon
	hrs = range(1,15,3)
	grib = os.path.join(dls_path,'dls-data','WW3','%s/%s/gwes00.glo_30m.t%02dz.grib2' % (dt,tm,int(tm)))
	grbsn = pygrib.open(grib)
	grbsn.seek(0)
	grbs=pygrib.index(grib,'shortName')	

	shwws = grbs.select(shortName="shww")
	mpwws = grbs.select(shortName="mpww")
	dirpws = grbs.select(shortName="dirpw")
	perpws = grbs.select(shortName="perpw")
	swhs = grbs.select(shortName="swh")

	seawave_all = []
	for shww,mpww,dirpw,perpw,shw in zip(shwws[start:limit],mpwws[start:limit],dirpws[start:limit],perpws[start:limit],swhs[start:limit]):
		shww_data = shww['values'][nlat][nlon]  	#.data(lat1=nlat,lat2=nlat,lon1=nlon,lon2=nlon)		
		mpww_data = mpww['values'][nlat][nlon]	 	#.data(lat1=nlat,lat2=nlat,lon1=nlon,lon2=nlon)
		dirpws_data = dirpw['values'][nlat][nlon]
		perpws_data = perpw['values'][nlat][nlon]
		swhs_data = shw['values'][nlat][nlon]
		if shww_data is numpy.ma.masked:
			shww_data = 999
		if mpww_data is numpy.ma.masked:
			mpww_data = 999
		if dirpws_data is numpy.ma.masked:
			dirpws_data = 999
		if perpws_data is numpy.ma.masked:
			perpws_data = 999
		if swhs_data is numpy.ma.masked:
			swhs_data = 999


		seawave_data = {}
		seawave_data['shww']=shww_data
		seawave_data['mpww']=mpww_data
		seawave_data['dirpw']=dirpws_data
		seawave_data['perpw']=perpws_data
		seawave_data['swhs']=swhs_data
		seawave_data['timestamp']=shww.validDate
		seawave_all.append(seawave_data)

	grbs=pygrib.index(grib,'shortName','nameOfFirstFixedSurface','level')

	dsw1s = grbs.select(shortName="swdir",nameOfFirstFixedSurface="241",level=1)
	hsw1s = grbs.select(shortName="swell",nameOfFirstFixedSurface="241",level=1)
	tsw1s = grbs.select(shortName="swper",nameOfFirstFixedSurface="241",level=1)
	dsw2s = grbs.select(shortName="swdir",nameOfFirstFixedSurface="241",level=2)
	hsw2s = grbs.select(shortName="swell",nameOfFirstFixedSurface="241",level=2)
	tsw2s = grbs.select(shortName="swper",nameOfFirstFixedSurface="241",level=2)

	swell_all = []	
	for dsw1,hsw1,tsw1,dsw2,hsw2,tsw2 in zip(dsw1s[start:limit],hsw1s[start:limit],hsw1s[start:limit],dsw2s[start:limit],hsw2s[start:limit],tsw2s[start:limit]):
		dsw1_data = dsw1['values'][nlat][nlon]
		hsw1_data = hsw1['values'][nlat][nlon]
		tsw1_data = tsw1['values'][nlat][nlon]
		dsw2_data = dsw2['values'][nlat][nlon]
		hsw2_data = hsw2['values'][nlat][nlon]
		tsw2_data = tsw2['values'][nlat][nlon]
		if dsw1_data is numpy.ma.masked:
			dsw1_data = 999
		if hsw1_data is numpy.ma.masked:
			hsw1_data = 999
		if tsw1_data is numpy.ma.masked:
			tsw1_data = 999
		if dsw2_data is numpy.ma.masked:
			dsw2_data = 999
		if hsw2_data is numpy.ma.masked:
			hsw2_data = 999
		if tsw2_data is numpy.ma.masked:
			tsw2_data = 999
		swell_data = {}
		swell_data['dsw1']=dsw1_data
		swell_data['hsw1']=hsw1_data
		swell_data['tsw1']=tsw1_data
		swell_data['dsw2']=dsw2_data
		swell_data['hsw2']=hsw2_data
		swell_data['tsw2']=tsw2_data
		swell_data['timestamp']=dsw1.validDate
		swell_all.append(swell_data)
	swell_all.sort(key=lambda k:k['timestamp'])
	seawave_all.sort(key=lambda k:k['timestamp'])

	return swell_all,seawave_all	


def get_gfs_data_at_lat_lon_idx(lat,lon, dt, tm,hrsfcst):
	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']
	hrs = range(3,hrsfcst+1,3)
	grbfs = ["gfs.t%sz.pgrb2.0p25.f%03d" %  (tm,hr) for hr in hrs]

	nlat,nlon = read_latlon2llidx(lat,lon,0.25)
	R2D = 57.2958
	wind_all = []
	for f in grbfs:
		grbf = os.path.join(os.path.join(dls_path,'dls-data',dt, tm,f))
		if os.path.exists(grbf):
			grbs=pygrib.index(grbf,'shortName','typeOfLevel','level')
			t2 = grbs.select(shortName="2t",typeOfLevel="heightAboveGround",level=2)[0]
			
			u10 = grbs.select(shortName="10u",typeOfLevel="heightAboveGround",level=10)[0]
			v10 = grbs.select(shortName="10v",typeOfLevel="heightAboveGround",level=10)[0]
			u10_data = u10['values'][nlat][nlon]
			v10_data = v10['values'][nlat][nlon]
			u10m,v10m = u10_data,v10_data
			ws_10m = math.sqrt(u10m*u10m+v10m*v10m) * 1.94384
			wd_10m = math.atan2(u10m,v10m) * R2D + 180

			gust = grbs.select(shortName="gust",typeOfLevel="surface",level=0)[0]
			gust_data = gust['values'][nlat][nlon]
			wind_gust = gust_data * 1.94384 
			wind_data = {}
			wind_data['ws_10m']=ws_10m
			wind_data['wd_10m']=wd_10m
			wind_data['gust']=wind_gust
			wind_data['timestamp']=u10.validDate
			wind_all.append(wind_data)
#	print len(wind_all)
	wind_all.sort(key=lambda k:k['timestamp'])
	return wind_all


if __name__ == "__main__":
	dtm = '20170309'
	tm = '18'
	#get_gfs_data_at_lat_lon(72.25,19.75,'20170227','06')
	wind = get_gfs_data_at_lat_lon_idx(72.25,19.75,dtm,tm,48)

	#get_ww3_data_at_lat_lon(72.25,19.75,'20170227','06')
#	seaswell = get_ww3_data_at_lat_lon_idx(72.25,19.75,dtm,tm)
	print wind[0]
#	print seaswell[0][0]
#	print seaswell[1][0]

