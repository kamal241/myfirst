import pygrib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib. path import Path
from matplotlib.colors import rgb2hex
from mpl_toolkits.basemap import Basemap, shiftgrid
from mpl_toolkits.basemap import interp
import numpy as np
import math
from uvunify import uvect, vvect, uvdir
import datetime
from django.conf import settings

def get_ws10prmsl(left,bottom,top,right,t,fv):
	lt1, lt2, ln1, ln2 = bottom,top,left,right
	w,h,dpi,fs=450,450,60,10
	plt.figure(figsize=(w/dpi,h/dpi))

	contmap = Basemap(projection='merc', llcrnrlat=lt1, urcrnrlat=lt2,llcrnrlon=ln1, urcrnrlon=ln2, resolution='h')
	parallels = np.arange(-90.,91.,1.)

	# Label the meridians and parallels
	contmap.drawparallels(parallels,labels=[False,True,True,False],fontsize=fs)

	# Draw Meridians and Labels
	meridians = np.arange(-180.,181.,1.)
	contmap.drawmeridians(meridians,labels=[False,False,False,True],fontsize=fs)
	contmap.drawcoastlines(color = 'k')

	
#	grib = '/home/megha/Synergy/gis_project/development/experiments/netcdf/SynergyTestData/GRIB/GFS/20161010/06/gfs.t06z.pgrb2.0p25.f006' 
#	grib = '/home/megha/Synergy/gis_project/development/experiments/netcdf/SynergyTestData/GRIB/GFS/%s/%s/gfs.t%02dz.pgrb2.0p25.f%03d' % (t[:8],t[8:11],int(t[8:11]),fv)
	import os
	if os.environ.has_key('dls_path'):
		dls_path = os.environ['dls_path']

	grib = os.path.join(dls_path,'dls-data','%s/%s/gfs.t%02dz.pgrb2.0p25.f%03d' % (t[:8],t[8:11],int(t[8:11]),fv))
#	print grib
	grbs = pygrib.open(grib)

	grbs.seek(0)

#	print "Processing Wind Parameters"
### Wind speed and wind direction	
	uin = grbs.select(shortName='10u',typeOfLevel="heightAboveGround",level=10)[0]
	vin = grbs.select(shortName='10v',typeOfLevel="heightAboveGround",level=10)[0]

	udata, lats, lons = uin.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
	vdata, lats, lons = vin.data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)

	x, y = contmap(lons, lats)


#	print "\tProcessing Wind Speed"
	##	Wind Speed
	wspeed = np.sqrt(udata*udata + vdata*vdata) * 1.94384
	ws_levs = range(0,51,5) #+ range(60,101,10)
	wspeed_contoursf = contmap.contourf(x,y,wspeed,ws_levs,cmap=plt.cm.jet, alpha=.4)	
	#	wspeed_contoursf = map.contourf(x[points],y[points],wspeed[points],cmap=plt.cm.jet, alpha=.5)
	cb = contmap.colorbar(location='right', pad="10%")
	cb.ax.tick_params(labelsize=10)

	# 1 degree resolution data
	yy = np.arange(0,y.shape[0], 1)
	xx = np.arange(0,x.shape[0], 1)

	points = np.meshgrid(yy,xx)

#	print "\tProcessing Wind Direction"
## Wind Direction
	mwdir = np.arctan2(udata,vdata) * 180/np.pi

	mudata = uvect(mwdir)
	mvdata = vvect(mwdir)

	## Experiment for black arrow
	contmap.quiver(x[points],y[points],mudata[points],mvdata[points], color='k', scale=24, headlength=6, headwidth=7, pivot='mid')

#	print "Processing PRMSL Parameters"
### PRMSL Isolines
	raw_prmsl_data = grbs.select(name='Pressure reduced to MSL',typeOfLevel="meanSea",level=0)

	prmsl_data, lats, lons = raw_prmsl_data[0].data(lat1=lt1,lat2=lt2,lon1=ln1,lon2=ln2)
	prmsl_data = prmsl_data * 0.01

	prmsl_min = int(math.floor(np.min(prmsl_data)))
	prmsl_max = int(math.ceil(np.max(prmsl_data)))
	prmsl_diff = 2

	prmsl_levs = range(prmsl_min,prmsl_max+prmsl_diff,prmsl_diff)
	prmsl_isolines = contmap.contour(x,y,prmsl_data,prmsl_levs,linewidths=2,colors='k')
	#csw = map.contour(x,y,prmsl_data,linewidths=2,colors='k')
	plt.clabel(prmsl_isolines,inline=1,inline_spacing=1,fontsize=14,fmt='%1.0f',colors='k',fontproperties={'weight': 'bold'})

