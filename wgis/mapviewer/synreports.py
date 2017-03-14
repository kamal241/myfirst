import math
import datetime
from datetime import timedelta

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table,TableStyle
from reportlab.lib.units import mm
from reportlab.platypus import *

from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.linecharts import SampleHorizontalLineChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib import colors
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.shapes import Line, Polygon, Group

import reports
from reports.theme import colors, DefaultTheme

from rangedict import RangeDict

from read_data_at_latlon import *

d = {(0.00, 11.25): 'N',(11.25, 33.75): 'NNE', (33.75, 56.25): 'NE',(56.25, 78.75): 'ENE', (78.75, 101.25): 'E',
    (101.25, 123.75): 'ESE', (123.75, 146.25): 'SE', (146.25, 168.75): 'SSE',  (168.75, 191.25): 'S',
     (191.25, 213.75): 'SSW', (213.75, 236.25): 'SW', (236.25, 258.75): 'WSW', (258.75, 281.25): 'W',
     (281.25, 303.75): 'WNW',(303.75, 326.25): 'NW',(326.25, 348.75): 'NNW', (348.75, 361.00): 'N'}

dn = {'N': 0.0, 'NNE': 22.5, 'NE': 45.0, 'ENE': 67.5,
        'E': 90.0, 'ESE': 112.5, 'SE': 135.0, 'SSE': 157.5,
        'S': 180.0, 'SSW': 202.5, 'SW': 225.0, 'WSW': 247.5,
        'W': 270.0, 'WNW': 292.5, 'NW': 315.0, 'NNW': 337.5}

dan = {(0.00, 11.25): 0,
        (11.25, 33.75): 337.5,
        (33.75, 56.25): 315,
        (56.25, 78.75): 292.5,
        (78.75, 101.25): 270,           # 270 : W
        (101.25, 123.75): 247.5,
        (123.75, 146.25): 225,
        (146.25, 168.75): 202.5,
        (168.75, 191.25): 180,
        (191.25, 213.75): 157.5,
        (213.75, 236.25): 135,
        (236.25, 258.75): 112.5,
        (258.75, 281.25): 90,           # 90 : E
        (281.25, 303.75): 67.5,
        (303.75, 326.25): 45,
        (326.25, 348.75): 22.5,
        (348.75, 360.00): 0}

dirnotation = RangeDict(d)
dirangnotation = RangeDict(dan)

class RotatedPara(Paragraph):
    def __init__(self, text, style, angle):
        Paragraph.__init__(self, text, style)
        self.angle = angle
    def draw(self):
        self.canv.saveState()
        self.canv.translate(0,0)
        self.canv.rotate(self.angle)
        Paragraph.draw(self)
        self.canv.restoreState()

def get_base_arrow():    
    bux, buy = 4, 8
    xf, yf = 1, 4
    
    
    pl_coord = [3, 0, 3, 10, 0, 10, 4, 16, 8, 10, 5, 10, 5, 0, 3, 0] 

    pl_arrow = Polygon(pl_coord,
            strokeWidth=1,
            strokeColor=colors.purple,
            fillColor=colors.purple)
    return pl_arrow


def dd2dms(dd):
    d = int(dd)
    m = int((dd-d)*60)
    s = int(dd-d-m/60) * 3600
    return (d,m,s)

def get_label(x,y,r,c):
    from reportlab.graphics.charts.textlabels import Label

    l = Label()
    
    l.fontSize = 11

    l.x = x
    l.y = y
#    l.strokeColor = colors.green
    l.fillColor = c
    if r>360 or r<0:
        l.setText(u'--')    # 279E
    else:
        l.setText(u'\u2191')    # 279E
        l.angle=dn[dirnotation[360-r]]
#    s = String(150,100, 'Hello World',fontSize=18, fillColor=colors.red)    
    return l

def get_chart_title(x,y,r,t):
    from reportlab.graphics.charts.textlabels import Label
    l = Label()
    l.angle=r
    l.fontSize = 12
    l.x = x
    l.y = y
#    l.fillColor = colors.red
    l.setText(t)
#    s = String(150,100, 'Hello World',fontSize=18, fillColor=colors.red)    
    return l

