"""S05 base details per bases_C.md Rev 3: B1 type S, B1-E near-edge, K21 saddle (type P), WP1, B2 through-bolt fallback, notes, minimum-zone table."""
import math
from common import *
from geom import *
from s04 import D, K
OX, OY = 260.0, 8.0
EW_COLS = {'K1','K2','K5','K9','K10','K11','K12','K13','K14','K21','K22','K23','K24'}     # 280 spacing E-W (0.4 x 0.2 columns)
EDGE = {'K1':'+y','K2':'+y','K3':'+y','K4':'+x,+y','K6':'-x','K8':'-x','K14':'+x','K15':'-x','K18':'+x','K19':'-x','K22':'-y','K23':'+x,-y','K25':'-x','K27':'+x'}
FALLBACK = {'K9','K10','K12','K13','K16','K19','K20','K22','K23'}
MINZONE = {'K1':550,'K2':600,'K3':400,'K4':400,'K5':600,'K6':450,'K7':550,'K8':500,'K9':600,'K10':650,'K11':500,'K12':650,'K13':600,'K14':550,'K15':450,'K16':700,'K17':400,'K18':600,'K19':750,'K20':700,'K21':450,'K22':700,'K23':750,'K24':450,'K25':600,'K26':550,'K27':650}
UTIL = {'K1':0.45,'K2':0.51,'K3':0.37,'K4':0.37,'K5':0.59,'K6':0.40,'K7':0.50,'K8':0.39,'K9':0.53,'K10':0.69,'K11':0.34,'K12':0.68,'K13':0.55,'K14':0.49,'K15':0.35,'K16':0.76,'K17':0.16,'K18':0.58,'K19':0.91,'K20':0.73,'K21':0.36,'K22':0.78,'K23':0.83,'K24':0.31,'K25':0.57,'K26':0.42,'K27':0.69}
def conc_col(d, cx, cy, ew, layer='S-EXIST'):
    """Existing concrete column 400 x 200 in plan (dashed) with 6 dia14 and the dia6 stirrup; ew = long axis horizontal."""
    a, b = (200, 100) if ew else (100, 200)
    d.rect(cx-a, cy-b, cx+a, cy+b, layer, linetype='DASHED'); d.rect(cx-a+30, cy-b+30, cx+a-30, cy+b-30, layer, linetype='DASHED')
    pts = [(-157, -57), (157, -57), (157, 57), (-157, 57), (0, -57), (0, 57)] if ew else [(-57, -157), (57, -157), (57, 157), (-57, 157), (-57, 0), (57, 0)]
    for x, y in pts: d.sh.circle(*d.P(cx+x, cy+y), 7*K, layer)
    d.text(cx, cy + (b+15), 'existing column 200 x 400, 6 dia14 + dia6/200 (scan)', 0.13, 'CENTER', layer=layer)
def hea_plan(d, cx, cy, ew):
    """HEA 160 in plan, web across the concrete column's short axis (ew: web along y)."""
    if ew: d.iprof(cx, cy-76, 152, 160, 6, 9, 'S-COL', rot=0)
    else: d.iprof(cx, cy-80, 160, 152, 9, 6, 'S-COL', rot=1)
def plan_S(d, cx, cy, ew, tag):
    conc_col(d, cx, cy, ew)
    a, b = (200, 150) if ew else (150, 200)
    d.rect(cx-a, cy-b, cx+a, cy+b, 'S-DETAIL', lineweight=50)
    hea_plan(d, cx, cy, ew)
    ax, ay = (140, 40) if ew else (40, 140)
    for sx in (-1, 1):
        for sy in (-1, 1): d.hole(cx+sx*ax, cy+sy*ay, 26)
    d.rect(cx-45, cy-45, cx+45, cy+45, 'S-DETAIL', lineweight=35); d.sh.circle(*d.P(cx, cy), 70*K, 'S-DETAIL', linetype='DASHED')
    d.text(cx-a, cy+b+60, tag, 0.16, 'LEFT')
    if ew: d.dimh(cx-140, cx+140, cy-b, -60); d.dimh(cx-200, cx+200, cy-b, -100); d.dimv(cy-40, cy+40, cx+a, 60); d.dimv(cy-150, cy+150, cx+a, 100)
    else: d.dimh(cx-40, cx+40, cy-b, -60); d.dimh(cx-150, cx+150, cy-b, -100); d.dimv(cy-140, cy+140, cx+a, 60); d.dimv(cy-200, cy+200, cx+a, 100)
