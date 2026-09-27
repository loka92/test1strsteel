"""S05 base details per bases_C.md Rev 4: B1 (concentric anchors + Key A [+ Key B]), B2 (through-bolts + inboard key pair), P (K21 pier), WP1."""
import math
from common import *
from geom import *
from s04 import D, K
OX, OY = 260.0, 8.0
B1 = ['K3','K4','K5','K6','K7','K8','K9','K11','K12','K13','K14','K16','K17','K24','K26']
B2 = ['K1','K2','K10','K15','K18','K19','K20','K22','K23','K25','K27']
EW = {'K1','K2','K5','K9','K10','K11','K12','K13','K14','K21','K22','K23','K24'}
KEYB = {'K3':'+y','K4':'+x,+y','K6':'-x','K8':'-x','K14':'+x'}
EDGE_B1 = {'K3','K4','K6','K7','K8','K11','K14'}
B2GEO = {  # keys pair, bolts, lever (mm from the column centre, x along E-W / y along N-S)
 'K1': ('(-300,-200)/(300,-200)', '(-140,-250)/(140,-250)', 2.39), 'K2': ('(-300,-200)/(300,-200)', '(-140,-250)/(140,-250)', 2.39), 'K10': ('(-300,-200)/(300,-200)', '(-140,-250)/(140,-250)', 2.39),
 'K15': ('(200,-300)/(200,300)', '(250,-140)/(250,140)', 2.39), 'K19': ('(200,-300)/(200,300)', '(250,-140)/(250,140)', 2.39),
 'K18': ('(-200,-300)/(-200,300)', '(-250,-140)/(-250,140)', 2.39), 'K20': ('(-200,-300)/(-200,300)', '(-250,-140)/(-250,140)', 2.39),
 'K22': ('(-300,200)/(300,200)', '(-140,250)/(140,250)', 2.39), 'K23': ('(-700,200)/(-100,200)', '(-380,250)/(-100,250)', 2.93),
 'K25': ('(200,0)/(200,600)', '(250,0)/(250,280)', 2.59), 'K27': ('(-200,0)/(-200,600)', '(-250,0)/(-250,280)', 2.59)}
UTIL = {'K1':.42,'K2':.45,'K3':.37,'K4':.53,'K5':.59,'K6':.48,'K7':.86,'K8':.61,'K9':.53,'K10':.38,'K11':.67,'K12':.68,'K13':.55,'K14':.66,'K15':.31,'K16':.76,'K17':.20,'K18':.54,'K19':.52,'K20':.42,'K21':.53,'K22':.74,'K23':.80,'K24':.31,'K25':.83,'K26':.54,'K27':.76}
ZONE_INT = {'K5':600,'K9':600,'K12':650,'K13':600,'K16':700,'K17':400,'K24':450,'K26':550}
def conc_col(d, cx, cy, ew, layer='S-EXIST', label=True):
    a, b = (200, 100) if ew else (100, 200)
    d.rect(cx-a, cy-b, cx+a, cy+b, layer, linetype='DASHED'); d.rect(cx-a+30, cy-b+30, cx+a-30, cy+b-30, layer, linetype='DASHED')
    pts = [(-157, -57), (157, -57), (157, 57), (-157, 57), (0, -57), (0, 57)] if ew else [(-57, -157), (57, -157), (57, 157), (-57, 157), (-57, 0), (57, 0)]
    for x, y in pts: d.sh.circle(*d.P(cx+x, cy+y), 7*K, layer)
    if label: d.text(cx-a, cy+b+15, 'existing column 200 x 400, 6 dia14 + dia6/200 (scan)', 0.12, layer=layer)
def hea_plan(d, cx, cy, ew):
    if ew: d.iprof(cx, cy-76, 152, 160, 6, 9, 'S-COL', rot=0)
    else: d.iprof(cx, cy-80, 160, 152, 9, 6, 'S-COL', rot=1)