def get_axis_subtitle(x,y,r,t):
    from reportlab.graphics.charts.textlabels import Label
    l = Label()
    l.angle=r
    l.fontSize = 7
    l.x = x
    l.y = y
#    l.fillColor = colors.red
    l.setText(t)
#    s = String(150,100, 'Hello World',fontSize=18, fillColor=colors.red)    
    return l


def get_axis_title(x,y,r,t):
    from reportlab.graphics.charts.textlabels import Label
    l = Label()
    l.angle=r
    l.fontSize = 9
    l.x = x
    l.y = y
#    l.fillColor = colors.red
    l.setText(t)
#    s = String(150,100, 'Hello World',fontSize=18, fillColor=colors.red)    
    return l

def get_wspd_10m(wndata):
    wspds = []
    wdirs = []
    wspds10m,wspds_gust = (),()        
    days = []
    for wind_raw in wndata:
	gust = wind_raw['gust']
        ws_10m = wind_raw['ws_10m']
        wd_10m = wind_raw['wd_10m']
        ltdate = wind_raw['timestamp']
        date2str = ltdate.strftime("%d-%m")
        days.append(date2str+"\n"+"%02d" % ltdate.hour +"\n\n"+dirnotation[int(wd_10m)])
        wspds10m += (int(ws_10m),)
        wdirs.append(int(wd_10m))
        wspds_gust += (int(gust),)
    wspds.append(wspds10m)
    wspds.append(wspds_gust)
    return wspds, days, wdirs

def get_ww3_cdata(swell,seawave):
    maxval = 0
    wwheights = []
    wwdirs = []
    sw1h, sw2h, ssh, hmax, sw1dir,  sw2dir = (), (), (), (), (), ()      
    days = []
    idx = 0
    if swell:
        for swell_raw,seawave_raw in zip(swell,seawave):
            ltdate = swell_raw['timestamp']
	    date2str = ltdate.strftime("%d-%m")
	    catstr = date2str+"\n"+"%02d" % ltdate.hour +"\n\n"

            htsgw = seawave_raw['swhs']
            htsgw15 = 0
            if htsgw == 999:
                htsgw=0
            else:
                htsgw=round(float(htsgw),1)
                htsgw15=htsgw*1.5
                htsgw15=round(htsgw15,1)

            dsw1 = swell_raw['dsw1']
            hsw1 = swell_raw['hsw1']
            dsw2 = swell_raw['dsw2']
            hsw2 = swell_raw['hsw2']

            if dsw1 == 999:
#                dsw1=0
                catstr+="--\n\n\n\n\n"
            else:
                catstr+=dirnotation[dsw1]+"\n\n\n\n"

            if hsw1 == 999:
                hsw1=0
            else:
                hsw1=round(hsw1,1)

            if dsw2 == 999:
#                dsw2=0
		catstr+="--"
            else:
                catstr+=dirnotation[dsw2]+"\n\n\n\n"

            if hsw2 == 999:
                hsw2=0
            else:
                hsw2=round(hsw2,1)

	    days.append(catstr)
            sw1h += (round(hsw1,1),)
            sw2h += (round(hsw2,1),)
            ssh += (round(htsgw,1),)
            hmax += (round(htsgw15,1),)
            sw1dir += (dsw1,)
            sw2dir += (dsw2,)
    wwheights.append(sw1h)
    wwheights.append(sw2h)
    wwheights.append(ssh)
    wwheights.append(hmax)
    wwdirs.append(sw1dir)
    wwdirs.append(sw2dir)
    return wwheights, days, wwdirs



def get_wind_graph(wvalues,cats,wdirs):
    d = Drawing(0, 200)
    # draw line chart
    chart = SampleHorizontalLineChart()
#        chart._catNames = '10 m', '925 mb'
    # set width and height
    chart.width = 480
    chart.height = 180
    chart.x = 30
    # set data values
    chart.data = wvalues #[(1,2,3,4,5,6,7,8,9,10,11)]
    # use(True) or not(False) line between points
    chart.joinedLines = True
    # set font desired
#    chart.lineLabels.fontName = 'FreeSans'
#    chart.lineLabelFormat = '%2d' #line_data_label_format

    # set color for the plot area border and interior area
