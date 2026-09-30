"""Technical and financial offer Rev D (design Rev 8a, economic scheme on 23 existing columns) - 3 pages A4 + 2 attachments. Client cost basis of 29 Sep 2026."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether)
from reportlab.lib.enums import TA_JUSTIFY
from pypdf import PdfWriter, PdfReader
import json, os, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # .../roof, wherever the repo is checked out
OUT = ROOT + '/offer'
DET = ROOT + '/detailing'
os.makedirs(OUT, exist_ok=True)

# ---------------- pricing (cost basis, LYD) ----------------
RATE_STEEL, RATE_PANEL = 6950.0, 150.0
S7 = json.load(open(ROOT + '/design/C7/calc/summary_C7.json'))
t_sections = round(S7['weight']['sections_hot_rolled']/1000, 1)   # IPE 300/330, IPE 240, HEA 140 (hot-rolled members)
t_total = round(S7['weight']['total_offer']/1000, 1)              # design Rev 7 take-off, girts excluded
area_roof = round(S7['roof_area'])
INV = json.load(open(OUT + '/sections_cost_invoice_rev8a.json'))      # supplier quotation 11486, Rev 8a cutting plan
MARGIN = 0.25
cost_material = round((INV['sections_cost'] + INV['plates_cost'])/100.0)*100.0   # material incl. plates at quotation prices, Rev 8a (client basis: 106,600 for Rev 8)
cost_assembly = 20000.0                                               # client basis: sections assembly (fabrication and erection)
cost_panels = 47000.0                                                 # client basis: sandwich panel supply and assembly (316 m2)
cost_steel = cost_material + cost_assembly; cost_gutters = 0.0; cost_bases = 0.0
cost_total = cost_material + cost_assembly + cost_panels
margin = MARGIN * cost_total
price = cost_total + margin
price_round = round(price / 500.0) * 500
json.dump({'cost_material': cost_material, 'cost_assembly': cost_assembly, 'cost_panels': cost_panels, 'cost_total': cost_total, 'margin': margin, 'price': price, 'price_round': price_round},
          open(OUT + '/pricing_internal_RevD.json', 'w'), indent=1)
P = '{:,.0f}'.format(price_round)
ADV = '{:,.0f}'.format(price_round * 0.5); MID = '{:,.0f}'.format(price_round * 0.25)

# ---------------- document ----------------
DATE = datetime.date(2026, 9, 29).strftime('%d %B %Y')
VALID = (datetime.date(2026, 9, 29) + datetime.timedelta(days=15)).strftime('%d %B %Y')
NAVY = colors.HexColor('#1f3a5f'); GREY = colors.HexColor('#555555')
base = ParagraphStyle('b', fontName='Helvetica', fontSize=9.5, leading=13, alignment=TA_JUSTIFY, spaceAfter=4)
cell = ParagraphStyle('c', parent=base, alignment=0, spaceAfter=0)
h1 = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=NAVY, spaceAfter=6)
h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=3)
small = ParagraphStyle('s', fontName='Helvetica', fontSize=8, leading=10, textColor=GREY)
bul = ParagraphStyle('bul', parent=base, leftIndent=10, bulletIndent=0, spaceAfter=2)
big = ParagraphStyle('big', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=NAVY)

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 10); canvas.setFillColor(NAVY)
    canvas.drawString(20*mm, 285*mm, 'Eng. MALEK ABOZRAIG  -  Steel Structures')
    canvas.setFont('Helvetica', 8); canvas.setFillColor(GREY)
    canvas.drawRightString(190*mm, 285*mm, 'malek.abozraig@gmail.com   |   Tripoli, Libya')
    canvas.setStrokeColor(NAVY); canvas.setLineWidth(0.8); canvas.line(20*mm, 283*mm, 190*mm, 283*mm)
    canvas.line(20*mm, 16*mm, 190*mm, 16*mm)
    canvas.drawString(20*mm, 11*mm, 'Offer RTV-2026-01 Rev D  -  Steel roof, Administration Building, Regatta Tourist Village, Tripoli')
    canvas.drawRightString(190*mm, 11*mm, 'Page %d' % doc.page)
    canvas.restoreState()

def tbl(rows, widths, header=True, size=9):
    t = Table(rows, colWidths=widths)
    st = [('FONT', (0, 0), (-1, -1), 'Helvetica', size), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#999999')), ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
          ('TOPPADDING', (0, 0), (-1, -1), 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5)]
    if header: st += [('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8eef5')), ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', size)]
    t.setStyle(TableStyle(st)); return t

def para_rows(rows):
    return [[Paragraph(c, cell) if isinstance(c, str) else c for c in r] for r in rows]

story = []
# ---- page 1: letter, scope ----
story += [Paragraph('TECHNICAL AND FINANCIAL OFFER', h1),
          Paragraph('Steel-framed sandwich-panel roof over the existing roof slab<br/><b>Administration Building, Regatta Tourist Village, Tripoli</b>', big), Spacer(1, 6)]
story.append(tbl(para_rows([
    ['Offer No.', 'RTV-2026-01 Rev D (supersedes earlier issues)', 'Date', DATE],
    ['To', 'Regatta Tourist Village - Administration', 'Valid until', VALID],
    ['From', 'Eng. MALEK ABOZRAIG, malek.abozraig@gmail.com', 'Design basis', 'Design Rev 8a (reduced roof area, architect\'s plan A_103)']]),
    [25*mm, 70*mm, 25*mm, 50*mm], header=False))
story += [Spacer(1, 8), Paragraph('Dear Sirs,', base),
          Paragraph('Further to the survey of the existing administration building, the structural design completed for it and the architect\'s 2nd-level layout of 29 September 2026, we are pleased to submit our revised offer for the supply, fabrication and erection of a steel roof structure with insulated sandwich-panel cladding over the existing roof slab, as described below and shown on the attached framing plan and 3D view. The offer is a lump sum covering all materials, workshop fabrication, transport, site works and erection listed in the scope, delivered as a complete and weather-tight roof.', base)]
story += [Paragraph('1. The structure', h2),
          Paragraph('The new roof is a light steel post-and-beam structure standing on the existing 300 mm roof slab, with one steel column on each of the 23 existing concrete columns under the enclosed area, so that all loads pass straight into the building\'s own structure. Level primary beams run along the column rows; sloping rafters, continuous over the middle row, sit on top of them and carry cold-formed purlins and 50 mm insulated PIR sandwich panels on a single roof plane falling 6 %% to the north, where two box gutters and four downpipes on the north facade take the rainwater away. Lateral stability is provided by six X-braced wall bays and a braced roof plane, designed for the Tripoli wind and seismic conditions. The stair well remains open with upstands and flashings; the south-west terrace and the skylight terrace are not roofed, and the roof edges sit on the existing column lines K19-K20 and K16-K17-K18. The roofed area is %d m2; the clear height under the steel is 3.0 m at the low north eave and about 4.0 m at the south edges.' % area_roof, base)]
story.append(tbl(para_rows([
    ['Element', 'Specification'],
    ['Columns', '23 no. HEA 140, S275, one over each existing concrete column under the roof'],
    ['Primary beams', 'IPE 200, S275, level, bolted cap plates on the columns'],
    ['Rafters and trimmers', 'IPE 180 continuous over the middle primaries, S275, single roof plane at 6 % falling north, bolted seats on the primaries'],
    ['Purlins', 'Z 200 x 2.0 cold-formed, S350GD galvanised, at 1.5 m centres (wall girts excluded)'],
    ['Bracing', 'L 60 x 6 wall diagonals in 6 bays; M20 roof rods in 12 panels'],
    ['Bases', '4 post-installed dia 16 rebars per column into the existing column head, grouted shear keys, 20 mm plates, 25 mm grout bed'],
    ['Roof cladding', 'PIR sandwich panels 50 mm, colour-coated steel both faces, with ridge, eave and verge flashings and well upstands'],
    ['Rainwater', 'Two box gutters 150 x 100 with overflows, four 100 mm downpipes on the north facade'],
    ['Steel weight', 'about %d tonnes, delivered blast-cleaned; corrosion protection is not included (see sections 3 and 7)' % round(t_total)],
]), [40*mm, 130*mm]))

# ---- page 2: scope, exclusions, programme, price ----
story += [PageBreak(), Paragraph('2. Scope of supply and works', h2)]
for s in ['Detailed fabrication drawings and the bill of materials based on the approved design (Rev 8a, reduced roof area).',
          'Supply of all structural steel sections, plates, bolts, rebars, anchors and cold-formed purlins and girts.',
          'Workshop fabrication, blast cleaning of the steel, transport to site and offloading.',
          'Site survey of the slab top, scanning of the 23 column heads, drilling and injection of the anchors, coring and grouting of the shear keys, and proof tests on three bars.',
          'Erection of columns, beams, rafters, bracing and purlins with all connections, including the temporary bracing needed during erection.',
          'Supply and fixing of the roof sandwich panels with all flashings, well upstands, sealants and fasteners.',
          'Supply and fixing of gutters, downpipes and the associated brackets and flashings.',
          'Site management, safety measures, cleaning of the site and handover with as-built drawings.']:
    story.append(Paragraph(s, bul, bulletText='-'))
story += [Paragraph('3. Not included', h2)]
for s in ['Corrosion protection of the steelwork (paint system or galvanising) is not within the scope of this offer; the recommended Jotun system is given in section 7 and can be offered separately.',
          'Wall cladding of any kind and its girts or fixings (the architect\'s drawings show 20 cm gypsum walls; to be offered separately once the wall system is selected).',
          'Verification of the existing building (as-built drawings, slab-top survey drawing, adequacy statement of the existing columns and foundations) and any strengthening it may require.',
          'Building permits, authority fees, independent checking and any works to the existing slab or facade beyond the anchors, keys and downpipe fixings.',
          'Electrical, mechanical, lighting, ceilings, floors and finishes under the new roof.']:
    story.append(Paragraph(s, bul, bulletText='-'))
story += [Paragraph('4. Programme', h2),
          Paragraph('The works are planned over about three weeks from receipt of the advance payment, subject to site access and to the scan results at the column heads.', base)]
story.append(tbl(para_rows([
    ['Week', 'Activity'],
    ['1', 'Fabrication drawings approved; slab survey and column-head scans; steel and panel procurement; workshop fabrication starts'],
    ['2', 'Fabrication completed and delivered; anchors drilled and injected, shear keys cored and grouted; columns and beams erected'],
    ['3', 'Rafters, bracing and purlins completed; roof panels, flashings, gutters and downpipes fixed; cleaning and handover'],
]), [18*mm, 152*mm]))
story += [Paragraph('5. Price', h2)]
story.append(tbl([[Paragraph('<b>Lump-sum price for the complete scope in section 2</b>', base), Paragraph('<b>LYD %s</b>' % P, big)],
                  [Paragraph('Libyan Dinars, fixed for the validity period, inclusive of materials, fabrication, transport, site works, erection and supervision. Taxes and fees, if any, are for the client\'s account.', small), '']],
                 [110*mm, 60*mm], header=False, size=9))
story += [Paragraph('6. Payment terms', h2)]
story.append(tbl(para_rows([
    ['Stage', 'Share', 'Amount, LYD'],
    ['Advance on signing the order; starts the programme', '50 %', ADV],
    ['On start of erection on site', '25 %', MID],
    ['On completion and handover', '25 %', MID]]), [100*mm, 25*mm, 45*mm]))

# ---- page 3: terms, signature ----
story += [PageBreak(), Paragraph('7. Conditions', h2)]
for s in ['Validity: this offer is valid for 15 days from its date, until %s, because of the movement of steel prices.' % VALID,
          'Warranty: 12 months from handover on the steel structure, panel fixings and workmanship; panel warranties as per the manufacturer.',
          'Corrosion protection (recommendation, not included): the site is 0.3-2 km from the sea, corrosivity category C5 (ISO 12944-2). We recommend a Jotun three-coat system applied in the workshop over Sa 2 1/2 blast cleaning: Barrier 80 zinc-rich epoxy primer 60 microns, Jotamastic 90 epoxy mastic 150 microns, Hardtop XP polyurethane topcoat 60 microns, total 270 microns dry film, ISO 12944-5 high durability (over 15 years); site touch-up of bolts, welds and damage with Jotamastic 90 and Hardtop XP. Hot-dip galvanising to EN ISO 1461 plus Hardtop XP is the alternative. This can be priced on request.',
          'The design is based on the assumptions listed in the design report (Rev 8a) and the load basis Rev 3. The client provides as-built information on the existing building and free access to the roof and to the north facade for the downpipes; anything found at the column heads that differs from the assumptions (bar positions, concrete quality, slab thickness) is dealt with by the fallback base details of the design set and, if it changes the scope, by a written variation before work continues.',
          'The client confirms that the six braced wall bays shown on the framing plan (K1-K2, K5-K7, K16-K17, K15-K19, K4-K14, K16-K20) remain free of doors and windows, and that the architect adjusts the 2nd-level wall lines to the roof edges shown.',
          'Materials: structural steel S275 to EN 10025, bolts 8.8, cold-formed purlins S350GD, PIR panels with a manufacturer\'s certificate; anchor system with a European Technical Assessment for post-installed rebar.',
          'Design standards: Eurocodes EN 1990, 1991, 1993 and 1998 with parameters for Tripoli, as recorded in the design report.',
          'Any change to the roof plane, the openings, the cladding type or the scope after the order is priced separately.',
          'The offer excludes anything not expressly stated in section 2.']:
    story.append(Paragraph(s, bul, bulletText='-'))
story += [Paragraph('8. Attachments', h2)]
for s in ['Attachment A: roof framing plan, design Rev 8a (A3).', 'Attachment B: 3D view of the steel structure, design Rev 8a.',
          'The detailed drawing set (fabrication and erection drawings, A2) is produced after the order on the approved Rev 8a design; the Rev 6a set RTV-ST-S00 to S06 remains available as reference for the typical details.']:
    story.append(Paragraph(s, bul, bulletText='-'))
story += [Spacer(1, 14), Paragraph('We remain at your disposal for any clarification and look forward to working with you on this project.', base), Spacer(1, 22)]
story.append(tbl(para_rows([['For the offer', 'For the client (acceptance)'],
                            ['<br/><br/><br/>Eng. MALEK ABOZRAIG<br/>malek.abozraig@gmail.com<br/>Date: ..................', '<br/><br/><br/>Name: ..................<br/>Position: ..................<br/>Date: ..................']]),
                 [85*mm, 85*mm], header=True))

doc = SimpleDocTemplate(OUT + '/offer_body.pdf', pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=25*mm, bottomMargin=22*mm,
                        title='Technical and financial offer - Steel roof, Regatta Tourist Village', author='Eng. MALEK ABOZRAIG')
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print('body pages:', len(PdfReader(OUT + '/offer_body.pdf').pages), 'price', P)

# ---- attachments: S01 and S03 as A3 landscape pages, 3D view as A4 landscape page ----
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfgen import canvas as rl_canvas
def image_page(path, img, title, pagesize):
    c = rl_canvas.Canvas(path, pagesize=pagesize); W, H = pagesize
    c.setFont('Helvetica-Bold', 11); c.setFillColor(NAVY); c.drawString(15*mm, H - 12*mm, title)
    c.setFont('Helvetica', 8); c.setFillColor(GREY); c.drawRightString(W - 15*mm, H - 12*mm, 'Offer RTV-2026-01 Rev D - Eng. MALEK ABOZRAIG')
    from reportlab.lib.utils import ImageReader
    ir = ImageReader(img); iw, ih = ir.getSize(); box_w, box_h = W - 30*mm, H - 30*mm
    s = min(box_w / iw, box_h / ih); w, h = iw * s, ih * s
    c.drawImage(ir, (W - w) / 2, (H - 18*mm - h) if h < box_h else 12*mm, w, h); c.showPage(); c.save()
image_page(OUT + '/att_A_RevD.pdf', ROOT + '/design/C7/framing_C7.png', 'Attachment A - Roof framing plan, design Rev 8a (utilisation shown per member; bracing bays in red)', landscape(A3))
image_page(OUT + '/att_B_RevD.pdf', ROOT + '/design/C7/view3d_C7.png', 'Attachment B - 3D view of the steel structure, design Rev 8a (roof panels hidden)', landscape(A4))
w = PdfWriter()
for p in [OUT + '/offer_body.pdf', OUT + '/att_A_RevD.pdf', OUT + '/att_B_RevD.pdf']: w.append(PdfReader(p))
with open(OUT + '/Offer_RTV-2026-01_RevD_steel_roof.pdf', 'wb') as f: w.write(f)
print('offer pdf pages:', len(PdfReader(OUT + '/Offer_RTV-2026-01_RevD_steel_roof.pdf').pages))

md = ["# Internal pricing of offer RTV-2026-01 Rev D (design Rev 8a, client cost basis of 29 Sep 2026, 25 % margin) - not for the client", "", "| Cost item | Basis | LYD |", "|---|---|---|",
      "| Steel material incl. plates, %.1f t | sections at supplier quotation 11486 prices (Rev 8a cutting plan) + plates and small items | %s |" % (t_total, '{:,.0f}'.format(cost_material)),
      "| Sections assembly (fabrication and erection) | client figure | %s |" % '{:,.0f}'.format(cost_assembly),
      "| Roof sandwich panels %d m2, supply and assembly | client figure | %s |" % (area_roof, '{:,.0f}'.format(cost_panels)),
      "| **Total cost** | | **%s** |" % '{:,.0f}'.format(cost_total), "| Profit margin | %d %% of the total cost | %s |" % (MARGIN*100, '{:,.0f}'.format(margin)),
      "| **Offer price (rounded)** | | **%s LYD** |" % P, "",
      "Not priced separately in this basis (covered by the lump sum and the margin): gutters and downpipes, base works (scans, 92 rebar holes, key pockets, grout, pull-out tests), transport. Earlier allowances were 12,000 and 18,500 LYD. Corrosion protection is excluded from the scope (Jotun Barrier 80 / Jotamastic 90 / Hardtop XP recommended, to be priced on request).",
      "Superseded: Rev A 284,000 LYD (Rev 7, 6,950 LYD/t all-in, 50 %%), Rev B 343,000 LYD (Rev 7, quotation-based, 25 %%), Rev C 217,000 LYD (Rev 8, client basis with material 106,600). Payment: %s advance / %s at erection start / %s at handover. Valid 15 days to %s. Warranty 12 months." % (ADV, MID, MID, VALID),
      "Generated by make_offer_rev10.py (pricing_internal_RevD.json holds the same numbers)."]
open(OUT + '/pricing_internal_RevD.md', 'w').write('\n'.join(md) + '\n')
