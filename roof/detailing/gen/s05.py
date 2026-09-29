"""S05 base details per bases_C.md Rev 8: type E (post-installed rebars + keys) at all 27 columns, P at K21, WP1."""
import math, textwrap
from common import *
from geom import *
from s04 import D, K, prep
OX, OY = 260.0, 8.0
def conc_col(d, cx, cy, ew, label=True):
    a, b = (200, 100) if ew else (100, 200)
    d.rect(cx-a, cy-b, cx+a, cy+b, 'S-EXIST', linetype='DASHED'); d.rect(cx-a+30, cy-b+30, cx+a-30, cy+b-30, 'S-EXIST', linetype='DASHED')
    pts = [(-157, -57), (157, -57), (157, 57), (-157, 57), (0, -57), (0, 57)] if ew else [(-57, -157), (57, -157), (57, 157), (-57, 157), (-57, 0), (57, 0)]
    for x, y in pts: d.circle(cx+x, cy+y, 7, 'S-EXIST')
    if label: d.label(cx-a, cy+b, 'existing column 200x400 (scan)', 0.16, prefer='L')
def hea_plan(d, cx, cy, ew):
    if ew: d.iprof(cx, cy-66.5, 133, 140, 5.5, 8.5, 'S-COL', rot=0)
    else: d.iprof(cx, cy-70, 140, 133, 8.5, 5.5, 'S-COL', rot=1)
def keyA(d, x, y): d.rect(x-45, y-45, x+45, y+45, 'S-DETAIL', lineweight=35); d.circle(x, y, 70, linetype='DASHED')
def keyB(d, x, y): d.circle(x, y, 30, lineweight=35); d.circle(x, y, 55, linetype='DASHED')
def rebars(d, cx, cy, ew):
    ax, ay = (120, 35) if ew else (35, 120)
    for sx in (-1, 1):
        for sy in (-1, 1): d.hole(cx+sx*ax, cy+sy*ay, 30)
def f_E_plan(sh, fx, fy):
    d = D(sh, fx, fy, 'E', 'BASE E PLAN', 'All 27 columns: plate 300x400x20 (key-pair plates per schedule), 4 dia 16 B500 post-installed bars at 70 x 240 (240 along the concrete long axis), Key A SHS 90x90x8 (+ Key B / key pair)', sheet='S05')
    d.title(1, 'Key A base, long axis E-W: K9, K11, K12, K13'); cx, cy = 200, 760
    conc_col(d, cx, cy, True); d.rect(cx-200, cy-150, cx+200, cy+150, 'S-DETAIL', lineweight=50); hea_plan(d, cx, cy, True); rebars(d, cx, cy, True); keyA(d, cx, cy)
    d.label(cx+45, cy, 'Key A SHS 90x90x8, pocket 140'); d.label(cx+120, cy+35, 'dia 16 bar, hole 30')
    d.dimh(cx-120, cx+120, cy-150, -60); d.dimh(cx-200, cx+200, cy-150, -100); d.dimv(cy-150, cy+150, cx+200, 60)
    d.title(2, 'Key A + B edge base, N-S: K3, K4, K6, K8 (K14 E-W)', y=310); cx, cy = 200, 80
    d.line(-80, cy+100, 520, cy+100, 'S-EXIST', lineweight=50); d.label(520, cy+100, 'building face', prefer='R')
    conc_col(d, cx, cy, False, label=False); d.rect(cx-150, cy-200, cx+150, cy+100, 'S-DETAIL', lineweight=50); hea_plan(d, cx, cy, False); rebars(d, cx, cy, False)
    keyA(d, cx, cy); d.rect(cx-45, cy+45, cx+45, cy+70, 'S-HATCH'); keyB(d, cx, cy-180)
    d.label(cx+30, cy-180, 'Key B dia 60, 180 inboard'); d.label(cx+45, cy+58, 'compressible strip 25')
    d.dimv(cy-120, cy+120, cx-210, -60); d.dimv(cy-200, cy+100, cx-210, -100); d.dimv(cy-180, cy, cx+160, 60); d.dimh(cx-150, cx+150, cy-200, -60)
    d.notes(['Bars 4 dia 16 B500 threaded M16, 70 x 240 centred on the column (35 / 120 from the centre), 26 nominal clear to the corner dia14; pattern set on site +/-15 from the scan. Plate holes 30 with 10 mm washers. Key B only where the schedule says so (K3 +y, K4 +x +y, K6 -x +y, K8 -x, K14 +x).'])
