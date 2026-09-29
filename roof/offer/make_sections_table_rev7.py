"""One-page bilingual (English / Arabic) table of sections and quantities - design Rev 6a."""
import os
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
FD = OUT + '/fonts'
AR_REG = FD + '/NotoNaskhArabic-Regular.ttf'; AR_BOLD = FD + '/NotoNaskhArabic-Bold.ttf'
if not (os.path.exists(AR_REG) and os.path.getsize(AR_REG) > 10000):
    AR_REG = AR_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
pdfmetrics.registerFont(TTFont('AR', AR_REG)); pdfmetrics.registerFont(TTFont('AR-B', AR_BOLD))
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DV-B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

def ar(t): return '<br/>'.join(get_display(arabic_reshaper.reshape(x)) for x in t.split('|'))

NAVY = colors.HexColor('#1f3a5f')
en = ParagraphStyle('en', fontName='DV', fontSize=7.6, leading=9.4)
enb = ParagraphStyle('enb', parent=en, fontName='DV-B')
arp = ParagraphStyle('ar', fontName='AR', fontSize=8.6, leading=10.6, alignment=2)   # right aligned
arb = ParagraphStyle('arb', parent=arp, fontName='AR-B')
ttl = ParagraphStyle('t', fontName='DV-B', fontSize=11.5, leading=14, textColor=NAVY)
ttl_ar = ParagraphStyle('ta', fontName='AR-B', fontSize=12.5, leading=15.5, textColor=NAVY, alignment=2)
small = ParagraphStyle('s', fontName='DV', fontSize=7.3, leading=9.5, textColor=colors.HexColor('#444444'))
small_ar = ParagraphStyle('sa', fontName='AR', fontSize=8.5, leading=11, textColor=colors.HexColor('#444444'), alignment=2)

# element, arabic, section, unit weight kg/m, pieces, length m, weight t (None = computed), remark
rows = [
    ('Columns (one on each of the 20 concrete columns under the roof)', 'الأعمدة (فوق 20 عموداً خرسانياً تحت السقف)', 'HEA 140, S275', 24.7, 20, 67.1, None, 'L = TOS - 0.335 m, cut to the surveyed level'),
    ('Wind posts on the two south eaves', 'أعمدة الرياح على الطنفين الجنوبيين', 'HEA 140, S275', 24.7, 3, 12.1, None, 'WP2, WP3, WP4: shear only, no roof load'),
    ('Primary and eave beams on the column rows', 'الكمرات الرئيسية وكمرات الطنف', 'IPE 300, S275', 42.2, 14, 64.9, None, 'level, on cap plates'),
    ('South eave beam of the east block (K17 - K18, 13.7 m)', 'كمرة الطنف الجنوبي|للكتلة الشرقية (13.7 م)', 'IPE 330, S275', 49.1, 1, 13.7, None, ''),
    ('Rafters, chord T3 and post ST2', 'العوارض المائلة والكمرة T3 والقائم ST2', 'IPE 240, S275', 30.7, 24, 144.6, None, 'single plane, 6 % falling north'),
    ('Roof purlins @ 1.5 m', 'مدادات السقف كل 1.5 م', 'Z 200 x 2.0, S350GD galvanised', 5.9, None, 217, None, 'with anti-sag rows and fly braces'),
    ('Wall X-bracing, 6 bays x 2 diagonals', 'شكالات الجدران X، 6 حيزات × 2', 'L 70 x 70 x 7, S275', 7.4, 12, 73.1, None, 'tension-only, gusset plates 10 mm'),
    ('Roof plane bracing, 12 panels x 2 rods', 'قضبان شكالات السقف، 12 لوح × 2', 'M24 rods, grade 8.8, turnbuckles', 3.55, 24, 167.8, None, ''),
    ('Base plates', 'صفائح القواعد', '300 x 400 x 20, S275', None, 23, None, 0.45, 'grout bed 25 mm'),
    ('Post-installed anchor bars', 'أسياخ التثبيت المزروعة', 'dia 16 B500, threaded end, 550-600 mm', None, 80, 47.0, 0.08, '4 per column into the column head, EAD 330087 resin'),
    ('Shear keys', 'مفاتيح القص', 'SHS 90 x 90 x 8 (30) and dia 60 bar (6)', None, 36, None, 0.16, 'in cored pockets, grouted'),
    ('Cap plates, fin plates, gussets, cleats, stiffeners, bolts', 'صفائح الوصلات والأغطية والحوامل والمسامير', 'S275 plates 8 - 20 mm, bolts 8.8 HDG', None, None, None, 1.78, 'allowance scaled from the Rev 6a BOM; detailing to follow'),
    ('Roof sandwich panels', 'ألواح الساندوتش للسقف', 'PIR 50 mm, colour-coated steel both faces', None, None, None, None, '316 m2 net + 5 % laps; flashings and well upstand'),
    ('Box gutters and downpipes (north)', 'المزاريب الصندوقية ومواسير النزول (شمال)', 'Gutter 150 x 100, 4 downpipes dia 100', None, None, None, None, '24 m gutter, 4 x 7.4 m downpipes'),
    ('Wall girts (NOT included - wall system open)', 'مدادات الجدران|(غير مشمولة - النظام مفتوح)', 'Z 200 x 2.0, S350GD galvanised', 5.9, None, 270, None, 'only if panel walls are chosen'),
]
tot = 0.0
data = [[Paragraph('No.', enb), Paragraph('Element', enb), Paragraph(ar('العنصر'), arb), Paragraph('Section / grade', enb),
         Paragraph('Pieces', enb), Paragraph('Length m', enb), Paragraph('Weight t', enb), Paragraph('Remarks', enb)]]
