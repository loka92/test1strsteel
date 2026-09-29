"""S03 typical sections A-A (x 87.19), B-B (row F), C-C (line 5) at true scale, Rev 6a levels."""
from common import *
from geom import *
OX, OY = 160.0, 8.0
PANEL_T, PURL_H = 0.05, 0.20
def iprof(sh, cx, ybot, h, b, tw, tf, layer, owner, lw=35):
    pts = [(cx-b/2, ybot), (cx+b/2, ybot), (cx+b/2, ybot+tf), (cx+tw/2, ybot+tf), (cx+tw/2, ybot+h-tf), (cx+b/2, ybot+h-tf), (cx+b/2, ybot+h), (cx-b/2, ybot+h), (cx-b/2, ybot+h-tf), (cx-tw/2, ybot+h-tf), (cx-tw/2, ybot+tf), (cx-b/2, ybot+tf)]
    sh.pline(pts, layer, True, owner=owner, lineweight=lw); sh.hatch(pts, 'S-HATCH', 'ANSI31', 0.05, 8)
def column(sh, U, Z, u, cy, mark):
    zt = cap_top(cy); o = mark
    sh.rect(U(u-0.07), Z(BASE_TOP), U(u+0.07), Z(zt-0.02), 'S-COL', owner=o, lineweight=35); sh.line(U(u), Z(BASE_TOP), U(u), Z(zt-0.02), 'S-COL', owner=o)
    sh.rect(U(u-0.2), Z(GROUT), U(u+0.2), Z(BASE_TOP), 'S-COL', owner=o); sh.rect(U(u-0.14), Z(zt-0.02), U(u+0.14), Z(zt), 'S-COL', owner=o)
    sh.rect(U(u-0.045), Z(-0.20), U(u+0.045), Z(GROUT), 'S-COL', owner=o)
    sh.label(mark + ' HEA 140', U(u), Z(1.4), TH_DIM, 'S-TEXT-MEMBER', rot=90, cands=[(0.12, 0, 'LEFT'), (-0.12, 0, 'RIGHT'), (0.12, 0.8, 'LEFT')], allowed=(o,), leader=False)
def slab(sh, U, Z, a, b, cols):
    sh.line(U(a), Z(0), U(b), Z(0), 'S-EXIST', owner='slab', lineweight=35); sh.line(U(a), Z(-0.30), U(b), Z(-0.30), 'S-EXIST', owner='slab')
    sh.hatch([(U(a),Z(-0.30)),(U(b),Z(-0.30)),(U(b),Z(0)),(U(a),Z(0))], 'S-EXIST', 'ANSI37', 0.12, 8)
    for u, k in cols:
        w = 0.4 if COLS[k]['bx'] > COLS[k]['by'] else 0.2
        sh.rect(U(u-w/2), Z(-1.1), U(u+w/2), Z(-0.30), 'S-EXIST', owner='slab', linetype='DASHED')
        sh.label('existing ' + k, U(u), Z(-0.75), 0.16, 'S-TEXT-DIM', cands=[(0, 0, 'CENTER'), (0, -0.25, 'CENTER'), (0.5, 0, 'LEFT')], allowed=('slab',), leader=False)
def wall(sh, U, Z, u, ztop, side):
    o = 'wall%.1f' % u
    sh.pline([(U(u), Z(0)), (U(u), Z(ztop)), (U(u)+0.08*side, Z(ztop)), (U(u)+0.08*side, Z(0))], 'S-DETAIL', owner=o)
    z = 0.5
    while z < ztop - 0.5: sh.rect(U(u)-0.08*side, Z(z-0.1), U(u), Z(z+0.1), 'S-PURL', owner=o); z += 1.2
    sh.label('BoardX wall on Z200 girts (D9)', U(u)+0.35*side, Z(0.6), 0.16, 'S-TEXT-DIM', rot=90, cands=[(0, 0, 'LEFT'), (0.3*side, 0, 'LEFT')], allowed=(o,), leader=False)
def rafter_pieces(sh, U, Z, edges, sups, mark):
    for a, b in zip(edges[:-1], edges[1:]):
        aa = a + (0.08 if a in sups else 0); bb = b - (0.08 if b in sups else 0)
        sh.pline([(U(aa), Z(TOS(aa))), (U(bb), Z(TOS(bb))), (U(bb), Z(TOS(bb)-0.24)), (U(aa), Z(TOS(aa)-0.24))], 'S-RAFT', True, owner=mark, lineweight=35)