def f_planS(sh, fx, fy):
    d = D(sh, fx, fy, 'B1', 'BASE B1 (S) PLAN', 'Interior bases K9, K11, K12, K13, K17 (Rev 3 accepted): plate 300x400x25, 4 M20 resin anchors 80 x 280 h_ef 200, Key A SHS 90x90x8', sheet='S05')
    d.title(-50, 1010, 'Concrete column long axis E-W: K9, K11, K12, K13 (280 spacing E-W)')
    plan_S(d, 200, 780, True, 'plate 400 (E-W) x 300')
    d.title(-50, 470, 'Concrete column long axis N-S: K17 (280 spacing N-S)')
    plan_S(d, 200, 200, False, 'plate 300 x 400 (N-S)')
    d.text(300, 690, 'Key A SHS 90x90x8 in a 140 pocket', 0.13); d.text(300, 110, 'holes 26 (tension only)', 0.13)
    d.notes(-50, -80, ['Anchors 60 mm inside the column-head faces, h_ef 200 in the slab, stopping 50 above the column top (no drilling into the head).',
        'HEA 160 web across the concrete column short axis (normal to the wall it supports). Weld a6 all round.'], 22)
def f_planE(sh, fx, fy):
    d = D(sh, fx, fy, 'KEY B', 'KEY B (NEAR EDGE)', 'Accepted Rev 3: Key B dia 60 at 180 inboard (c1 250) at K1-K4, K6, K8, K14, K15, K18, K19, K22, K23, K25, K27; plate / anchors shown superseded by B2 (Rev 4)', sheet='S05')
    d.title(-50, 1010, 'PLAN, slab edge at the top (example K1, edge +y): Key B and Key A positions; anchors shown are the Rev 3 layout, replaced by B2 through-bolts')
    cx, cy = 200, 700
    d.line(-150, cy+100, 550, cy+100, 'S-EXIST', lineweight=50); d.text(560, cy+90, 'free slab edge', 0.13)
    conc_col(d, cx, cy, True)
    d.rect(cx-200, cy-250, cx+200, cy+100, 'S-DETAIL', lineweight=50)
    hea_plan(d, cx, cy, True)
    for sx in (-1, 1):
        for sy in (-1, 1): d.hole(cx+sx*140, cy+sy*40, 26)
    d.rect(cx-45, cy-45, cx+45, cy+45, 'S-DETAIL', lineweight=35); d.sh.circle(*d.P(cx, cy), 70*K, 'S-DETAIL', linetype='DASHED')
    d.rect(cx-45, cy+45, cx+45, cy+70, 'S-HATCH'); d.text(cx+80, cy+50, 'compressible strip 25 on the outboard face of pocket A', 0.12)
    d.sh.circle(*d.P(cx, cy-180), 30*K, 'S-DETAIL', lineweight=35); d.sh.circle(*d.P(cx, cy-180), 55*K, 'S-DETAIL', linetype='DASHED')
    d.text(cx+70, cy-190, 'KEY B dia 60 S355 in a 110 pocket', 0.13)
    d.dimv(cy, cy+100, cx-260, -60); d.dimv(cy-250, cy, cx-260, -60); d.dimv(cy-180, cy, cx+230, 60); d.dimv(cy-210, cy+100, cx+330, 60)
    d.text(cx+360, cy-120, 'c1 = 250 to the bar face', 0.13, rot=90); d.dimh(cx-200, cx+200, cy-250, -60)
    d.notes(-50, 330, ['Corners K4, K6, K23, K25: two Key B, one per edge. Perimeter plate and bolt layout per bases_C.md Rev 4 (B2 through-bolts, Key A moved inboard) - pending.',
        'Key B lies on the axis of the outward force; it takes only the shear towards the free edge (plain-concrete edge breakout, V_Rd,c 38.2 kN at c1 250, 49.5 at K3 c1 350).',
        'Key A takes the shear along the wall and the inward shear across; the 25 mm compressible strip stops it from bearing outwards.',
        'The 280 anchor spacing follows the concrete long axis (E-W or N-S, schedule at right); anchors 60 inside the head faces, holes 26.',
        'Corner K23 (+x, -y) shown in reactions_C.csv with two Key B; K21 (pier) is type P with the saddle - see below.'], 22)
