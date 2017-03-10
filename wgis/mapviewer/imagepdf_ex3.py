# Let's import the wrapper
from datetime import timedelta

import reports
from reports.theme import colors, DefaultTheme

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

from django.templatetags.static import static

import math
import datetime

from rangedict import RangeDict


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

def add_2axis_chart():
    from reportlab.graphics.shapes import Drawing,colors
    from reportlab.graphics.widgets.markers import makeMarker
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.charts.lineplots import LinePlot
    from reportlab.graphics.charts.axes import XCategoryAxis,YValueAxis

    drawing = Drawing(400, 200)
    data = [(13, 5, 20, 22, 37, 45, 19, 4)
            ]
    noOfBars=len(data[0])

    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = data

    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 50        
    bc.categoryAxis.categoryNames = ['Jan-99','Feb-99','Mar-99','Apr-99','May-99','Jun-99','Jul-99','Aug-99']
    drawing.add(bc)

    data3=[[(0.5, 4), (1.5, 3), (2.5, 4), (3.5, 6), (4.5, 4), (5.5, 2), (6.5, 5), (7.5, 6)]
           ]

    lp = LinePlot()
    lp.x = bc.x
    lp.y = bc.y
    lp.height = bc.height
    lp.width = bc.width
    lp.data = data3
    lp.joinedLines = 1
    lp.lines[0].symbol = makeMarker('Circle')
    lp.lines[0].strokeColor=colors.blue
    lp.lineLabelFormat = '%2.0f'
    lp.xValueAxis.valueMin = 0
    lp.xValueAxis.valueMax = noOfBars
    lp.yValueAxis.valueMin = 0
    lp.yValueAxis.valueMax = 8
    lp.xValueAxis.visible=False
    lp.yValueAxis.visible=False #Hide 2nd plot its Yaxis
    drawing.add(lp)

    y2Axis = YValueAxis()#Replicate 2nd plot Yaxis in the right
    y2Axis.setProperties(lp.yValueAxis.getProperties())
    y2Axis.setPosition(lp.x+lp.width,lp.y,lp.height)
    y2Axis.tickRight=5
    y2Axis.tickLeft=0

    y2Axis.configure(data3)
    y2Axis.visible=True
    drawing.add(y2Axis)
    return drawing

def get_arrow():
    from reportlab.graphics.shapes import Polygon
    return Polygon([14,8,14,18,11,17,15,22,19,17,16,18,16,8,14,8],
        strokeWidth=1,
        strokeColor=colors.purple,
        fillColor=colors.purple)


def get_base_arrow():    
    bux, buy = 4, 8
    xf, yf = 1, 4
    
    
    pl_coord = [3, 0, 3, 10, 0, 10, 4, 16, 8, 10, 5, 10, 5, 0, 3, 0] 

    pl_arrow = Polygon(pl_coord,
            strokeWidth=1,
            strokeColor=colors.purple,
            fillColor=colors.purple)
    return pl_arrow

def get_arrow_atr2(ba,x,y,r):
    ga = Group(ba)
#    ga.translate(x,y)
    ga.shift(-x-4,-y-8)    
    ga.rotate(r)
    ga.shift(x+4,y+8)
    return ga

def get_wdir_group_label(x,y,r):
    ll = get_wdir_label(x,y-65,r)
    ln = get_label(x,y-80,r,colors.red)
    lg = Group()
    lg.add(ll)
    lg.add(ln)
    return lg

def get_wdir_label(x,y,r):
    from reportlab.graphics.charts.textlabels import Label
    l = Label()    
    l.fontSize = 7
    l.x = x
    l.y = y
    l.setText(dirnotation[r])    # 279E
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

def get_arrow_atr(ba,x,y,r,xg):
    ga = Group(ba)
    nx, ny = x, y
    wangle = dirangnotation[r]

    nx = x + (16.0 * math.sin(math.radians(wangle))/2) + (8.0 * math.sin(math.radians(wangle))/4)
    ny = y - (8.0 * math.cos(math.radians(wangle))/2) - (16.0 * math.cos(math.radians(wangle))/4)
    """
    print wangle
    if wangle==0:
        nx=nx-2
    if wangle==90:
        nx=nx-16
    if wangle==270:
        nx=nx+18
    if wangle==180:
        nx=nx+5
    """    


#    nx = x + (16.0 * math.sin(math.radians(r))/2) + (8.0 * math.sin(math.radians(r))/4)
#    ny = y - (8.0 * math.cos(math.radians(r))/2) - (16.0 * math.cos(math.radians(r))/4)

#    if r >=0 and r<=90:
#        nx = x + (16.0 * math.sin(math.radians(r))/2) + (8.0 * math.sin(math.radians(r))/4)
#        ny = y - (8.0 * math.cos(math.radians(r))/2) - (16.0 * math.cos(math.radians(r))/4)
#    if r>90 and r<180:
#        nx = x + (16.0 * math.sin(math.radians(r))/2) + (8.0 * math.sin(math.radians(r))/4)
#        ny = y - (16.0 * math.cos(math.radians(r))/2) - (8.0 * math.cos(math.radians(r))/4)
#    if r==180:    
#        nx = x + (16.0 * math.sin(math.radians(r))/2) + (8.0 * math.sin(math.radians(r))/4)
#        ny = y - (8.0 * math.cos(math.radians(r))/2) - (16.0 * math.cos(math.radians(r))/4)

#    print r,(x,y)," --> ",(math.sin(math.radians(r)),math.cos(math.radians(r)))," --> ",(nx,ny)
    ga.translate(x,y)    
