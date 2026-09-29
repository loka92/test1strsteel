"""S01 roof framing plan at true coordinates (frame x 60-102, y 8-38)."""
from common import *
from geom import *
from plan import Plan, inside
OX, OY = 60.0, 8.0
LEGEND = [('S-PRIM','line','Primaries IPE 300 (P13 IPE 330)'), ('S-RAFT','line','Rafters, T2, ST1/ST2 IPE 240'),
          ('S-COL','box','Columns HEA 140 (C) on K1-K27'), ('S-PURL','line','Purlins Z200 @ 1.5 m, eave rails'),
          ('S-BRACE','dash','Roof rods M24, 13 panels'), ('S-BRACE','x','Wall X bays 2 L70x7'),
          ('S-OPEN','hatch','Openings, not roofed'), ('S-EXIST','line','Existing slab / columns'),
          ]
def dbubble(sh, tag, sheet, ax, ay, cands=None, r=0.42):
    """Detail bubble near (ax, ay) at the first free spot with a leader."""
    cands = cands or [(1.2, 1.2), (-1.2, 1.2), (1.2, -1.2), (-1.2, -1.2), (2.0, 0.4), (-2.0, 0.4), (0.4, 2.0), (0.4, -2.0), (2.6, 1.6), (-2.6, 1.6), (2.6, -1.6), (-2.6, -1.6), (3.2, 0), (-3.2, 0), (0, 3.0), (0, -3.0)]
    cands = list(cands) + [(rr*math.cos(a), rr*math.sin(a)) for rr in (3.6, 4.0, 4.4, 4.9, 5.3, 5.8, 6.3, 6.9, 7.5, 8.2, 9.0, 9.8, 10.5, 11.5, 12.5) for a in [k*math.pi/16 for k in range(32)]] + [(rr*math.cos(a), rr*math.sin(a)) for rr in (3.8, 4.6, 5.5, 6.5, 7.6, 9.0, 10.5) for a in [k*math.pi/12 for k in range(24)]]
    dbg = tag in DEBUG_LABELS; why = {}
    for dx, dy in cands:
        cx, cy = ax + dx, ay + dy; box = (sh.ox + cx - r, sh.oy + cy - r, sh.ox + cx + r, sh.oy + cy + r)
        if not (0.5 < cx - r and cx + r < SHEET_W - 0.5 and STRIP + 0.3 < cy - r and cy + r < SHEET_H - 0.4): why['oob'] = why.get('oob', 0) + 1; continue
        hh = sh.reg.hits(box, (), 0.05)
        if hh:
            if dbg: why[str(hh[0])] = why.get(str(hh[0]), 0) + 1
            continue
        seg = (sh.ox + ax, sh.oy + ay, sh.ox + cx, sh.oy + cy)
        if any(seg_box(seg, bx) for cl in sh.reg._cells((min(seg[0],seg[2]), min(seg[1],seg[3]), max(seg[0],seg[2]), max(seg[1],seg[3]))) for bx, o in sh.reg.tboxes.get(cl, [])): why['leader'] = why.get('leader', 0) + 1; continue
        o = sh.bubble(cx, cy, tag, sheet, r)
        d = math.hypot(dx, dy); ex, ey = cx - dx/d*r, cy - dy/d*r
        l = sh.line(ax, ay, ex, ey, 'S-LEADER', owner=o); return o
    if dbg: print('  DBG bubble', tag, why)
    sh.unplaced = getattr(sh, 'unplaced', 0) + 1; sh.unplaced_list = getattr(sh, 'unplaced_list', []) + ['bubble ' + tag]; return sh.bubble(ax + cands[-1][0], ay + cands[-1][1], tag, sheet, r)
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S01', 'ROOF FRAMING PLAN', 'Scale 1:1 in model space (m); print 1:200 on A1')
    pl = Plan(sh, OX, OY, 0, 0, 1.0, None)
    pl.existing(); pl.openings(); pl.purlins(); pl.members(); pl.columns(); pl.bracing(); pl.gutters()
    # grids: lines through the plan, bubbles top (x) and left (y)
    for g, x in XGRID:
        sh.line(x-OX, (19.3 if x > 77.85 else 13.9)-OY, x-OX, 36.75-OY, 'S-GRID', owner='grid'); sh.bubble(x-OX, 37.25-OY, g, r=0.45)
    for g, y in YGRID:
        bx = 65.4 if g != 'H' else 64.3; xe = 78.6 if g == 'A' else 96.4
        sh.line(bx+0.45-OX, y-OY, xe-OX, y-OY, 'S-GRID', owner='grid'); sh.bubble(bx-OX, y-OY, g, r=0.45)
    # dimension strings in tidy rows outside the plan
    xs = [x for _, x in XGRID]
    for a, b in zip(xs[:-1], xs[1:]): sh.dimh(a-OX, b-OX, 35.87-OY, 0.48)
    sh.dimh(67.89-OX, 77.89-OX, 15.57-OY, -0.55); sh.dimh(77.89-OX, 95.69-OX, 19.97-OY, -0.55)
    sh.dimh(67.89-OX, 95.69-OX, 15.57-OY, -1.65, loc=(74.5-OX, 14.05-OY))
    ys = [y for _, y in YGRID]
    for a, b in zip(ys[:-1], ys[1:]):
        if b - a > 0.8: sh.dimv(a-OY, b-OY, 67.89-OX, -0.75)
    sh.dimv(15.57-OY, 35.87-OY, 67.89-OX, -1.45, loc=(66.35-OX, 24.0-OY)); sh.dimv(19.97-OY, 35.87-OY, 95.69-OX, 0.55, loc=(96.4-OX, 27.0-OY))
    sh.dimv(35.37-OY, 35.87-OY, 81.79-OX, 0.0, 'S-M', loc=(82.9-OX, 36.1-OY)) if False else None
    # enlarged plan references
    for (R, tag) in (((89.4, 28.9, 95.9, 36.0), 'EP-A'), ((77.3, 23.8, 82.4, 29.8), 'EP-B'), ((77.2, 19.5, 82.5, 21.6), 'EP-C'), ((77.2, 34.7, 82.5, 36.2), 'EP-D')):
        sh.rect(R[0]-OX, R[1]-OY, R[2]-OX, R[3]-OY, 'S-TITLE', owner=tag, linetype='DASHDOT')
    # static blocks first (legend, levels table, notes, north arrow, scale bar), then the marks avoid them
    sh.legend_block(LEGEND, 18.3, 6.45, 9.2)
    sh.north_arrow(40.6, 27.7, 1.2); sh.scale_bar(36.9, 26.3, 0.9, 5)
    rows = [['%.2f' % y, '%.3f' % TOS(y), '%.3f' % prim_top(y), '%.3f' % col_top(y), '%.3f' % L_col(y)] for y in sorted({c['cy'] for c in COLS.values()}, reverse=True)]
    sh.table(36.7, 19.6, [('row y', 1.0), ('TOS', 0.95), ('prim top', 1.0), ('col top', 1.0), ('L col', 0.95)], rows, 0.36, TH_DIM, title='LEVELS (m)')
    sh.note_block(28.0, 10.6, 'NOTES', ['General notes, load basis, materials and erection: S00. Sections per legend; every member mark on S06.', 'Clear height 3.03 m under the cap-plate nuts at C1/C2, 3.07 m under the eave primary. Primary top TOS + 0.03, column top TOS - 0.29.',
        'Enlarged partial plans EP-A (east bay, NE corner), EP-B (jog panel), EP-C (notch corner), EP-D (north jog) on S01a. Fin plates FP1 2 M20 / FP2 2x2 M20 (S01a, D1).',
        'Stair well open to the north face: wall header, no roof, no eave beam. Rafters R1-R5 cantilever 0.10 past P1 / P2 to y 35.37.'], TH_DIM, 7.6)
    # section marks and detail bubbles
    for (x, tag, ybub) in ((87.19, 'A', 10.85), (77.78, 'C', 5.4)):
        sh.line(x-OX, (15.57 if tag == 'C' else 19.97)-1.7-OY, x-OX, 36.6-OY, 'S-TITLE', owner='sec' + tag, lineweight=50)
        sh.pline([(x-0.4-OX, 36.6-OY), (x-OX, 37.0-OY), (x+0.4-OX, 36.6-OY)], 'S-TITLE', owner='sec' + tag) if False else None
        sh.bubble(x-1.1-OX, ybub, tag, 'S03', 0.45); sh.line(x-OX, ybub, x-0.65-OX, ybub, 'S-TITLE', owner='sec' + tag)
    sh.line(66.0-OX, 29.3-OY, 96.6-OX, 29.3-OY, 'S-TITLE', owner='secB', lineweight=50)
    sh.bubble(97.5-OX, 30.2-OY, 'B', 'S03', 0.45); sh.line(96.6-OX, 29.3-OY, 97.5-OX, 29.75-OY, 'S-TITLE', owner='secB')
    # marks
    pl.mark_members(); pl.mark_bracing()
    for dp, x in DOWNPIPES: sh.label(dp, x-OX, north_edge(x)+0.13-OY, TH_DIM, 'S-TEXT-DIM', cands=[(0.12, 0.13, 'LEFT'), (-0.12, 0.13, 'RIGHT'), (0.12, 0.45, 'LEFT')], allowed=(dp,), leader=False)
    for g in GUTTERS: sh.label(g['id'], g['x0']+0.05-OX, g['y']+0.13-OY, TH_DIM, 'S-TEXT-DIM', cands=[(0.15, 0.13, 'LEFT'), (0.15, 0.45, 'LEFT'), (1.0, 0.13, 'LEFT')], allowed=(g['id'],), leader=False)
    sh.label('HEADER', 79.84-OX, 35.37-OY, TH_DIM, 'S-TEXT-DIM', cands=[(0, -0.35, 'CENTER'), (0, 0.15, 'CENTER'), (0, -0.7, 'CENTER')], allowed=('header',), leader=False)
    sh.label('RETURN', 81.79-OX, 35.62-OY, TH_DIM, 'S-TEXT-DIM', cands=[(0.15, 0, 'LEFT'), (-0.15, 0, 'RIGHT'), (0.15, -0.4, 'LEFT')], allowed=('return',), leader=False)
    sh.label('CRICKET', 79.84-OX, 27.37-OY, TH_DIM, 'S-TEXT-DIM', cands=[(0, -0.35, 'CENTER'), (0.3, -0.35, 'LEFT'), (0, -0.7, 'CENTER')], allowed=('cricket',), leader=False)
    sh.label('FALL 6 %', 85.8-OX, 25.6-OY, TH_DIM, 'S-TEXT-DIM', cands=[(0, 0, 'CENTER'), (0, 0.5, 'CENTER'), (0, -0.5, 'CENTER'), (-1.5, 0, 'CENTER'), (1.5, 0, 'CENTER')], leader=False)
    sh.pline([(85.8-OX, 26.2-OY), (85.8-OX, 27.4-OY)], 'S-TEXT-DIM', owner='fall'); sh.pline([(85.55-OX, 26.95-OY), (85.8-OX, 27.4-OY), (86.05-OX, 26.95-OY)], 'S-TEXT-DIM', owner='fall')
    for (x, y, d) in ((84.50, 29.27, 'D1'), (87.19, 29.27, 'D2'), (81.85, 29.27, 'D3'), (95.55, 26.9, 'D4'), (72.09, 26.37, 'D5'), (79.8, 24.09, 'D6'), (90.5, 35.87, 'D7'), (86.0, 32.57, 'D8'), (95.55, 22.3, 'D9'), (WP1[0], WP1[1], 'D10'), (67.99, 26.9, 'D11')):
        sh.late.append(lambda x=x, y=y, d=d: dbubble(sh, d, 'S04', x-OX, y-OY))
    sh.late.append(lambda: dbubble(sh, 'E', 'S05', 72.09-OX, 29.27-OY)); sh.late.append(lambda: dbubble(sh, 'E', 'S05', 67.99-OX, 21.76-OY))
    return sh