#	plt.show()
#	fname = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
       	fname = "WSPRMSL_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_%d_%d_%d_%d.png" % (w,h,dpi,fs)
	fpath = os.path.join(settings.MEDIA_ROOT,'media','images',fname)
	plt.savefig(fpath)
	return fname
#	return fpath
#	plt.figure(figsize=(800/dpi,800/dpi))
#	plt.savefig('/home/megha/Synergy/gis_project/development/synergygis_project/synergygis/media/images/%s.png' % fname, bbox_inches='tight', dpi=dpi)

def get_swh(left,bottom,top,right,t,fv,hrsofst=0):
        lt1, lt2, ln1, ln2 = bottom,top,left,right
        w,h,dpi,fs=450,450,60,10
        plt.figure(figsize=(w/dpi,h/dpi))

        contmap = Basemap(projection='merc', llcrnrlat=lt1, urcrnrlat=lt2,llcrnrlon=ln1, urcrnrlon=ln2, resolution='h')
        parallels = np.arange(-90.,91.,1.)

        # Label the meridians and parallels
        contmap.drawparallels(parallels,labels=[False,True,True,False],fontsize=fs)

	# Draw Meridians and Labels
        meridians = np.arange(-180.,181.,1.)
        contmap.drawmeridians(meridians,labels=[False,False,False,True],fontsize=fs)
        contmap.drawcoastlines(color = 'k')

        import os
        if os.environ.has_key('dls_path'):
                dls_path = os.environ['dls_path']

        grib = os.path.join(dls_path,'dls-data','WW3','%s/%s/gwes00.glo_30m.t%02dz.grib2' % (t[:8],t[8:11],int(t[8:11])))
	print grib
        grbs = pygrib.open(grib)
        grbs.seek(0)

	grb = grbs.select(name='Significant height of wind waves')[hrsofst]
	print grb.validDate,grb.dataDate
	data = grb.values
	lats, lons = grb.latlons()

	x, y = contmap(lons, lats)

	levs = [ i*0.5 for i in range((int(math.ceil(np.max(data)))+1)*2)]

	x2 = np.linspace(x[0][0],x[0][-1],x.shape[1]*5)
	y2 = np.linspace(y[0][0],y[-1][0],y.shape[0]*5)

	x2, y2 = np.meshgrid(x2, y2)
	
	cs = contmap.contourf(x,y,data,cmap=plt.cm.BrBG, alpha=0.6)
	cb = contmap.colorbar(location='right', pad="10%")
	cb.ax.tick_params(labelsize=10)
	
	csw = contmap.contour(x,y,data,levs,linewidths=1,colors='k')
	plt.clabel(csw,inline=1,inline_spacing=1,fontsize=12,fmt='%1.0f',colors='k')

#	lon = 58.57
#	lat = 23.57
	
#	x, y = m(lon, lat)

#	plt.text(x, y, '#',fontsize=10,fontweight='bold',
 #                   ha='left',va='center',color='b',
  #                  bbox=dict(facecolor='b', alpha=0.2))

	fname = "SWHGT_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_%d_%d_%d_%d.png" % (w,h,dpi,fs)
#	fpath = os.path.join('/syndata/staging/synweatherweb/synweather/','media','images',fname)
        fpath = os.path.join(settings.MEDIA_ROOT,'media','images',fname)
#	plt.savefig(fpath, bbox_inches='tight', dpi=dpi)
	plt.savefig(fpath)	
	return fname
	

if __name__ ==  "__main__":
	get_ws10prmsl(70.80078106373549,13.089288487776358,19.289542354858398,77.12890606373547,"2017031306",1)
#	get_swh(70.80078106373549,13.089288487776358,19.289542354858398,77.12890606373547,"2016111906",6)