#    ga.translate(nx,ny)
    ga.rotate(r)
    return ga

def get_arrow_at(x,y,s):    
    bux, buy = 4, 8
    xf, yf = 1, 4
    from reportlab.graphics.shapes import Polygon, Group
    pl_coord = [x-s,y-(s*buy),
                    x-s,y+(s*yf/2),
                    x-(s*bux),y+(s*yf)/2,
                    x,y+(s*buy),
                    x+(s*bux),y+(s*yf)/2,
                    x+s,y+(s*yf/2),
                    x+s,y-(s*buy),
                    x-s,y-(s*buy)]
    print pl_coord
    pl_arrow = Polygon(pl_coord,
            strokeWidth=1,
            strokeColor=colors.purple,
            fillColor=colors.purple)
    ar_g = Group()
    ar_g.add(pl_arrow)
    ar_g.translate()
    ar_g.rotate(45)
    return ar_g


def add_line_chart():
    from reportlab.graphics.charts.linecharts import HorizontalLineChart
    from reportlab.graphics.shapes import Circle
    drawing = Drawing(400, 200)
    data = [
    (13, 5, 20, 22, 37, 45, 19, 4),
    (5, 20, 46, 38, 23, 21, 6, 14)
    ]
    lc = HorizontalLineChart()
    lc.x = 50
    lc.y = 50
    lc.height = 125
    lc.width = 300
    lc.data = data
    lc.joinedLines = 1
    catNames = 'Jan Feb Mar Apr May Jun Jul Aug'.split(' ')
#    rp = reports.Paragraph("<b>Jan24</b>",DefaultTheme.paragraph)
#    catNames = []
#    catNames.append(rp)
    lc.categoryAxis.categoryNames = catNames
    lc.categoryAxis.labels.boxAnchor = 'n'
    lc.categoryAxis.tickDown = 50
    lc.valueAxis.valueMin = 0
    lc.valueAxis.valueMax = 60
    lc.valueAxis.valueStep = 15
    lc.lines[0].strokeWidth = 2
    lc.lines[1].strokeWidth = 1.5
    drawing.add(lc)

    refl = Line(69,0,69,300)
    drawing.add(refl)
    d = 25/2.0
    circle = Circle(10, 10, d)
    circle.strokeColor = colors.red
    circle.fillColor = colors.white

#    drawing.add(circle)
#    drawing.add(get_arrow())
#    drawing.add(get_arrow_at(10,10,1))
    ba = get_base_arrow()

    """
    base_x = 65
    base_y=25
    space_y = 25
    base_angle = 0

    drawing.add(get_arrow_atr(ba, base_x, base_y + (0*space_y),0))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (0*space_y),base_angle + 0))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (1*space_y),base_angle + 15))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (2*space_y),base_angle + 30))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (3*space_y),base_angle + 45))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (4*space_y),base_angle + 60))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (5*space_y),base_angle + 75))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (6*space_y),base_angle + 90))

    refl = Line(129,0,129,300)
    drawing.add(refl)

    base_x = 125
    base_y=25
    space_y = 25
    base_angle = 90
    
    drawing.add(get_arrow_atr(ba, base_x, base_y + (0*space_y),0))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (1*space_y),base_angle + 0))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (2*space_y),base_angle + 15))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (3*space_y),base_angle + 30))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (4*space_y),base_angle + 45))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (5*space_y),base_angle + 60))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (6*space_y),base_angle + 75))
    drawing.add(get_arrow_atr(ba, base_x, base_y + (7*space_y),base_angle + 90))
    """
    
    base_x=65
    space_x = 25
#    drawing.add(get_arrow_atr(ba, base_x + (0*space_x),15,0))
 #   drawing.add(get_arrow_atr(ba, base_x + (0*space_x),15,45))
 #   drawing.add(get_arrow_atr(ba, base_x + (0*space_x),15,90))
 #   drawing.add(get_arrow_atr(ba, base_x + (0*space_x),15,135))
#    drawing.add(get_arrow_atr(ba, base_x + (0*space_x),15,180))
 #   drawing.add(get_arrow_atr(ba, base_x + (0*space_x),15,225))
#    drawing.add(get_arrow_atr(ba, base_x + (0*space_x),15,270))
 #   drawing.add(get_arrow_atr(ba, base_x + (0*space_x),15,315))
#    drawing.add(get_arrow_atr(ba, base_x + (0*space_x),15,360))
    drawing.add(get_arrow_atr(ba, base_x + (0*space_x),15,0))
    drawing.add(get_arrow_atr(ba, base_x + (1*space_x),15,15))
    drawing.add(get_arrow_atr(ba, base_x + (2*space_x),15,30))
    drawing.add(get_arrow_atr(ba, base_x + (3*space_x),15,45))
    drawing.add(get_arrow_atr(ba, base_x + (4*space_x),15,60))
    drawing.add(get_arrow_atr(ba, base_x + (5*space_x),15,75))
    drawing.add(get_arrow_atr(ba, base_x + (6*space_x),15,90))
    drawing.add(get_arrow_atr(ba, base_x + (7*space_x),15,105))
    drawing.add(get_arrow_atr(ba, base_x + (8*space_x),15,120))
    drawing.add(get_arrow_atr(ba, base_x + (9*space_x),15,135))
    drawing.add(get_arrow_atr(ba, base_x + (10*space_x),15,150))
    drawing.add(get_arrow_atr(ba, base_x + (11*space_x),15,165))
    drawing.add(get_arrow_atr(ba, base_x + (12*space_x),15,180))    

    drawing.add(get_arrow_atr(ba, base_x + (0*space_x),45,195))
    drawing.add(get_arrow_atr(ba, base_x + (1*space_x),45,210))
    drawing.add(get_arrow_atr(ba, base_x + (2*space_x),45,225))
    drawing.add(get_arrow_atr(ba, base_x + (3*space_x),45,240))
    drawing.add(get_arrow_atr(ba, base_x + (4*space_x),45,255))
    drawing.add(get_arrow_atr(ba, base_x + (5*space_x),45,270))
    drawing.add(get_arrow_atr(ba, base_x + (6*space_x),45,285))
    drawing.add(get_arrow_atr(ba, base_x + (7*space_x),45,300))
    drawing.add(get_arrow_atr(ba, base_x + (8*space_x),45,315))
    drawing.add(get_arrow_atr(ba, base_x + (9*space_x),45,330))
    drawing.add(get_arrow_atr(ba, base_x + (10*space_x),45,345))
    drawing.add(get_arrow_atr(ba, base_x + (11*space_x),45,360))

