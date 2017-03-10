from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import date
from weather_data import *
from weather_swave import *
from raster_data import get_pres_msl_contour, get_contours, get_multi_contours
from generate_cp import get_ws10prmsl, get_swh
from mapviewer.synreports import *

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
	wsjson_data = get_swave_data(lt1, lt2, ln1, ln2, dtm)
	return HttpResponse(wsjson_data,content_type='application/json')	


def reports_location(request):
	response = HttpResponse(content_type='application/pdf')
        today = date.today()
        filename = 'Location_Weather_Report_' + today.strftime('%Y-%m-%d')
        response['Content-Disposition'] =  'attachement; filename={0}.pdf'.format(filename)
        t=request.GET['dtm']
#        fv= int(request.GET['fv'])
        lat = float(request.GET['lat'])
        lon = float(request.GET['lon'])
	"""
        rlat, rlon = round(lat*2)/2, round(lon*2)/2
        target_loc = Point(lon,lat)
        rtarget_loc = Point(rlon,rlat)

        ln1,ln2,lt1,lt2 = lon-5,lon+5,lat-5,lat+5
        fname = get_ws10prmsl(ln1,lt1,lt2,ln2,t,fv)
        swhgt_fname = get_swh(ln1,lt1,lt2,ln2,t,fv)
#       print fpath

        wsn = SynForecastLocation.objects.filter(lcpt__dwithin=(target_loc,0.1768),wdtid=1)
        twnlcid = wsn[0].lcid
        wwn = SynForecastLocation.objects.filter(lcpt__dwithin=(rtarget_loc,0.1767),wdtid=1)
        twwlcid = wwn[0].lcid
        ftm = datetime.datetime.strptime(t,"%Y%m%d%H")
        response = HttpResponse(content_type='application/pdf')
        today = date.today()
        filename = 'pdf_demo' + today.strftime('%Y-%m-%d')
        response['Content-Disposition'] =  'attachement; filename={0}.pdf'.format(filename)
        buffer = BytesIO()
#       report = PdfPrint(buffer, 'A4')
#       stms = SynForecastTimestamp.objects.filter(tmtimestamp__range=["2016-09-14","2016-09-25"])
        hrs = range(6,121,6)
#       wndstms = SynForecastTimestamp.objects.filter(tmtimestamp='2016-11-19 06:00:00',tmfcstvalid__in=hrs,wdtid=1)
#       wndata = SynForecastWindParameter.objects.filter(lcid=283403,tmid__in=wndstms).order_by('tmid__tmfcstvalid')
        wndstms = SynForecastTimestamp.objects.filter(tmtimestamp=ftm,tmfcstvalid__in=hrs,wdtid=1)
        wndata = SynForecastWindParameter.objects.filter(lcid=twnlcid,tmid__in=wndstms).order_by('tmid__tmfcstvalid')
#       print len(wndata)
#       wwstms = SynForecastTimestamp.objects.filter(tmtimestamp='2016-11-19 06:00:00',tmfcstvalid__in=hrs,wdtid=2) $
#       wwdata = SynForecastWw3Parameter.objects.filter(lcid=283403,tmid__in=wwstms).order_by('tmid__tmfcstvalid')
        wwstms = SynForecastTimestamp.objects.filter(tmtimestamp=ftm,tmfcstvalid__in=hrs,wdtid=2)
        wwdata = SynForecastWw3Parameter.objects.filter(lcid=twwlcid,tmid__in=wwstms).order_by('tmid__tmfcstvalid')
#        wpdf = weather_report_pdf("", wndata, wwdata,fname,swhgt_fname,(lon,lat),ftm)
	"""
        dt = t[:8]
        tm = t[8:]
        wpdf = weather_report_pdf((lon,lat),dt,tm)#"", wndata, wwdata,fname,swhgt_fname,(lon,lat),ftm) 
        if wpdf is None:
                print "WPDF Error"
        else:
                print "WPDF Success"
        response.write(wpdf)
        return response
