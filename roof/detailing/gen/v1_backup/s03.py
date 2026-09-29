"""S03 typical sections at true scale: A-A N-S at x 87.19, B-B E-W along y 29.3, C-C braced line 5 (x 77.78)."""
from common import *
from geom import *
OX, OY = 160.0, 8.0
PANEL_T = 0.05; PURL_H = 0.20
def iprof(sh, cx, ybot, h, b, tw, tf, layer, lw=35):
    """I-section profile centred at cx, bottom at ybot (sheet-local units)."""
    pts = [(cx-b/2, ybot), (cx+b/2, ybot), (cx+b/2, ybot+tf), (cx+tw/2, ybot+tf), (cx+tw/2, ybot+h-tf), (cx+b/2, ybot+h-tf),
           (cx+b/2, ybot+h), (cx-b/2, ybot+h), (cx-b/2, ybot+h-tf), (cx-tw/2, ybot+h-tf), (cx-tw/2, ybot+tf), (cx-b/2, ybot+tf)]
    sh.pline(pts, layer, True, lineweight=lw); sh.hatch(pts, 'S-HATCH', 'ANSI31', 0.05, 8)
def column(sh, U, Z, u, cy, mark):
    zt = cap_top(cy); k = 'K' + mark[1:]; bt = base_top(k)
    sh.rect(U(u-0.08), Z(bt), U(u+0.08), Z(zt-0.02), 'S-COL', lineweight=35); sh.line(U(u), Z(bt), U(u), Z(zt-0.02), 'S-COL')
    sh.rect(U(u-0.2), Z(GROUT), U(u+0.2), Z(bt), 'S-COL'); sh.rect(U(u-0.14), Z(zt-0.02), U(u+0.14), Z(zt), 'S-COL')
    sh.rect(U(u-0.045), Z(-0.20), U(u+0.045), Z(0.04), 'S-COL')   # Key A SHS 90 stub, 180 embedded (Rev 4)
    sh.text(U(u)+0.12, Z(1.2), mark + ' HEA 160 (' + base_type(k) + ')', TH_SMALL, 'S-COL', rot=90)
def slab(sh, U, Z, a, b, cols):
    sh.line(U(a), Z(0), U(b), Z(0), 'S-EXIST', lineweight=35); sh.line(U(a), Z(-0.25), U(b), Z(-0.25), 'S-EXIST')
    sh.hatch([(U(a),Z(-0.25)),(U(b),Z(-0.25)),(U(b),Z(0)),(U(a),Z(0))], 'S-EXIST', 'ANSI37', 0.12, 8)
    for u, k in cols:
        w = 0.4 if COLS[k]['bx'] > COLS[k]['by'] else 0.2
        sh.rect(U(u-w/2), Z(-1.1), U(u+w/2), Z(-0.25), 'S-EXIST', linetype='DASHED'); sh.text(U(u), Z(-0.95), 'existing ' + k, 0.14, 'S-EXIST', 'CENTER')
        sh.rect(U(u-0.4), Z(-0.25), U(u+0.4), Z(0), 'S-EXIST', linetype='DASHED')   # solid zone 800 assumed
    sh.text(U(a)+0.3, Z(-0.17), 'EXISTING 250 mm HOLLOW-BLOCK SLAB (assumed), solid zones >= 800 x 800 at column heads (cores to confirm)', 0.14, 'S-EXIST')
def wall(sh, U, Z, u, ztop, side):
    d = 0.06 if side > 0 else -0.06
    sh.rect(U(u), Z(0), U(u)+d*side*side, Z(ztop), 'S-DETAIL') if False else None
    sh.pline([(U(u), Z(0)), (U(u), Z(ztop)), (U(u)+0.08*side, Z(ztop)), (U(u)+0.08*side, Z(0))], 'S-DETAIL')
    z = 0.5
    while z < ztop - 0.5: sh.rect(U(u)-0.08*side, Z(z-0.1), U(u), Z(z+0.1), 'S-PURL'); z += 1.2
    sh.text(U(u)+0.15*side, Z(1.0), 'BoardX wall panel on Z200 girts (D9)', 0.14, rot=90, align='LEFT' if side < 0 else 'RIGHT')