#    drawing.add(get_arrow_atr(ba, base_x + (6*space_x),15,0))
#    drawing.add(get_arrow_atr(ba, base_x + (7*space_x),15,270))


    """
    drawing.add(get_arrow_atr(ba, base_x + (1*space_x),15,45))
    drawing.add(get_arrow_atr(ba, base_x + (2*space_x),15,90))
    drawing.add(get_arrow_atr(ba, base_x + (3*space_x),15,135))    
    drawing.add(get_arrow_atr(ba, base_x + (4*space_x),15,180))
    drawing.add(get_arrow_atr(ba, base_x + (5*space_x),15,215))    
    drawing.add(get_arrow_atr(ba, base_x + (6*space_x),15,270))
    drawing.add(get_arrow_atr(ba, base_x + (7*space_x),15,315))    
    drawing.add(get_arrow_atr(ba, base_x + (8*space_x),15,360))
    """
#    drawing.add(get_arrow_at(100,100,3))
    return drawing

def get_route_wspd_10m(wndata,locs):
    wspds = []
    wdirs = []
    wspds10m,wspds_925mb,wspds_975mb,wspds_gust = (),(),(),()        
    days = []
    idx = 0
    for v in wndata:
        ltdate = (v.tmid.tmtimestamp + timedelta(hours=v.tmid.tmfcstvalid))
        olnc, oltc = dd2dms(locs[idx][0]), dd2dms(locs[idx][1])    
        

        date2str = ltdate.strftime("%d-%m")
        catstr = date2str+"\n"+"%02d" % ltdate.hour +"\n\n"+dirnotation[int(v.wnddir_10m)]+"\n\n\n"
        catstr+="%d" % olnc[0]+ u'\N{DEGREE SIGN}' +" %d' E" % olnc[1]
        catstr+="\n"
        catstr+="%d" % oltc[0]+ u'\N{DEGREE SIGN}' +" %d' N" % oltc[1]
        idx = idx + 1

#            days.append(date2str+"\n"+v.town.name)
#        days.append(date2str+"\n"+"06\n\n"+dirnotation[int(v.wnddir_10m)]+"\n\n\n\n"+dirnotation[int(v.wnddir_10m)])
#        days.append(date2str+"\n"+"%02d" % ltdate.hour +"\n\n"+dirnotation[int(v.wnddir_10m)])  #+"\n\n\n\n"+dirnotation[int(v.wnddir_10m)])
        days.append(catstr)  #+"\n\n\n\n"+dirnotation[int(v.wnddir_10m)])
        wspds10m += (int(v.wndspd_10m),)
        wdirs.append(int(v.wnddir_10m))
        wspds_925mb += (int(v.wndspd_925mb),)
        wspds_975mb += (int(v.wndspd_975mb),)
        wspds_gust += (int(v.wndspd_gust),)
    wspds.append(wspds10m)
#    wspds.append(wspds_925mb)
#    wspds.append(wspds_975mb)
    wspds.append(wspds_gust)
    return wspds, days, wdirs


def get_wspd_10m(wndata):
    wspds = []
    wdirs = []
    wspds10m,wspds_925mb,wspds_975mb,wspds_gust = (),(),(),()        
    days = []
    for v in wndata:
        ltdate = (v.tmid.tmtimestamp + timedelta(hours=v.tmid.tmfcstvalid))
        date2str = ltdate.strftime("%d-%m")
#            days.append(date2str+"\n"+v.town.name)
#        days.append(date2str+"\n"+"06\n\n"+dirnotation[int(v.wnddir_10m)]+"\n\n\n\n"+dirnotation[int(v.wnddir_10m)])
        days.append(date2str+"\n"+"%02d" % ltdate.hour +"\n\n"+dirnotation[int(v.wnddir_10m)])  #+"\n\n\n\n"+dirnotation[int(v.wnddir_10m)])
        wspds10m += (int(v.wndspd_10m),)
        wdirs.append(int(v.wnddir_10m))
        wspds_925mb += (int(v.wndspd_925mb),)
        wspds_975mb += (int(v.wndspd_975mb),)
        wspds_gust += (int(v.wndspd_gust),)
    wspds.append(wspds10m)
#    wspds.append(wspds_925mb)
#    wspds.append(wspds_975mb)
    wspds.append(wspds_gust)
    return wspds, days, wdirs

def line_data_label_format(dir):
    return '%2d'