def purlins_panel(sh, U, Z, ya, yb, opens=()):
    for y in PURLIN_Y:
        if ya < y < yb and not any(o0 < y < o1 for o0, o1 in opens): sh.rect(U(y-0.035), Z(TOS(y)), U(y+0.035), Z(TOS(y)+PURL_H), 'S-PURL', owner='purl')
    sh.line(U(ya), Z(TOS(ya)+PURL_H), U(yb), Z(TOS(yb)+PURL_H), 'S-DETAIL', owner='panel', lineweight=35); sh.line(U(ya), Z(TOS(ya)+PURL_H+PANEL_T), U(yb), Z(TOS(yb)+PURL_H+PANEL_T), 'S-DETAIL', owner='panel', lineweight=35)
def secA(sh, x0, y0):
    U = lambda y: x0 + (y - 19.97); Z = lambda z: y0 + z; o = 'secA'
    sh.text(x0, y0+5.6, 'SECTION A-A  rafter line 8 (x 87.19), looking west', TH_TITLE, 'S-TEXT-NOTE', allowed=(o,), owner=o)
    slab(sh, U, Z, 19.97, 35.87, [(29.27, 'K12'), (35.77, 'K1')])
    column(sh, U, Z, 29.27, 29.27, 'C12'); column(sh, U, Z, 35.77, 35.77, 'C1')
    for y, mk in ((20.07, 'P15'), (29.27, 'P10'), (35.77, 'P4')):
        iprof(sh, U(y), Z(prim_top(y)-0.30), 0.30, 0.15, 0.0071, 0.0107, 'S-PRIM', mk)
        sh.label(mk + ' IPE 300', U(y), Z(prim_top(y)), TH_DIM, 'S-TEXT-MEMBER', cands=[(0.15, 0.12, 'LEFT'), (-0.15, 0.12, 'RIGHT'), (0.15, 0.5, 'LEFT')], allowed=(mk,), leader=False)
    rafter_pieces(sh, U, Z, [19.97, 20.07, 29.27, 35.77, 35.97], [20.07, 29.27, 35.77], 'R8')
    sh.label('RAFTER R8 IPE 240: 9.20 m span, fin plates FP1 (D1), fly braces at the third points (D8)', U(24.5), Z(TOS(24.5)-0.24), TH_DIM, 'S-TEXT-MEMBER', cands=[(0, -0.45, 'CENTER'), (0, -0.8, 'CENTER')], allowed=('R8',), leader=False)
    purlins_panel(sh, U, Z, 19.97, 35.95)
    sh.label('PIR sandwich panel 50 on Z200x2.0 purlins @ 1.50 m', U(31.0), Z(TOS(31.0)+0.25), TH_DIM, 'S-TEXT-DIM', cands=[(0, 0.15, 'CENTER'), (0, 0.5, 'CENTER'), (-2, 0.15, 'CENTER')], allowed=('panel', 'purl'), leader=False)
    sh.rect(U(35.97), Z(TOS(35.9)+0.02), U(36.12), Z(TOS(35.9)+0.12), 'S-DRAIN', owner='gut', lineweight=35)
    sh.label('box gutter 150x100 (D7)', U(36.1), Z(TOS(35.9)+0.07), TH_DIM, 'S-TEXT-DIM', cands=[(0.15, 0.3, 'LEFT'), (0.15, -0.5, 'LEFT'), (0.5, 0.6, 'LEFT')], allowed=('gut',))
    wall(sh, U, Z, 35.87, TOS(35.87)+0.30, +1); wall(sh, U, Z, 19.97, TOS(19.97)+0.30, -1)
    ue = U(36.5)
    sh.dimv(Z(0), Z(BASE_TOP), ue, 0.7, 'S-MM1', loc=(ue + 1.0, Z(BASE_TOP) + 0.45)); sh.dimv(Z(0), Z(col_top(35.77)), ue, 1.3, 'S-MM1'); sh.dimv(Z(0), Z(TOS(35.87)), ue, 1.9, 'S-MM1'); sh.dimv(Z(0), Z(TOS(35.87)+0.30), ue, 2.5, 'S-MM1')
    sh.label('levels mm: plate / column top / TOS / wall', ue+2.9, Z(0.3), 0.16, 'S-TEXT-DIM', rot=90, cands=[(0, 0, 'LEFT'), (0.3, 0, 'LEFT')], leader=False)
    uw = U(19.97) - 0.5
    sh.dimv(Z(0), Z(TOS(19.97)), uw, -0.7, 'S-MM1'); sh.dimv(Z(0), Z(col_top(20.07)), uw, -1.3, 'S-MM1')
    sh.label('TOS south edge / column top row B', uw-1.7, Z(0.3), 0.16, 'S-TEXT-DIM', rot=90, cands=[(0, 0, 'LEFT')], leader=False)
    sh.dimh(U(19.97), U(20.07), Z(0), -1.55, loc=(U(19.4), Z(-1.5))); sh.dimh(U(20.07), U(29.27), Z(0), -1.55); sh.dimh(U(29.27), U(35.77), Z(0), -1.55); sh.dimh(U(35.77), U(35.87), Z(0), -1.55, loc=(U(36.5), Z(-1.5)))
    sh.dimh(U(19.97), U(35.87), Z(0), -2.0)