def slab_section(d, x0, x1, edge=None):
    d.line(x0, 0, x1, 0, 'S-EXIST', lineweight=35); d.line(x0, -250, x1, -250, 'S-EXIST', lineweight=35)
    d.hatch([(x0, -250), (x1, -250), (x1, 0), (x0, 0)], 0.12, 8, 45)
    d.text(x0+10, -240, 'existing slab 250 (solid zone, cores to confirm)', 0.13)
    if edge is not None: d.line(edge, 0, edge, -250, 'S-EXIST', lineweight=50); d.text(edge+10, -120, 'free slab edge', 0.13, rot=90)
def f_secS(sh, fx, fy):
    d = D(sh, fx, fy, 'B1', 'BASE B1 (S) SECTION', 'Interior bases: section along the concrete long axis, anchors at 280, Key A SHS stub 180 embedded in a 140 cored pocket, 40 grout', sheet='S05')
    d.title(-50, 1010, 'SECTION 1-1 (along the 400 axis of the concrete column)')
    slab_section(d, -350, 550)
    d.rect(-200, -250, 200, -900, 'S-EXIST', linetype='DASHED'); d.text(0, -880, 'existing column 400 x 200 (not drilled)', 0.13, 'CENTER')
    for x in (-157, 0, 157): d.line(x, -260, x, -900, 'S-EXIST', linetype='DASHED')
    d.rect(-200, 0, 200, 40, 'S-HATCH'); d.text(210, 5, 'grout 40 (Rev 3 text: 25 - confirm)', 0.12)
    d.rect(-200, 40, 200, 65, 'S-DETAIL', lineweight=50); d.text(210, 60, 'plate 300 x 400 x 25', 0.13)
    d.rect(-80, 65, 80, 600, 'S-COL', lineweight=35); d.line(0, 65, 0, 600, 'S-COL'); d.text(0, 350, 'HEA 160', 0.16, 'CENTER', 90); d.weld(80, 65, 6, 1, 'a6')
    for x in (-140, 140):
        d.rect(x-10, -200, x+10, 65, 'S-DETAIL', lineweight=35); d.rect(x-13, -200, x+13, 0, 'S-DETAIL', linetype='DASHED')
        d.rect(x-16, 65, x+16, 78, 'S-DETAIL'); d.rect(x-16, 78, x+16, 95, 'S-DETAIL'); d.line(x-40, -150, x-13, -150, 'S-GRID')
    d.text(-320, 110, 'M20 8.8 resin anchor, h_ef 200', 0.13); d.text(170, -205, 'anchors stop >= 50 above the column top', 0.12)
    d.rect(-70, -200, 70, 40, 'S-HATCH'); d.rect(-45, -180, 45, 40, 'S-DETAIL', lineweight=50); d.line(-37, -180, -37, 40, 'S-DETAIL'); d.line(37, -180, 37, 40, 'S-DETAIL')
    d.text(170, -95, 'KEY A SHS 90x90x8 S355, welded a8, 180 embedded, 20 grout under the toe', 0.12); d.text(170, -150, 'pocket cored 140 x 200 deep (by scan, <= 1 top bar cut)', 0.12)
    d.dimh(-140, 140, 100, 60); d.dimh(-200, 200, 100, 100); d.dimv(0, 40, -260, -60); d.dimv(40, 65, -260, -60); d.dimv(-200, 0, -260, -100); d.dimv(-250, 0, 260, 60); d.dimv(-180, 40, -60, -60) if False else None
    d.dimh(-70, 70, -250, -60); d.dimh(-45, 45, -250, -100)
    d.notes(-350, -930, ['Erection: level on shims, grout the pockets and the bed, then drill and set the resin anchors through the plate (holes 26); nuts snug + 1/4 turn.',
        'Load path: uplift -> 4 anchors (cone in the slab, N_Rd,c 98.5 kN with psi_ec); shear -> Key A (bearing, 85 mm lever taken into the anchor group).'], 22)
