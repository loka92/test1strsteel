"""S02 column schedule and wall elevations (Rev 6a: HEA 140 columns, IPE 300 eave beams, IPE 240 edge rafters)."""
from common import *
from geom import *
OX, OY = 110.0, 8.0
def elev(sh, face, x0, y0, flip, title):
    a, b = face['a'], face['b']; horiz = face['normal'][0] == 'y'; fid = 'el' + face['id']
    U = lambda u: x0 + ((b - u) if flip else (u - a)); Z = lambda z: y0 + z
    posts = face['posts']
    def uv(p):
        x, y = POSTXY[p]; return (x if horiz else y), (y if horiz else x)
    ztitle = (TOS(face['c']) if horiz else max(TOS(a), TOS(b))) + 0.30 + 0.15
    sh.text(x0, y0 + ztitle, title, TH_TITLE, 'S-TEXT-NOTE', allowed=(fid,), owner=fid)
    sh.line(U(a), Z(0), U(b), Z(0), 'S-EXIST', owner=fid, lineweight=35); sh.line(U(a), Z(-0.3), U(b), Z(-0.3), 'S-EXIST', owner=fid)
    for p in posts:
        if p in ('WP1', 'RET'): continue
        u, v = uv(p); w = COLS[p]['bx'] if horiz else COLS[p]['by']
        sh.rect(U(u-w/2), Z(-1.0), U(u+w/2), Z(-0.3), 'S-EXIST', owner=fid); sh.hatch([(U(u-w/2),Z(-1.0)),(U(u+w/2),Z(-1.0)),(U(u+w/2),Z(-0.3)),(U(u-w/2),Z(-0.3))], 'S-EXIST', 'ANSI31', 0.08)
    if horiz:
        zt = TOS(face['c']) + 0.30; sh.pline([(U(a), Z(0)), (U(a), Z(zt)), (U(b), Z(zt)), (U(b), Z(0))], 'S-DETAIL', owner=fid)
    else:
        za, zb = TOS(a) + 0.30, TOS(b) + 0.30; sh.pline([(U(a), Z(0)), (U(a), Z(za)), (U(b), Z(zb)), (U(b), Z(0))], 'S-DETAIL', owner=fid)
        r = RAFTERS[0] if face['id'] == 'W' else RAFTERS[-1]
        for dz in (0.0, -0.24): sh.line(U(a), Z(TOS(a)+dz), U(b), Z(TOS(b)+dz), 'S-RAFT', owner=r['mark'], lineweight=35)
        um = 0.5*(a+b); sh.label('%s IPE 240 edge rafter' % r['mark'], U(um), Z(TOS(um)), TH_DIM, 'S-TEXT-MEMBER', cands=[(dx, 0.12 + 0.06*abs(dx)*(1 if flip else -1)*(-1), 'CENTER') for dx in (0, -2, 2, -4, 4, -6, 6)] + [(dx, 0.5, 'CENTER') for dx in (0, -3, 3)], allowed=(r['mark'],), leader=False)
    for p in posts:
        u, v = uv(p)
        if p == 'WP1':
            zt = TOS(19.97) - 0.30; sh.rect(U(u-0.07), Z(0.04), U(u+0.07), Z(zt), 'S-COL', owner='WP1', lineweight=35)
            sh.label('WP1', U(u), Z(-0.45), TH_DIM, 'S-TEXT-MEMBER', cands=[(0, 0, 'CENTER'), (0, -0.4, 'CENTER'), (0.5, 0, 'LEFT')], allowed=('WP1',), leader=False); continue
        if p == 'RET':
            zt = TOS(35.37) + 0.30; sh.rect(U(u-0.03), Z(0.05), U(u+0.03), Z(zt), 'S-DETAIL', owner='RET', lineweight=35)
            sh.label('RETURN POST', U(u), Z(-0.45), TH_DIM, 'S-TEXT-MEMBER', cands=[(0, 0, 'CENTER'), (0, -0.4, 'CENTER'), (-0.6, 0, 'RIGHT')], allowed=('RET',), leader=False); continue
        cy = COLS[p]['cy']; zt = cap_top(cy); n = int(p[1:]); o = 'C%d' % n
        sh.rect(U(u-0.07), Z(BASE_TOP), U(u+0.07), Z(zt-0.02), 'S-COL', owner=o, lineweight=35)
        sh.rect(U(u-0.2), Z(GROUT), U(u+0.2), Z(BASE_TOP), 'S-COL', owner=o); sh.rect(U(u-0.14), Z(zt-0.02), U(u+0.14), Z(zt), 'S-COL', owner=o)
        sh.label('C%d/K%d' % (n, n), U(u), Z(-0.45), TH_DIM, 'S-TEXT-MEMBER', cands=[(0, 0, 'CENTER'), (0, -0.45, 'CENTER'), (0.6, 0, 'LEFT'), (-0.6, 0, 'RIGHT')], allowed=(o,), leader=False)
    if horiz:
        for p in PRIMARIES:
            if p['kind'] == 'trim': continue
            if abs(p['y'] - face['c']) < 0.75 and p['x0'] >= a - 0.2 and p['x1'] <= b + 0.2:
                zt = prim_top(p['y']); h = 0.33 if p['mark'] == 'P13' else 0.30
                sh.rect(U(p['x0']), Z(zt-h), U(p['x1']), Z(zt), 'S-PRIM', owner=p['mark'], lineweight=35)
                sh.label('%s %s' % (p['mark'], prim_sec(p)), U(0.5*(p['x0']+p['x1'])), Z(zt), TH_DIM, 'S-TEXT-MEMBER', cands=[(0, 0.1, 'CENTER'), (0, 0.45, 'CENTER'), (-1.2, 0.1, 'CENTER'), (1.2, 0.1, 'CENTER')], allowed=(p['mark'],), leader=False)
    if face['id'] == 'N1':
        u1, u2 = uv('K7')[0], uv('RET')[0]; zh = TOS(35.37) + 0.03
        sh.rect(U(u1), Z(zh-0.2), U(u2), Z(zh), 'S-PURL', owner='header', lineweight=35)
        sh.label('WALL HEADER 2 C200x60x2.5', U(0.5*(u1+u2)), Z(zh), TH_DIM, 'S-TEXT-MEMBER', cands=[(0, 0.12, 'CENTER'), (0, 0.5, 'CENTER'), (0, -0.55, 'CENTER')], allowed=('header',), leader=False)
    for p, q in zip(posts[:-1], posts[1:]):
        u1, u2 = uv(p)[0], uv(q)[0]; s = girt_spacing(p, q); o = 'girt' + p + q
        zmax = (prim_top(face['c']) - 0.30 if horiz else TOS(min(u1, u2)) - 0.24) - 0.15
        z = 0.5
        while z < zmax:
            sh.line(U(u1), Z(z), U(u2), Z(z), 'S-PURL', owner=o); z += s
        sh.label('girts Z200 @ %.1f m%s' % (s, ' sleeved' if s < 1.5 else ''), U(0.5*(u1+u2)), Z(0.25), 0.16, 'S-TEXT-DIM', cands=[(0, 0, 'CENTER'), (0, 0.35, 'CENTER'), (0, 0.65, 'CENTER')], allowed=(o,), leader=False)
    for bid, d, (p, q) in BAYS:
        if p in posts and q in posts and abs(posts.index(p) - posts.index(q)) == 1:
            u1, u2 = uv(p)[0], uv(q)[0]; z1 = 0.15; z2 = min(cap_top(COLS[p]['cy']), cap_top(COLS[q]['cy'])) + 0.17
            sh.line(U(u1), Z(z1), U(u2), Z(z2), 'S-BRACE', owner=bid, lineweight=50); sh.line(U(u1), Z(z2), U(u2), Z(z1), 'S-BRACE', owner=bid, lineweight=50)
            sh.label(bid + ' 2 L70x7 X', U(0.5*(u1+u2)), Z(0.5*(z1+z2)), TH_DIM, 'S-TEXT-MEMBER', cands=[(0, 0.45, 'CENTER'), (0, -0.7, 'CENTER'), (0, 0.9, 'CENTER'), (0, -1.1, 'CENTER')], allowed=(bid,), leader=False)
    us = [uv(p)[0] for p in posts]
    for u1, u2 in zip(us[:-1], us[1:]): sh.dimh(U(u1), U(u2), Z(0), -0.95)
    ue = max(U(a), U(b)) + 0.3; zc = cap_top(face['c']) if horiz else cap_top(b); zw = (TOS(face['c']) if horiz else TOS(b)) + 0.30
    sh.dimv(Z(0), Z(zc), ue, 0.8, outer=True); sh.dimv(Z(0), Z(zw), ue, 1.5, outer=True)
    sh.label('cap top', ue+0.95, Z(0.4), 0.16, 'S-TEXT-DIM', rot=90, cands=[(0, 0, 'LEFT')], leader=False); sh.label('wall panel top', ue+1.65, Z(0.4), 0.16, 'S-TEXT-DIM', rot=90, cands=[(0, 0, 'LEFT')], leader=False)
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S02', 'COLUMN SCHEDULE AND WALL ELEVATIONS', 'Elevations 1:1 in model space (m); print 1:200 on A1')
    cols = [('Mark',0.85),('Conc.',0.75),('Section',1.1),('x (m)',0.95),('y (m)',0.95),('L col',0.9),('Col top',0.9),('Plate top',0.95),('Base',0.65),('Conc. col.',1.35),('HEA web',0.95),('Bays',1.1),('Face',0.95)]
    rows = []
    for k, c in COLS.items():
        n = int(k[1:]); ew = c['bx'] > c['by']; faces = [f['id'] for f in FACES if k in f['posts']]
        rows.append(['C%d' % n, k, 'HEA 140', '%.2f' % c['cx'], '%.2f' % c['cy'], '%.3f' % L_col(c['cy']), '%.3f' % col_top(c['cy']), '+0.045', base_type(k), 'E-W 400x200' if ew else 'N-S 200x400', 'N-S' if ew else 'E-W', ','.join(BAY_OF.get(k, [])) or '-', ','.join(faces) or 'int'])
    rows.append(['WP1', '-', 'HEA 140', '77.61', '20.25', '4.24', 'slotted', '+0.040', 'post', 'edge beam', 'N-S', '-', 'S2,EN'])
    yb = sh.table(0.5, 29.3, cols, rows, 0.35, 0.15, title='COLUMN SCHEDULE (HEA 140 S275)')
    sh.note_block(0.5, yb - 0.4, 'SCHEDULE NOTES', ['Column top = TOS - 0.29 (cap-plate underside); L nominal = TOS - 0.335 (25 grout + 20 plate). Column lengths are NOMINAL: cut columns to the surveyed plate-top level from the slab-top survey (S00 section 9); grout bed 25 +/- 5 mm.',
        'Clear height 3.03 m under the cap-plate nuts at C1/C2, 3.07 m under the eave primary. Bases type E (P at K21) per S05; base plate top +0.045.',
        'Girts Z200x2.0 on cleats (D9); rows per bay as noted; bottom row 0.50 above the slab; wall sill / base rail D11. Bays B1-B7, B9 door-free (client).'], 0.16, 16.5)
    elev(sh, FACES[5], 19.0, 23.8, True, 'W  WEST ELEV. x 67.89, north left')
    elev(sh, FACES[4], 19.0, 17.2, False, 'E  EAST ELEV. x 95.69, north right')
    elev(sh, FACES[1], 17.5, 11.45, True, 'N2  NORTH ELEV. EAST y 35.87')
    elev(sh, FACES[0], 1.5, 11.45, True, 'N1  NORTH ELEV. WEST y 35.37')
    elev(sh, FACES[2], 1.5, 4.55, False, 'S1  SOUTH ELEV. WEST y 15.57')
    elev(sh, FACES[3], 14.3, 4.55, False, 'S2  SOUTH ELEV. EAST y 19.97')
    elev(sh, FACES[6], 34.2, 4.55, False, 'EN  NOTCH FACE')
    return sh