def secB(sh, x0, y0):
    U = lambda x: x0 + (x - 67.89); Z = lambda z: y0 + z; o = 'secB'
    sh.text(x0, y0+5.0, 'SECTION B-B  primary row F (y 29.27), looking north', TH_TITLE, 'S-TEXT-NOTE', allowed=(o,), owner=o)
    cols = [(k, COLS[k]['cx']) for k in ('K8','K9','K10','K11','K12','K13','K14')]
    slab(sh, U, Z, 67.89, 95.69, [(x, k) for k, x in cols])
    for k, x in cols: column(sh, U, Z, x, COLS[k]['cy'], 'C' + k[1:])
    for p in PRIMARIES:
        if 29.2 < p['y'] < 29.4:
            zt = prim_top(p['y']); sh.rect(U(p['x0']), Z(zt-0.30), U(p['x1']), Z(zt), 'S-PRIM', owner=p['mark'], lineweight=35)
            sh.line(U(p['x0']), Z(zt-0.0107), U(p['x1']), Z(zt-0.0107), 'S-PRIM', owner=p['mark']); sh.line(U(p['x0']), Z(zt-0.30+0.0107), U(p['x1']), Z(zt-0.30+0.0107), 'S-PRIM', owner=p['mark'])
            sh.label(p['mark'] + ' IPE 300', U(0.5*(p['x0']+p['x1'])), Z(zt), TH_DIM, 'S-TEXT-MEMBER', cands=[(0, 0.1, 'CENTER'), (0, 0.5, 'CENTER'), (0.8, 0.1, 'CENTER')], allowed=(p['mark'],), leader=False)
    zr = TOS(29.3)
    for r in RAFTERS:
        sh.rect(U(r['x']-0.06), Z(zr-0.24), U(r['x']+0.06), Z(zr), 'S-RAFT', owner=r['mark'], linetype='DASHED')
        sh.label(r['mark'], U(r['x']), Z(zr-0.24), 0.16, 'S-TEXT-MEMBER', cands=[(0, -0.35, 'CENTER'), (0.2, -0.35, 'LEFT'), (0, -0.7, 'CENTER')], allowed=(r['mark'],), leader=False)
    for x0_, x1_ in ((67.89, 77.89), (81.79, 95.69)):
        sh.line(U(x0_), Z(zr+PURL_H), U(x1_), Z(zr+PURL_H), 'S-DETAIL', owner='panel', lineweight=35); sh.line(U(x0_), Z(zr+PURL_H+PANEL_T), U(x1_), Z(zr+PURL_H+PANEL_T), 'S-DETAIL', owner='panel', lineweight=35)
    zt = prim_top(29.27)
    for x in (77.89, 81.79): sh.rect(U(x-0.05), Z(zt), U(x+0.05), Z(zr+PURL_H+PANEL_T+0.15), 'S-DETAIL', owner='upst')
    sh.line(U(77.84), Z(zr+PURL_H+PANEL_T+0.15), U(81.84), Z(zr+PURL_H+PANEL_T+0.15), 'S-DETAIL', owner='upst', lineweight=35)
    sh.label('STAIR WELL beyond (open to the north face): 150 upstand on P8 / R5 / R6 (D6), cricket north of P8', U(79.84), Z(zr+0.4), TH_DIM, 'S-TEXT-DIM', cands=[(0, 0.15, 'CENTER'), (0, 0.5, 'CENTER'), (0, 0.85, 'CENTER')], allowed=('upst',), leader=False)
    wall(sh, U, Z, 67.89, zr+0.30, -1); wall(sh, U, Z, 95.69, zr+0.30, +1)
    xs = [x for _, x in cols]
    sh.dimh(U(67.89), U(xs[0]), Z(0), -1.55, loc=(U(67.2), Z(-1.5)))
    for a, b in zip(xs[:-1], xs[1:]): sh.dimh(U(a), U(b), Z(0), -1.55)
    sh.dimh(U(xs[-1]), U(95.69), Z(0), -1.55, loc=(U(96.4), Z(-1.5))); sh.dimh(U(67.89), U(95.69), Z(0), -2.0)
    uw = U(67.89) - 0.5
    sh.dimv(Z(0), Z(col_top(29.27)), uw, -0.7, 'S-MM1'); sh.dimv(Z(0), Z(zr), uw, -1.3, 'S-MM1'); sh.dimv(Z(0), Z(zr+PURL_H+PANEL_T), uw, -1.9, 'S-MM1')
    sh.label('column top / TOS / panel top, row F', uw-2.3, Z(0.3), 0.16, 'S-TEXT-DIM', rot=90, cands=[(0, 0, 'LEFT')], leader=False)