#        chart.strokeColor = colors.white
#        chart.fillColor = colors.lightblue
    # set lines color and width
    chart.lines[0].strokeColor = colors.red
    chart.lines[0].strokeWidth = 2
    chart.lines[0].name = "10m"      
    """
    chart.lines[1].strokeColor = colors.blue
    chart.lines[1].strokeWidth = 2
    chart.lines[1].name = "925mb"
    chart.lines[2].strokeColor = colors.green
    chart.lines[2].strokeWidth = 2
    chart.lines[2].name = "975mb "
    """
    chart.lines[1].strokeColor = colors.orange
    chart.lines[1].strokeWidth = 2
    chart.lines[1].name = "Gust"

    # set symbol for points
    
    chart.lines.symbol = makeMarker('Circle')
    
    #chart.categoryAxis.labels.angle = 45
    #chart.categoryAxis.labels.boxAnchor = 'ne'

    chart.categoryAxis.categoryNames = cats
    chart.categoryAxis.visibleGrid = 1
    chart.categoryAxis.gridStrokeDashArray = (0.3,1)
    chart.categoryAxis.gridStrokeWidth = 0.25
    chart.categoryAxis.tickUp = 5
    chart.categoryAxis.tickDown = 50
    chart.categoryAxis.labels.fontSize = 6
    chart.categoryAxis.labels.textAnchor = 'middle'
    chart.categoryAxis.visibleLabels = 1
    

    chart.valueAxis.visibleGrid = 1
    chart.valueAxis.gridStrokeDashArray = (0.3,1)
    chart.valueAxis.gridStrokeWidth = 0.25
    chart.valueAxis.valueStep = 2
    chart.valueAxis.valueMin = 0
    chart.valueAxis.visibleLabels = 1
    chart.valueAxis.labels.fontSize = 6
#    chart.valueAxis.labelTextFormat = '%2d'
#    chart.xValueAxis.labelTextFormat = '%2d'
    chart.valueAxis.valueMax = math.ceil(max(max(wvalues)) * 1.1)
    chart._seriesCount = 2

    from reportlab.graphics.charts.legends import Legend
    from reportlab.lib.validators import Auto
    legend = Legend()
    legend.colorNamePairs   =  Auto(obj=chart)
    legend.fontName         = 'Helvetica'
    legend.fontSize         = 10
    legend.alignment        ='right'
    legend.columnMaximum    = 1
    legend.dxTextSpace      = 5
    legend.variColumn       = 1
    legend.autoXPadding     = 15
    legend.boxAnchor = 'sw'
    legend.x = chart.width/2    
    legend.y = chart.y - 80
    legend.dx = 10
    legend.dy = 10

    chmargin = 30
#    xgap = (chart.width - chmargin)/(len(wvalues[0])-1)
    xgap = chart.width/(len(wvalues[0]))

#    xabase = chmargin + (xgap/2)
    xabase = chart.x + (xgap/2.0)

    #print chart.x,chart.width,xgap,xabase
    d.add(legend)
    llabels = ['Wind Speed (10m)']
    ba = get_base_arrow()
    idx = 0
    prevx = 0.5 + xabase
#    DIRB = 135
    #print "idx*xgap, xabase + idx*xgap, prevx"
    for wdir in wdirs:
#        d.add(get_arrow_atr(ba, xabase + idx*xgap,chart.y - 80,wdir,xgap))
#        d.add(get_label(xabase + idx*xgap,chart.y - 70,wdir))
#        print idx * xgap, xabase + idx*xgap, prevx
        if wdir>90 and wdir<270:
            d.add(get_label(prevx + 1,chart.y - 40,(wdir+180)%360,colors.red))
#`           d.add(get_label(prevx + 1,chart.y - 60,(DIRB + idx*22.5)%360)
        else:
            d.add(get_label(prevx,chart.y - 40,(wdir+180)%360,colors.red))
#            d.add(get_label(prevx,chart.y - 60,(DIRB + idx*22.5)%360))
#        d.add(get_label(prevx,chart.y - 40,wdir))   
           
        #prevx = prevx + xgap + (idx*0.2%2.0)
        prevx = prevx + xgap #+ (idx*0.2%2.0)