def f_E_sec(sh, fx, fy):
    d = D(sh, fx, fy, 'E', 'BASE E SECTION', 'Section along the concrete long axis: bars at 240, hole 20 x 600 (300 slab + 300 head, 250 min), top 300 debonded (sleeve), resin in the head only; Key A stub 180 in a 140 pocket', sheet='S05')
    d.title(1, 'SECTION 1-1 along the concrete long axis')
    d.line(-280, 0, 520, 0, 'S-EXIST', lineweight=35); d.line(-280, -300, 520, -300, 'S-EXIST', lineweight=35); d.hatch([(-280,-300),(520,-300),(520,0),(-280,0)], 0.12, 8, 45); d.label(-280, -300, 'slab 300 (GPR)', prefer='R')
    d.rect(-200, -300, 200, -950, 'S-EXIST', linetype='DASHED'); d.label(0, -950, 'column head 400x200, 6 dia14', prefer='C')
    for x in (-157, 0, 157): d.line(x, -310, x, -950, 'S-EXIST', linetype='DASHED')
    d.rect(-200, 0, 200, 25, 'S-HATCH'); d.label(200, 12, 'grout 25', prefer='R'); d.rect(-200, 25, 200, 45, 'S-DETAIL', lineweight=50); d.label(-200, 40, 'plate 300x400x20', prefer='L')
    d.rect(-70, 45, 70, 600, 'S-COL', lineweight=35); d.line(0, 330, 0, 600, 'S-COL'); d.label(70, 350, 'HEA 140, a6'); d.weld(70, 45, 6, 1)
    for x in (-120, 120):
        d.rect(x-8, -600, x+8, 45, 'S-DETAIL', lineweight=35); d.rect(x-10, -600, x+10, 0, 'S-DETAIL', linetype='DASHED')
        d.rect(x-13, -300, x+13, 0, 'S-DETAIL'); d.rect(x-14, 45, x+14, 57, 'S-DETAIL'); d.rect(x-14, 57, x+14, 72, 'S-DETAIL')
    d.label(-120, 60, 'dia 16 bar, M16 nut', prefer='L'); d.label(128, -150, 'sleeve, top 300 debonded', prefer='R'); d.label(128, -450, 'resin 300 into the head', prefer='R')
    d.rect(-70, -200, 70, 25, 'S-HATCH'); d.rect(-45, -180, 45, 25, 'S-DETAIL', lineweight=50); d.line(-37, -180, -37, 25, 'S-DETAIL'); d.line(37, -180, 37, 25, 'S-DETAIL')
    d.label(-45, -120, 'Key A SHS 90, pocket 140, a8', prefer='L')
    d.dimv(-300, 0, -260, -60); d.dimv(-600, -300, -260, -60)
    d.notes(['Load path: uplift -> 4 bars lapped with the column-head bars (bond 4 x 33.9 kN per 250 mm, no slab cone); shear -> Key A (83.8 kN, rigid-post key moment V x 85 into the group); outward shear at edges -> Key B or the inboard key pair.',
             'Procedure (bases_C.md s.1, V3): cover-meter on 4 faces, GPR from above, mark the pattern, 10 mm pilot 600 deep with feed monitoring (steel contact: relocate +/-15, re-pilot), 20 mm hole, clean x2, sleeve the top 300, inject the head part, set the bar; proof test 3 bars >= 60 kN, 2 min, <= 1 mm.'])