def get_route_wind_graph(wvalues,cats,wdirs):

    """
    for i in range(len(wvalues)):
        wvalues[i] = wvalues[i] + wvalues[i]

    cats = cats + cats
    wdirs = wdirs + wdirs    
    """
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
    chart.categoryAxis.tickDown = 70
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
    legend.y = chart.y - 100
    legend.dx = 10
    legend.dy = 10
    #legend.colorNamePairs  = [(chart.lines[i].strokeColor, chart._catNames[i]) for i in xrange(len(wvalues))]

    chmargin = 30
#    xgap = (chart.width - chmargin)/(len(wvalues[0])-1)
    xgap = chart.width/(len(wvalues[0]))

#    xabase = chmargin + (xgap/2)
    xabase = chart.x + (xgap/2.0)

    print chart.x,chart.width,xgap,xabase
    d.add(legend)
    llabels = ['Wind Speed (10m)']
    ba = get_base_arrow()
    idx = 0
    prevx = 0.5 + xabase
#    DIRB = 135
    print "idx*xgap, xabase + idx*xgap, prevx"
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
    d.add(get_axis_title(chart.x + (chart.width/2),-65,0,"Date/Time"))
    
    d.add(chart)
#        d.add(self.legend_draw(llabels, chart, x=400, y=150, type='line'))
    return d


def get_wind_graph(wvalues,cats,wdirs):

    """
    for i in range(len(wvalues)):
        wvalues[i] = wvalues[i] + wvalues[i]

    cats = cats + cats
    wdirs = wdirs + wdirs    
    """
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
    #legend.colorNamePairs  = [(chart.lines[i].strokeColor, chart._catNames[i]) for i in xrange(len(wvalues))]

    chmargin = 30
#    xgap = (chart.width - chmargin)/(len(wvalues[0])-1)
    xgap = chart.width/(len(wvalues[0]))

#    xabase = chmargin + (xgap/2)
    xabase = chart.x + (xgap/2.0)

    print chart.x,chart.width,xgap,xabase
    d.add(legend)
    llabels = ['Wind Speed (10m)']
    ba = get_base_arrow()
    idx = 0
    prevx = 0.5 + xabase
#    DIRB = 135
    print "idx*xgap, xabase + idx*xgap, prevx"
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


def get_ww3_cdata(wwdata):
    maxval = 0
    wwheights = []
    wwdirs = []
    sw1h, sw2h, ssh, hmax, sw1dir,  sw2dir = (), (), (), (), (), ()      
    days = []
    idx = 0
    for v in wwdata:
        ltdate = (v.tmid.tmtimestamp + timedelta(hours=v.tmid.tmfcstvalid))
        date2str = ltdate.strftime("%d-%m")
        catstr = date2str+"\n"+"%02d" % ltdate.hour +"\n\n"
        dsw1 = v.dsw1_surface
        dsw2 = v.dsw2_surface
        if dsw1 == 999:
            dsw1=0
            catstr+="--\n\n\n\n"
        else:
            catstr+=dirnotation[int(dsw1)]+"\n\n\n\n"

        if dsw2 == 999:
            dsw2=0
            catstr+="--"
        else:
            catstr+=dirnotation[int(dsw2)]

#        days.append(date2str+"\n"+"%02d" % ltdate.hour +"\n\n"+dirnotation[int(dsw1)]+"\n\n\n\n"+dirnotation[int(dsw2)])
        days.append(catstr)
        hsw1 = v.hsw1_surface
        hsw2 = v.hsw2_surface
        htsgw = v.htsgw_surface
        htsgw15=0
        if hsw1 == 999:
            hsw1=0    
        if hsw2 == 999:
            hsw2=0    
        if htsgw == 999:
            htsgw=0
        else:
            htsgw15=float(htsgw)*1.5

        sw1h += (round(hsw1,1),)
        sw2h += (round(hsw2,1),)
        ssh += (round(htsgw,1),)
        hmax += (round(htsgw15,1),)
        sw1dir += (v.dsw1_surface,)
        sw2dir += (v.dsw2_surface,)
    wwheights.append(sw1h)
    wwheights.append(sw2h)
    wwheights.append(ssh)
    wwheights.append(hmax)
    wwdirs.append(sw1dir)
    wwdirs.append(sw2dir)

    return wwheights, days, wwdirs


def get_ww3_route_cdata(wwdata,locs):
    maxval = 0
    wwheights = []
    wwdirs = []
    sw1h, sw2h, ssh, hmax, sw1dir,  sw2dir = (), (), (), (), (), ()      
    days = []
    idx = 0

    for v in wwdata:
        ltdate = (v.tmid.tmtimestamp + timedelta(hours=v.tmid.tmfcstvalid))
        date2str = ltdate.strftime("%d-%m")

        catstr = date2str+"\n"+"%02d" % ltdate.hour +"\n\n"
        dsw1 = v.dsw1_surface
        dsw2 = v.dsw2_surface
        if dsw1 == 999:
            dsw1=0
            catstr+="--\n\n\n\n"
        else:
            catstr+=dirnotation[int(dsw1)]+"\n\n\n\n"

        olnc, oltc = dd2dms(locs[idx][0]), dd2dms(locs[idx][1])    
        coords_text = "%d" % olnc[0]+ u'\N{DEGREE SIGN}' +" %d' N / %d" % (olnc[1],oltc[0])+ u'\N{DEGREE SIGN}' +" %d' E" % oltc[1]
        catstr+="%d" % olnc[0]+ u'\N{DEGREE SIGN}' +" %d' E" % olnc[1]
        catstr+="\n"
        catstr+="%d" % oltc[0]+ u'\N{DEGREE SIGN}' +" %d' N" % oltc[1]
        idx = idx + 1
        """    
        if dsw2 == 999:
            dsw2=0
            catstr+="--"
        else:
            catstr+=dirnotation[int(dsw2)]
        """    
