"""One-page, four-column steel sections table: No., Section, Grade, Total length (EN / AR headings)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
import os
OUT = os.path.dirname(os.path.abspath(__file__))   # .../roof/offer, wherever the repo is checked out
def dejavu(name):   # DejaVu TTF: the system font on Linux, otherwise the copy shipped with matplotlib
    p = '/usr/share/fonts/truetype/dejavu/' + name
    if os.path.exists(p): return p
    import matplotlib; return os.path.join(matplotlib.get_data_path(), 'fonts', 'ttf', name)
pdfmetrics.registerFont(TTFont('DV', dejavu('DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DV-B', dejavu('DejaVuSans-Bold.ttf')))
def ar(t): return '<br/>'.join(get_display(arabic_reshaper.reshape(x)) for x in t.split('|'))
NAVY = colors.HexColor('#1f3a5f')
en = ParagraphStyle('en', fontName='DV', fontSize=10.5, leading=13.5)
enb = ParagraphStyle('enb', parent=en, fontName='DV-B')
enc = ParagraphStyle('enc', parent=en, alignment=1)
hd = ParagraphStyle('hd', fontName='DV-B', fontSize=10, leading=13, alignment=1)
ttl = ParagraphStyle('t', fontName='DV-B', fontSize=13, leading=16, textColor=NAVY)
ttl_ar = ParagraphStyle('ta', fontName='DV-B', fontSize=13, leading=17, textColor=NAVY, alignment=2)
small = ParagraphStyle('s', fontName='DV', fontSize=8.5, leading=11, textColor=colors.HexColor('#444444'))
small_ar = ParagraphStyle('sa', fontName='DV', fontSize=9.5, leading=12.5, textColor=colors.HexColor('#444444'), alignment=2)

rows = [('HEA 140', 'S275 JR', '79.2 m'), ('IPE 300', 'S275 JR', '64.9 m'), ('IPE 330', 'S275 JR', '13.7 m'), ('IPE 240', 'S275 JR', '144.6 m'),
        ('Z 200 x 2.0 cold-formed (purlins)', 'S350GD + Z275', '217 m'), ('L 70 x 70 x 7', 'S275 JR', '73.1 m'), ('Round bar M24, threaded', 'Grade 8.8', '167.8 m'),
        ('SHS 90 x 90 x 8', 'S275 J0H', '5.5 m'), ('Round bar dia 60', 'S355 J2', '1.2 m'), ('Rebar dia 16, threaded end', 'B500B', '47 m'),
        ('Plates 8 to 20 mm', 'S275 JR', 'by weight')]
def H(e, a): return Paragraph(e + '<br/>' + ar(a), hd)
data = [[H('No.', 'م'), H('Section', 'القطاع'), H('Grade', 'الدرجة'), H('Total length', 'الطول الإجمالي')]]
for i, (s, g, L) in enumerate(rows, 1):
    data.append([Paragraph(str(i), enc), Paragraph(s, enb), Paragraph(g, en), Paragraph(L, enc)])
data.append([Paragraph('', en), Paragraph('Total &nbsp; ' + ar('الإجمالي'), enb), Paragraph('', en), Paragraph('<b>760 m, 12.2 t</b>', enc)])
t = Table(data, colWidths=[16*mm, 78*mm, 44*mm, 46*mm], repeatRows=1)
t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#8a8a8a')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e3ebf4')), ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f2f2f2')),
                       ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5), ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
sty = [('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]
head = Table([[Paragraph('STEEL SECTIONS LIST<br/>Steel roof - Administration Building,<br/>Regatta Tourist Village, Tripoli', ttl),
               Paragraph(ar('قائمة القطاعات الحديدية|السقف الحديدي - المبنى الإداري|قرية ريقاطة السياحية، طرابلس'), ttl_ar)]], colWidths=[100*mm, 84*mm], style=sty)
sub = Table([[Paragraph('Design Rev 7 (reduced roofed area, 316 m2), 29 Sep 2026; no detailing yet.<br/>Issued by Eng. MALEK ABOZRAIG, malek.abozraig@gmail.com.', small),
              Paragraph(ar('التصميم مراجعة 7 (مساحة السقف المخفضة 316 م2)|29 سبتمبر 2026 - قبل التفصيل - إعداد: م. مالك أبوزريق'), small_ar)]], colWidths=[100*mm, 84*mm], style=sty)
foot = Table([[Paragraph('Lengths are net member lengths from the member schedule; add cutting and connection allowances for ordering. Plates, keys and anchors add 2.5 t; the offer total is 14.7 t. Wall girts (270 m Z200) are not included: the wall system is open. Hot-dip galvanised to EN ISO 1461 or shop-primed and painted as agreed; cold-formed sections pre-galvanised Z275.', small),
               Paragraph(ar('الأطوال صافية من جدول العناصر؛|تضاف نسبة للقطع والوصلات عند الطلب.|الصفائح والمفاتيح والأسياخ تضيف 2.5 طن؛|إجمالي العرض 14.7 طن.|مدادات الجدران (270 م) غير مشمولة:|نظام الجدران مفتوح.|جلفنة بالغمس الساخن وفق EN ISO 1461|أو دهان بالورشة حسب الاتفاق؛|القطاعات المشكلة على البارد مجلفنة مسبقاً Z275.'), small_ar)]], colWidths=[100*mm, 84*mm], style=sty)
story = [head, Spacer(1, 6), sub, Spacer(1, 12), t, Spacer(1, 12), foot]
doc = SimpleDocTemplate(OUT + '/Steel_sections_list_4col_EN_AR_Rev7.pdf', pagesize=A4, leftMargin=13*mm, rightMargin=13*mm, topMargin=15*mm, bottomMargin=15*mm,
                        title='Steel sections list - steel roof, Regatta Tourist Village', author='Eng. MALEK ABOZRAIG')
doc.build(story)
import pymupdf
d = pymupdf.open(OUT + '/Steel_sections_list_4col_EN_AR_Rev7.pdf'); print('pages', len(d)); d[0].get_pixmap(dpi=110).save(OUT + '/preview_sections_list4_rev7.png')