def f_pair(sh, fx, fy):
    d = D(sh, fx, fy, 'E', 'KEY-PAIR PLAN', 'Edge / braced bases K1, K2, K5, K7, K10, K15, K18, K19, K20, K22, K23, K25, K27: plate 800 x 400 x 20 standard (K7 / K23 / K25 / K27 / K15-K20 per schedule), inboard SHS 90 key pair, same 4 bars', sheet='S05')
    d.title(1, 'PLAN, building face at the top (K1: E-W, edge +y)'); cx, cy = 230, 560
    d.line(-150, cy+100, 620, cy+100, 'S-EXIST', lineweight=50); d.label(620, cy+100, 'building face', prefer='R')
    conc_col(d, cx, cy, True, label=False); d.rect(cx-400, cy-300, cx+400, cy+100, 'S-DETAIL', lineweight=50); hea_plan(d, cx, cy, True); rebars(d, cx, cy, True)
    for sx in (-1, 1): keyA(d, cx+sx*300, cy-200)
    d.label(cx-300, cy-245, 'Key A pair SHS 90x90x8', prefer='L'); d.label(cx+120, cy+35, '4 dia 16 at 70 x 240')
    d.dimv(cy, cy+100, cx-420, -60); d.dimv(cy-300, cy, cx-420, -60); d.dimv(cy-200, cy, cx+420, 60); d.dimh(cx-120, cx+120, cy-300, -60); d.dimh(cx-300, cx+300, cy-300, -100); d.dimh(cx-400, cx+400, cy-300, -140)
    d.notes(['Key pair >= 300 from every slab edge: K7 plate 400 x 950 keys (-200, -700) / (-200, -100); K23 1000 x 400 keys (-700, 200) / (-100, 200); K25 400 x 850 keys (200, 0) / (200, 600); K27 mirrored; N-S walls K15 / K19 keys (200, +/-300), K18 / K20 (-200, +/-300); K22 (+/-300, 200); K5 / K10 as K1. No stiffeners (concentric uplift, no lever).',
             'Slab solid 300 over the key bodies (schedule) - GPR; bars unchanged; plate strip under the key moment governs at the E-W bay bases (K23 0.68, K22 0.67, K20 0.64, K27 0.64).'])
