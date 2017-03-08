import pygrib
import numpy as np
import math
import json
from decimal import *
import os

def cld_pr2feet(clpr):
	clpr_mb = 0.01 * clpr
	clhgt_feet = (1 - (clpr_mb/1013.25) ** (0.190284)) * 145366.45
	return clhgt_feet


def get_weather_data(lt1, lt2, ln1, ln2, dt, tm):
	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']

	R2D = 57.2958

#	lt1, lt2, ln1, ln2 = 20,25,335,340
	tms = range(1,25,3)  #[1,4,7,10,13]
	fhead = "gfs.t%sz.pgrb2.0p25.f" % tm
#	grbfs =  ["gfs.t%sz.pgrb2.0p25.f001" % tm,"gfs.t%sz.pgrb2.0p25.f004" % tm,"gfs.t%sz.pgrb2.0p25.f007" % tm,"gfs.t%sz.pgrb2.0p25.f010" % tm]
#	grbfs =  ["gfs.t00z.pgrb2.0p25.f001","gfs.t00z.pgrb2.0p25.f002","gfs.t00z.pgrb2.0p25.f003","gfs.t00z.pgrb2.0p25.f004"]
	grbfs = [ fhead + "%03d" % td for td in tms]

	ws10_all, ws925_all, ws975_all = [], [], []
	wd10_all, wd925_all, wd975_all = [], [], []
	ccl_all, lcl_all, mcl_all = [], [], []
	ccbl_all, lcbl_all, mcbl_all = [], [], []
	tmp2m_all, prmsl_all, rh_all, apcp_all = [], [], [], []
	gust_all = []

	for f in grbfs:
#		data = pygrib.open('/home/megha/Synergy/aws/dls-prod/dls-data/%s/00/%s' % (dtm, f))
		data = pygrib.open(os.path.join(dls_path,'dls-data',dt, tm,f))
		t2 = data.select(shortName="2t",typeOfLevel="heightAboveGround",level=2)[0]
		prmsl = data.select(shortName="prmsl",typeOfLevel="meanSea",level=0)[0]
		rh = data.select(shortName="r",typeOfLevel="heightAboveGround",level=2)[0]
		apcp = data.select(shortName="tp",typeOfLevel="surface",level=0)[0]

		gust = data.select(shortName="gust",typeOfLevel="surface",level=0)[0]

		u10 = data.select(shortName="10u",typeOfLevel="heightAboveGround",level=10)[0]
		v10 = data.select(shortName="10v",typeOfLevel="heightAboveGround",level=10)[0]	

		u925 = data.select(shortName="u",typeOfLevel="isobaricInhPa",level=925)[0]
		v925 = data.select(shortName="v",typeOfLevel="isobaricInhPa",level=925)[0]

		u975 = data.select(shortName="u",typeOfLevel="isobaricInhPa",level=975)[0]
		v975 = data.select(shortName="v",typeOfLevel="isobaricInhPa",level=975)[0]

		ccl = data.select(shortName="tcc",nameOfFirstFixedSurface="244")[0]
		lcl = data.select(shortName="tcc",nameOfFirstFixedSurface="214")[0]
		mcl = data.select(shortName="tcc",nameOfFirstFixedSurface="224")[0]

		ccbl = data.select(shortName="pres",nameOfFirstFixedSurface="242")[0]
		lcbl = data.select(shortName="pres",nameOfFirstFixedSurface="212")[0]
		mcbl = data.select(shortName="pres",nameOfFirstFixedSurface="222")[0]

		t2_data, lats, lons = t2.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		prmsl_data, lats, lons = prmsl.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		rh_data, lats, lons = rh.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		apcp_data, lats, lons = apcp.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)

		u10_data, lats, lons = u10.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		v10_data, lats, lons = v10.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		
		u925_data, lats, lons = u925.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		v925_data, lats, lons = v925.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)

		u975_data, lats, lons = u975.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		v975_data, lats, lons = v975.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		
		gust_data, lats, lons = gust.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		
		ccl_data, lats, lons = ccl.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		lcl_data, lats, lons = lcl.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		mcl_data, lats, lons = mcl.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)

		ccbl_data, lats, lons = ccbl.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		lcbl_data, lats, lons = lcbl.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
		mcbl_data, lats, lons = mcbl.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)

		np.set_printoptions(precision=2)
		tmp2m_C_data = t2_data - 273

		ws10m_data = np.sqrt(np.square(u10_data) + np.square(v10_data))
		wd10m_data = np.arctan2(u10_data,v10_data) * R2D + 180

		tmp2m_all.append(tmp2m_C_data)
		prmsl_all.append(prmsl_data)
		rh_all.append(rh_data)
		apcp_all.append(apcp_data)


		ws10_all.append(ws10m_data * 1.94384)
		wd10_all.append(wd10m_data)

		ws925m_data = np.sqrt(np.square(u925_data) + np.square(v925_data))
		wd925m_data = np.arctan2(u925_data,v925_data) * R2D + 180

		ws925_all.append(ws925m_data * 1.94384)
		wd925_all.append(wd925m_data)

		ws975m_data = np.sqrt(np.square(u975_data) + np.square(v975_data))
		wd975m_data = np.arctan2(u975_data,v975_data) * R2D + 180
		
		ws975_all.append(ws975m_data * 1.94384)
		wd975_all.append(wd975m_data)
		
		gust_all.append(gust_data * 1.94384)

		ccl_all.append(ccl_data)
		lcl_all.append(lcl_data)
		mcl_all.append(mcl_data)

		pa2feet = np.vectorize(cld_pr2feet)

		ccbl_feet = pa2feet(ccbl_data).filled(999999)
		lcbl_feet = pa2feet(lcbl_data).filled(999999)
		mcbl_feet = pa2feet(mcbl_data).filled(999999)

		ccbl_all.append(ccbl_feet)
		lcbl_all.append(lcbl_feet)
		mcbl_all.append(mcbl_feet)
	"""
	np.round(tmp2m_all,2)
	np.round(prmsl_all,2)
	np.round(rh_all,2)
	np.round(apcp_all,2)
	"""


	tmp2m = np.dstack((tmp2m_all))
	pr_msl = np.dstack((prmsl_all))
	rh2m = np.dstack((rh_all))
	apcp_s = np.dstack((apcp_all))
	"""
	np.round(tmp2m,2)
	np.round(pr_msl,2)
	np.round(rh2m,2)
	np.round(apcp_s,2)
	"""
	wspd10 = np.dstack((ws10_all))
	wdir10 = np.dstack((wd10_all))

	wspd925 = np.dstack((ws925_all))
	wdir925 = np.dstack((wd925_all))

	wspd975 = np.dstack((ws975_all))
	wdir975 = np.dstack((wd975_all))

	gust_s = np.dstack((gust_all))

	clpccl = np.dstack((ccl_all))
	clplcl = np.dstack((lcl_all))
	clpmcl = np.dstack((mcl_all))

	clpccbl = np.dstack((ccbl_all))
	clplcbl = np.dstack((lcbl_all))
	clpmcbl = np.dstack((mcbl_all))

	wind_properties = [ [{"wind":{"ws_10m": [float(Decimal("%.2f" % e)) for e in dws10.tolist()] , "wd_10m": [float(Decimal("%.2f" % e)) for e in dwd10.tolist() ], "ws_925m": [float(Decimal("%.2f" % e)) for e in dws925.tolist()] , "wd_925m": [float(Decimal("%.2f" % e)) for e in dwd925.tolist()] , "ws_975m": [float(Decimal("%.2f" % e)) for e in dws975.tolist()] , "wd_975m": [float(Decimal("%.2f" % e)) for e in dwd975.tolist()] , "gust" : [float(Decimal("%.2f" % e)) for e in dgust.tolist() ] }} for dws10,dwd10,dws925,dwd925,dws975,dwd975,dgust in zip(wspd10i,wdir10i,wspd925i,wdir925i,wspd975i,wdir975i,gusti)]for wspd10i,wdir10i,wspd925i,wdir925i,wspd975i,wdir975i,gusti in zip(wspd10,wdir10,wspd925,wdir925,wspd975,wdir975,gust_s)]

	cloud_properties = [ [{"cloud":{"ccl": [float(Decimal("%.2f" % e)) for e in dccl.tolist()] , "lcl": [float(Decimal("%.2f" % e)) for e in dlcl.tolist()] , "mcl": [float(Decimal("%.2f" % e)) for e in dmcl.tolist()] , "ccbl": [float(Decimal("%.2f" % e)) for e in dccbl.tolist()] , "lcbl": [float(Decimal("%.2f" % e)) for e in dlcbl.tolist()] , "mcbl": [float(Decimal("%.2f" % e)) for e in dmcbl.tolist()] }} for dccl,dlcl,dmcl,dccbl,dlcbl,dmcbl in zip(ccli,lcli,mcli,ccbli,lcbli,mcbli) ] for ccli,lcli,mcli,ccbli,lcbli,mcbli in zip(clpccl,clplcl,clpmcl,clpccbl,clplcbl,clpmcbl)]

	tpha_properties = [ [{"tpha":{"tmp2m": [float(Decimal("%.2f" % e)) for e in dtmp.tolist()] , "prmsl": [float(Decimal("%.2f" % e)) for e in dpr.tolist()] , "rh2m": [float(Decimal("%.2f" % e)) for e in drh.tolist()] , "apcp": [float(Decimal("%.2f" % e)) for e in dapcp.tolist()] }} for dtmp,dpr,drh,dapcp in zip(dtmpi,dpri,drhi,dapcpi)]  for dtmpi,dpri,drhi,dapcpi in zip(tmp2m, pr_msl, rh2m, apcp_s) ]

	wct_all = np.dstack((lons,lats,wind_properties,cloud_properties,tpha_properties))

	features = [ [{"type": "Feature", "geometry": {"type": "Point", "coordinates" : [ln, lt]}, "properties": { "wind" : w['wind'] , "cloud" : c['cloud'], "tpha" : t['tpha']  } }]  for dllwsd in wct_all for ln,lt,w,c,t in dllwsd ]

	other_properties = [{"timestamp": dt+tm, "hours": hr} for hr in tms]
	f_coll = {"type": "FeatureCollection", "features": features, "properties" : other_properties}

	return json.dumps(f_coll)

if __name__ == "__main__":
	lt1, lt2, ln1, ln2 = 20,21,335,336
	dtm = "2017022806"
	dt = dtm[:8]
	tm = dtm[8:]
	wjson_data = get_weather_data(lt1, lt2, ln1, ln2, dt, tm)
	with open('wjson_%s.geojson'% dtm,'w') as wf:
		wf.write(wjson_data)
		