for i, (e, a, s, kg, n, L, w, rem) in enumerate(rows, 1):
    if w is None and kg is not None and L is not None: w = kg * L / 1000.0
    if w: tot += w
    data.append([Paragraph(str(i), en), Paragraph(e, en), Paragraph(ar(a), arp), Paragraph(s, en),
                 Paragraph('' if n is None else str(n), en), Paragraph('' if L is None else '%.1f' % L, en),
                 Paragraph('' if w is None else '%.2f' % w, en), Paragraph(rem, en)])
data.append([Paragraph('', en), Paragraph('Total structural steel in the offer (girts excluded)', enb), Paragraph(ar('إجمالي الحديد الإنشائي في العرض|(بدون مدادات الجدران)'), arb),
             Paragraph('', en), Paragraph('', en), Paragraph('', en), Paragraph('<b>14.7</b>', enb), Paragraph('offer basis (take-off %.1f t incl. girts line; girts %.1f t excluded)' % (tot, 1.59), en)])
widths = [8*mm, 60*mm, 64*mm, 52*mm, 13*mm, 16*mm, 16*mm, 48*mm]
t = Table(data, colWidths=widths, repeatRows=1)
st = [('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#8a8a8a')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
      ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e3ebf4')), ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f2f2f2')),
      ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 1.0), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.0)]
t.setStyle(TableStyle(st))

story = [Table([[Paragraph('SECTIONS AND QUANTITIES - STEEL ROOF, ADMINISTRATION BUILDING, REGATTA TOURIST VILLAGE, TRIPOLI', ttl),
                 Paragraph(ar('جدول القطاعات والكميات - السقف الحديدي|المبنى الإداري، قرية ريقاطة السياحية، طرابلس'), ttl_ar)]],
                colWidths=[150*mm, 127*mm], style=[('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]),
         Table([[Paragraph('Design Rev 7, reduced roofed area per the architect 2nd-level plan (29 Sep 2026), no detailing yet. Issued by Eng. MALEK ABOZRAIG, malek.abozraig@gmail.com. Steel S275 hot-dip galvanised or shop-primed; roofed area 316 m2 on 20 of the 27 existing columns.', small),
                 Paragraph(ar('التصميم مراجعة 7 (29 سبتمبر 2026)، قبل التفصيل:|مساحة السقف المخفضة حسب مخطط المعماري.|إعداد: م. مالك أبوزريق. الحديد S275 مجلفن بالغمس الساخن أو مدهون بالورشة.|مساحة السقف 316 م2 على 20 من الأعمدة القائمة الـ27.'), small_ar)]],
                colWidths=[150*mm, 127*mm], style=[('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]),
         Spacer(1, 4), t, Spacer(1, 4),
         Table([[Paragraph('Notes: lengths are net member lengths from the member schedule; pieces are erection pieces. Wall panels, their fixings and the existing-structure verification are not included. Bolt, fastener and flashing quantities follow with the detailing.', small),
                 Paragraph(ar('ملاحظات: الأطوال هي الأطوال الصافية للعناصر من جدول العناصر؛ القطع هي قطع التركيب.|لا تشمل ألواح الجدران وتثبيتاتها ولا التحقق من المبنى القائم.|كميات المسامير والمثبتات والفلاشينج تأتي مع التفصيل.'), small_ar)]],
                colWidths=[150*mm, 127*mm], style=[('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0), ('VALIGN', (0, 0), (-1, -1), 'TOP')])]
doc = SimpleDocTemplate(OUT + '/Sections_and_quantities_EN_AR_Rev7.pdf', pagesize=landscape(A4), leftMargin=10*mm, rightMargin=10*mm, topMargin=7*mm, bottomMargin=6*mm,
                        title='Sections and quantities - steel roof, Regatta Tourist Village', author='Eng. MALEK ABOZRAIG')
doc.build(story)
import pymupdf
d = pymupdf.open(OUT + '/Sections_and_quantities_EN_AR_Rev7.pdf'); print('pages', len(d), 'font', AR_REG)
d[0].get_pixmap(dpi=120).save(OUT + '/preview_sections_rev7.png')