#        d.add(get_label(chart.categoryAxis.labels[idx].x,chart.y - 40,wdir))        
#        d.add(get_label(chart.x,chart.y - 40,wdir))
#        d.add(get_label(chart.width,chart.y - 40,wdir))
#        d.add(get_label(chart.x+chart.width,chart.y - 40,wdir))
#        d.add(get_wdir_label(xabase + idx*xgap,chart.y - 60,wdir))
#        d.add(get_wdir_group_label(xabase + idx*xgap,chart.y,wdir))
        idx = idx+1
        
    d.add(get_chart_title(chart.x + (chart.width/2),chart.height+20,0,"Wind Graphs"))    
    d.add(get_axis_title(5,chart.y + (chart.height/2),90,"Wind Speed (Knots)"))
    d.add(get_axis_title(chart.x + (chart.width/2),-45,0,"Date/Time"))
    
    d.add(chart)
#        d.add(self.legend_draw(llabels, chart, x=400, y=150, type='line'))
    return d

def get_ww3_graph(wvalues,cats,wdirs):
    #print wdirs
    d = Drawing(0, 200)
    # draw line chart
    chart = SampleHorizontalLineChart()
#        chart._catNames = '10 m', '925 mb'
    # set width and height
    chart.width = 480
    chart.height = 180
    chart.x = 30
    # set data values
    chart.data = wvalues #[(1,2,3,4,5,6,7,8,9,10,11)]
    # use(True) or not(False) line between points
    chart.joinedLines = True
    # set font desired
    chart.lines[0].strokeColor = colors.red
    chart.lines[0].strokeWidth = 2
    chart.lines[0].name = "Swell 1 (Hsw1)"      
    
    chart.lines[1].strokeColor = colors.blue
    chart.lines[1].strokeWidth = 2
    chart.lines[1].name = "Swell 2 (Hsw2)"
    
    chart.lines[2].strokeColor = colors.green
    chart.lines[2].strokeWidth = 2
    chart.lines[2].name = "Sea+Swell (Hs)"
    
    chart.lines[3].strokeColor = colors.orange
    chart.lines[3].strokeWidth = 2
    chart.lines[3].name = "Hmax"

    # set symbol for points
    
    chart.lines.symbol = makeMarker('Circle')


    chart.categoryAxis.categoryNames = cats
    chart.categoryAxis.visibleGrid = 1
    chart.categoryAxis.gridStrokeDashArray = (0.3,1)
    chart.categoryAxis.gridStrokeWidth = 0.25
    chart.categoryAxis.tickUp = 5
    chart.categoryAxis.tickDown = 80
    chart.categoryAxis.labels.fontSize = 6
    chart.categoryAxis.labels.textAnchor = 'middle'
    chart.categoryAxis.visibleLabels = 1
    

    chart.valueAxis.visibleGrid = 1
    chart.valueAxis.valueMax = math.ceil(max(max(wvalues)) * 1.1)
    chart.valueAxis.gridStrokeDashArray = (0.3,1)
    chart.valueAxis.gridStrokeWidth = 0.25
    chart.valueAxis.valueStep = 0.5
    chart.valueAxis.valueMin = 0
    chart.valueAxis.visibleLabels = 1
    chart.valueAxis.labels.fontSize = 6
    chart._seriesCount = 4

    from reportlab.graphics.charts.legends import Legend
    from reportlab.lib.validators import Auto
    legend = Legend()
    legend.colorNamePairs   =  Auto(obj=chart)
    legend.fontName         = 'Helvetica'
    legend.fontSize         = 10
    legend.alignment        ='right'
    legend.columnMaximum    = 1
    legend.dxTextSpace      = 5
    legend.variColumn       = 1
#    legend.autoXPadding     = 15
    legend.boxAnchor = 's'
    legend.y = chart.y - 120
    legend.x = chart.width/2