def keyA(d, x, y): d.rect(x-45, y-45, x+45, y+45, 'S-DETAIL', lineweight=35); d.sh.circle(*d.P(x, y), 70*K, 'S-DETAIL', linetype='DASHED')
def keyB(d, x, y): d.sh.circle(*d.P(x, y), 30*K, 'S-DETAIL', lineweight=35); d.sh.circle(*d.P(x, y), 55*K, 'S-DETAIL', linetype='DASHED')
def slab_section(d, x0, x1, edge=None):
    d.line(x0, 0, x1, 0, 'S-EXIST', lineweight=35); d.line(x0, -250, x1, -250, 'S-EXIST', lineweight=35)
    d.hatch([(x0, -250), (x1, -250), (x1, 0), (x0, 0)], 0.12, 8, 45)
    d.text(x0+10, -240, 'existing slab 250 (solid zone per coring criterion)', 0.12)
    if edge is not None: d.line(edge, 0, edge, -250, 'S-EXIST', lineweight=50); d.text(edge-30, -230, 'building face / slab edge', 0.12, rot=90)
# ---------------------------------------------------------------- B1
def f_B1_plan(sh, fx, fy):
    d = D(sh, fx, fy, 'B1', 'BASE B1 PLAN', '15 bases K3-K9, K11-K14, K16, K17, K24, K26: plate 300x400x25, 4 M20 resin anchors 80 x 280 h_ef 200, Key A SHS 90x90x8 centred (+ Key B dia 60 at K3, K4, K6, K8, K14)', sheet='S05')
    d.title(-50, 1010, 'B1 interior (K5, K9, K12, K13, K16, K17, K24, K26): example K9, long axis E-W, plate 400 (E-W) x 300')
    cx, cy = 200, 760
    conc_col(d, cx, cy, True); d.rect(cx-200, cy-150, cx+200, cy+150, 'S-DETAIL', lineweight=50); hea_plan(d, cx, cy, True)
    for sx in (-1, 1):
        for sy in (-1, 1): d.hole(cx+sx*140, cy+sy*40, 26)
    keyA(d, cx, cy); d.text(cx+215, cy-15, 'KEY A SHS 90x90x8 in a 140 pocket', 0.12)
    d.dimh(cx-140, cx+140, cy-150, -60); d.dimh(cx-200, cx+200, cy-150, -100); d.dimv(cy-40, cy+40, cx-200, -60); d.dimv(cy-150, cy+150, cx-200, -100)
    d.title(-50, 470, 'B1 edge head (K3, K4, K6, K7, K8, K11, K14): example K3, long axis N-S, edge +y, plate 350 across (100 out / 250 in) + Key B')
    cx, cy = 200, 130
    d.line(-80, cy+100, 520, cy+100, 'S-EXIST', lineweight=50); d.text(530, cy+90, 'building face', 0.12)
    conc_col(d, cx, cy, False, label=False); d.rect(cx-150, cy-250, cx+150, cy+100, 'S-DETAIL', lineweight=50); hea_plan(d, cx, cy, False)
    for sx in (-1, 1):
        for sy in (-1, 1): d.hole(cx+sx*40, cy+sy*140, 26)
    keyA(d, cx, cy); d.rect(cx-45, cy+45, cx+45, cy+70, 'S-HATCH'); keyB(d, cx, cy-180)
    d.text(cx+165, cy-190, 'KEY B dia 60 S355 in a 110 pocket, 180 inboard (c1 250)', 0.12); d.text(cx+165, cy+50, 'compressible strip 25 on the outboard face of pocket A', 0.12)
    d.dimv(cy-140, cy+140, cx-210, -60); d.dimv(cy-250, cy+100, cx-210, -100); d.dimv(cy-180, cy, cx+160, 60); d.dimh(cx-40, cx+40, cy-250, -60); d.dimh(cx-150, cx+150, cy-250, -100)
    d.notes(-50, -200, ['Anchors 26 clearance holes (tension only), 280 spacing along the concrete long axis (E-W or N-S per schedule); anchors 60 inside the head faces, h_ef 200 in the slab, nothing drilled into the column head.',
        'Key B only where the schedule says so (outward shear > 3 kN towards an edge < 0.25 m); corners K4: two Key B. HEA web across the concrete short axis, weld a6 all round.'], 22)
