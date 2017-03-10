import cStringIO
from io import BytesIO
import urllib
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus.flowables import Image
from reportlab.platypus import Paragraph, Spacer, KeepTogether
from reportlab.lib import colors
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.units import mm

from theme import DefaultTheme
from util import calc_table_col_widths
from common import *

class RotatedPara(Paragraph):
    def __init__(self, text,style,angle):
#        super(self.__class__, self).__init__(text,style)
        Paragraph.__init__(self,text,style)
        self.angle = angle
    def draw(self): 
#        print dir(self.canv)
        self.canv.saveState() 
        self.canv.translate(50,50) 
        self.canv.rotate(self.angle) 
        Paragraph.draw(self) 
        self.canv.restoreState() 


class Pdf(object):

    story = []    
    theme = DefaultTheme
    
    def __init__(self, title, author):
        self.title = title
        self.author = author
    
    def set_theme(self, theme):
        self.theme = theme
        
    def add(self, flowable):
        self.story.append(flowable)
    
    def add_header(self, text, level=H1):
        p = Paragraph(text, self.theme.header_for_level(level))
        self.add(p)
    
    def add_spacer(self, height_inch=None):
        height_inch = height_inch or self.theme.spacer_height
        self.add(Spacer(1, height_inch)) # magic 1? no, first param not yet implemented by rLab guys
        
    def add_paragraph(self, text, style=None):
        style = style or self.theme.paragraph
        p = Paragraph(text, style)
        self.add(p)

    def add_arrow(self, text, style=None,angl=0):
        style = style or self.theme.paragraph
        p = RotatedPara(text, style,angl)
        print angl
        self.add(p)    
    
    def add_list(self, items, list_style=UL):
        raise NotImplementedError

    def add_route_table(self, rows, width=None, col_widths=None, align=CENTER,extra_style=[]):
        style = self.theme.table_style + extra_style
        if width and col_widths is None: # one cannot spec table width in rLab only col widths
            col_widths = calc_table_col_widths(rows, width) # this helper calcs it for us
#        table = Table(rows, col_widths, style=style, hAlign=align)

        wsp_cw = 10*mm
        wsp_cw1 = 12*mm
        wsp_cw2 = 16*mm
        wsp_cw3 = 18*mm
        wsp_cw4 = 20*mm
        wsp_cw5 = 25*mm
        #                0,     1,      2,         3,       4,      5,      6,      7,      8,         9,     10,     11 
        colWidths=(wsp_cw3, wsp_cw5, wsp_cw, wsp_cw2, wsp_cw1, wsp_cw1, wsp_cw2, wsp_cw, wsp_cw, wsp_cw2, wsp_cw, wsp_cw)        
        table = Table(rows, colWidths, style=style, hAlign=align)
        self.add(table)

    
    def add_table(self, rows, width=None, col_widths=None, align=CENTER,extra_style=[]):
        style = self.theme.table_style + extra_style
        if width and col_widths is None: # one cannot spec table width in rLab only col widths
            col_widths = calc_table_col_widths(rows, width) # this helper calcs it for us
#        table = Table(rows, col_widths, style=style, hAlign=align)

        wsp_cw = 10*mm
        wsp_cw1 = 12*mm
        wsp_cw2 = 16*mm
        wsp_cw3 = 18*mm
        wsp_cw4 = 20*mm
        wsp_cw5 = 25*mm
        #                0,     1,      2,         3,       4,      5,      6,      7,      8,      9,       10,      11,      12,     13    
        colWidths=(wsp_cw3, wsp_cw, wsp_cw2, wsp_cw1, wsp_cw1, wsp_cw2, wsp_cw, wsp_cw, wsp_cw2, wsp_cw, wsp_cw, wsp_cw2, wsp_cw, wsp_cw)        
        table = Table(rows, colWidths, style=style, hAlign=align)
        self.add(table)

    def add_image(self, src, width, height, align=CENTER):
        img = Image(src, width, height)
        img.hAlign = align
        self.add(img)
        
    def add_qrcode(self, data, size=150, align=CENTER):
        "FIXME: ReportLib also supports QR-Codes. Check it out."        
        src = "http://chart.googleapis.com/chart?"
        src += "chs=%sx%s&" % (size, size)
        src += "cht=qr&"
        src += "chl=" + urllib.quote(data)
        self.add_image(src, size, size, align)
    
    def render(self):
        buffer = cStringIO.StringIO()
        doc_template_args = self.theme.doc_template_args()
        doc = SimpleDocTemplate(buffer, title=self.title, author=self.author,**doc_template_args)
        doc.build(self.story)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def renderb(self):
        pbuffer = BytesIO()
        doc_template_args = self.theme.doc_template_args()
        doc = SimpleDocTemplate(pbuffer, title=self.title, author=self.author,pageCompression=True,**doc_template_args)
        doc.build(self.story)
        pdf = pbuffer.getvalue()
        pbuffer.close()
        return pdf


    def render2File(self,fpath):        
        doc_template_args = self.theme.doc_template_args()
        doc = SimpleDocTemplate(fpath, title=self.title, author=self.author,pageCompression=1,**doc_template_args)
        doc.build(self.story)
#        pdf = buffer.getvalue()
#        buffer.close()
#        return pdf