#    legend.dx = 10
    legend.dy = 10

    d.add(legend)

    chmargin = 30
    xgap = chart.width/(len(wvalues[0]))

    xabase = chart.x + (xgap/2.0)
    
    idx = 0
    prevx = 0.5 + xabase

    for wdir in wdirs[0]:
        if wdir > 360:
            d.add(get_label(prevx + 1,chart.y - 40,wdir,colors.red))
        else:
            if wdir>90 and wdir<270:
                d.add(get_label(prevx + 1,chart.y - 40,(wdir+180)%360,colors.red))
            else:
                d.add(get_label(prevx,chart.y - 40,(wdir+180)%360,colors.red))
           
        prevx = prevx + xgap 
        idx = idx+1

    idx = 0
    prevx = 0.5 + xabase

    for wdir in wdirs[1]:
        if wdir > 360:
            d.add(get_label(prevx + 1,chart.y - 70,wdir,colors.blue))
        else:
            if wdir>90 and wdir<270:
                d.add(get_label(prevx + 1,chart.y - 70,(wdir+180)%360,colors.blue))
            else:
                d.add(get_label(prevx,chart.y - 70,(wdir+180)%360,colors.blue))
           
        prevx = prevx + xgap 
        idx = idx+1


    d.add(get_chart_title(chart.x + (chart.width/2),chart.height+20,0,"Seas Graphs"))    
    d.add(get_axis_title(5,chart.y + (chart.height/2),90,"Height (meters)"))
    d.add(get_axis_title(chart.x + (chart.width/2),-80,0,"Date/Time"))
    
    d.add(get_axis_subtitle(15,chart.y - 30,0,"Dir"))
    d.add(get_axis_subtitle(15,chart.y - 40,0,"Swell 1"))
    d.add(get_axis_subtitle(15,chart.y - 60,0,"Dir"))
    d.add(get_axis_subtitle(15,chart.y - 70,0,"Swell 2"))


    d.add(chart)

    return d

def weather_report_pdf(rloc,dt,tm,fname,sw_fname,dayfcst=2):#dc, weather_history, ww_hs,fname,sw_fname,rloc,dtm=None):
    # and define a constant
    TABLE_WIDTH = 480 # this you cannot do in rLab which is why I wrote the helper initially
	
    # then let's extend the Default theme. I need more space so I redefine the margins
    # also I don't want tables, etc to break across pages (allowSplitting = False)
    # see http://www.reportlab.com/docs/reportlab-userguide.pdf
    hrsfcst = dayfcst *24

    wind_data = get_gfs_data_at_lat_lon_idx(rloc[0],rloc[1],dt,tm,hrsfcst)
#    print wind_data[0]
    swell,seawave = get_ww3_data_at_lat_lon_idx(rloc[0],rloc[1],dt,tm,hrsfcst)
#    print len(wind_data),len(swell),len(seawave)
#    print "SWELL"
#    print swell
#    print "SEAWAVE"
#    print seawave
#    print swell[0]
#    print seawave[0]
    class MyTheme(DefaultTheme):
        doc = {
            'leftMargin': 25,
            'rightMargin': 25,
            'topMargin': 20,
            'bottomMargin': 25,
            'allowSplitting': False            
            }

        table_style2 = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('VALIGN', (0, 1), (-1, 1), 'MIDDLE'),
            ('VALIGN', (0, 2), (-1, 2), 'MIDDLE'),             
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(0xEDBD3E)),
            ('SPAN',(1,0),(3,0)),
            ('SPAN',(4,0),(7,0)),
            ('SPAN',(0,1),(0,2)),
            ('SPAN',(1,1),(2,1)),
            ('SPAN',(3,1),(4,1)),
            ('SPAN',(5,1),(6,1)),
            ('ALIGN', (1,3), (1,-1), 'DECIMAL'),
            ('ALIGN', (3,3), (3,-1), 'DECIMAL'),
            ('ALIGN', (5,3), (5,-1), 'DECIMAL'),
            ('ALIGN', (7,3), (7,-1), 'DECIMAL'),            
            ('HALIGN', (1, 3), (1, -1), 'CENTER'),            
            ('RIGHTPADDING', (1,3), (1,-1), 20),
            ('RIGHTPADDING', (3,3), (3,-1), 20),
            ('RIGHTPADDING', (5,3), (5,-1), 20),
            ('RIGHTPADDING', (7,3), (7,-1), 20)]

        table_style = [('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.75, colors.black),
#            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
#            ('VALIGN', (0, 1), (-1, 1), 'MIDDLE'),
#            ('VALIGN', (0, 2), (-1, 2), 'MIDDLE'),             
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(0xEDBD3E)),
            ('BACKGROUND', (0, 1), ( 5, 1), colors.HexColor(0x93A8A9)),
            ('BACKGROUND', (6, 1), ( -1, 1), colors.HexColor(0x8ED2C9)),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor(0x93A8A9)),
            ('SPAN',(1,0),(3,0)),       # Wind 10m (Knots)
            ('SPAN',(4,0),(13,0)),       # Seas (m)
            ('SPAN',(0,1),(0,2)),       # Time (LT)
            ('SPAN',(1,1),(1,2)),       # Dir
            ('SPAN',(2,1),(2,2)),       # Avg Speed (10m)
            ('SPAN',(3,1),(3,2)),       # Gusts (10m)
            ('SPAN',(4,1),(4,2)),       # Wind Sea Hs
            ('SPAN',(5,1),(5,2)),       # Period (s)
            ('SPAN',(6,1),(8,1)),       # Swell 1
            ('SPAN',(9,1),(11,1)),      # Swell 2
            ('SPAN',(12,1),(13,1)),     # Sea + Swell            