def f_B1_sec(sh, fx, fy):
    d = D(sh, fx, fy, 'B1', 'BASE B1 SECTION 1-1', 'Section along the concrete long axis: anchors at 280, Key A SHS 90x90x8 stub 180 embedded in a 140 cored pocket 200 deep, Key B beyond (dashed) at edge heads', sheet='S05')
    d.title(-50, 1010, 'SECTION 1-1 along the 400 axis of the concrete column')
    slab_section(d, -350, 550)
    d.rect(-200, -250, 200, -900, 'S-EXIST', linetype='DASHED'); d.text(0, -880, 'existing column 400 x 200 (not drilled)', 0.12, 'CENTER')
    for x in (-157, 0, 157): d.line(x, -260, x, -900, 'S-EXIST', linetype='DASHED')
    d.rect(-200, 0, 200, 40, 'S-HATCH'); d.text(210, 5, 'non-shrink grout 40 (see grout note)', 0.12)
    d.rect(-200, 40, 200, 65, 'S-DETAIL', lineweight=50); d.text(210, 60, 'plate 300 x 400 x 25 S275', 0.12)
    d.rect(-80, 65, 80, 600, 'S-COL', lineweight=35); d.line(0, 65, 0, 600, 'S-COL'); d.text(0, 350, 'HEA 160', 0.16, 'CENTER', 90); d.weld(80, 65, 6, 1, 'a6')
    for x in (-140, 140):
        d.rect(x-10, -200, x+10, 65, 'S-DETAIL', lineweight=35); d.rect(x-13, -200, x+13, 0, 'S-DETAIL', linetype='DASHED')
        d.rect(x-16, 65, x+16, 78, 'S-DETAIL'); d.rect(x-16, 78, x+16, 95, 'S-DETAIL')
    d.text(-330, 110, 'M20 8.8 resin anchor h_ef 200 (ETA, cracked C25)', 0.12)
    d.rect(-70, -200, 70, 40, 'S-HATCH'); d.rect(-45, -180, 45, 40, 'S-DETAIL', lineweight=50); d.line(-37, -180, -37, 40, 'S-DETAIL'); d.line(37, -180, 37, 40, 'S-DETAIL')
    d.text(170, -95, 'KEY A SHS 90x90x8 S355, welded a8, 180 embedded, 20 grout under the toe', 0.12); d.text(170, -150, 'pocket cored 140 x 200 deep (by scan, <= 1 top bar cut)', 0.12); d.text(170, -205, 'anchors stop >= 50 above the column top', 0.12)
    d.rect(-240, -200, -180, 40, 'S-DETAIL', linetype='DASHED'); d.text(-330, -120, 'Key B beyond (edge heads), 180 inboard', 0.11, 'LEFT', 90) if False else d.text(-345, -190, 'Key B beyond', 0.11)
    d.dimh(-140, 140, 100, 60); d.dimh(-200, 200, 100, 100); d.dimv(0, 40, -260, -60); d.dimv(40, 65, -260, -60); d.dimv(-200, 0, -260, -100); d.dimv(-250, 0, 260, 60)
    d.dimh(-70, 70, -250, -60); d.dimh(-45, 45, -250, -100)
    d.notes(-350, -900, ['Uplift -> 4 anchors (cone with real edges: 98.5 interior / 50.4 one edge / 37.8 corner kN, x psi_ec); shear -> Key A (83.8 kN, V x 85 mm into the group); outward at edges -> Key B (38.2 kN).',
        'Level on shims, grout pockets and bed, then set the resin anchors through the plate; nuts snug + 1/4 turn. Worst B1: K7 0.86.'], 22)