#        days.append(date2str+"\n"+"%02d" % ltdate.hour +"\n\n"+dirnotation[int(dsw1)]+"\n\n\n\n"+dirnotation[int(dsw2)])
        days.append(catstr)
        hsw1 = v.hsw1_surface
        hsw2 = v.hsw2_surface
        htsgw = v.htsgw_surface
        htsgw15=0
        if hsw1 == 999:
            hsw1=0    
        if hsw2 == 999:
            hsw2=0    
        if htsgw == 999:
            htsgw=0
        else:
            htsgw15=float(htsgw)*1.5

        sw1h += (round(hsw1,1),)
        sw2h += (round(hsw2,1),)
        ssh += (round(htsgw,1),)
        hmax += (round(htsgw15,1),)
        sw1dir += (v.dsw1_surface,)
        sw2dir += (v.dsw2_surface,)
    wwheights.append(sw1h)
    #wwheights.append(sw2h)
    wwheights.append(ssh)
    wwheights.append(hmax)
    wwdirs.append(sw1dir)
    wwdirs.append(sw2dir)

    return wwheights, days, wwdirs

def get_ww3_route_graph(wvalues,cats,wdirs):
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
#    chart.lineLabelFormat = '%.1f' #line_data_label_format

    # set color for the plot area border and interior area
#        chart.strokeColor = colors.white
#        chart.fillColor = colors.lightblue
    # set lines color and width
    chart.lines[0].strokeColor = colors.red
    chart.lines[0].strokeWidth = 2
    chart.lines[0].name = "Swell (Hsw)"      
    """
    chart.lines[1].strokeColor = colors.blue
    chart.lines[1].strokeWidth = 2
    chart.lines[1].name = "Swell 2 (Hsw2)"
    """
    chart.lines[1].strokeColor = colors.green
    chart.lines[1].strokeWidth = 2
    chart.lines[1].name = "Sea+Swell (Hs)"
    
    chart.lines[2].strokeColor = colors.orange
    chart.lines[2].strokeWidth = 2
    chart.lines[2].name = "Hmax"

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
    chart._seriesCount = 3

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
    """    
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
    """    

    d.add(get_chart_title(chart.x + (chart.width/2),chart.height+20,0,"Seas Graphs"))    
    d.add(get_axis_title(5,chart.y + (chart.height/2),90,"Height (meters)"))
    d.add(get_axis_title(chart.x + (chart.width/2),-80,0,"Date/Time"))
    
    d.add(get_axis_subtitle(15,chart.y - 30,0,"Dir"))
    d.add(get_axis_subtitle(15,chart.y - 40,0,"Swell"))
    d.add(get_axis_subtitle(15,chart.y - 60,0,"Lon"))
    d.add(get_axis_subtitle(15,chart.y - 70,0,"Lat"))


    """
    d.add(get_axis_subtitle(15,chart.y - 60,0,"Dir"))
    d.add(get_axis_subtitle(15,chart.y - 70,0,"Swell 2"))
    """

    d.add(chart)

    return d


def get_ww3_graph(wvalues,cats,wdirs):
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
#    chart.lineLabelFormat = '%.1f' #line_data_label_format

    # set color for the plot area border and interior area
#        chart.strokeColor = colors.white
#        chart.fillColor = colors.lightblue
    # set lines color and width
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

def dd2dms(dd):
    d = int(dd)
    m = int((dd-d)*60)
    s = int(dd-d-m/60) * 3600
    return (d,m,s)

# this is a helper in my controller

def weather_report_pdf(dc, weather_history, ww_hs,fname,sw_fname,rloc,dtm=None):
    # and define a constant
    TABLE_WIDTH = 480 # this you cannot do in rLab which is why I wrote the helper initially

    # then let's extend the Default theme. I need more space so I redefine the margins
    # also I don't want tables, etc to break across pages (allowSplitting = False)
    # see http://www.reportlab.com/docs/reportlab-userguide.pdf



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

    # Report generation Timestamp and validity Details
    base_forecast = weather_history[0].tmid.tmtimestamp.strftime("%a %d-%b-%Y %H:%M LT")   #datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')
    report_base_fcst = reports.Paragraph("Report issued at : <b>" + base_forecast +"</b>",MyTheme.paragraph)

#    print report_base_fcst
    report_gen_ts = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
    report_gen_ts = weather_history[0].tmid.tmtimestamp.strftime("%b %d %Y %H:%M:%S")