def f_secE(sh, fx, fy):
    d = D(sh, fx, fy, 'B2', 'B2 PERIMETER SECTION', 'Section across the wall: through-bolt rows 150 / 350 inboard, Key A moved inboard, Key B at 180 inboard (c1 250) - layout per Rev 4 pending', sheet='S05')
    d.title(-50, 1010, 'SECTION 2-2 across the wall (slab edge left; perimeter columns are flush with the slab edge)')
    slab_section(d, -100, 620, edge=-100)
    d.rect(-100, -250, 100, -900, 'S-EXIST', linetype='DASHED'); d.text(0, -880, 'existing column (200 across)', 0.13, 'CENTER')
    d.rect(-100, 0, 400, 40, 'S-HATCH'); d.rect(-100, 40, 400, 70, 'S-DETAIL', lineweight=50); d.text(410, 45, 'base plate 400 x 450 x 30 (or 25 + stiffeners)', 0.13)
    d.rect(-76, 70, 76, 600, 'S-COL', lineweight=35); d.line(-76, 79, 76, 79, 'S-COL'); d.line(-76, 591, 76, 591, 'S-COL'); d.text(0, 350, 'HEA 160', 0.14, 'CENTER', 90)
    for x in (150, 350):
        d.rect(x-10, -330, x+10, 70, 'S-DETAIL', lineweight=35); d.rect(x-16, 70, x+16, 100, 'S-DETAIL'); d.rect(x-16, -330, x+16, -300, 'S-DETAIL')
        d.rect(x-13, -250, x+13, 0, 'S-DETAIL', linetype='DASHED')
    d.rect(100, -265, 400, -250, 'S-DETAIL', lineweight=50); d.text(120, -290, 'under-slab plate 300 x 400 x 15 (or four 100 x 100 x 15 washers)', 0.12)
    d.text(130, 110, 'M20 8.8 through-bolts, 2 rows at 150 and 350 inboard, +/- 250 along the wall', 0.12)
    d.rect(180, -200, 320, 40, 'S-HATCH'); d.rect(205, -180, 295, 40, 'S-DETAIL', lineweight=50); d.line(213, -180, 213, 40, 'S-DETAIL'); d.line(287, -180, 287, 40, 'S-DETAIL')
    d.text(330, -120, 'KEY A SHS 90x90x8 moved inboard (position per Rev 4)', 0.12)
    d.rect(125, -200, 175, 40, 'S-HATCH') if False else None
    d.sh.circle(*d.P(150, -100), 30*K, 'S-DETAIL', linetype='DASHED'); d.text(-95, -60, 'Key B dia 60 at 180 inboard where the table says so (accepted Rev 3)', 0.12, rot=90)
    d.dimh(-100, 0, 110, 60); d.dimh(0, 150, 110, 60); d.dimh(150, 350, 110, 60); d.dimh(-100, 400, 110, 100); d.dimv(-250, 0, 470, 60); d.dimv(0, 70, 470, 60)
    d.notes(-100, -930, ['PERIMETER BASE LAYOUT PER bases_C.md Rev 4 - PENDING: anchors fail on edge distance (column flush with the slab edge), so through-bolts are the primary detail.',
        'Uplift N_t x 250 eccentricity taken by the row couple (K19: 91 kN row, 2 M20 = 282 kN); tension to the under-slab plate, no cone / bond; shear stays with the keys.'], 22)