def secA(sh, x0, y0):
    U = lambda y: x0 + (y - 19.97); Z = lambda z: y0 + z
    sh.text(x0, y0+5.5, 'SECTION A-A  N-S through the east block on rafter line 8 (x 87.19), looking west (north on the right)', TH)
    slab(sh, U, Z, 19.97, 35.87, [(29.27, 'K12'), (35.77, 'K1')])
    column(sh, U, Z, 29.27, 29.27, 'C12'); column(sh, U, Z, 35.77, 35.77, 'C1')
    for y, mk in ((20.07, 'P15'), (29.27, 'P10'), (35.77, 'P4')):
        iprof(sh, U(y), Z(prim_top(y)-0.33), 0.33, 0.16, 0.0075, 0.0115, 'S-PRIM'); sh.text(U(y)+0.12, Z(prim_top(y)+0.08), mk + ' IPE 330', TH_SMALL, 'S-PRIM')
    # rafter R8 pieces between primaries (fin plates), sloping
    pieces = [(19.97, 20.07-0.09), (20.07+0.09, 29.27-0.09), (29.27+0.09, 35.77-0.09), (35.77+0.09, 35.97)]
    for a, b in pieces:
        sh.pline([(U(a), Z(TOS(a))), (U(b), Z(TOS(b))), (U(b), Z(TOS(b)-0.27)), (U(a), Z(TOS(a)-0.27))], 'S-RAFT', True, lineweight=35)
    sh.text(U(24.5), Z(TOS(24.5)-0.5), 'RAFTER R8 IPE 270, 9.20 m, fin plates D1 each side of the primaries, fly braces at third points (D8)', TH_SMALL, 'S-RAFT')
    for y in PURLIN_Y:
        if 19.97 < y < 35.87: sh.rect(U(y-0.035), Z(TOS(y)), U(y+0.035), Z(TOS(y)+PURL_H), 'S-PURL')
    sh.line(U(19.97), Z(TOS(19.97)+PURL_H), U(35.95), Z(TOS(35.95)+PURL_H), 'S-DETAIL', lineweight=35); sh.line(U(19.97), Z(TOS(19.97)+PURL_H+PANEL_T), U(35.95), Z(TOS(35.95)+PURL_H+PANEL_T), 'S-DETAIL', lineweight=35)
    sh.text(U(31.0), Z(TOS(31.0)+0.45), 'PIR SANDWICH PANEL 50 on Z200x2.0 purlins @ 1.50 m', TH_SMALL)
    # gutter and walls
    sh.rect(U(35.97), Z(TOS(35.9)+0.02), U(36.12), Z(TOS(35.9)+0.12), 'S-DRAIN', lineweight=35); sh.text(U(36.2), Z(TOS(35.9)-0.1), 'box gutter 150x100 (D7)', TH_SMALL, 'S-DRAIN')
    wall(sh, U, Z, 35.87, TOS(35.87)+0.30, +1); wall(sh, U, Z, 19.97, TOS(19.97)+0.30, -1)
    # levels
    ue = U(36.5)
    sh.dimv(Z(0), Z(base_top('K1')), ue, 0.6, 'S-MM1'); sh.dimv(Z(0), Z(col_top(35.77)), ue, 1.1, 'S-MM1'); sh.dimv(Z(0), Z(TOS(35.87)), ue, 1.6, 'S-MM1'); sh.dimv(Z(0), Z(TOS(35.87)+0.30), ue, 2.1, 'S-MM1')
    sh.text(ue+2.45, Z(0.4), 'mm above slab: plate top %d (C1, B2), column top %d, TOS %d, wall %d; clear 3.02 m under the cap nuts, 3.06 m under P4' % (round(base_top('K1')*1000), round(col_top(35.77)*1000), 3330, 3630), 0.13, rot=90)
    uw = U(19.97) - 0.5
    sh.dimv(Z(0), Z(TOS(19.97)), uw, -0.6, 'S-MM1'); sh.dimv(Z(0), Z(col_top(20.07)), uw, -1.1, 'S-MM1')
    sh.text(uw-1.4, Z(0.4), 'TOS south edge %d; column top row B %d' % (round(TOS(19.97)*1000), round(col_top(20.07)*1000)), 0.14, rot=90)
    sh.dimh(U(19.97), U(20.07), Z(0), -1.35); sh.dimh(U(20.07), U(29.27), Z(0), -1.35); sh.dimh(U(29.27), U(35.77), Z(0), -1.35); sh.dimh(U(35.77), U(35.87), Z(0), -1.35)
    sh.dimh(U(19.97), U(35.87), Z(0), -1.75)
    for (y, z, d, s) in ((29.27, 0.1, 'B1', 'S05'), (35.77, cap_top(35.77), 'D2', 'S04'), (20.07, prim_top(20.07)-0.15, 'D1', 'S04'), (35.95, TOS(35.9)+0.1, 'D7', 'S04'), (32.57, TOS(32.57)+0.1, 'D8', 'S04')):
        sh.line(U(y), Z(z), U(y)+0.7, Z(z)+0.6, 'S-TEXT'); sh.bubble(U(y)+1.0, Z(z)+0.85, d, s, 0.42)