# ---------------------------------------------------------------- B2
def f_B2_plan(sh, fx, fy):
    d = D(sh, fx, fy, 'B2', 'BASE B2 PLAN', '11 bases K1, K2, K10, K15, K18-K20, K22, K23, K25, K27: plate 700 x 550 x 30 + 2 stiffeners, 2 M24 through-bolts 250 inboard @ 280, pair of SHS 90x90x8 keys 200 inboard, +/-300 along', sheet='S05')
    d.title(-50, 1010, 'PLAN, building face at the top (example K1, long axis E-W, edge +y); row / pair shifted along the wall at K23, K25, K27 (schedule)')
    cx, cy = 230, 560
    d.line(-150, cy+100, 620, cy+100, 'S-EXIST', lineweight=50); d.text(630, cy+90, 'building face', 0.12)
    conc_col(d, cx, cy, True, label=False); d.text(cx-200, cy-250+ -10, '', 0.1)
    d.rect(cx-350, cy-450, cx+350, cy+100, 'S-DETAIL', lineweight=50)
    hea_plan(d, cx, cy, True)
    for sx in (-1, 1): d.rect(cx+sx*80-5, cy-450, cx+sx*80+5, cy-76, 'S-DETAIL', lineweight=35)
    d.text(cx+95, cy-330, 'stiffeners 2 x 120 x 10, flange tips to the inboard end', 0.11)
    for sx in (-1, 1): d.hole(cx+sx*140, cy-250, 26)
    d.text(cx+170, cy-262, 'M24 8.8 through-bolts (26 holes)', 0.12)
    for sx in (-1, 1): keyA(d, cx+sx*300, cy-200)
    d.text(cx-350, cy-140, 'KEY A pair SHS 90x90x8 in 140 pockets', 0.12)
    d.rect(cx-175, cy-450, cx+175, cy-390, 'S-HATCH'); d.text(cx+185, cy-440, 'tip bearing strip 350 x 60 (grout pad)', 0.11)
    d.rect(cx-200, cy-350, cx+200, cy-150, 'S-DETAIL', linetype='DASHDOT'); d.text(cx-200, cy-370, 'under-slab plate 400 x 200 x 20 (dash-dot)', 0.11)
    d.dimv(cy, cy+100, cx-370, -60); d.dimv(cy-250, cy, cx-370, -60); d.dimv(cy-450, cy, cx-370, -100); d.dimv(cy-200, cy, cx+370, 60); d.dimv(cy-450, cy-390, cx+370, 60)
    d.dimh(cx-140, cx+140, cy-450, -60); d.dimh(cx-300, cx+300, cy-450, -100); d.dimh(cx-350, cx+350, cy-450, -140)
    d.notes(-50, -20, ['Bolt row and key pair >= 300 mm from every slab edge: K23 bolts at (-380, 250) / (-100, 250), keys (-700, 200) / (-100, 200); K25 bolts (250, 0) / (250, 280), keys (200, 0) / (200, 600); K27 mirrored; N-S walls (K15, K18-K20): row 250 inboard on x, 280 apart on y.',
        'Bolts in clearance holes carry no shear; keys carry no tension. Ceiling opening ~600 x 600 under each B2 base for the under-slab plate (dry-pack seated).'], 22)