def f_P_WP(sh, fx, fy):
    d = D(sh, fx, fy, 'P', 'K21 PIER, WP1', 'K21: plate 300x400x20, 4 dia 16 bars into the 200 pier (pattern fixed on site from the scan) + saddle 2 x 400x150x15; WP1: plate 250x250x15, one centred dia 60 key, 280 inboard', sheet='S05')
    d.title(1, 'K21 - SECTION N-S across the pier', y=560)
    d.line(-300, 0, 450, 0, 'S-EXIST', linetype='DASHED'); d.rect(-100, -560, 100, 0, 'S-EXIST', lineweight=35); d.hatch([(-100,-560),(100,-560),(100,0),(-100,0)], 0.12)
    for x in (-57, 57): d.line(x, -560, x, -10, 'S-EXIST', linetype='DASHED')
    for y in (-100, -300, -500): d.rect(-70, y-3, 70, y+3, 'S-EXIST')
    d.label(0, -560, 'pier 200: 6 dia14 + links (scan)', 0.16, prefer='C'); d.label(-300, -60, 'notch', prefer='L'); d.label(300, -60, 'shaft well', prefer='R')
    d.rect(-150, 0, 150, 25, 'S-HATCH'); d.rect(-150, 25, 150, 45, 'S-DETAIL', lineweight=50); d.label(150, 35, 'plate 300x400x20')
    d.rect(-66.5, 45, 66.5, 480, 'S-COL', lineweight=35); d.label(66.5, 300, 'HEA 140')
    for x in (-35, 35): d.rect(x-8, -400, x+8, 45, 'S-DETAIL', lineweight=35); d.rect(x-14, 45, x+14, 70, 'S-DETAIL')
    d.label(-43, -400, 'dia 16 bars, 300 into the pier', prefer='L')
    for s in (-1, 1):
        d.rect(s*100 + (0 if s > 0 else -15), -150, s*100 + (15 if s > 0 else 0), 25, 'S-DETAIL', lineweight=50); d.rect(s*100 + (15 if s > 0 else -40), -150, s*100 + (40 if s > 0 else -15), 0, 'S-HATCH')
    d.label(140, -150, 'saddle 2 x 15, grouted', prefer='R')
    d.dimh(-100, 100, -560, -60); d.dimv(-400, 0, 200, 60)
    d.title(2, 'WP1 - PLAN at the notch corner', y=-760); y0 = -1250
    d.line(-450, y0, 350, y0, 'S-EXIST', lineweight=50); d.line(-450, y0, -450, y0+400, 'S-EXIST', lineweight=50); d.label(-450, y0+350, 'slab edges', prefer='L')
    cx, cy = -170, y0+280
    d.rect(cx-125, cy-125, cx+125, cy+125, 'S-DETAIL', lineweight=50); d.label(cx+125, cy+100, 'plate 250x250x15')
    d.iprof(cx, cy-66.5, 133, 140, 5.5, 8.5, 'S-COL'); keyB(d, cx, cy); d.label(cx+30, cy, 'key dia 60, c1 250')
    for x in (cx-100, cx+100): d.hole(x, cy-100, 14)
    d.label(cx+100, cy-100, '2 M12 location'); d.dimh(-450, cx, y0, -60); d.dimv(y0, cy, -450, -60)
    d.notes(['WP1: 11.4 / 8.5 kN vs 41.9 kN edge breakout (0.27); corner girts cantilever 280 to the wall line (D9); notch edge beam by GPR. K21: saddle 82.5 kN N-S; pier faces accessible from the notch and the shaft top (client).'])
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S05', 'BASE DETAILS TYPE E / P / WP1 AND SCHEDULE', 'Details drawn 4x or 5x in model space (scale in each frame); DIMENSION text = true mm (dimlfac 250 / 200)')
    for f, fx in ((f_E_plan, 0.3), (f_E_sec, 10.65), (f_pair, 21.0), (f_P_WP, 31.35)): prep(f); f(sh, fx, 16.4)
    u = base_util(); rows = []
    for k in COLS:
        ew = k in EW_COLS; typ = base_type(k)
        keys = 'saddle' if k == 'K21' else ('A pair ' + KEYPAIR[k] if k in KEYPAIR else 'A centre' + (' + B ' + KEYB[k] if k in KEYB else ''))
        plate = '300x400x20 + saddle' if k == 'K21' else PLATE.get(k, '300x400x20')
        rows.append(['C' + k[1:], k, typ, 'E-W' if ew else 'N-S', '4 d16 (+/-%d, +/-%d)' % ((120, 35) if ew else (35, 120)), keys, plate, '%.2f' % u.get(k, (0, ''))[0], u.get(k, (0, ''))[1][:38]])
    rows.append(['WP1', '-', 'post', '-', '2 M12', 'one dia 60 centred', '250x250x15', '0.27', 'key edge breakout'])
    yb = sh.table(0.3, 15.6, [('Mark',0.8),('K',0.6),('Type',0.6),('Axis',0.7),('Bars (mm from centre)',2.4),('Keys (mm from centre)',3.2),('Plate (extents from centre)',4.2),('Util.',0.7),('Governing check',3.9)], rows, 0.33, 0.14,
                  title='BASE SCHEDULE (bases_C.md Rev 8 s.3): x E-W, y N-S; all type E, P at K21; worst K7 0.83')
    sh.note_block(18.2, 15.6, 'SLAB AND COLUMN-HEAD VERIFICATION (bases_C.md Rev 8 s.5-6)', [
        'No solid-zone criterion for the anchorage: the bars depend on the column head only (6 dia14, dia6 links, C25) - confirmed by the face cover-meter scan of every head and 3-6 cores for the grade. The slab must be solid (no blocks) and 300 mm thick under each base plate and around the key pockets (Key A +/- 400; key pairs: the key breakout bodies, +/- 700 along the wall for the standard pair) - GPR from above at all 27 heads, also for the slab top bars at the pockets.',
        'A head with fewer than 4 sound corner bars or links > 200: embedment 300-350 (bond alone 4 x 33.9 kN per 250) and the lap re-checked with the scanned bars before drilling; a head that cannot be drilled: appendix B1 detail (4 M20 resin anchors h_ef 250 in the slab, GPR-verified 800 x 800 solid zone) at that head - client option for the 7 interior columns K9, K12, K13, K16, K17, K24, K26.',
        'Before installation: scan sequence (faces from below, GPR from above, pilot drill); pockets 140 / 110 placed to cut at most one slab top bar; proof tests of 3 production bars (interior, edge, corner) to >= 60 kN held 2 min, displacement <= 1 mm; EAD 330087 injection system, certified installer; nuts snug + 1/4 turn after the grout has cured; scan sheet with the final pattern filed per head.',
        'No through-bolts, no ceiling access, no under-slab plates (Rev 8). Grout bed 25 +/- 5 mm; columns cut to the surveyed plate-top level (S00 s.9).'], 0.16, 23.2)
    sh.legend_block([('S-COL','box','HEA 140 column'), ('S-DETAIL','box','Base plate / keys'), ('S-EXIST','hatch','Existing slab / column head'), ('S-HATCH','hatch','Grout / pockets')], 0.3, 3.4, 8.4)
    return sh
