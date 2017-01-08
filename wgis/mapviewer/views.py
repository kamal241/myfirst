from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from weather_data import *
from raster_data import get_pres_msl_contour, get_contours
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
	print dtm
	wjson_data = get_weather_data(lt1, lt2, ln1, ln2, dtm)
	return HttpResponse(wjson_data,content_type='application/json')

def weather_raster(request):
	lt1, lt2, ln1, ln2 = 20,21,70,75
	dtm = request.GET.get('dtm')
	lt1 = float(request.GET.get('lt1'))
	lt2 = float(request.GET.get('lt2'))
	ln1 = float(request.GET.get('ln1'))
	ln2 = float(request.GET.get('ln2'))
	wjson_data = get_contours(lt1, lt2, ln1, ln2, dtm,4)
	return HttpResponse(wjson_data,content_type='application/json')	