def secC(sh, x0, y0):
    U = lambda y: x0 + (y - 15.57); Z = lambda z: y0 + z; o = 'secC'
    sh.text(x0, y0+5.6, 'SECTION C-C  braced line 5 (x 77.78), looking west', TH_TITLE, 'S-TEXT-NOTE', allowed=(o,), owner=o)
    cols = [('K27', 15.87), ('K20', 21.76), ('K16', 24.46), ('K10', 29.27), ('K7', 35.17)]
    slab(sh, U, Z, 15.57, 35.37, [(y, k) for k, y in cols])
    for k, y in cols: column(sh, U, Z, y, y, 'C' + k[1:])
    for y, mk in ((15.92, 'P19'), (21.76, 'P13'), (24.46, 'P12'), (29.27, 'P7/P8'), (35.22, 'P2')):
        h = 0.33 if mk == 'P13' else 0.30
        iprof(sh, U(y), Z(prim_top(y)-h), h, 0.16 if mk == 'P13' else 0.15, 0.0075, 0.011, 'S-PRIM', mk)
        sh.label(mk + (' IPE 330' if mk == 'P13' else ''), U(y), Z(prim_top(y)), TH_DIM, 'S-TEXT-MEMBER', cands=[(0.15, 0.12, 'LEFT'), (-0.15, 0.12, 'RIGHT'), (0.15, 0.5, 'LEFT'), (-0.15, 0.5, 'RIGHT')], allowed=(mk,), leader=False)
    iprof(sh, U(24.09), Z(TOS(24.09)-0.24), 0.24, 0.12, 0.0062, 0.0098, 'S-RAFT', 'T2')
    sh.label('T2 IPE 240', U(24.09), Z(TOS(24.09)), TH_DIM, 'S-TEXT-MEMBER', cands=[(-0.15, 0.12, 'RIGHT'), (-0.15, 0.5, 'RIGHT'), (0.3, 0.6, 'LEFT')], allowed=('T2',), leader=False)
    rafter_pieces(sh, U, Z, [15.57, 15.92, 21.76, 24.46, 29.27, 35.22, 35.37], [15.92, 21.76, 24.46, 29.27, 35.22], 'R5')
    purlins_panel(sh, U, Z, 15.57, 35.37)
    for (ya, yb) in ((20.17, 24.16), (29.37, 35.37)):
        sh.line(U(ya), Z(TOS(ya)+PURL_H+PANEL_T+0.15), U(yb), Z(TOS(yb)+PURL_H+PANEL_T+0.15), 'S-DETAIL', owner='upst', lineweight=35)
        for y in (ya, yb): sh.rect(U(y-0.05), Z(TOS(y)+PURL_H), U(y+0.05), Z(TOS(y)+PURL_H+PANEL_T+0.15), 'S-DETAIL', owner='upst')
        sh.label('well upstand along R5 (D6)', U(0.5*(ya+yb)), Z(TOS(ya)+0.45), TH_DIM, 'S-TEXT-DIM', cands=[(0, 0.15, 'CENTER'), (0, 0.5, 'CENTER')], allowed=('upst',), leader=False)
    ya, yb = 15.87, 21.76; z1 = 0.15; z2 = min(cap_top(ya), cap_top(yb)) + 0.17
    sh.line(U(ya), Z(z1), U(yb), Z(z2), 'S-BRACE', owner='B7', lineweight=50); sh.line(U(ya), Z(z2), U(yb), Z(z1), 'S-BRACE', owner='B7', lineweight=50)
    sh.label('B7 2 L70x7 X (D4)', U(0.5*(ya+yb)), Z(0.5*(z1+z2)), TH_DIM, 'S-TEXT-MEMBER', cands=[(0, 0.45, 'CENTER'), (0, -0.7, 'CENTER'), (0, 0.9, 'CENTER')], allowed=('B7',), leader=False)
    sh.rect(U(20.25-0.07), Z(BASE_TOP), U(20.25+0.07), Z(TOS(19.97)-0.30), 'S-COL', owner='WP1', linetype='DASHED')
    sh.label('WP1 beyond (x 77.61), D10', U(20.25), Z(0.6), 0.16, 'S-TEXT-DIM', rot=90, cands=[(0.12, 0, 'LEFT'), (-0.12, 0, 'RIGHT')], allowed=('WP1',), leader=False)
    sh.rect(U(35.32), Z(TOS(35.37)+0.02), U(35.47), Z(TOS(35.37)+0.12), 'S-DRAIN', owner='gut', lineweight=35)
    sh.label('G-W gutter (D7), stop end at x 77.89', U(35.45), Z(TOS(35.37)-0.1), TH_DIM, 'S-TEXT-DIM', cands=[(0.15, -0.35, 'LEFT'), (0.15, 0.4, 'LEFT'), (0.5, -0.7, 'LEFT')], allowed=('gut',))
    wall(sh, U, Z, 35.37, TOS(35.37)+0.30, +1)
    ys = [y for _, y in cols]
    sh.dimh(U(15.57), U(ys[0]), Z(0), -1.55, loc=(U(14.9), Z(-1.5)))
    for a, b in zip(ys[:-1], ys[1:]): sh.dimh(U(a), U(b), Z(0), -1.55)
    sh.dimh(U(ys[-1]), U(35.37), Z(0), -1.55, loc=(U(36.0), Z(-1.5))); sh.dimh(U(15.57), U(35.37), Z(0), -2.0)
    uw = U(15.57) - 0.5; sh.dimv(Z(0), Z(TOS(15.57)), uw, -0.7, 'S-MM1'); sh.dimv(Z(0), Z(col_top(15.87)), uw, -1.3, 'S-MM1')
    sh.label('TOS south / column top C27', uw-1.7, Z(0.3), 0.16, 'S-TEXT-DIM', rot=90, cands=[(0, 0, 'LEFT')], leader=False)
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S03', 'TYPICAL SECTIONS A-A, B-B, C-C', 'Sections 1:1 in model space (m); levels in mm; print 1:100 on A1')
    secA(sh, 12.0, 23.0); secB(sh, 4.0, 14.5); secC(sh, 8.0, 5.2)
    sh.note_block(0.5, 29.4, 'SECTION NOTES', ['A-A: north on the right; rafter R8 9.20 m span; C1 and C12 in section; gutter G-E at the north eave. Clear height 3.03 m under the cap-plate nuts at C1/C2, 3.07 m under the eave primary P4.',
        'B-B: east on the right; rafters R1-R11 beyond shown dashed; stair well beyond open to the north face. C-C: north on the right; R5 ends at y 35.37 (west north edge); bay B7 C27-C20; WP1 beyond.'], 0.16, 11.0)
    sh.legend_block([('S-PRIM','box','Primaries IPE 300 (P13 IPE 330)'), ('S-RAFT','line','Rafters IPE 240, T2'), ('S-COL','box','Columns HEA 140'), ('S-PURL','box','Purlins Z200 + panel 50'), ('S-BRACE','x','Bracing B7')], 32.0, 3.4, 9.6)
    return sh