def secB(sh, x0, y0):
    U = lambda x: x0 + (x - 67.89); Z = lambda z: y0 + z
    sh.text(x0, y0+5.4, 'SECTION B-B  E-W along primary row F (y 29.27-29.37), looking north (east on the right); rafters and purlins beyond shown dashed', TH)
    cols = [(k, COLS[k]['cx']) for k in ('K8','K9','K10','K11','K12','K13','K14')]
    slab(sh, U, Z, 67.89, 95.69, [(x, k) for k, x in cols])
    for k, x in cols: column(sh, U, Z, x, COLS[k]['cy'], 'C' + k[1:])
    for p in PRIMARIES:
        if 29.2 < p['y'] < 29.4:
            zt = prim_top(p['y']); sh.rect(U(p['x0']), Z(zt-0.33), U(p['x1']), Z(zt), 'S-PRIM', lineweight=35)
            sh.line(U(p['x0']), Z(zt-0.0115), U(p['x1']), Z(zt-0.0115), 'S-PRIM'); sh.line(U(p['x0']), Z(zt-0.33+0.0115), U(p['x1']), Z(zt-0.33+0.0115), 'S-PRIM')
            sh.text(U(0.5*(p['x0']+p['x1'])), Z(zt+0.08), p['mark'] + ' IPE 330', TH_SMALL, 'S-PRIM', 'CENTER')
    zr = TOS(29.3)
    for r in RAFTERS:
        sh.rect(U(r['x']-0.0675), Z(zr-0.27), U(r['x']+0.0675), Z(zr), 'S-RAFT', linetype='DASHED'); sh.text(U(r['x']), Z(zr-0.5), r['mark'], 0.14, 'S-RAFT', 'CENTER')
    for x0_, x1_ in ((67.89, 77.89), (81.79, 95.69)):
        sh.line(U(x0_), Z(zr+PURL_H), U(x1_), Z(zr+PURL_H), 'S-DETAIL', lineweight=35); sh.line(U(x0_), Z(zr+PURL_H+PANEL_T), U(x1_), Z(zr+PURL_H+PANEL_T), 'S-DETAIL', lineweight=35)
    # upstand at the stair well south edge on P8 (D6)
    zt = prim_top(29.27)
    for x in (77.89, 81.79):
        sh.rect(U(x-0.05), Z(zt), U(x+0.05), Z(zr+PURL_H+PANEL_T+0.15), 'S-DETAIL')
    sh.line(U(77.84), Z(zr+PURL_H+PANEL_T+0.15), U(81.84), Z(zr+PURL_H+PANEL_T+0.15), 'S-DETAIL', lineweight=35)
    sh.text(U(79.84), Z(zr+0.55), 'STAIR WELL beyond, open to the north face (no roof, no eave beam): 150 upstand C100x50x3 + flashing on P8 / R5 / R6 (D6), cricket north of P8', TH_SMALL, align='CENTER')
    wall(sh, U, Z, 67.89, zr+0.30, -1); wall(sh, U, Z, 95.69, zr+0.30, +1)
    xs = [x for _, x in cols]
    sh.dimh(U(67.89), U(xs[0]), Z(0), -1.35)
    for a, b in zip(xs[:-1], xs[1:]): sh.dimh(U(a), U(b), Z(0), -1.35)
    sh.dimh(U(xs[-1]), U(95.69), Z(0), -1.35); sh.dimh(U(67.89), U(95.69), Z(0), -1.75)
    uw = U(67.89) - 0.5
    sh.dimv(Z(0), Z(col_top(29.27)), uw, -0.6, 'S-MM1'); sh.dimv(Z(0), Z(zr), uw, -1.1, 'S-MM1'); sh.dimv(Z(0), Z(zr+PURL_H+PANEL_T), uw, -1.6, 'S-MM1')
    sh.text(uw-1.95, Z(0.3), 'column top %d / TOS %d / panel top %d (row F)' % (round(col_top(29.27)*1000), round(zr*1000), round((zr+PURL_H+PANEL_T)*1000)), 0.14, rot=90)
    for (x, z, d, s) in ((87.19, cap_top(29.27), 'D2', 'S04'), (81.85, cap_top(29.27), 'D3', 'S04'), (72.09, 0.1, 'B1', 'S05'), (81.79, zr+0.4, 'D6', 'S04'), (95.48, 0.3, 'D4', 'S04')):
        sh.line(U(x), Z(z), U(x)+0.7, Z(z)+0.6, 'S-TEXT'); sh.bubble(U(x)+1.0, Z(z)+0.85, d, s, 0.42)
