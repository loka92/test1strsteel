"""One-page list of steel sections: section, grade, total length (EN / AR)."""
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
OUT = '/home/user/test1strsteel/roof/offer'
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DV-B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
def ar(t): return '<br/>'.join(get_display(arabic_reshaper.reshape(x)) for x in t.split('|'))
NAVY = colors.HexColor('#1f3a5f')
en = ParagraphStyle('en', fontName='DV', fontSize=9.5, leading=12)
enb = ParagraphStyle('enb', parent=en, fontName='DV-B')
arp = ParagraphStyle('ar', fontName='DV', fontSize=10.5, leading=13, alignment=2)
arb = ParagraphStyle('arb', parent=arp, fontName='DV-B')
ttl = ParagraphStyle('t', fontName='DV-B', fontSize=13, leading=16, textColor=NAVY)
ttl_ar = ParagraphStyle('ta', fontName='DV-B', fontSize=13.5, leading=17, textColor=NAVY, alignment=2)
small = ParagraphStyle('s', fontName='DV', fontSize=8, leading=10.5, textColor=colors.HexColor('#444444'))
small_ar = ParagraphStyle('sa', fontName='DV', fontSize=9, leading=12, textColor=colors.HexColor('#444444'), alignment=2)

# section, arabic use, grade, total length m, kg/m
rows = [
    ('HEA 140', 'أعمدة', 'الأعمدة وعمود الرياح', 'S275 JR (EN 10025-2)', 99.9, 24.7),
    ('IPE 300', 'كمرات', 'الكمرات الرئيسية وكمرات الطنف', 'S275 JR (EN 10025-2)', 82.7, 42.2),
    ('IPE 330', 'كمرة', 'الكمرة الرئيسية P13', 'S275 JR (EN 10025-2)', 9.8, 49.1),
    ('IPE 240', 'عوارض', 'العوارض المائلة وكمرات الحافة', 'S275 JR (EN 10025-2)', 204.4, 30.7),
    ('Z 200 x 2.0 (cold-formed)', 'مدادات', 'مدادات السقف والجدران', 'S350GD + Z275 (EN 10346)', 571.0, 5.9),
    ('L 70 x 70 x 7', 'شكالات', 'شكالات الجدران (X)', 'S275 JR (EN 10025-2)', 103.8, 7.4),
    ('Round bar M24 (threaded rod)', 'قضبان', 'قضبان شكالات السقف', 'Grade 8.8 (EN ISO 898-1)', 188.6, 3.55),
    ('SHS 90 x 90 x 8', 'مفاتيح', 'مفاتيح القص عند القواعد', 'S275 J0H (EN 10210)', 7.0, 20.0),
    ('Round bar dia 60', 'مفاتيح', 'مفاتيح القص الجانبية', 'S355 J2 (EN 10025-2)', 1.5, 22.2),
    ('Rebar dia 16 (threaded end)', 'أسياخ', 'أسياخ تثبيت القواعد', 'B500B (EN 10080)', 63.0, 1.58),
    ('Plates 8 - 20 mm', 'صفائح', 'صفائح القواعد والوصلات', 'S275 JR (EN 10025-2)', None, None),
]
use_en = {'HEA 140': 'Columns and wind post', 'IPE 300': 'Primary and eave beams', 'IPE 330': 'Primary beam P13 (9.8 m span)',
          'IPE 240': 'Rafters, edge beams, trimmer, truss posts', 'Z 200 x 2.0 (cold-formed)': 'Roof purlins and wall girts',
          'L 70 x 70 x 7': 'Wall X-bracing', 'Round bar M24 (threaded rod)': 'Roof plane bracing rods', 'SHS 90 x 90 x 8': 'Shear keys at the bases',
          'Round bar dia 60': 'Edge shear keys', 'Rebar dia 16 (threaded end)': 'Post-installed base anchors', 'Plates 8 - 20 mm': 'Base, cap, fin and gusset plates'}
