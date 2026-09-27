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
        if p == 'WP1': continue
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
            zt = TOS(19.97) - 0.30; sh.rect(U(u-0.08), Z(BASE_TOP), U(u+0.08), Z(zt), 'S-COL', lineweight=35)
            sh.text(U(u), Z(-0.45), 'WP1', TH_SMALL, 'S-COL', 'CENTER'); continue
        cy = COLS[p]['cy']; zt = cap_top(cy); n = int(p[1:])
        sh.rect(U(u-0.08), Z(BASE_TOP), U(u+0.08), Z(zt), 'S-COL', lineweight=35)
        sh.rect(U(u-0.2), Z(0.04), U(u+0.2), Z(BASE_TOP), 'S-COL'); sh.rect(U(u-0.14), Z(zt-0.02), U(u+0.14), Z(zt), 'S-COL')
        sh.text(U(u), Z(-0.45), 'C%d' % n, TH_SMALL, 'S-COL', 'CENTER'); sh.text(U(u), Z(-0.68), '(K%d)' % n, 0.14, 'S-COL', 'CENTER')
    # eave beams (N/S faces) as level rectangles on their rows
    if horiz:
        for p in PRIMARIES:
            if p['kind'] == 'trim': continue
            if abs(p['y'] - face['c']) < 0.75 and p['x0'] >= a - 0.2 and p['x1'] <= b + 0.2:
                zt = prim_top(p['y']); sh.rect(U(p['x0']), Z(zt-0.33), U(p['x1']), Z(zt), 'S-PRIM', lineweight=35)
                sh.text(U(0.5*(p['x0']+p['x1'])), Z(zt+0.08), '%s IPE 330' % p['mark'], TH_SMALL, align='CENTER')
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
            u1, u2 = uv(p)[0], uv(q)[0]; z1 = BASE_TOP + 0.1; z2 = min(cap_top(COLS[p]['cy']), cap_top(COLS[q]['cy'])) + 0.17
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
    cols = [('Mark',1.1),('Conc.',1.0),('Section',1.5),('x (m)',1.2),('y (m)',1.2),('L col (m)',1.4),('Cap top (m)',1.6),('Base pl. top',1.6),('Conc. col. orient.',2.4),('HEA web',1.6),('Braced bays',1.8),('Face',1.2)]
    rows = []
    for k, c in COLS.items():
        n = int(k[1:]); ew = c['bx'] > c['by']
        faces = [f['id'] for f in FACES if k in f['posts']]
        rows.append(['C%d' % n, k, 'HEA 160', '%.2f' % c['cx'], '%.2f' % c['cy'], '%.2f' % L_col(c['cy']), '%.3f' % cap_top(c['cy']), '+0.065',
                     'E-W (400 x 200)' if ew else 'N-S (200 x 400)', 'N-S' if ew else 'E-W', ','.join(BAY_OF.get(k, [])) or '-', ','.join(faces) or 'int'])
    rows.append(['WP1', '-', 'HEA 160', '77.89', '19.97', '4.21', 'slotted', '+0.055', 'notch edge beam (core)', 'N-S', '-', 'S2,EN'])
    sh.table(0.5, 29.3, cols, rows, 0.4, 0.13, title='COLUMN SCHEDULE - all columns HEA 160 S275, pinned bases B1 / B2 / P per Rev 4 (S05), cap plate 200x280x20 (D2); base plate top +0.065 above slab (40 grout + 25 plate); cap top = TOS(y) - 0.28')
    elev(sh, FACES[4], 19.0, 23.3, True, FACES[4]['title'] + ' - viewed from outside, north on the left')
    elev(sh, FACES[3], 19.0, 16.4, False, FACES[3]['title'] + ' - viewed from outside, north on the right')
    elev(sh, FACES[0], 1.5, 10.0, True, FACES[0]['title'] + ' - viewed from outside, east on the left')
    elev(sh, FACES[1], 1.5, 3.6, False, FACES[1]['title'])
    elev(sh, FACES[2], 13.0, 3.6, False, FACES[2]['title'])
    elev(sh, FACES[5], 33.5, 3.6, False, FACES[5]['title'])
    sh.note_block(0.5, 17.0, 'ELEVATION NOTES', ['Wall: BoardX panels on Z200x2.0 girts (D9), girts span column to column; rows per bay as noted, sleeved where marked.',
        'Bracing bays B1-B10 must stay door-free (client). B7/B8 on line 5 (x 77.78) are shown on S03 section C-C.',
        'Interior columns C9-C13, C16, C17 not in an elevation: see schedule and S03.', 'Girt bottom row 0.50 m above slab; top row 150 mm below the eave beam.'], 0.13, 0.22)
    return sh