def secC(sh, x0, y0):
    U = lambda y: x0 + (y - 15.57); Z = lambda z: y0 + z
    sh.text(x0, y0+5.5, 'SECTION C-C  braced line 5 (rafter R5, x 77.78) with bays B7 (C27-C20) and B8 (C10-C16), looking west (north on the right); R5 ends at the west north edge y 35.37', TH)
    cols = [('K27', 15.87), ('K20', 21.76), ('K16', 24.46), ('K10', 29.27), ('K7', 35.17)]
    slab(sh, U, Z, 15.57, 35.37, [(y, k) for k, y in cols])
    for k, y in cols: column(sh, U, Z, y, y, 'C' + k[1:])
    for y, mk in ((15.92, 'P19'), (21.76, 'P13'), (24.46, 'P12'), (29.27, 'P7/P8'), (35.22, 'P2')):
        iprof(sh, U(y), Z(prim_top(y)-0.33), 0.33, 0.16, 0.0075, 0.0115, 'S-PRIM'); sh.text(U(y)+0.12, Z(prim_top(y)+0.08), mk, TH_SMALL, 'S-PRIM')
    for y, mk in ((24.09, 'T2'),):
        iprof(sh, U(y), Z(TOS(y)-0.27), 0.27, 0.135, 0.0066, 0.0102, 'S-RAFT'); sh.text(U(y)-0.5, Z(TOS(y)+0.35), mk + ' IPE 270', TH_SMALL, 'S-RAFT')
    sups = [15.92, 21.76, 24.46, 29.27, 35.22]; edges = [15.57] + [s for s in sups] + [35.37]
    for a, b in zip(edges[:-1], edges[1:]):
        aa = a + (0.09 if a in sups else 0); bb = b - (0.09 if b in sups else 0)
        sh.pline([(U(aa), Z(TOS(aa))), (U(bb), Z(TOS(bb))), (U(bb), Z(TOS(bb)-0.27)), (U(aa), Z(TOS(aa)-0.27))], 'S-RAFT', True, lineweight=35)
    for y in PURLIN_Y:
        if y < 35.37: sh.rect(U(y-0.035), Z(TOS(y)), U(y+0.035), Z(TOS(y)+PURL_H), 'S-PURL')
    sh.line(U(15.57), Z(TOS(15.57)+PURL_H), U(35.37), Z(TOS(35.37)+PURL_H), 'S-DETAIL', lineweight=35)
    sh.rect(U(35.32), Z(TOS(35.37)+0.02), U(35.47), Z(TOS(35.37)+0.12), 'S-DRAIN', lineweight=35); sh.text(U(35.5), Z(TOS(35.37)-0.15), 'G-W gutter (D7), stop end at x 77.89', TH_SMALL, 'S-DRAIN')
    wall(sh, U, Z, 35.37, TOS(35.37)+0.30, +1)
    for (ya, yb) in ((20.17, 24.16), (29.37, 35.37)):
        sh.line(U(ya), Z(TOS(ya)+PURL_H+PANEL_T+0.15), U(yb), Z(TOS(yb)+PURL_H+PANEL_T+0.15), 'S-DETAIL', lineweight=35)
        for y in (ya, yb): sh.rect(U(y-0.05), Z(TOS(y)+PURL_H), U(y+0.05), Z(TOS(y)+PURL_H+PANEL_T+0.15), 'S-DETAIL')
        sh.text(U(0.5*(ya+yb)), Z(TOS(ya)+0.65), 'well upstand along R5 (D6)', TH_SMALL, align='CENTER')
    for bid, (ya, yb) in (('B7', (15.87, 21.76)), ('B8', (24.46, 29.27))):
        z1 = BASE_TOP + 0.1; z2 = min(cap_top(ya), cap_top(yb)) + 0.17
        sh.line(U(ya), Z(z1), U(yb), Z(z2), 'S-BRACE', lineweight=50); sh.line(U(ya), Z(z2), U(yb), Z(z1), 'S-BRACE', lineweight=50)
        sh.text(U(0.5*(ya+yb)), Z(0.5*(z1+z2)+0.4), bid + ' 2 x L70x7 X (D4)', TH_SMALL, 'S-BRACE', 'CENTER')
    sh.rect(U(20.25-0.08), Z(BASE_TOP), U(20.25+0.08), Z(TOS(19.97)-0.30), 'S-COL', linetype='DASHED'); sh.text(U(20.25)+0.1, Z(0.8), 'WP1 beyond (77.61, 20.25), D10', 0.14, 'S-COL', rot=90)
    sh.text(U(17.0), Z(TOS(17.0)+0.6), 'notch verge flashing y 19.97 and south wall y 15.57 beyond', 0.14)
    ys = [y for _, y in cols]
    sh.dimh(U(15.57), U(ys[0]), Z(0), -1.35)
    for a, b in zip(ys[:-1], ys[1:]): sh.dimh(U(a), U(b), Z(0), -1.35)
    sh.dimh(U(ys[-1]), U(35.37), Z(0), -1.35); sh.dimh(U(15.57), U(35.37), Z(0), -1.75)
    uw = U(15.57) - 0.5; sh.dimv(Z(0), Z(TOS(15.57)), uw, -0.6, 'S-MM1'); sh.dimv(Z(0), Z(col_top(15.87)), uw, -1.1, 'S-MM1')
    sh.text(uw-1.4, Z(0.3), 'TOS south %d / column top C27 %d' % (round(TOS(15.57)*1000), round(col_top(15.87)*1000)), 0.14, rot=90)
    sh.line(U(18.8), Z(1.0), U(18.8)+0.7, Z(1.6), 'S-TEXT'); sh.bubble(U(18.8)+1.0, Z(1.85), 'D4', 'S04', 0.42)
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S03', 'TYPICAL SECTIONS A-A, B-B, C-C', 'Sections 1:1 in model space (m); levels in mm; print 1:100 on A1')
    secA(sh, 12.0, 22.5); secB(sh, 4.0, 14.0); secC(sh, 8.0, 4.5)
    return sh
