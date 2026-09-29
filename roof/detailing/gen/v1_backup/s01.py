"""S01 roof framing plan at true coordinates. Sheet frame x 60-102, y 8-38."""
from common import *
from geom import *
OX, OY = 60.0, 8.0
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S01', 'ROOF FRAMING PLAN', 'SCALE 1:1 in model space (m); print 1:200 on A1')
    L = lambda x, y: (x-OX, y-OY)
    T = lambda x, y, s, h=TH, layer='S-TEXT', align='LEFT', rot=0: sh.text(x-OX, y-OY, s, h, layer, align, rot)
    # existing slab outline + concrete columns (grey)
    sh.pline([L(67.89,15.57), L(77.89,15.57), L(77.89,19.97), L(95.69,19.97), L(95.69,35.87), L(81.79,35.87), L(81.79,35.37), L(67.89,35.37)], 'S-EXIST', True, lineweight=35)
    for k, c in COLS.items():
        x, y, bx, by = c['cx'], c['cy'], c['bx'], c['by']
        pts = [L(x-bx/2,y-by/2), L(x+bx/2,y-by/2), L(x+bx/2,y+by/2), L(x-bx/2,y+by/2)]
        sh.pline(pts, 'S-EXIST', True); sh.hatch(pts, 'S-EXIST', 'ANSI31', 0.08, 8)
    # openings
    for name, o in OPEN.items():
        pts = [L(o['x0'],o['y0']), L(o['x1'],o['y0']), L(o['x1'],o['y1']), L(o['x0'],o['y1'])]
        sh.pline(pts, 'S-OPEN', True, lineweight=35); sh.hatch(pts, 'S-OPEN', 'ANSI31', 0.3, 8, 45)
        cx, cy = 0.5*(o['x0']+o['x1']), 0.5*(o['y0']+o['y1'])
        T(cx, cy+0.4, name + ' WELL', TH, 'S-TEXT', 'CENTER'); T(cx, cy-0.1, 'NOT ROOFED', TH_SMALL, 'S-TEXT', 'CENTER')
        T(cx, cy-0.5, 'OPEN TO THE NORTH FACE (no roof, no eave beam)' if name == 'STAIR' else '150 UPSTAND + FLASHING ALL SIDES', TH_SMALL, 'S-TEXT', 'CENTER')
        if name == 'STAIR': T(cx, cy-0.85, '150 UPSTAND + FLASHING on P8 / R5 / R6', TH_SMALL, 'S-TEXT', 'CENTER')
    # grids
    for g, x in XGRID:
        sh.line(*L(x, 14.4), *L(x, 36.9), 'S-GRID'); sh.bubble(x-OX, 37.3-OY, g, r=0.42)
    for g, y in YGRID:
        sh.line(*L(65.2, y), *L(96.6, y), 'S-GRID'); sh.bubble(64.7-OX, y-OY, g, r=0.42)
    # purlins + eave rail
    for y, a, b in purlin_segments(): sh.line(*L(a, y), *L(b, y), 'S-PURL')
    sh.line(*L(67.89, 35.32), *L(77.89, 35.32), 'S-PURL', lineweight=25); sh.line(*L(81.79, 35.82), *L(95.69, 35.82), 'S-PURL', lineweight=25)
    sh.line(*L(77.89, 35.37), *L(81.79, 35.37), 'S-PURL', lineweight=50); T(79.84, 34.55, 'WALL HEADER C200x60x2.5 x2 boxed', TH_SMALL, 'S-PURL', 'CENTER'); T(79.84, 34.3, '(no roof, no eave beam) + gutter stop ends', TH_SMALL, 'S-PURL', 'CENTER')
    sh.line(*L(81.79, 35.37), *L(81.79, 35.87), 'S-DETAIL', lineweight=50); T(81.65, 35.45, '0.5 m WALL RETURN on brackets from C3', TH_SMALL, 'S-TEXT', 'RIGHT', 90)
    T(70.2, 34.0, 'Z200x2.0 PURLINS @ 1.50 m (E-W), first row <= 1.3 m from the north edges (east 35.57, west 34.07); anti-sag row at mid-span of every purlin span', TH_SMALL)
    T(84.0, 35.62, 'EAVE RAIL C200x60x2.5 (gutter bracket rail) on every rafter end, both eaves', TH_SMALL)
    # primaries, trimmers
    for p in PRIMARIES:
        lw = 50 if p['kind'] != 'trim' else 35
        sh.line(*L(p['x0'], p['y']), *L(p['x1'], p['y']), 'S-PRIM', lineweight=lw)
        sec = 'IPE 330' if p['kind'] != 'trim' else 'IPE 270'
        T(0.5*(p['x0']+p['x1']), p['y']+0.12, '%s %s' % (p['mark'], sec), TH, 'S-TEXT', 'CENTER')
    for s in POSTS:
        sh.line(*L(s['x0'], s['y']), *L(s['x1'], s['y']), 'S-RAFT', lineweight=35)
        T(0.5*(s['x0']+s['x1']), s['y']+0.12, '%s IPE 270 (roof-truss post)' % s['id'], TH_SMALL, 'S-TEXT', 'CENTER')
    # rafters
    for r in RAFTERS:
        sh.line(*L(r['x'], r['y0']), *L(r['x'], r['y1']), 'S-RAFT', lineweight=35)
        yl = r['y0'] + 1.3 if r['y0'] > 16 else 17.6
        T(r['x']+0.12, yl, '%s IPE 270' % r['mark'], TH, 'S-TEXT', 'LEFT', 90)
    # roof rod bracing
    for tid, panels in ROOF_TRUSSES:
        for (x0, x1, y0, y1) in panels:
            sh.line(*L(x0, y0), *L(x1, y1), 'S-BRACE'); sh.line(*L(x0, y1), *L(x1, y0), 'S-BRACE')
        x0, x1, y0, y1 = panels[0]
        T(x0+0.15, y0+0.35, tid + ' M24 RODS', TH_SMALL, 'S-BRACE')
    # steel columns (H symbol) + marks
    for k, c in COLS.items():
        x, y = c['cx'], c['cy']; n = int(k[1:])
        ew = c['bx'] > c['by']                      # concrete long axis E-W -> HEA web along y (across the short axis)
        b, h = 0.16, 0.152
        if ew:   # flanges parallel to x, web along y
            sh.line(*L(x-b/2, y-h/2), *L(x+b/2, y-h/2), 'S-COL', lineweight=50); sh.line(*L(x-b/2, y+h/2), *L(x+b/2, y+h/2), 'S-COL', lineweight=50)
            sh.line(*L(x, y-h/2), *L(x, y+h/2), 'S-COL', lineweight=50)
        else:
            sh.line(*L(x-h/2, y-b/2), *L(x-h/2, y+b/2), 'S-COL', lineweight=50); sh.line(*L(x+h/2, y-b/2), *L(x+h/2, y+b/2), 'S-COL', lineweight=50)
            sh.line(*L(x-h/2, y), *L(x+h/2, y), 'S-COL', lineweight=50)
        sh.rect(*L(x-0.2, y-0.15), *L(x+0.2, y+0.15), 'S-COL')   # base plate 300x400 (long side along the concrete 400 axis)
        dx, dy = (0.25, -0.55) if y < 30 else (0.25, 0.3)
        if k in ('K21','K22','K23','K25','K26','K24','K27'): dy = -0.75
        T(x+dx, y+dy, 'C%d' % n, TH, 'S-COL'); T(x+dx, y+dy-0.25, '(K%d) HEA160' % n, TH_SMALL, 'S-COL')
    sh.rect(*L(WP1[0]-0.08, WP1[1]-0.08), *L(WP1[0]+0.08, WP1[1]+0.08), 'S-COL', lineweight=50)
    T(77.0, 20.5, 'WP1 HEA160 wind post (77.61, 20.25), 280 inboard (Rev 4b)', TH_SMALL, 'S-COL')
    # wall bracing bays
    for b, d, (a, c) in BAYS:
        (x1, y1), (x2, y2) = KXY[a], KXY[c]
        sh.line(*L(x1, y1), *L(x2, y2), 'S-BRACE', lineweight=70)
        xm, ym = 0.5*(x1+x2), 0.5*(y1+y2)
        if d == 'x':
            sh.line(*L(xm-0.5, ym-0.35), *L(xm+0.5, ym+0.35), 'S-BRACE', lineweight=50); sh.line(*L(xm-0.5, ym+0.35), *L(xm+0.5, ym-0.35), 'S-BRACE', lineweight=50)
            T(xm, ym-0.75 if ym < 30 else ym+0.45, b + ' L70x7 X', TH, 'S-BRACE', 'CENTER')
        else:
            sh.line(*L(xm-0.35, ym-0.5), *L(xm+0.35, ym+0.5), 'S-BRACE', lineweight=50); sh.line(*L(xm-0.35, ym+0.5), *L(xm+0.35, ym-0.5), 'S-BRACE', lineweight=50)
            T(xm+0.45 if xm < 80 else xm-0.45, ym, b + ' L70x7 X', TH, 'S-BRACE', 'LEFT' if xm < 80 else 'RIGHT', 90)
    # drainage
    for g in GUTTERS:
        y = g['y']; sh.line(*L(g['x0'], y+0.05), *L(g['x1'], y+0.05), 'S-DRAIN'); sh.line(*L(g['x0'], y+0.20), *L(g['x1'], y+0.20), 'S-DRAIN')
        for xe in (g['x0'], g['x1']): sh.line(*L(xe, y+0.05), *L(xe, y+0.20), 'S-DRAIN', lineweight=35)
        sh.line(*L(g['hp'], y+0.03), *L(g['hp'], y+0.38), 'S-DRAIN'); T(g['hp'], y+0.55, 'HP/EJ', 0.12, 'S-DRAIN', 'CENTER')
        T(g['x0']+0.3, y+0.26, '%s BOX GUTTER 150x100 at y %.2f, x %.2f-%.2f, fall 1:350 from HP' % (g['id'], y, g['x0'], g['x1']), 0.12, 'S-DRAIN')
    for dp, x in DOWNPIPES:
        y = north_edge(x); sh.circle(x-OX, y+0.43-OY, 0.1, 'S-DRAIN'); sh.line(*L(x, y+0.20), *L(x, y+0.33), 'S-DRAIN')
        T(x+0.15, y+0.38, '%s dia100' % dp, 0.12, 'S-DRAIN', 'LEFT')
    for x in SPOUTS:
        y = north_edge(x - 0.01) if x in (77.89,) else north_edge(x); sh.pline([L(x, y+0.05), L(x, y+0.5)], 'S-DRAIN'); T(x + (0.08 if x < 80 else -0.08), y+0.52, 'spout', 0.11, 'S-DRAIN', 'LEFT' if x < 80 else 'RIGHT')
    T(67.9, 37.78, 'GUTTERS: G-W at y 35.37 (x 67.89-77.89, stop ends) and G-E at y 35.87 (x 81.79-95.69, stop ends); overflow spouts 100x30 at the stop ends x 67.89 / 77.89 / 81.79 / 95.69; DP1-DP4 dia 100 on the north facade', TH_SMALL, 'S-DRAIN')
    sh.line(*L(79.84, 29.37), *L(79.84, 27.37), 'S-DRAIN'); sh.line(*L(79.84, 27.37), *L(77.89, 29.37), 'S-DRAIN'); sh.line(*L(79.84, 27.37), *L(81.79, 29.37), 'S-DRAIN')
    T(79.84, 26.95, 'CRICKET ridge 120 mm at the upstand, 2.0 m up-slope', TH_SMALL, 'S-DRAIN', 'CENTER')
    T(79.94, 19.6, 'ELEV well: no cricket, south upstand merged with the notch verge flashing', TH_SMALL, 'S-DRAIN', 'CENTER')
    # slope arrow
    sh.pline([L(84.0, 27.5), L(84.0, 31.5)], 'S-TEXT'); sh.pline([L(83.7, 31.0), L(84.0, 31.5), L(84.3, 31.0)], 'S-TEXT')
    T(84.15, 29.0, 'FALL 6 % (3.43 deg) NORTH', TH_SMALL, 'S-TEXT', 'LEFT', 90)
    # dimensions: X bays (top), Y bays (left), overall (bottom / far left)
    xs = [x for _, x in XGRID]
    for a, b in zip(xs[:-1], xs[1:]): sh.dimh(a-OX, b-OX, 35.87-OY, 0.75)
    sh.dimh(67.89-OX, 95.69-OX, 15.57-OY, -0.9); sh.dimh(67.89-OX, 77.89-OX, 15.57-OY, -0.5); sh.dimh(77.89-OX, 95.69-OX, 19.97-OY, -0.5)
    ys = [y for _, y in YGRID]
    for a, b in zip(ys[:-1], ys[1:]): sh.dimv(a-OY, b-OY, 67.89-OX, -0.75)
    sh.dimv(15.57-OY, 35.87-OY, 67.89-OX, -1.6); sh.dimv(19.97-OY, 35.87-OY, 95.69-OX, 0.45)
    # section marks
    for (x, y0, y1, tag) in ((87.19, 14.3, 37.0, 'A'),):
        sh.line(*L(x, y0), *L(x, y1), 'S-TEXT', lineweight=50)
        for yy, dy in ((y0, -0.4), (y1, 0.4)):
            sh.pline([L(x-0.5, yy), L(x+0.5, yy)], 'S-TEXT', lineweight=50); sh.bubble(x-1.0-OX, yy+dy-OY, tag, 'S03', 0.45)
    sh.line(*L(65.6, 29.3), *L(97.0, 29.3), 'S-TEXT', lineweight=50)
    for xx in (65.6, 97.0):
        sh.pline([L(xx, 28.8), L(xx, 29.8)], 'S-TEXT', lineweight=50); sh.bubble(xx-OX, 30.4-OY, 'B', 'S03', 0.45)
    # detail bubbles
    for (x, y, d) in ((84.50, 29.27, 'D1'), (87.19, 35.77, 'D2'), (81.85, 29.27, 'D3'), (95.55, 26.9, 'D4'), (84.5, 35.67, 'D5'),
                      (79.8, 24.09, 'D6'), (90.5, 35.87, 'D7'), (86.0, 32.57, 'D8'), (95.55, 22.3, 'D9'), (77.61, 20.25, 'D10'), (72.09, 26.4, 'D11'), (67.99, 21.76, 'B1')):
        bx, by = x + 0.9, y + 0.9
        if d in ('D9', 'D4'): bx = x - 1.3
        sh.line(*L(x, y), *L(bx-0.45, by-0.3), 'S-TEXT'); sh.bubble(bx-OX, by-OY, d, 'S05' if d == 'B1' else 'S04', 0.45)
    sh.north_arrow(100.3-OX, 35.6-OY)
    # TOS table (right)
    rows = []
    for y in sorted({c['cy'] for c in COLS.values()}, reverse=True):
        ks = ','.join(k for k, c in COLS.items() if c['cy'] == y)
        rows.append(['%.2f' % y, '%.3f' % TOS(y), '%.3f' % prim_top(y), '%.3f' % col_top(y), '%.3f' % L_col(y), '%.3f' % L_col(y, True), ks if len(ks) <= 10 else ks[:8] + '..'])
    sh.table(95.95-OX, 34.4-OY, [('row y', 0.7), ('TOS', 0.7), ('prim', 0.7), ('col top', 0.75), ('L B1', 0.7), ('L B2', 0.7), ('cols', 1.25)], rows, 0.36, 0.12,
             title='LEVELS m: TOS = 3.33+0.06(35.87-y)')
    sh.note_block(95.95-OX, 28.5-OY, 'NOTES', [
        'Levels: top of steel of the sloping rafters; level', 'primaries top at TOS + 0.05; column top (cap-plate', 'underside) TOS - 0.30; column length TOS - 0.35 (B1,', '25 grout + 25 plate) / TOS - 0.355 (B2, 30 plate).',
        'Clear height 3.02 m under the cap-plate nuts at C1/C2,', '3.06 m under the eave primary and the rafter ends.',
        'North face jogs: y 35.37 west of x 81.79 (R1-R5 end', 'there, 0.10 m past P1/P2), 35.87 east; stair well open', 'to the north face: no roof, no eave beam, wall header.',
        'Marks: Cn steel column over concrete column Kn;', 'P primaries/eave beams IPE 330 (level); R rafters IPE 270',
        '(sloping, spliced at every primary, D1); T2 trimmer;', 'ST roof-truss posts; WP wind post; B wall X bays;',
        'RT roof rod panels (M24 8.8 rods, turnbuckles).', 'Steel S275 J0, bolts 8.8, hot-dip galvanised.',
        'Grids 1-11 on the rafter lines, A-H on the primary rows;', 'columns at true positions (K-coordinates).',
        'Rafters bear on fin plates each side of the primary', 'web (D1), bottom flanges flush (10 mm up), no copes.',
        'Fly braces to the bottom flange at mid-span (L <= 6.6 m)', 'and at the third points (7.5 and 9.2 m spans), D8.',
        'Existing slab and concrete columns shown grey.', 'Bases B1 (13) / B2 (13) / P (K21) per Rev 4b, S05.', 'Fin plates plain (no slots); thermal +/-20 K service', 'checked through the B2-RT-N-W-row F-RT-N-E-B1 path.'], 0.13, 0.24)
    return sh