def f_B2_sec2(sh, fx, fy):
    d = D(sh, fx, fy, 'B2', 'BASE B2 SECTION 2-2', 'Across the wall: lever action - bolt row at c = 250 holds the plate down, inboard tip strip at b = 430 bears (T = N_t b/(b-c)); under-slab plate; keys at 200 inboard', sheet='S05')
    d.title(-50, 1010, 'SECTION 2-2 across the wall (building face left, column flush with the face)')
    slab_section(d, -100, 700, edge=-100)
    d.rect(-100, -250, 100, -900, 'S-EXIST', linetype='DASHED'); d.text(0, -880, 'existing column (200 across)', 0.12, 'CENTER')
    d.rect(-100, 0, 450, 40, 'S-HATCH'); d.rect(-100, 40, 450, 70, 'S-DETAIL', lineweight=50); d.text(460, 55, 'plate 700 x 550 x 30', 0.12)
    d.rect(80, 70, 90, 400, 'S-DETAIL', lineweight=35); d.line(90, 400, 450, 70, 'S-DETAIL', lineweight=35); d.text(200, 300, 'stiffener 120 x 10 (2)', 0.12)
    d.rect(-76, 70, 76, 600, 'S-COL', lineweight=35); d.line(-76, 79, 76, 79, 'S-COL'); d.line(-76, 591, 76, 591, 'S-COL'); d.text(-60, 350, 'HEA 160', 0.14, 'LEFT', 90)
    x = 250
    d.rect(x-12, -330, x+12, 70, 'S-DETAIL', lineweight=35); d.rect(x-19, 70, x+19, 105, 'S-DETAIL'); d.rect(x-19, -330, x+19, -295, 'S-DETAIL'); d.rect(x-13, -250, x+13, 0, 'S-DETAIL', linetype='DASHED')
    d.text(x+30, 120, 'M24 8.8 through-bolt (2 @ 280 along the wall), 26 holes, snug + 1/4 turn after grout cure', 0.11)
    d.rect(150, -270, 350, -250, 'S-DETAIL', lineweight=50); d.text(360, -290, 'under-slab plate 400 (along) x 200 x 20 on the solid soffit, dry-packed; ceiling opening ~600 x 600', 0.11)
    d.rect(390, 0, 450, 40, 'S-HATCH'); d.hatch([(390,0),(450,0),(450,40),(390,40)], 0.03, 7, 135); d.text(300, -60, 'tip bearing strip 350 x 60 at 10 MPa (210 kN)', 0.11)
    d.rect(155, -200, 245, 40, 'S-DETAIL', linetype='DASHED'); d.text(-95, -60, 'keys SHS 90 beyond, pair at 200 inboard, +/-300 along', 0.11, rot=90)
    d.dimh(-100, 0, 110, 60); d.dimh(0, 250, 110, 60); d.dimh(0, 430, 110, 100); d.dimh(-100, 450, 110, 140); d.dimv(-250, 0, 480, 60); d.dimv(0, 70, 480, 60)
    d.text(-95, 400, 'c = 250, b = 430: T = N_t b/(b - c) = 2.39 N_t (2.59 / 2.93 at shifted rows)', 0.11)
    d.notes(-100, -900, ['Lever action: bolts T = 2.39 N_t (K19: 175 kN vs 2 M24 = 407 kN), tip compression C = T - N_t on the strip; plate checked for N_t c + M_key (M_Rd 48 kNm). Worst B2: K25 0.83.',
        'Solid concrete from the face to >= 550 inboard and +/- 400 along, soffit accessible; else Rev 2 concept (anchors into the head, h_ef >= 300) at that head, agreed with the reviewer.'], 22)
def f_B2_sec3(sh, fx, fy):
    d = D(sh, fx, fy, 'B2', 'BASE B2 SECTION 3-3', 'Along the wall through the bolt row (250 inboard): 2 M24 at 280, under-slab plate 400 x 200 x 20, keys SHS 90x90x8 at +/-300 beyond', sheet='S05')
    d.title(-50, 1010, 'SECTION 3-3 along the wall, cut 250 mm inboard (through the bolt row and the under-slab plate)')
    slab_section(d, -450, 550)
    d.rect(-200, -250, 200, -900, 'S-EXIST', linetype='DASHED'); d.text(0, -880, 'existing column 400 x 200 beyond (not drilled)', 0.12, 'CENTER')
    d.rect(-350, 0, 350, 40, 'S-HATCH'); d.rect(-350, 40, 350, 70, 'S-DETAIL', lineweight=50); d.text(360, 55, 'plate 700 x 550 x 30', 0.12)
    d.rect(-80, 70, 80, 600, 'S-COL', linetype='DASHED'); d.text(0, 350, 'HEA 160 beyond', 0.14, 'CENTER', 90)
    d.rect(-85, 70, -75, 400, 'S-DETAIL', lineweight=35); d.rect(75, 70, 85, 400, 'S-DETAIL', lineweight=35); d.text(95, 380, 'stiffeners 120 x 10 (cut)', 0.11)
    for x in (-140, 140):
        d.rect(x-12, -330, x+12, 70, 'S-DETAIL', lineweight=35); d.rect(x-19, 70, x+19, 105, 'S-DETAIL'); d.rect(x-19, -330, x+19, -295, 'S-DETAIL'); d.rect(x-13, -250, x+13, 0, 'S-DETAIL', linetype='DASHED')
    d.rect(-200, -270, 200, -250, 'S-DETAIL', lineweight=50); d.text(210, -285, 'under-slab plate 400 x 200 x 20', 0.11)
    for x in (-300, 300):
        d.rect(x-70, -200, x+70, 40, 'S-HATCH'); d.rect(x-45, -180, x+45, 40, 'S-DETAIL', lineweight=50)
    d.text(-440, -110, 'KEY A pair SHS 90x90x8, 180 embedded, 140 pockets (beyond, at 200 inboard)', 0.11)
    d.dimh(-140, 140, 110, 60); d.dimh(-300, 300, 110, 100); d.dimh(-350, 350, 110, 140); d.dimv(-250, 0, 380, 60); d.dimv(-330, 70, -380, -60)
    d.notes(-450, -900, ['Bolts M24 8.8 x 420 in 26 holes cored beside the column head after the rebar scan (<= 1 top bar cut), >= 300 mm to every slab edge; seal the holes; no coring into a column head.',
        'Keys take the whole base shear (bearing 83.8 kN each; outward: edge breakout 41.5 kN each at c1 255); bolts and anchors take none.'], 22)