#            ('ALIGN', (2,3), (2,-1), 'DECIMAL'),
#            ('ALIGN', (3,3), (3,-1), 'DECIMAL'),
#            ('ALIGN', (5,3), (5,-1), 'DECIMAL'),
#            ('ALIGN', (7,3), (7,-1), 'DECIMAL'),            
            ('HALIGN', (1, 3), (1, -1), 'CENTER'),            
#            ('RIGHTPADDING', (1,3), (1,-1), 10),
#            ('RIGHTPADDING', (3,3), (3,-1), 10),
#            ('RIGHTPADDING', (5,3), (5,-1), 10),
#            ('RIGHTPADDING', (7,3), (7,-1), 10),
            ('BOTTOMPADDING', (0,3), (13,-1), 0),
            ('BOTTOMPADDING', (0,0), (13,2), 0),
            ('FONTSIZE',(0,3),(13,-1),6),
            ('ALIGN', (0,3), (13,-1), 'CENTER'),
            ('VALIGN', (0,3), (13,-1), 'MIDDLE')]

    # let's create the doc and specify title and author
    doc = reports.Pdf('Weather Report', 'Synergy Wave')

    # now we apply our theme
    doc.set_theme(MyTheme)

    # give me some space
    doc.add_spacer()
    
    # this header defaults to H1
    doc.add_header('Synergy Wave',reports.H2)

    dc = {'name':'Synergy Wave','add1':'57 Mohamed Sultan Road', 'add2':'#01-05 Sultan Link','city':'Singapore 238997','tel': '+65 6593 9419','mob': '+65 9752 3209','email':'p.dupuis@synergy-wave.com','web':'www.synergy-wave.com'}

#   <b>%(name)s</b><br/>        
#   %(add1)s<br/>
#   %(add2)s<br/>
#   %(city)s<br/>


    address = reports.Paragraph("""Tel  : %(tel)s<br/>
        Mob  : %(mob)s<br/>
        Email: %(email)s<br/>
        %(web)s<br/>""" % dc, MyTheme.paragraph) 

    doc.add(address) 
    doc.add_spacer()

    # Location Details
    location_name = reports.Paragraph("Location : <b>Singapore</b>",MyTheme.paragraph)
    ln_dms, lt_dms = dd2dms(rloc[0]),dd2dms(rloc[1])
    ln_sym, lt_sym = 'E','N'
    if rloc[0]<0:
        ln_sym = 'W'
    else:
        ln_sym = 'E'

    if rloc[1]<0:
        lt_sym = 'S'
    else:
        lt_sym = 'N'

    lc_st = "Coordinates : <b>%d" % ln_dms[0]+ u'\N{DEGREE SIGN}' +" %d' %d\" %s / %d" % (ln_dms[1],ln_dms[2],ln_sym,lt_dms[0])+ u'\N{DEGREE SIGN}' +" %d' %d\" %s</b>" % (lt_dms[1],lt_dms[2],lt_sym)

#    print lc_st
    location_coord = reports.Paragraph(lc_st, MyTheme.paragraph)
