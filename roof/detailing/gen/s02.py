"""S02 column schedule and wall elevations."""
from common import *
from geom import *
OX, OY = 110.0, 8.0
def elev(sh, face, x0, y0, flip, title):
    a, b = face['a'], face['b']; horiz = face['normal'][0] == 'y'
    U = lambda u: x0 + ((b - u) if flip else (u - a))
    Z = lambda z: y0 + z
    posts = face['posts']
    def uv(p):
        x, y = POSTXY[p]; return (x if horiz else y), (y if horiz else x)
    sh.text(x0, y0 + 5.35, title, TH)
    # slab and existing columns below
    sh.line(U(a), Z(0), U(b), Z(0), 'S-EXIST', lineweight=35); sh.line(U(a), Z(-0.25), U(b), Z(-0.25), 'S-EXIST')
    for p in posts:
        if p in ('WP1', 'RET'): continue
        u, v = uv(p); w = COLS[p]['bx'] if horiz else COLS[p]['by']
        sh.rect(U(u-w/2), Z(-1.0), U(u+w/2), Z(-0.25), 'S-EXIST'); sh.hatch([(U(u-w/2),Z(-1.0)),(U(u+w/2),Z(-1.0)),(U(u+w/2),Z(-0.25)),(U(u-w/2),Z(-0.25))], 'S-EXIST', 'ANSI31', 0.08)
    # wall panel outline and roof line
    if horiz:
        yface = face['c']; zt = TOS(yface) + 0.30
        sh.pline([(U(a), Z(0)), (U(a), Z(zt)), (U(b), Z(zt)), (U(b), Z(0))], 'S-DETAIL')
    else:
        za, zb = TOS(a) + 0.30, TOS(b) + 0.30
        sh.pline([(U(a), Z(0)), (U(a), Z(za)), (U(b), Z(zb)), (U(b), Z(0))], 'S-DETAIL')
        r = RAFTERS[0] if face['id'] == 'W' else RAFTERS[-1]
        for dz in (0.0, -0.27): sh.line(U(a), Z(TOS(a)+dz), U(b), Z(TOS(b)+dz), 'S-RAFT', lineweight=35)
        sh.text(U(0.5*(a+b)), Z(TOS(0.5*(a+b))+0.12), 'EDGE RAFTER %s IPE 270, 6 %% fall north' % r['mark'], TH_SMALL, align='CENTER')
    # columns
    for p in posts:
        u, v = uv(p)
        if p == 'WP1':
            zt = TOS(19.97) - 0.30; sh.rect(U(u-0.08), Z(0.04), U(u+0.08), Z(zt), 'S-COL', lineweight=35)
            sh.text(U(u), Z(-0.45), 'WP1', TH_SMALL, 'S-COL', 'CENTER'); continue
        if p == 'RET':
            zt = TOS(35.37) + 0.30; sh.rect(U(u-0.03), Z(0.05), U(u+0.03), Z(zt), 'S-DETAIL', lineweight=35)
            sh.text(U(u), Z(-0.45), 'RETURN', 0.13, 'S-TEXT', 'CENTER'); sh.text(U(u)+0.15, Z(1.6), '0.5 m wall return post, brackets from C3', 0.13, rot=90); continue
        cy = COLS[p]['cy']; zt = cap_top(cy); n = int(p[1:]); bt = base_top(p)
        sh.rect(U(u-0.08), Z(bt), U(u+0.08), Z(zt-0.02), 'S-COL', lineweight=35)
        sh.rect(U(u-0.2), Z(GROUT), U(u+0.2), Z(bt), 'S-COL'); sh.rect(U(u-0.14), Z(zt-0.02), U(u+0.14), Z(zt), 'S-COL')
        sh.text(U(u), Z(-0.45), 'C%d' % n, TH_SMALL, 'S-COL', 'CENTER'); sh.text(U(u), Z(-0.68), '(K%d)' % n, 0.14, 'S-COL', 'CENTER')
    # eave beams (N/S faces) as level rectangles on their rows
    if horiz:
        for p in PRIMARIES:
            if p['kind'] == 'trim': continue
            if abs(p['y'] - face['c']) < 0.75 and p['x0'] >= a - 0.2 and p['x1'] <= b + 0.2:
                zt = prim_top(p['y']); sh.rect(U(p['x0']), Z(zt-0.33), U(p['x1']), Z(zt), 'S-PRIM', lineweight=35)
                sh.text(U(0.5*(p['x0']+p['x1'])), Z(zt+0.08), '%s IPE 330' % p['mark'], TH_SMALL, align='CENTER')
    if face['id'] == 'N1':
        u1, u2 = uv('K7')[0], uv('RET')[0]; zh = TOS(35.37) + 0.05
        sh.rect(U(u1), Z(zh-0.2), U(u2), Z(zh), 'S-PURL', lineweight=35); sh.text(U(0.5*(u1+u2)), Z(zh+0.08), 'WALL HEADER 2 x C200x60x2.5 (no roof)', 0.12, 'S-PURL', 'CENTER')
    # girts between consecutive posts
    for p, q in zip(posts[:-1], posts[1:]):
        u1, u2 = uv(p)[0], uv(q)[0]; s = girt_spacing(p, q)
        zmax = (prim_top(face['c']) - 0.33 if horiz else TOS(min(u1,u2)) - 0.27) - 0.15
        z = 0.5; k = 0
        while z < zmax:
            sh.line(U(u1), Z(z), U(u2), Z(z), 'S-PURL'); z += s; k += 1
        sh.text(U(0.5*(u1+u2)), Z(0.22), 'girts Z200x2.0 @ %.1f m%s' % (s, ' sleeved' if s < 1.5 else ''), 0.14, 'S-PURL', 'CENTER')
    # wall bracing
    for bid, d, (p, q) in BAYS:
        if p in posts and q in posts and abs(posts.index(p) - posts.index(q)) == 1:
            u1, u2 = uv(p)[0], uv(q)[0]; z1 = 0.15; z2 = min(cap_top(COLS[p]['cy']), cap_top(COLS[q]['cy'])) + 0.17
            sh.line(U(u1), Z(z1), U(u2), Z(z2), 'S-BRACE', lineweight=50); sh.line(U(u1), Z(z2), U(u2), Z(z1), 'S-BRACE', lineweight=50)
            sh.text(U(0.5*(u1+u2)), Z(0.5*(z1+z2)+0.35), bid + ' 2 x L70x7 (X, tension only)', TH_SMALL, 'S-BRACE', 'CENTER')
    # dimensions: bays and clear height
    us = [uv(p)[0] for p in posts]
    for u1, u2 in zip(us[:-1], us[1:]): sh.dimh(U(u1), U(u2), Z(0), -0.95 if not flip else -0.95)
    sh.dimh(U(a), U(b), Z(0), -1.35)
    ue = U(b) + (0.3 if not flip else 0.3)
    zc = cap_top(face['c'] if horiz else b) if horiz else cap_top(b)
    sh.dimv(Z(0), Z(zc), ue, 0.9); sh.text(ue+1.25, Z(zc/2), 'cap top', 0.14, rot=90, align='CENTER')
    if horiz: sh.dimv(Z(0), Z(TOS(face['c'])+0.30), ue, 1.6)
    else: sh.dimv(Z(0), Z(TOS(b)+0.30), ue, 1.6)
    sh.text(ue+1.95, Z(1.5), 'wall panel top', 0.14, rot=90, align='CENTER')
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S02', 'COLUMN SCHEDULE AND WALL ELEVATIONS', 'Elevations 1:1 in model space (m); print 1:200 on A1')
    cols = [('Mark',1.0),('Conc.',0.9),('Section',1.4),('x (m)',1.1),('y (m)',1.1),('Base',0.9),('L col (m)',1.4),('Col top (m)',1.5),('Base pl. top',1.5),('Conc. col. orient.',2.3),('HEA web',1.4),('Braced bays',1.7),('Face',1.2)]
    rows = []
    for k, c in COLS.items():
        n = int(k[1:]); ew = c['bx'] > c['by']; bt = base_type(k)
        faces = [f['id'] for f in FACES if k in f['posts']]
        rows.append(['C%d' % n, k, 'HEA 160', '%.2f' % c['cx'], '%.2f' % c['cy'], bt, '%.3f' % L_col(c['cy'], bt == 'B2'), '%.3f' % col_top(c['cy']), '+%.3f' % base_top(k),
                     'E-W (400 x 200)' if ew else 'N-S (200 x 400)', 'N-S' if ew else 'E-W', ','.join(BAY_OF.get(k, [])) or '-', ','.join(faces) or 'int'])
    rows.append(['WP1', '-', 'HEA 160', '77.61', '20.25', 'post', '4.24', 'slotted', '+0.040', 'notch edge beam (core)', 'N-S', '-', 'S2,EN'])
    sh.table(0.5, 29.3, cols, rows, 0.4, 0.13, title='COLUMN SCHEDULE - all columns HEA 160 S275; bases B1 / B2 / P per Rev 4b (S05); column top = cap-plate underside = TOS(y) - 0.30; L = TOS - 0.35 (B1: 25 grout + 25 plate) / TOS - 0.355 (B2: 30 plate); cap plate 200x280x20 (D2)')
    elev(sh, FACES[5], 19.0, 23.3, True, FACES[5]['title'] + ' - viewed from outside, north on the left')
    elev(sh, FACES[4], 19.0, 16.4, False, FACES[4]['title'] + ' - viewed from outside, north on the right')
    elev(sh, FACES[1], 17.5, 10.0, True, 'NORTH ELEVATION N2 - EAST BLOCK (y 35.87, gutter G-E), from outside')
    elev(sh, FACES[0], 1.5, 10.0, True, 'NORTH ELEVATION N1 - WEST BLOCK (y 35.37, gutter G-W), from outside')
    elev(sh, FACES[2], 1.5, 3.6, False, FACES[2]['title'])
    elev(sh, FACES[3], 13.0, 3.6, False, FACES[3]['title'])
    elev(sh, FACES[6], 33.5, 3.6, False, FACES[6]['title'])
    sh.note_block(0.5, 17.0, 'ELEVATION NOTES', ['Wall: BoardX panels on Z200x2.0 girts (D9), girts span column to column; rows per bay as noted, sleeved where marked.',
        'Bracing bays B1-B10 must stay door-free (client). B7/B8 on line 5 (x 77.78) are shown on S03 section C-C. North face jogs at x 81.79: N1 at y 35.37 (west), N2 at y 35.87 (east), 0.5 m return on brackets from C3.',
        'Stair well open to the north face: wall header 2 x C200x60x2.5 over x 77.89-81.79 carries the wall, girts and gutter stop ends; no roof, no eave beam. Wall sill / base rail at the slab edge: D11.',
        'Interior columns C9-C13, C16, C17 not in an elevation: see schedule and S03.', 'Girt bottom row 0.50 m above slab; top row 150 mm below the eave beam. Clear height 3.02 m under the cap-plate nuts at C1/C2, 3.06 m under the eave primary.',
        'COLUMN LENGTHS ARE NOMINAL (TOS - 0.35 B1 / - 0.355 B2). Cut columns to the surveyed plate-top level from the slab-top survey (S00); grout bed 25 +/- 5 mm.'], 0.13, 0.22)
    return sh