#    print report_gen_ts
    rv_para = {}
    rv_para['hrs']='120'
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

    """
    tdata = [Paragraph("Time(LT)", styles['Right']),
        Paragraph("10m", styles['Center']),"",
        Paragraph("925mb", styles['Center']),"",
        Paragraph("975mb", styles['Center']),"",
        Paragraph("Gust", styles['Center'])]
    table_data.append(tdata)
    """

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


    if weather_history:
        for idx,sobj in enumerate(weather_history):
            ltdate = (sobj.tmid.tmtimestamp + timedelta(hours=sobj.tmid.tmfcstvalid))
            wvhgt = ww_hs[idx].wvhgt_surface
            wvper = ww_hs[idx].wvper_surface
            dsw1 = ww_hs[idx].dsw1_surface
            hsw1 = ww_hs[idx].hsw1_surface
            tsw1 = ww_hs[idx].tsw1_surface
            dsw2 = ww_hs[idx].dsw2_surface
            hsw2 = ww_hs[idx].hsw2_surface
            tsw2 = ww_hs[idx].tsw2_surface
            htsgw = ww_hs[idx].htsgw_surface
            htsgw15='*'

            if wvhgt == 999:
                wvhgt='*'
            else:
                wvhgt = round(wvhgt,1) 

            if wvper == 999:
                wvper='*'
            else:
                wvper=round(wvper,1)        

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

            if htsgw == 999:
                htsgw='*'
            else:
                htsgw=round(float(htsgw),1)
                htsgw15=htsgw*1.5
                htsgw15=round(htsgw15,1)

            table_data.append([ltdate.strftime("%a %d %H"),
                dirnotation[sobj.wnddir_10m],int(sobj.wndspd_10m),
                int(sobj.wndspd_gust),
                wvhgt,wvper,dsw1,hsw1,tsw1,dsw2,hsw2,tsw2,htsgw,htsgw15
#                round(wvhgt,1),round(wvper,1),dirnotation[dsw1],round(hsw1,1),round(tsw1,1),dirnotation[dsw2],round(hsw2,1),round(tsw2,1),round(htsgw,1),round(htsgw15,1)
#                ,
#                sobj.wndspd_925mb,dirnotation[sobj.wnddir_925mb],
#                sobj.wndspd_975mb,dirnotation[sobj.wnddir_975mb]
                ])
            """
            table_data.append([sobj.tmid.tmtimestamp.strftime("%a %d/%m"),
                sobj.wndspd_10m,Paragraph(dirnotation[sobj.wnddir_10m], styles['Center']),
                sobj.wndspd_925mb,Paragraph(dirnotation[sobj.wnddir_925mb], styles['Center']),
                sobj.wndspd_975mb,Paragraph(dirnotation[sobj.wnddir_975mb], styles['Center']),
                sobj.wndspd_gust])
            """
    """    
    if ww_hs:
        for idx,wwobj in enumerate(ww_hs):
            if wwobj.wvhgt_surface != 999999:
                table_data[idx].append(wwobj.wvhgt_surface)
            else:
                table_data[idx].append(0)
            if wwobj.wvper_surface != 999999:
                table_data[idx].append(wwobj.wvhgt_surface)
            else:
                table_data[idx].append(0)
    """            
    doc.add(Paragraph("Tabular Forecast Data", styles['ContentTitle']))
    doc.add_spacer()
    doc.add_table(table_data)
    
    doc.add_spacer()
    
    doc.add(PageBreak())

    doc.add_spacer()
    doc.add_spacer()

    if weather_history:
        wspds, days, wdirs = get_wspd_10m(weather_history)
        wsp_chart = get_wind_graph(wspds,days,wdirs)
        doc.add_spacer()
        doc.add(wsp_chart)
    
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()

    if ww_hs:
        wwheights, days, wsdirs = get_ww3_cdata(ww_hs)
        sg_chart = get_ww3_graph(wwheights, days, wsdirs)

#        doc.add(Paragraph("Wind Graphs", styles['ContentTitle']))
        doc.add_spacer()
        doc.add(sg_chart)


    import os

    doc.add(PageBreak())

    doc.add_spacer()
    

    #doc.add_header("Temprature 2m " + u'\N{DEGREE SIGN}' + "C & 10m Wind (Knots)",reports.H4)

#    doc.add(Paragraph("Pressure (" + u'\N{DEGREE SIGN}' + "C ) & 10m Wind (Knots)", styles['ContentTitle']))    
#    ctitle = "%s/%s/%s %s:00" % (dtm[:2],dtm[2:4],dtm[4:])
    print dtm
    doc.add(Paragraph(" MSL Pressure (mb)  & 10m Wind (Knots) 10/10/2016 12:00", styles['ContentTitle']))    
#    iurl ="http://localhost:8000/synergymapviewer/media/media/images/sg_prw.png"    
    iurl ="http://localhost:8000/synergymapviewer/media/media/images/" + fname
    doc.add_image(iurl, 500, 350, reports.CENTER)

    doc.add_spacer()
    

    doc.add(Paragraph("Significant Wave Height (meter) 10/10/2016 12:00", styles['ContentTitle']))
#    swaveurl ="http://localhost:8000/synergymapviewer/media/media/images/sg_swave.png"    
    swaveurl ="http://localhost:8000/synergymapviewer/media/media/images/" + sw_fname

    doc.add_image(swaveurl, 500, 350, reports.CENTER)
    

    """
    arrow_sym = u'\u27B5'
    arrow_syms = {} 
    arrow_syms['ars'] = arrow_sym
#    arrow_line = reports.Paragraph("%(ars)s" % arrow_syms,MyTheme.arrow_style)
    arrow_img = reports.Paragraph('<img src="http://localhost:8000/synergymapviewer/media/media/images/ua.png" width="15" height="15"/>',MyTheme.arrow_style)

#    doc.add(arrow_line)
    doc.add_spacer()
    doc.add_spacer()
#    doc.add_paragraph(arrow_sym,MyTheme.arrow_style)
#    doc.add(arrow_img)
    doc.add_spacer()  
    doc.add(add_line_chart())  
    doc.add_spacer()
#    doc.add(add_2axis_chart())

    doc.render2File("reporttheme.pdf")
    """
    return doc.renderb()