#    location_coord = reports.Paragraph("Coordinates : <b>40"+ u'\N{DEGREE SIGN}' +" 58' 45.32\" N / 70"+ u'\N{DEGREE SIGN}' +" 34' 12.34\" E</b>",MyTheme.paragraph)
    doc.add(reports.Table([[location_name,location_coord]], style=[('VALIGN', (0,0), (-1,-1), 'TOP'),('BOX', (0, 0), (-1, -1), 0.5, colors.black)]))
    doc.add_spacer()

    base_forecast = wind_data[0]['timestamp'].strftime("%a %d-%b-%Y %H:%M LT")   #datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')
    report_base_fcst = reports.Paragraph("Report issued at : <b>" + base_forecast +"</b>",MyTheme.paragraph)

#    print report_base_fcst
    report_gen_ts = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
    report_gen_ts = wind_data[0]['timestamp'].strftime("%b %d %Y %H:%M:%S")
#    print report_gen_ts
    rv_para = {}
    rv_para['hrs']='%d' % hrsfcst
    rv_para['rgt']=report_gen_ts
    report_validity = reports.Paragraph("<b>Valid %(hrs)s </b>hours from : <b>%(rgt)s</b>" % rv_para,MyTheme.paragraph)
#    print report_validity
    doc.add(reports.Table([[report_base_fcst,report_validity]], style=[('VALIGN', (0,0), (-1,-1), 'TOP'),('BOX', (0, 0), (-1, -1), 0.5, colors.black)]))
#    doc.add(reports.Table([[report_validity]], style=[('VALIGN', (0,0), (-1,-1), 'TOP'),('BOX', (0, 0), (-1, -1), 0.5, colors.black)]))
    doc.add_spacer()

    # a collection of styles offer by the library
    styles = getSampleStyleSheet()
    # add custom paragraph style
    styles.add(ParagraphStyle(name="TableHeader", fontSize=8, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="TableSubHeader", fontSize=6, alignment=TA_CENTER))
#    styles.add(ParagraphStyle(name="TableSubHeader", fontSize=6))
    styles.add(ParagraphStyle(name="ParagraphTitle", fontSize=11, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name="ContentTitle", fontSize=11, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name="Center", fontSize=6, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="Left", fontSize=6, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name="Right", fontSize=6, alignment=TA_RIGHT))

    # list used for elements added into document
    data = []
    table_data = []

    # Row 0
    theader = [Paragraph("Day /", styles['Left']),Paragraph("Wind 10m (Knots)", styles['Center']),"","",Paragraph("Seas (m)", styles['Center'])]
    table_data.append(theader)

    # Row 1
    tdata = [Paragraph("Time(LT)", styles['Right']),                # 0th Column
        Paragraph("Dir", styles['TableSubHeader']),                    # 1st Column
        Paragraph("Avg Speed<br/>(10 m)", styles['TableSubHeader']),   # 2nd Column
        Paragraph("Gusts<br/>(10 m)", styles['TableSubHeader']),       # 3rd Column
        Paragraph("Wind sea Hs", styles['TableSubHeader']),            # 4th Column
        Paragraph("Period( s)", styles['TableSubHeader']),             # 5th Column
        Paragraph("Swell 1", styles['TableSubHeader']),                # 6th Column
        "",                                                         
        "",
        Paragraph("Swell 2", styles['TableSubHeader']),                # 9th Column        
        "",
        "",
        Paragraph("Sea + Swell", styles['TableSubHeader']),            # 12th Column
        ""]

    table_data.append(tdata)

    # Row 2
    tdata = ["","","","","","",
        Paragraph("Dir1", styles['TableSubHeader']),
        Paragraph("Hsw1", styles['TableSubHeader']),
        Paragraph("Period1(s)", styles['TableSubHeader']),
        Paragraph("Dir2", styles['TableSubHeader']),
        Paragraph("Hsw2", styles['TableSubHeader']),
        Paragraph("Period2(s)", styles['TableSubHeader']),
        Paragraph("Hs tot", styles['TableSubHeader']),
        Paragraph("Hmax", styles['TableSubHeader'])]

    table_data.append(tdata)

    if wind_data:
	for wind_raw,swell_raw,seawave_raw in zip(wind_data,swell,seawave):
	    gust = wind_raw['gust']
	    ws_10m = wind_raw['ws_10m']
	    wd_10m = wind_raw['wd_10m']
	    ltdate = wind_raw['timestamp']
            wvhgt = seawave_raw['shww']
	    wvper = seawave_raw['mpww']
	    htsgw = seawave_raw['swhs']
	    htsgw15 = '*'