def f_P_WP(sh, fx, fy):
    d = D(sh, fx, fy, 'B1-P', 'K21 SADDLE, WP1 BASE', 'K21 pier 200 thick: two 15 mm saddle plates 400 x 150 grouted against the pier faces; WP1 offset 280 inboard, single Key', sheet='S05')
    d.title(-50, 1010, 'K21 - SECTION N-S across the pier (notch edge y 19.97 left, shaft opening y 20.17 right)')
    d.line(-300, 0, 450, 0, 'S-EXIST', linetype='DASHED'); d.rect(-100, -450, 100, 0, 'S-EXIST', lineweight=35); d.hatch([(-100,-450),(100,-450),(100,0),(-100,0)], 0.12)
    d.text(0, -440, 'pier 200 (K21)', 0.13, 'CENTER'); d.text(-290, -100, 'notch (outside)', 0.13); d.text(120, -100, 'shaft well', 0.13)
    d.rect(-150, 0, 150, 40, 'S-HATCH'); d.rect(-150, 40, 150, 65, 'S-DETAIL', lineweight=50); d.text(160, 45, 'plate 300 x 400 x 25', 0.13)
    d.rect(-76, 65, 76, 500, 'S-COL', lineweight=35); d.text(0, 300, 'HEA 160', 0.14, 'CENTER', 90)
    for x in (-40, 40): d.rect(x-10, -200, x+10, 65, 'S-DETAIL', lineweight=35); d.rect(x-16, 65, x+16, 95, 'S-DETAIL')
    for s in (-1, 1):
        d.rect(s*100 + (0 if s > 0 else -15), -150, s*100 + (15 if s > 0 else 0), 40, 'S-DETAIL', lineweight=50)
        d.rect(s*100 + (15 if s > 0 else -40), -150, s*100 + (40 if s > 0 else -15), 0, 'S-HATCH')
    d.text(-290, 60, 'saddle plates 2 x 15 S275, 400 long x 150 deep, welded a6 to the base plate, grouted 25 against the pier faces', 0.12)
    d.dimh(-100, 100, -250, -60); d.dimv(-150, 40, 200, 60); d.text(120, -300, 'no key; N-S shear by bearing on the pier faces; anchors h_ef 200 in the pier top (cone 200 x 800)', 0.12)
    d.title(-50, -540, 'WP1 - PLAN at the notch corner (77.89, 19.97); post centre moved to (77.61, 20.25)')
    y0 = -1040
    d.line(-450, y0, 350, y0, 'S-EXIST', lineweight=50); d.line(-450, y0, -450, y0+400, 'S-EXIST', lineweight=50); d.text(-460, y0+60, 'slab edges', 0.13, 'RIGHT')
    cx, cy = -450+280, y0+280
    d.rect(cx-125, cy-125, cx+125, cy+125, 'S-DETAIL', lineweight=50); d.text(cx+135, cy+100, 'plate 250 x 250 x 15', 0.13)
    d.iprof(cx, cy-76, 152, 160, 6, 9, 'S-COL')
    d.sh.circle(*d.P(cx, cy), 30*K, 'S-DETAIL', lineweight=35); d.sh.circle(*d.P(cx, cy), 55*K, 'S-DETAIL', linetype='DASHED'); d.text(cx+135, cy+40, 'Key dia 60, pocket 110 x 200', 0.12)
    for x in (cx-100, cx+100): d.hole(x, cy-100, 14)
    d.text(cx+135, cy-110, '2 M12 for location (no uplift)', 0.12)
    d.dimh(-450, cx, y0, -60); d.dimv(y0, cy, -450, -60); d.dimv(y0, cy-30, cx+200, 60); d.text(cx+230, y0+100, 'c1 = 250 both ways', 0.12, rot=90)
    d.text(-440, y0-70, 'Demand 11.8 / 8.8 kN vs 38.2 kN edge breakout (0.31). Corner girts cantilever 280 to the wall line (D9). Notch edge beam: core to confirm (else type S plate with two Key B).', 0.12)