# ---------------------------------------------------------------- P and WP1
def f_P_WP(sh, fx, fy):
    d = D(sh, fx, fy, 'P', 'K21 PIER BASE, WP1 BASE', 'K21: plate 300x400x25, 4 M16 resin anchors 70 x 280 h_ef 400 into the 200 pier (lap with the pier bars) + saddle 2 x 400x150x15; WP1: plate 250x250x15, one centred 60 key, 280 inboard', sheet='S05')
    d.title(-50, 1010, 'K21 - SECTION N-S across the pier (notch edge y 19.97 left, shaft opening y 20.17 right)')
    d.line(-300, 0, 450, 0, 'S-EXIST', linetype='DASHED'); d.rect(-100, -560, 100, 0, 'S-EXIST', lineweight=35); d.hatch([(-100,-560),(100,-560),(100,0),(-100,0)], 0.12)
    for x in (-57, 57): d.line(x, -560, x, -10, 'S-EXIST', linetype='DASHED')
    for y in (-100, -300, -500): d.rect(-70, y-3, 70, y+3, 'S-EXIST')
    d.text(0, -550, 'pier 200 (K21): 6 dia14 + dia6 links <= 200 (scan)', 0.11, 'CENTER'); d.text(-290, -80, 'notch (outside)', 0.12); d.text(120, -80, 'shaft well', 0.12)
    d.rect(-150, 0, 150, 40, 'S-HATCH'); d.rect(-150, 40, 150, 65, 'S-DETAIL', lineweight=50); d.text(160, 50, 'plate 300 x 400 x 25', 0.12)
    d.rect(-76, 65, 76, 480, 'S-COL', lineweight=35); d.text(0, 280, 'HEA 160', 0.14, 'CENTER', 90)
    for x in (-35, 35): d.rect(x-8, -400, x+8, 65, 'S-DETAIL', lineweight=35); d.rect(x-13, 65, x+13, 90, 'S-DETAIL')
    d.text(-290, 100, 'M16 8.8 resin anchors, 4 at 70 x 280, h_ef 400 into the pier (lap with the pier bars)', 0.11)
    for s in (-1, 1):
        d.rect(s*100 + (0 if s > 0 else -15), -150, s*100 + (15 if s > 0 else 0), 40, 'S-DETAIL', lineweight=50)
        d.rect(s*100 + (15 if s > 0 else -40), -150, s*100 + (40 if s > 0 else -15), 0, 'S-HATCH')
    d.text(-290, -230, 'saddle 2 x 15 S275, 400 long x 150 deep, welded a6 to the plate, grouted 25 against the pier faces: N-S shear 82.5 kN', 0.11)
    d.dimh(-100, 100, -280, -60); d.dimh(-35, 35, 100, 60); d.dimv(-400, 0, 200, 60); d.dimv(-150, 40, 200, 100)
    d.title(-50, -560, 'WP1 - PLAN at the notch corner (77.89, 19.97); post centre at (77.61, 20.25)')
    y0 = -1040
    d.line(-450, y0, 350, y0, 'S-EXIST', lineweight=50); d.line(-450, y0, -450, y0+400, 'S-EXIST', lineweight=50); d.text(-460, y0+60, 'slab edges', 0.12, 'RIGHT')
    cx, cy = -450+280, y0+280
    d.rect(cx-125, cy-125, cx+125, cy+125, 'S-DETAIL', lineweight=50); d.text(cx+135, cy+100, 'plate 250 x 250 x 15', 0.12)
    d.iprof(cx, cy-76, 152, 160, 6, 9, 'S-COL'); keyB(d, cx, cy); d.text(cx+135, cy+40, 'key dia 60, pocket 110 x 200, c1 250 both ways', 0.11)
    for x in (cx-100, cx+100): d.hole(x, cy-100, 14)
    d.text(cx+135, cy-110, '2 M12 for location (no uplift)', 0.11)
    d.dimh(-450, cx, y0, -60); d.dimv(y0, cy, -450, -60)
    d.text(-440, y0-70, 'Demand 11.8 / 8.8 kN vs 38.2 kN edge breakout (0.31); corner girts cantilever 280 to the wall line (D9). Notch edge beam: core to confirm.', 0.11)