#            wvper = ww_hs[idx].wvper_surface
#            htsgw = ww_hs[idx].htsgw_surface
#            htsgw15='*'
            if wvhgt == 999:
                wvhgt='*'
            else:
                wvhgt = round(wvhgt,1) 

            if wvper == 999:
                wvper='*'
            else:
                wvper=round(wvper,1) 

            if htsgw == 999:
                htsgw='*'
            else:
                htsgw=round(float(htsgw),1)
                htsgw15=htsgw*1.5
                htsgw15=round(htsgw15,1)


            dsw1 = swell_raw['dsw1']
            hsw1 = swell_raw['hsw1']
            tsw1 = swell_raw['tsw1']
            dsw2 = swell_raw['dsw2']
            hsw2 = swell_raw['hsw2']
            tsw2 = swell_raw['tsw2']

            if dsw1 == 999:
                dsw1='*' 
            else:   
                dsw1=dirnotation[dsw1]

            if hsw1 == 999:
                hsw1='*'    
            else:   
                hsw1=round(hsw1,1)

            if tsw1 == 999:
                tsw1='*'    
            else:   
                tsw1=round(tsw1,1)

            if dsw2 == 999:
                dsw2='*'    
            else:   
                dsw2=dirnotation[dsw2]

            if hsw2 == 999:
                hsw2='*'    
            else:   
                hsw1=round(hsw2,1)

            if tsw2 == 999:
                tsw2='*'    
            else:   
                tsw2=round(tsw2,1)

            table_data.append([ltdate.strftime("%a %d %H"),
                dirnotation[wd_10m],int(ws_10m),
                int(gust),
#                "","",dsw1,hsw1,tsw1,dsw2,hsw2,tsw2,"",""
		wvhgt,wvper,dsw1,hsw1,tsw1,dsw2,hsw2,tsw2,htsgw,htsgw15
#                round(wvhgt,1),round(wvper,1),dirnotation[dsw1],round(hsw1,1),round(tsw1,1),dirnotation[dsw2],round(hsw2,1),round(tsw2,1),round(htsgw,1),round(htsgw15,1)
#                ,
#                sobj.wndspd_925mb,dirnotation[sobj.wnddir_925mb],
#                sobj.wndspd_975mb,dirnotation[sobj.wnddir_975mb]
                ])

    doc.add(Paragraph("Tabular Forecast Data", styles['ContentTitle']))
    doc.add_spacer()
    doc.add_table(table_data)
    
    doc.add_spacer()

    doc.add(PageBreak())

    doc.add_spacer()
    doc.add_spacer()

    if wind_data:
        wspds, days, wdirs = get_wspd_10m(wind_data)
        wsp_chart = get_wind_graph(wspds,days,wdirs)
        doc.add_spacer()
        doc.add(wsp_chart)
    
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()

    if swell:
	wwheights, days, swsdirs = get_ww3_cdata(swell,seawave)
        sg_chart = get_ww3_graph(wwheights, days, swsdirs)
        doc.add_spacer()
        doc.add(sg_chart)

    print "Report Images"
    print fname, sw_fname

    doc.add(PageBreak())

    doc.add_spacer()

    doc.add(Paragraph(" MSL Pressure (mb)  & 10m Wind (Knots) %s " % datetime.datetime.strftime(datetime.datetime.strptime(dt+tm,'%Y%m%d%H'),'%d/%m/%Y %H:%M'), styles['ContentTitle']))    
    iurl ="http://localhost:8000/mapviewer/media/media/images/" + fname    
    doc.add_image(iurl, 500, 350, reports.CENTER)

    doc.add_spacer()

    doc.add(Paragraph("Significant Wave Height (meter) %s " % datetime.datetime.strftime(datetime.datetime.strptime(dt+tm,'%Y%m%d%H'),'%d/%m/%Y %H:%M'), styles['ContentTitle']))
    swaveurl ="http://localhost:8000/mapviewer/media/media/images/" + sw_fname    
    doc.add_image(swaveurl, 475, 350, reports.CENTER)

    return doc.renderb()