def f_B2(sh, fx, fy):
    d = D(sh, fx, fy, 'B2', 'B2 SECTION 3-3', 'Perimeter base (22 columns): 4 M20 through-bolts at 500 along x 300 across, under-slab plate 300x400x15, base plate 400x450x30 - Rev 4 pending', sheet='S05')
    d.title(-50, 1010, 'SECTION 3-3 along the wall (both bolt rows inboard, behind each other)')
    slab_section(d, -400, 550)
    d.rect(-200, -250, 200, -900, 'S-EXIST', linetype='DASHED'); d.text(0, -880, 'existing column 400 x 200 (not drilled)', 0.13, 'CENTER')
    d.rect(-225, 0, 225, 40, 'S-HATCH'); d.rect(-225, 40, 225, 70, 'S-DETAIL', lineweight=50); d.text(235, 45, 'base plate 400 x 450 x 30', 0.13)
    d.rect(-80, 70, 80, 600, 'S-COL', lineweight=35); d.line(0, 70, 0, 600, 'S-COL'); d.text(0, 350, 'HEA 160', 0.16, 'CENTER', 90); d.weld(80, 70, 6, 1, 'a6')
    for x in (-250, 250):
        d.rect(x-10, -330, x+10, 70, 'S-DETAIL', lineweight=35); d.rect(x-16, 70, x+16, 100, 'S-DETAIL'); d.rect(x-16, -330, x+16, -300, 'S-DETAIL')
        d.rect(x-13, -250, x+13, 0, 'S-DETAIL', linetype='DASHED')
    d.rect(-300, -265, -200, -250, 'S-DETAIL', lineweight=50); d.rect(200, -265, 300, -250, 'S-DETAIL', lineweight=50)
    d.text(-390, -300, 'under-slab plate 300 x 400 x 15 cut around the column (two 400 x 50 strips + 100 cross plates) or four 100 x 100 x 15 washers on solid concrete', 0.12)
    d.rect(-70, -200, 70, 40, 'S-HATCH'); d.rect(-45, -180, 45, 40, 'S-DETAIL', lineweight=50); d.text(60, -110, 'Key A (inboard, behind) / Key B per section 2-2', 0.12)
    d.dimh(-250, 250, 110, 60); d.dimh(-225, 225, 110, 100); d.dimv(-250, 0, 320, 60); d.dimv(-330, 70, -330, -60)
    d.notes(-400, -930, ['Bolts M20 8.8 through 26 holes cored beside the column head (access to the slab soffit / ceiling void required); seal the holes; no coring into a column head.',
        'Interior bases K9, K11, K12, K13, K17: type B1 (resin anchors, Rev 3 accepted). K21: type P saddle (accepted). Perimeter: B2 per Rev 4 - pending.'], 22)
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S05', 'BASE DETAILS B1 / B1-E / P / WP1 / B2 AND NOTES', 'Details drawn 5x in model space (1 m = 200 mm); DIMENSION text = true mm (dimlfac 200)')
    f_planS(sh, 0.4, 16.2); f_planE(sh, 8.7, 16.2); f_secS(sh, 17.0, 16.2)
    f_secE(sh, 0.4, 2.9); f_P_WP(sh, 8.7, 2.9); f_B2(sh, 17.0, 2.9)
    # schedule of bases (right)
    rows = []
    for k in COLS:
        interior = k in ('K9', 'K11', 'K12', 'K13', 'K17')
        typ = 'P saddle' if k == 'K21' else ('B1 (Rev 3)' if interior else 'B2 (Rev 4)')
        rows.append(['C' + k[1:], k, 'E-W' if k in EW_COLS else 'N-S', typ, EDGE.get(k, '-') if k != 'K21' else 'saddle N-S', ','.join(BAY_OF.get(k, [])) or '-', MINZONE[k] if interior else '-', '%.2f' % UTIL[k] if (interior or k == 'K21') else 'Rev 4'])
    rows.append(['WP1', '-', '-', 'WP1 key', 'key c1 250', '-', 'edge beam', '0.31'])
    yb = sh.table(25.7, 29.0, [('Mark',0.9),('K',0.8),('280 axis',1.3),('Type',1.6),('Key B / edge',1.7),('Bays',1.4),('Min zone',1.3),('Util.',1.1)], rows, 0.33, 0.13,
                  title='BASE SCHEDULE - interior B1, K21, WP1 per Rev 3 (accepted); perimeter B2 per Rev 4 (pending)')
    yb = sh.note_block(25.7, yb - 0.5, 'STATUS AND CORING ACCEPTANCE CRITERION (Rev 3, section 5)', [
        'Sign-off: interior bases (K9, K11, K12, K13, K17), Key B, K21 saddle and WP1 accepted; PERIMETER BASES fail on anchor edge distance -> type B2 through-bolts, Key A inboard: layout per bases_C.md Rev 4 - PENDING.',
        '100 mm cores at 3 heads first, then a 60 mm core or GPR at every head: solid concrete (no blocks, no voids) over at least the',
        'minimum zone of the schedule, in all cases >= 750 x 750 mm, full depth >= 250 mm, C25 or better, and an edge / drop beam under',
        'every perimeter wall line. K19, K23 need 750; K16, K20, K22 need 700; all others <= 650. Below the minimum: build type B2.',
        'No coring or drilling into a column head in any case. If neither B1 nor B2 can be built, the bay layout is revised, not the anchorage.'], 0.14, 0.24, 118)
    yb = sh.note_block(25.7, yb - 0.45, 'SITE VERIFICATION BEFORE ANCHOR INSTALLATION', [
        '1. Cores as above; rebar scan of the slab top bars at every head to place the 140 (Key A) and 110 (Key B) pockets (<= 1 top bar cut),',
        '   anchors 20 mm clear of the slab bars; scan the column-head cage (6 dia14 + dia6/200) although nothing is drilled into it.',
        '2. Pull-out test on 3 sacrificial M20 anchors (h_ef 200) to 1.3 x max anchor = 60 kN before production drilling; supplier ETA group check.',
        '3. K21: confirm access to the pier faces (notch side and shaft top). WP1: confirm the notch edge beam by core.'], 0.14, 0.24, 118)
    yb = sh.note_block(25.7, yb - 0.45, 'MATERIALS', [
        'Structural steel S275 J0 (EN 10025-2); shear keys and Key B bar S355 (bar f_y 335); plates S275. Bolts 8.8 (EN 15048 / ISO 4014-4032), hot-dip galvanised, snug tight unless noted.',
        'Resin anchors M20 8.8 (M12 at WP1) with an ETA for cracked concrete C25, h_ef 200; installed per the ETA (hole cleaning, cure at 40 C+).',
        'Non-shrink cementitious grout C50 class for the 40 mm bed and the key pockets. Hot-dip galvanising EN ISO 1461 (85 um) all steel; site touch-up zinc-rich.',
        'Cold-formed Z200x2.0 / C sections S350GD+Z275. PIR panel 50 mm, BoardX walls (product data to be confirmed).'], 0.14, 0.24, 118)
    yb = sh.note_block(25.7, yb - 0.45, 'ERECTION SEQUENCE', [
        '1 Cores, scans, pull-out tests, acceptance per head (B1 / B1-E / P / B2).   2 Core the key pockets; set shims and level (top of plate +0.065).',
        '3 Erect columns C1-C27 and WP1 with keys in the pockets; grout pockets and beds; drill and set the resin anchors through the plates; cure.',
        '4 Primaries P1-P19 on the cap plates (4 M20 each, tie plates at rows F and B); temporary guys.   5 Rafters R1-R11, trimmers T1/T2, posts ST1/ST2 (fin plates).',
        '6 Wall bracing B1-B10 and roof rods RT-* (turnbuckles snug, lock nuts); release guys.   7 Purlins, fly braces, eave rail, girts, anti-sag rows.',
        '8 Roof panels from the south (high) edge north, well upstands and flashings, gutter and downpipes, wall panels. No panel before all bracing is in.'], 0.14, 0.24, 118)
    yb = sh.note_block(25.7, yb - 0.45, 'TOLERANCES (EN 1090-2 class 1 unless noted)', [
        'Column base position +/- 10 mm, plumb h/300 (max 10 mm); primary level +/- 5 mm at the cap; rafter TOS +/- 10 mm; anchor pattern +/- 20 mm (cone/bond change < 3 %),',
        'but never closer than 20 mm to a slab bar; pocket position set by scan; grout bed 40 +/- 10 (schedule levels follow: cap top = TOS - 0.28).',
        'Grout thickness: bases_C.md Rev 3 text says 25 mm; 40 mm kept on these drawings for the column lengths (TOS - 0.34) - to be confirmed at sign-off.'], 0.14, 0.24, 118)
    return sh
