from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import date
from weather_data import *
from weather_swave import *
#from django.contrib.gis.geos import Point
from raster_data import get_pres_msl_contour, get_contours, get_multi_contours
from generate_cp import get_ws10prmsl, get_swh
from mapviewer.synreports import *
import datetime
# Create your views here.

def index(request):
	context = {}
	return render(request, 'mapviewer/index.html', context)
    #return HttpResponse("Hello, world. You're at the MapViewer index.")


def weather(request):
	lt1, lt2, ln1, ln2 = 20,21,70,75
	dtm = request.GET.get('dtm')
	lt1 = float(request.GET.get('lt1'))
	lt2 = float(request.GET.get('lt2'))
	ln1 = float(request.GET.get('ln1'))
	ln2 = float(request.GET.get('ln2'))
#	print dtm
	dt = dtm[:8]
	tm = dtm[8:]
#	print dt, tm
	wjson_data = get_weather_data(lt1, lt2, ln1, ln2, dt, tm)
	return HttpResponse(wjson_data,content_type='application/json')

def weather_raster(request):
	lt1, lt2, ln1, ln2 = 20,21,70,75
	dtm = request.GET.get('dtm')
	lt1 = float(request.GET.get('lt1'))
	lt2 = float(request.GET.get('lt2'))
	ln1 = float(request.GET.get('ln1'))
	ln2 = float(request.GET.get('ln2'))
#	wjson_data = get_contours(lt1, lt2, ln1, ln2, dtm,4)
	wjson_data = get_multi_contours(lt1, lt2, ln1, ln2, dtm,4)
	return HttpResponse(wjson_data,content_type='application/json')	

def weather_swave(request):
	lt1, lt2, ln1, ln2 = 20,21,70,75
	dtm = request.GET.get('dtm')
	lt1 = float(request.GET.get('lt1'))
	lt2 = float(request.GET.get('lt2'))
	ln1 = float(request.GET.get('ln1'))
	ln2 = float(request.GET.get('ln2'))
	hrsofst = 0
	if 'hrsofst' in request.GET.keys():
		hrsofst = int(request.GET.get('hrsofst'))
	wsjson_data = get_swave_data(lt1, lt2, ln1, ln2, dtm, hrsofst)
	if wsjson_data != 304:
		return HttpResponse(wsjson_data,content_type='application/json')	
	else:
		dt = datetime.datetime.strptime(dtm,"%Y%m%d%H")
		td = datetime.timedelta(hours=-6)
		ndtm = (dt+td).strftime("%Y%m%d%H")
		hrsofst = 2
		location = "http://ec2-54-254-159-111.ap-southeast-1.compute.amazonaws.com:8000/mapviewer/weather_swave?lt1=12.878241020688549&lt2=17.87824102068855&ln1=91.33216857910155&ln2=96.33216857910155&dtm=%s&hrsofst=%d" % (ndtm,hrsofst)
		res = HttpResponse(location,status=302)
		res['Location'] = location
		return res

def reports_location(request):
        t=request.GET['dtm']
	gt = t
	lat = float(request.GET['lat'])
	lon = float(request.GET['lon'])
        fv=int(t[8:11])
	gfv = fv
        hrsofst = 0
        if 'hrsofst' in request.GET.keys():
                hrsofst = int(request.GET.get('hrsofst'))
		dt = datetime.datetime.strptime(t,"%Y%m%d%H")
		td = datetime.timedelta(hours=6)
		gt = (dt+td).strftime("%Y%m%d%H")				
		gfv = int(gt[8:11])
#		print t,fv,gt,gfv,hrsofst

       	if os.environ.has_key('dls_path'):
                dls_path = os.environ['dls_path']

	grib = os.path.join(dls_path,'dls-data','WW3','%s/%s/gwes00.glo_30m.t%02dz.grib2' % (t[:8],t[8:11],int(t[8:11])))
	if os.path.exists(grib):
		response = HttpResponse(content_type='application/pdf')
	        today = date.today()
	        filename = 'Location_Weather_Report_' + today.strftime('%Y-%m-%d')
	        response['Content-Disposition'] =  'attachement; filename={0}.pdf'.format(filename)
	#        fv= int(request.GET['fv'])
	        rlat, rlon = round(lat*2)/2, round(lon*2)/2
	#        target_loc = Point(lon,lat)
	#        rtarget_loc = Point(rlon,rlat)
	
		if lon < 5:
			ln1,ln2,lt1,lt2 = 0,10,lat-5,lat+5
		else:
		        ln1,ln2,lt1,lt2 = lon-5,lon+5,lat-5,lat+5
	        fname = get_ws10prmsl(ln1,lt1,lt2,ln2,gt,gfv)
	        swhgt_fname = get_swh(ln1,lt1,lt2,ln2,t,fv,hrsofst)
	        dt = gt[:8]
	        tm = gt[8:]
	        wpdf = weather_report_pdf((lon,lat),dt,tm,fname,swhgt_fname,hrsofst)#"", wndata, wwdata,fname,swhgt_fname,(lon,lat),ftm) 
	        if wpdf is None:
	                print "WPDF Error"
	        else:
	                print "WPDF Success"
	        response.write(wpdf)
	        return response
	else:
                dt = datetime.datetime.strptime(t,"%Y%m%d%H")
                td = datetime.timedelta(hours=-6)
                ndtm = (dt+td).strftime("%Y%m%d%H")
                hrsofst = 2
                location = "http://ec2-54-254-159-111.ap-southeast-1.compute.amazonaws.com:8000/mapviewer/reports/location?&lon=%f&lat=%f&dtm=%s&hrsofst=%d" % (lon,lat,ndtm,hrsofst)
                res = HttpResponse(location,status=302)
                res['Location'] = location
                return res