def route_weather_report_pdf(dc, weather_history, ww_hs, orgn, dest, vs, hvalid, locs):
    # and define a constant
    TABLE_WIDTH = 480 # this you cannot do in rLab which is why I wrote the helper initially

    # then let's extend the Default theme. I need more space so I redefine the margins
    # also I don't want tables, etc to break across pages (allowSplitting = False)
    # see http://www.reportlab.com/docs/reportlab-userguide.pdf

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
            ('BACKGROUND', (0, 1), ( 6, 1), colors.HexColor(0x93A8A9)),
            ('BACKGROUND', (7, 1), ( -1, 1), colors.HexColor(0x8ED2C9)),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor(0x93A8A9)),
            ('SPAN',(2,0),(4,0)),       # Wind 10m (Knots)
            ('SPAN',(5,0),(11,0)),       # Seas (m)
            ('SPAN',(1,0),(1,2)),       # Coordinates
            ('SPAN',(0,1),(0,2)),       # Time (LT)
            ('SPAN',(2,1),(2,2)),       # Dir
            ('SPAN',(3,1),(3,2)),       # Avg Speed (10m)
            ('SPAN',(4,1),(4,2)),       # Gusts (10m)
            ('SPAN',(5,1),(5,2)),       # Wind Sea Hs
            ('SPAN',(6,1),(6,2)),       # Period (s)
            ('SPAN',(7,1),(9,1)),       # Swell 1
            ('SPAN',(10,1),(11,1)),      # Swell 2
#            ('SPAN',(12,1),(13,1)),     # Sea + Swell            
#            ('ALIGN', (2,3), (2,-1), 'DECIMAL'),
#            ('ALIGN', (3,3), (3,-1), 'DECIMAL'),
#            ('ALIGN', (5,3), (5,-1), 'DECIMAL'),
#            ('ALIGN', (7,3), (7,-1), 'DECIMAL'),            
            ('HALIGN', (1, 3), (1, -1), 'CENTER'),            
#            ('RIGHTPADDING', (1,3), (1,-1), 10),
#            ('RIGHTPADDING', (3,3), (3,-1), 10),
#            ('RIGHTPADDING', (5,3), (5,-1), 10),
#            ('RIGHTPADDING', (7,3), (7,-1), 10),
            ('BOTTOMPADDING', (0,3), (11,-1), 0),
            ('BOTTOMPADDING', (0,0), (11,2), 0),
            ('FONTSIZE',(0,3),(11,-1),6),
            ('ALIGN', (0,3), (11,-1), 'CENTER'),
            ('VALIGN', (0,3), (11,-1), 'MIDDLE')]

            
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
    olnc,oltc = dd2dms(locs[0][0]), dd2dms(locs[0][1])  
    dlnc,dltc = dd2dms(locs[len(locs)-1][0]), dd2dms(locs[len(locs)-1][1])  
#    print olnc,oltc,dlnc,dltc
    
    orgn_coords = "Origin : <b>%d" % olnc[0]+ u'\N{DEGREE SIGN}' +" %d' %d\" E / %d" % (olnc[1],olnc[2],oltc[0])+ u'\N{DEGREE SIGN}' +" %d' %d\" N</b>" % (oltc[1],oltc[2])
    dest_coords = "Destination : <b>%d"% dlnc[0]+ u'\N{DEGREE SIGN}' +" %d' %d\" E / %d" % (dlnc[1],dlnc[2],dltc[0])+ u'\N{DEGREE SIGN}' +" %d' %d\" N</b>" % (dltc[1],dltc[2]) 
    origin = reports.Paragraph(orgn_coords,MyTheme.paragraph)
    destination = reports.Paragraph(dest_coords,MyTheme.paragraph)    
    doc.add(reports.Table([[origin,destination]], style=[('VALIGN', (0,0), (-1,-1), 'TOP'),('BOX', (0, 0), (-1, -1), 0.5, colors.black)]))

    vspeed = reports.Paragraph("Vessel Speed : <b>%.2f</b> Knots" % vs,MyTheme.paragraph)
    doc.add(reports.Table([[vspeed]], style=[('VALIGN', (0,0), (-1,-1), 'TOP'),('BOX', (0, 0), (-1, -1), 0.5, colors.black)]))

    """
    origin = reports.Paragraph("Origin : <b>40"+ u'\N{DEGREE SIGN}' +" 58' 45.32\" N / 70"+ u'\N{DEGREE SIGN}' +" 34' 12.34\" E</b>",MyTheme.paragraph)
    destination = reports.Paragraph("Destination : <b>40"+ u'\N{DEGREE SIGN}' +" 58' 45.32\" N / 70"+ u'\N{DEGREE SIGN}' +" 34' 12.34\" E</b>",MyTheme.paragraph)
    doc.add(reports.Table([[origin,destination]], style=[('VALIGN', (0,0), (-1,-1), 'TOP'),('BOX', (0, 0), (-1, -1), 0.5, colors.black)]))
    """

    doc.add_spacer()

    # Report generation Timestamp and validity Details
    base_forecast = weather_history[0].tmid.tmtimestamp.strftime("%a %d-%b-%Y %H:%M LT")   #datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')
    report_base_fcst = reports.Paragraph("Report issued at : <b>" + base_forecast +"</b>",MyTheme.paragraph)
#    print report_base_fcst
    report_gen_ts = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
    report_gen_ts = weather_history[0].tmid.tmtimestamp.strftime("%b %d %Y %H:%M:%S")