# ---------------------------------------------------------------- sheet
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S05', 'BASE DETAILS B1 / B2 / P / WP1 AND NOTES', 'Details drawn 5x in model space (1 m = 200 mm); DIMENSION text = true mm (dimlfac 200)')
    f_B1_plan(sh, 0.4, 16.2); f_B1_sec(sh, 8.7, 16.2); f_B2_plan(sh, 17.0, 16.2)
    f_B2_sec2(sh, 0.4, 2.9); f_B2_sec3(sh, 8.7, 2.9); f_P_WP(sh, 17.0, 2.9)
    rows = []
    for k in COLS:
        ew = k in EW; ax = 'E-W' if ew else 'N-S'
        if k in B1:
            keys = 'A centre' + (' + B ' + KEYB[k] if k in KEYB else ''); bolts = '4 M20 h_ef 200, 80 x 280 (280 %s)' % ax
            plate = '350x400x25' if k in EDGE_B1 else '300x400x25'
            zone = 'face / >=300 in / +/-300 along' if k in EDGE_B1 else '>= %d x %d centred' % (ZONE_INT[k], ZONE_INT[k])
            typ = 'B1'
        elif k in B2:
            kp, bp, lev = B2GEO[k]; keys = 'A pair ' + kp; bolts = '2 M24 through ' + bp + ', lever %.2f' % lev; plate = '700x550x30 + 2 stiff.'; zone = '>=550 in, +/-400 along, soffit'; typ = 'B2'
        else:
            keys = 'saddle N-S'; bolts = '4 M16 h_ef 400 in the pier, 70 x 280'; plate = '300x400x25 + saddle'; zone = 'pier 200 x >= 800, scan'; typ = 'P'
        rows.append(['C' + k[1:], k, typ, ax, keys, bolts, plate, '%.2f' % UTIL[k], zone])
    rows.append(['WP1', '-', 'post', '-', 'one dia 60 centred', '2 M12 location', '250x250x15', '0.31', 'notch edge beam (core)'])
    yb = sh.table(25.7, 29.0, [('Mark',0.8),('K',0.6),('Type',0.7),('Axis',0.7),('Keys (mm from col. centre)',3.1),('Bolts / anchors (mm from col. centre)',4.2),('Plate',2.3),('Util.',0.7),('Solid zone required',2.6)], rows, 0.33, 0.11,
                  title='BASE SCHEDULE (bases_C.md Rev 4 s.3) - worst B1 K7 0.86, B2 K25 0.83, P K21 0.53; x = E-W, y = N-S')
    yb = sh.note_block(25.7, yb - 0.45, 'CORING ACCEPTANCE CRITERION (one-sided at edge heads, Rev 4 section 5)', [
        'B1 heads: solid concrete (no blocks, no voids, full depth >= 250, C25 by rebound + core) over the zone in the schedule: interior heads centred (650 at K12, 600 at K5/K9/K13, 700 at K16, others <= 550); edge heads one-sided: outboard to the building face (100 mm), inboard >= 300 from the column centre, +/- 300 along the wall. A B1 head that fails is built as B2 (no cone needed).',
        'B2 heads: solid concrete from the face to >= 550 mm inboard and +/- 400 along the wall (bolts 300-450 from the face, under-slab plate, key pockets), soffit accessible from below (ceiling opening ~600 x 600 at each of the 11 bases). Not accessible: Rev 2 concept (anchors into the column head, h_ef >= 300, scan) at that head only, agreed with the reviewer.',
        'K21: rebar scan confirming 6 dia14 and links <= 200 in the top 500 mm of the pier; pier faces accessible for the saddle. WP1: notch edge beam by core.',
        'Sequence: cores at 3 heads first (one B1 interior, one B1 edge, one B2), then every head by 60 mm core or GPR against its own line of the schedule. No coring or drilling into a column head except the K21 pier anchors.'], 0.13, 0.22, 128)
    yb = sh.note_block(25.7, yb - 0.4, 'BEFORE ANCHOR / BOLT INSTALLATION (Rev 4 section 6)', [
        '1. Rebar scan of the slab top bars at every head; place the 140 / 110 pockets and the through-bolt holes to cut at most one top bar; anchors 20 mm clear of slab bars.',
        '2. Pull-out test on 3 sacrificial M20 resin anchors (h_ef 200) to 1.3 x max B1 anchor = 45 kN before production drilling; supplier ETA group verification.',
        '3. B2: torque the M24 through-bolts to snug + 1/4 turn after the grout has cured; check the under-slab plate seating (dry-pack). B1: nuts snug + 1/4 turn, no preload relied upon.'], 0.13, 0.22, 128)
    yb = sh.note_block(25.7, yb - 0.4, 'MATERIALS', [
        'Structural steel S275 J0 (EN 10025-2); keys SHS 90x90x8 and Key B bar S355 (bar f_y 335); plates S275. Bolts 8.8 (EN 15048 / ISO 4014-4032), hot-dip galvanised; through-bolts M24 8.8 x 420 with 60 x 6 washers.',
        'Resin anchors M20 8.8 (M16 at K21, M12 at WP1) with an ETA for cracked concrete C25; installed per the ETA (hole cleaning, cure at 40 C+). Non-shrink cementitious grout C50 class for the bed, pockets, saddle and tip strip; dry-pack under the B2 under-slab plates.',
        'Hot-dip galvanising EN ISO 1461 (85 um) all steel; site touch-up zinc-rich. Cold-formed Z200x2.0 / C sections S350GD+Z275. PIR panel 50 mm, BoardX walls (product data to be confirmed).'], 0.13, 0.22, 128)
    yb = sh.note_block(25.7, yb - 0.4, 'ERECTION SEQUENCE', [
        '1 Cores, scans, pull-out tests, acceptance per head (B1 / B2 / P).  2 Core the key pockets and B2 bolt holes; open the ceiling at the 11 B2 bases; set shims and level (top of plate +0.065).',
        '3 Erect columns C1-C27 and WP1 with keys in the pockets; grout pockets and beds; B1: drill and set the resin anchors through the plate; B2: fit the under-slab plates and through-bolts, torque after cure.',
        '4 Primaries P1-P19 on the cap plates (4 M20 each, tie plates at rows F and B); temporary guys.  5 Rafters R1-R11, trimmers T1/T2, posts ST1/ST2 (fin plates).',
        '6 Wall bracing B1-B10 and roof rods RT-* (turnbuckles snug, lock nuts); release guys.  7 Purlins, fly braces, eave rail, girts, anti-sag rows.',
        '8 Roof panels from the south (high) edge north, well upstands and flashings, gutter and downpipes, wall panels. No panel before all bracing is in.'], 0.13, 0.22, 128)
    yb = sh.note_block(25.7, yb - 0.4, 'TOLERANCES (EN 1090-2 class 1 unless noted) AND GROUT NOTE', [
        'Column base position +/- 10 mm, plumb h/300 (max 10 mm); primary level +/- 5 mm at the cap; rafter TOS +/- 10 mm; anchor / bolt pattern +/- 20 mm (cone / lever change < 3 %) but never closer than 20 mm to a slab bar and never < 300 mm to a slab edge (B2); pocket positions set by scan.',
        'Grout: bases_C.md Rev 4 specifies 25 mm non-shrink grout; the column lengths in the schedule (TOS - 0.34) assume a 65 mm base (40 grout + 25 plate). Fabricate columns to the schedule and make up the difference with the grout bed (25-40 mm), or shorten the B2 columns by 5 mm for the 30 mm plate - confirm with the fabricator.'], 0.13, 0.22, 128)
    return sh