data = [[Paragraph('No.', enb), Paragraph('Section', enb), Paragraph('Used for', enb), Paragraph(ar('الاستخدام'), arb), Paragraph('Steel grade', enb), Paragraph('Total length m', enb), Paragraph('Weight t', enb)]]
Ltot = 0.0; Wtot = 0.0
for i, (sec, _, ause, grade, L, kg) in enumerate(rows, 1):
    w = None if L is None else L * kg / 1000.0
    if L: Ltot += L
    if w: Wtot += w
    data.append([Paragraph(str(i), en), Paragraph(sec, enb), Paragraph(use_en[sec], en), Paragraph(ar(ause), arp), Paragraph(grade, en),
                 Paragraph('' if L is None else '%.1f' % L, en), Paragraph('' if w is None else '%.2f' % w, en)])
data.append([Paragraph('', en), Paragraph('Total', enb), Paragraph('all sections above', en), Paragraph(ar('الإجمالي'), arb), Paragraph('', en),
             Paragraph('%.0f' % Ltot, enb), Paragraph('%.1f' % Wtot, enb)])
t = Table(data, colWidths=[9*mm, 50*mm, 56*mm, 72*mm, 46*mm, 20*mm, 20*mm], repeatRows=1)
t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#8a8a8a')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e3ebf4')), ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f2f2f2')),
                       ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
head = [[Paragraph('STEEL SECTIONS LIST - STEEL ROOF, ADMINISTRATION BUILDING,<br/>REGATTA TOURIST VILLAGE, TRIPOLI', ttl),
         Paragraph(ar('قائمة القطاعات الحديدية|السقف الحديدي - المبنى الإداري|قرية ريقاطة السياحية، طرابلس'), ttl_ar)]]
sub = [[Paragraph('Design Rev 6a, drawings RTV-ST-S00 to S06, 29 Sep 2026. Issued by Eng. MALEK ABOZRAIG, malek.abozraig@gmail.com. Lengths are net member lengths from the member schedule; add cutting and connection allowances for ordering.', small),
        Paragraph(ar('التصميم مراجعة 6a، الرسومات RTV-ST-S00 إلى S06، 29 سبتمبر 2026.|إعداد: م. مالك أبوزريق.|الأطوال صافية من جدول العناصر؛ تضاف نسبة للقطع والوصلات عند الطلب.'), small_ar)]]
sty = [('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]
story = [Table(head, colWidths=[150*mm, 123*mm], style=sty), Spacer(1, 4), Table(sub, colWidths=[150*mm, 123*mm], style=sty), Spacer(1, 8), t, Spacer(1, 4),
         Table([[Paragraph('Sections above 17.8 t; with plates, keys and anchors 3.3 t the bill-of-materials total is 22.2 t.', small), Paragraph(ar('القطاعات أعلاه 17.8 طن؛ مع الصفائح والمفاتيح والأسياخ 3.3 طن|يكون إجمالي جدول الكميات 22.2 طن.'), small_ar)]], colWidths=[150*mm, 123*mm], style=sty), Spacer(1, 6),
         Table([[Paragraph('Surface protection: hot-dip galvanising to EN ISO 1461 (or shop primer + two-coat paint system as agreed); cold-formed sections pre-galvanised Z275. Bolts M20 / M16 / M12 grade 8.8 hot-dip galvanised, quantities on drawing S06.', small),
                 Paragraph(ar('الحماية السطحية: جلفنة بالغمس الساخن وفق EN ISO 1461|أو دهان أساس بالورشة مع طبقتين حسب الاتفاق.|القطاعات المشكلة على البارد مجلفنة مسبقاً Z275.|المسامير M20 / M16 / M12 درجة 8.8 مجلفنة؛ الكميات في الرسم S06.'), small_ar)]],
               colWidths=[150*mm, 123*mm], style=sty)]
doc = SimpleDocTemplate(OUT + '/Steel_sections_list_EN_AR.pdf', pagesize=landscape(A4), leftMargin=12*mm, rightMargin=12*mm, topMargin=10*mm, bottomMargin=10*mm,
                        title='Steel sections list - steel roof, Regatta Tourist Village', author='Eng. MALEK ABOZRAIG')
doc.build(story)
import pymupdf
d = pymupdf.open(OUT + '/Steel_sections_list_EN_AR.pdf'); print('pages', len(d)); d[0].get_pixmap(dpi=110).save(OUT + '/preview_sections_list.png')