#    print report_gen_ts
    rv_para = {}
    rv_para['hrs']= str(hvalid)
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
    theader = [Paragraph("Day /", styles['Left']),Paragraph("Coordinates", styles['Center']),Paragraph("Wind 10m (Knots)", styles['Center']),"","",Paragraph("Seas (m)", styles['Center'])]
    table_data.append(theader)

    # Row 1
    tdata = [Paragraph("Time(LT)", styles['Right']),                # 0th Column
        "",
        Paragraph("Dir", styles['TableSubHeader']),                    # 1st Column
        Paragraph("Avg Speed<br/>(10 m)", styles['TableSubHeader']),   # 2nd Column
        Paragraph("Gusts<br/>(10 m)", styles['TableSubHeader']),       # 3rd Column
        Paragraph("Wind sea Hs", styles['TableSubHeader']),            # 4th Column
        Paragraph("Period( s)", styles['TableSubHeader']),             # 5th Column
        Paragraph("Swell", styles['TableSubHeader']),                # 6th Column
        "",                                                         
        "",
        Paragraph("Sea + Swell", styles['TableSubHeader']),                # 9th Column        
        ""
#        ,
#        "",
#        Paragraph("Sea + Swell", styles['TableSubHeader'])            # 12th Column
        ]

    table_data.append(tdata)

    # Row 2
    tdata = ["","","","","","","",
        Paragraph("Dir", styles['TableSubHeader']),
        Paragraph("Hsw", styles['TableSubHeader']),
        Paragraph("Period(s)", styles['TableSubHeader']),
#        Paragraph("Dir2", styles['TableSubHeader']),
#        Paragraph("Hsw2", styles['TableSubHeader']),
#        Paragraph("Period2(s)", styles['TableSubHeader']),
        Paragraph("Hs tot", styles['TableSubHeader']),
        Paragraph("Hmax", styles['TableSubHeader'])]

    table_data.append(tdata)

    loc_texts = []
    if weather_history:
        for idx,sobj in enumerate(weather_history):
            ltdate = (sobj.tmid.tmtimestamp + timedelta(hours=sobj.tmid.tmfcstvalid))
            wvhgt = ww_hs[idx].wvhgt_surface
            wvper = ww_hs[idx].wvper_surface
            dsw1 = ww_hs[idx].dsw1_surface
            hsw1 = ww_hs[idx].hsw1_surface
            tsw1 = ww_hs[idx].tsw1_surface
            dsw2 = ww_hs[idx].dsw2_surface
            hsw2 = ww_hs[idx].hsw2_surface
            tsw2 = ww_hs[idx].tsw2_surface
            htsgw = ww_hs[idx].htsgw_surface
            htsgw15='*'

            if wvhgt == 999:
                wvhgt='*'
            else:
                wvhgt = round(wvhgt,1) 

            if wvper == 999:
                wvper='*'
            else:
                wvper=round(wvper,1)        

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

            if htsgw == 999:
                htsgw='*'
            else:
                htsgw=round(float(htsgw),1)
                htsgw15=htsgw*1.5
                htsgw15=round(htsgw15,1)
            olnc, oltc = dd2dms(locs[idx][0]), dd2dms(locs[idx][1])    
            coords_text = "%d" % olnc[0]+ u'\N{DEGREE SIGN}' +" %d' E / %d" % (olnc[1],oltc[0])+ u'\N{DEGREE SIGN}' +" %d' N" % oltc[1]    
            table_data.append([ltdate.strftime("%a %d / %H"),coords_text,
                dirnotation[sobj.wnddir_10m],int(sobj.wndspd_10m),
                int(sobj.wndspd_gust),
#                "","","","","","","","","",""
#                wvhgt,wvper,dsw1,hsw1,tsw1,dsw2,hsw2,tsw2,htsgw,htsgw15
                wvhgt,wvper,dsw1,hsw1,tsw1,htsgw,htsgw15
                ])
    doc.add(Paragraph("Tabular Route Forecast Data", styles['ContentTitle']))
    doc.add_spacer()
    doc.add_route_table(table_data)
    
    doc.add(PageBreak())

    doc.add_spacer()
    doc.add_spacer()

    if weather_history:
        wspds, days, wdirs = get_route_wspd_10m(weather_history,locs)
        wsp_chart = get_route_wind_graph(wspds,days,wdirs)
        doc.add_spacer()
        doc.add(wsp_chart)
    
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()
    doc.add_spacer()

    if ww_hs:
        wwheights, days, wsdirs = get_ww3_route_cdata(ww_hs,locs)
        sg_chart = get_ww3_route_graph(wwheights, days, wsdirs)
        doc.add_spacer()
        doc.add(sg_chart)

    doc.add(PageBreak())

    doc.add_spacer()

    doc.add(Paragraph(" MSL Pressure (mb)  & 10m Wind (Knots) 10/10/2016 12:00", styles['ContentTitle']))    
    iurl ="http://localhost:8000/synergymapviewer/media/media/images/sg_prw_route.png"    
    doc.add_image(iurl, 500, 350, reports.CENTER)

    doc.add_spacer()
    

    doc.add(Paragraph("Significant Wave Height (meter) 10/10/2016 12:00", styles['ContentTitle']))
    swaveurl ="http://localhost:8000/synergymapviewer/media/media/images/sg_swave_route.png"    
    doc.add_image(swaveurl, 475, 350, reports.CENTER)

    return doc.renderb()



#if __name__ == "__main__":
#    if weather_report_pdf(None, None) is None:
#        print "Error"
#    else:
#        print "PDF Generated"
