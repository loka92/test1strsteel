"""Member checks to EN 1993-1-1: beams (6.2.5, 6.2.6, 6.3.2 LTB gravity/uplift, SLS L/200), columns (6.3.1/6.3.3),
purlins vs basis capacities, plus the column/base reaction envelope.  kN, m, kNm."""
import numpy as np, math
from model import *
from model import edge_distances, COL_LONG, SADDLE, NEAR_EDGE
from loads import *
from sections import sec, Mb_Rd, Nb_Rd, chi, FY, E as ES
from takedown import build, TYPES, COMBOS, combine
import bracing
from statics import simple_span

PURLIN_S = 1.5                       # purlin spacing (m along the slope, ~ plan)
PURLIN_MRD = dict(single=12.5, sleeved=16.0)
FLY_RULE = lambda L: 2 if L <= 6.6 else 3      # number of segments between fly braces (1 fly brace at mid-span, or third points)

def C1_of(s, M, p, q):
    """C1 for the segment [p,q] of the span from the moment diagram (EN 1993-1-1 NCCI: C1 = 1.88-1.40psi+0.52psi^2 <= 2.7
    for a linear distribution between end moments); if the maximum lies inside the segment C1 = 1.0 (conservative)."""
    i = (s >= p - 1e-6) & (s <= q + 1e-6)
    Ms = M[i]; Ma, Mb = Ms[0], Ms[-1]; Mmax = np.abs(Ms).max()
    if Mmax > 1.02*max(abs(Ma), abs(Mb)): return 1.0, Mmax
    big, small = (Ma, Mb) if abs(Ma) >= abs(Mb) else (Mb, Ma)
    psi = small/big if abs(big) > 1e-6 else 1.0
    return min(2.7, 1.88 - 1.40*psi + 0.52*psi**2), Mmax

def ltb_segments(sp, S, restr, combos):
    """Max utilisation over restraint segments for the given combos (gravity: sagging M>0; uplift: M<0)."""
    u = 0.0; worst = (0, 1.0, 0, 0)
    for c in combos:
        M = sp['Marr'][c]; s = sp['s']
        Mc = M if c in ('ULS1', 'ULS2') else -M
        for p, q in zip(restr[:-1], restr[1:]):
            C1, Mmax = C1_of(s, Mc, p, q)
            if Mmax <= 0: continue
            MbR, x, lam = Mb_Rd(S, q - p, C1)
            if Mmax/MbR > u: u = Mmax/MbR; worst = (Mmax, C1, q - p, MbR)
    return u, worst

def beam_checks(res):
    rows = []
    # restraint positions on primaries = rafter connection points (both flanges restrained by the fin plate over the web)
    for sp in res['spans']:
        S = sec(sp['section']); L = sp['L']
        Mg = max(sp['M'][c][0] for c in ('ULS1', 'ULS2'))
        Mu = -min(sp['M'][c][1] for c in ('ULS3N', 'ULS3S', 'ULS3E', 'ULS3W'))
        V = max(sp['V'][c] for c in COMBOS)
        if sp['kind'] == 'raft':
            Lg = PURLIN_S                                    # top flange held by purlins @ 1.5 m
            nseg = FLY_RULE(L); Lu = L/nseg                  # fly braces to the bottom flange
            rg = list(np.arange(0, L, PURLIN_S)) + [L]; ru = [L*i/nseg for i in range(nseg + 1)]
        else:   # primaries: both flanges held at the rafter fin plates (web-depth plate) and at the columns
            pts = sorted([sp['a'], sp['b']] + [x for x in [r['x'] for r in RAFTERS] if sp['a'] + 0.3 < x < sp['b'] - 0.3 and sp['axis'] == 'x' and sp['kind'] in ('prim', 'eave')])
            rg = ru = [p - sp['a'] for p in pts]
            Lg = max(b - a for a, b in zip(pts[:-1], pts[1:])); Lu = Lg; nseg = 0
        uG, wG = ltb_segments(sp, S, rg, ('ULS1', 'ULS2'))
        uU, wU = ltb_segments(sp, S, ru, ('ULS3N', 'ULS3S', 'ULS3E', 'ULS3W'))
        MbG = wG[3] if wG[3] else Mb_Rd(S, Lg)[0]; MbU = wU[3] if wU[3] else Mb_Rd(S, Lu)[0]
        d = sp['d']['SLS']; dlim = L*1000/200
        u = dict(M=Mg/S['Mpl_y'], V=V/S['Vpl'], LTBg=uG, LTBu=uU, defl=d/dlim, Mu=Mu/S['Mpl_y'])
        gov = max(u, key=u.get)
        rows.append(dict(id=sp['id'], span='%s-%s' % (sp['sa'], sp['sb']), section=S['name'], L=L, kind=sp['kind'],
                         M_Ed=Mg, Mu_Ed=Mu, V_Ed=V, N_Ed=0.0, Mpl=S['Mpl_y'], Vpl=S['Vpl'], MbG=MbG, MbU=MbU, Lg=Lg, Lu=Lu, nfly=nseg-1 if nseg else 0,
                         d=d, dlim=dlim, util=u, umax=u[gov], gov=gov, C1g=wG[1], C1u=wU[1], a=sp['a'], b=sp['b'], axis=sp['axis'],
                         RA=sp['RA'], RB=sp['RB']))
    return rows

def column_orientation(cid, ft):
    """(strong_normal, weak_normal): the wall face normal resisted by the strong axis (web normal to that wall)."""
    faces = ft.get(cid, [])
    if not faces: return None, None
    faces = sorted(faces, key=lambda f: -f[1]); strong = faces[0][2]
    weak = next((f[2] for f in faces if f[2][0] != strong[0]), None)
    return strong, weak

UDIR = {'N': (0.0, -1.0), 'S': (0.0, 1.0), 'E': (-1.0, 0.0), 'W': (1.0, 0.0)}
NVEC = {'x+': (1, 0), 'x-': (-1, 0), 'y+': (0, 1), 'y-': (0, -1)}

def wall_loads(cid, d, ft, L):
    """Wall wind on column cid for wind from d (characteristic): base shear vector on the concrete (kN), moments
    about the strong/weak axis (kNm) with the web normal to the governing wall."""
    cx, cy = COLS[cid]; strong, weak = column_orientation(cid, ft)
    Vx = Vy = 0.0; My = Mz = 0.0
    for fid, trib, normal in ft.get(cid, []):
        f = next(ff for ff in FACES if ff['id'] == fid)
        along = cy if normal[0] == 'x' else cx
        corner = f['b'] if d in ('N', 'E') else f['a']
        s = abs(along - corner) if normal[0] != {'N':'y','S':'y','E':'x','W':'x'}[d] else 0.0
        cp = wall_cp_net(normal, d, s)
        w = abs(cp)*QP*trib; M = w*L**2/8
        if normal == strong: My += M
        else: Mz += M
        n = NVEC[normal]; Vx += -n[0]*cp*QP*trib*L/2; Vy += -n[1]*cp*QP*trib*L/2   # pressure pushes inward
    return (Vx, Vy), My, Mz

def column_checks(res, Hchar, H4):
    """Hchar: {d: {bay: H char}} wind; H4: {'x': {bay: H}, 'y': {...}} seismic (1.0 E). Returns member rows, the
    per-case base actions {col: [case dicts]} and the base-check envelope."""
    import connections
    SC = res['sections']['col']; ft = res['wall_trib']; R = connections.anchor_resistances()
    rows, cases_all, base_env = [], {}, {}
    for cid, (cx, cy) in COLS.items():
        L = L_col(cy); v = res['colloads'][cid]; edges = edge_distances(cx, cy)
        NbR, xy, xz, ly, lz = Nb_Rd(SC, L, L); MbR, xlt, llt = Mb_Rd(SC, L)
        mybays = [b for b in BAYS if cid in b['c']]
        def brace(Hd, ud, ud2=None):
            """bracing at this column for bay forces Hd (magnitudes) and wind unit vector ud; ud2 = direction of the
            N-S roof-suction component (northward) that loads the y-bays under E/W wind. Returns
            (V aligned signed, Vcross unsigned, N_windward(-uplift), N_leeward(+))."""
            Vx = Vy = 0.0; cxs = [0.0, 0.0]; Nt = Nc = 0.0
            for b in mybays:
                H = Hd[b['id']]; other = b['c'][1] if b['c'][0] == cid else b['c'][0]
                bd = (1, 0) if b['dir'] == 'x' else (0, 1)
                proj = ud[0]*bd[0] + ud[1]*bd[1]
                if abs(proj) < 0.5 and ud2 is not None and abs(ud2[0]*bd[0] + ud2[1]*bd[1]) > 0.5:
                    proj = ud2[0]*bd[0] + ud2[1]*bd[1]
                w, h, Ld, xm, ym = bay_geom(b)
                if abs(proj) > 0.5:      # bay aligned with the wind
                    me = COLS[cid][0]*bd[0] + COLS[cid][1]*bd[1]; ot = COLS[other][0]*bd[0] + COLS[other][1]*bd[1]
                    windward = (me - ot)*proj < 0
                    if windward: Vx += H*proj*bd[0]; Vy += H*proj*bd[1]; Nt += H*h/w
                    else: Nc += H*h/w
                else:                    # cross bay (torsion share): both signs possible
                    cxs[0] += H*bd[0]; cxs[1] += H*bd[1]; Nt += H*h/w; Nc += H*h/w
            return (Vx, Vy), tuple(cxs), Nt, Nc
        cases = []
        cases.append(dict(case='ULS1', N=1.35*v['G'] + 1.5*v['Q'], V=(0.0, 0.0), Vc=(0.0, 0.0), My=0.0, Mz=0.0))
        cases.append(dict(case='SLS', N=v['G'] + v['Q'], V=(0.0, 0.0), Vc=(0.0, 0.0), My=0.0, Mz=0.0))
        for d in 'NSEW':
            (Vwx, Vwy), My, Mz = wall_loads(cid, d, ft, L)
            (Vbx, Vby), Vc, Nt, Nc = brace(Hchar[d], UDIR[d], (0.0, 1.0) if d in 'EW' else None)   # roof-suction component acts northward
            V15 = (1.5*(Vwx + Vbx), 1.5*(Vwy + Vby)); Vc15 = (1.5*Vc[0], 1.5*Vc[1])
            cases.append(dict(case='ULS2' + d, N=1.35*v['G'] + 1.5*v['W_D'] + 1.5*Nc, V=V15, Vc=Vc15, My=1.5*My, Mz=1.5*Mz))
            cases.append(dict(case='ULS3' + d, N=1.0*v['Gmin'] + 1.5*v['W_' + d] - 1.5*Nt, V=V15, Vc=Vc15, My=1.5*My, Mz=1.5*Mz))
            cases.append(dict(case='SLSW' + d, N=v['G'] + v['W_' + d] - Nt, V=(Vwx + Vbx, Vwy + Vby), Vc=Vc, My=My, Mz=Mz))
        for ax, ud in (('+x', (1, 0)), ('-x', (-1, 0)), ('+y', (0, 1)), ('-y', (0, -1))):
            (Vbx, Vby), Vc, Nt, Nc = brace(H4[ax[1]], ud)
            cases.append(dict(case='ULS4' + ax, N=1.0*v['G'] + Nc, V=(Vbx, Vby), Vc=Vc, My=0.0, Mz=0.0, Nt=1.0*v['G'] - Nt))
        # base checks per case (ULS only). Key B directions = near-edge directions with an outward demand in any case
        keyB = []
        for k in ('+x', '-x', '+y', '-y'):
            if edges[k] < NEAR_EDGE and cid not in SADDLE:
                dem = 0.0
                for c in cases:
                    if c['case'].startswith('SLS'): continue
                    comp = {'+x': c['V'][0] + c['Vc'][0], '-x': -c['V'][0] + c['Vc'][0], '+y': c['V'][1] + c['Vc'][1], '-y': -c['V'][1] + c['Vc'][1]}[k]
                    dem = max(dem, comp)
                if dem > 3.0: keyB.append(k)   # > 3 kN: cross-bay torsion shares (<= 1.5 kN) do not call for a Key B
        env = dict(Nc=(-1e9, ''), Nt=(-1e9, ''), Vt=(-1e9, ''), umax=(0, '', ''), keyB=keyB, orient=COL_LONG[cid], saddle=cid in SADDLE, zreq=0, Nmax=0.0, Mkey=0.0)
        for c in cases:
            if c['case'].startswith('SLS'): continue
            Ns = [c['N']] + ([c['Nt']] if 'Nt' in c else [])
            for N in Ns:
                bc = connections.base_check(N, c['V'], c['Vc'], edges, R, COL_LONG[cid], tuple(keyB), cid in SADDLE)
                c.setdefault('base', []).append((N, bc))
                if N > env['Nc'][0]: env['Nc'] = (N, c['case'])
                if -N > env['Nt'][0]: env['Nt'] = (-N, c['case'])
                if bc['Vt'] > env['Vt'][0]: env['Vt'] = (bc['Vt'], c['case'])
                if bc['umax'] > env['umax'][0]: env['umax'] = (bc['umax'], c['case'], bc['gov'])
                env['zreq'] = max(env['zreq'], bc['zreq']); env['Nmax'] = max(env['Nmax'], bc['Nmax']); env['Mkey'] = max(env['Mkey'], bc['M_along'] + bc['M_across'])
        # utilisation of the governing tension case at smaller solid zones (R3)
        env['u_zone'] = {}
        for z in (800, 750, 700, 600):
            uz = 0.0
            for c in cases:
                if c['case'].startswith('SLS'): continue
                for N in [c['N']] + ([c['Nt']] if 'Nt' in c else []):
                    if N < 0:
                        bz = connections.base_check(N, c['V'], c['Vc'], edges, None, COL_LONG[cid], tuple(keyB), cid in SADDLE, zone=z)
                        uz = max(uz, max(v for k, v in bz['util'].items() if 'cone' in k))
            env['u_zone'][z] = uz
        cases_all[cid] = cases; base_env[cid] = env
        # member check 6.3.3 (Annex B, Table B.2 for LTB-susceptible members: k_zy per B.2, review F7)
        best = None
        for c in cases:
            if c['case'].startswith('SLS'): continue
            N = max(c['N'], 0.0); My, Mz = c['My'], c['Mz']; Npl = SC['Npl']
            ny = N/(xy*Npl); nz = N/(xz*Npl); Cm = 0.95; CmLT = 0.95
            kyy = min(Cm*(1 + (ly - 0.2)*ny), Cm*(1 + 0.8*ny))
            kzz = min(Cm*(1 + (2*lz - 0.6)*nz), Cm*(1 + 1.4*nz))
            kzy = max(1 - 0.1*lz*nz/(CmLT - 0.25), 1 - 0.1*nz/(CmLT - 0.25)) if lz >= 0.4 else 0.6 + lz
            kyz = 0.6*kzz
            u1 = N/(xy*Npl) + kyy*My/MbR + kyz*Mz/SC['Mpl_z']
            u2 = N/(xz*Npl) + kzy*My/MbR + kzz*Mz/SC['Mpl_z']
            uxs = abs(c['N'])/Npl + My/SC['Mpl_y'] + Mz/SC['Mpl_z']
            u = max(u1, u2, uxs)
            if best is None or u > best['u']: best = dict(u=u, u1=u1, u2=u2, uxs=uxs, kzy=kzy, **{k: c[k] for k in ('case', 'N', 'My', 'Mz')})
        uN = env['Nc'][0]/NbR
        rows.append(dict(id=cid, section=SC['name'], L=L, N_Ed=best['N'], My=best['My'], Mz=best['Mz'], case=best['case'],
                         NbRd=NbR, MbRd=MbR, util=dict(N=uN, NM=best['u'], Nt=env['Nt'][0]/SC['Npl']), kzy=best['kzy'],
                         umax=max(uN, best['u']), gov='6.3.3' if best['u'] > uN else '6.3.1', chi_y=xy, chi_z=xz, lam_z=lz,
                         orient=column_orientation(cid, ft)[0], bays=[b['id'] for b in mybays], edges=edges))
    return rows, cases_all, base_env

def purlin_checks(res):
    """Worst purlin span: integrate the field along each purlin span (trib 1.5 m) for gravity and uplift."""
    X, Y, R, dx = res['grid']; f = res['fields']
    ys = np.arange(ENV['y1'] - 0.3, ENV['y0'], -PURLIN_S)
    worst = dict(gravity=(0, None), uplift=(0, None))
    for y in ys:
        act = sorted([r['x'] for r in RAFTERS if r['y0'] <= y <= r['y1']])
        j = int((y - ENV['y0'])/dx)
        for a, b in zip(act[:-1], act[1:]):
            ia, ib = int((a - ENV['x0'])/dx), int((b - ENV['x0'])/dx)
            if not R[ia:ib, j].any(): continue
            xs = X[ia:ib, j]
            for name, arr in (('gravity', 1.35*f['G'][ia:ib, j] + 1.5*f['Q'][ia:ib, j]),
                              ('uplift', np.min([f['Gmin'][ia:ib, j] + 1.5*f['W_' + d][ia:ib, j] for d in 'NSEW'], axis=0))):
                w = arr*PURLIN_S
                sp = simple_span(b - a, lambda s, w=w, xs=xs: np.interp(a + s, xs, w), n=100)
                M = sp['Mmax'] if name == 'gravity' else -sp['Mmin']
                if M > worst[name][0]: worst[name] = (M, (a, b, y, b - a))
    # deflection SLS G+Q on the longest span (uniform), I = 3.9e6 mm4
    Lmax = max(b - a for y in ys for a, b in zip(*(lambda l: (l[:-1], l[1:]))(sorted([r['x'] for r in RAFTERS if r['y0'] <= y <= r['y1']]))))
    w = (G_ROOF + Q_ROOF)*PURLIN_S
    d = 5*w*Lmax**4/(384*ES*1e3*3.9e6*1e-12)*1000
    return dict(worst=worst, Lmax=Lmax, d=d, dlim=Lmax*1000/150)

def run(sec_prim=SEC_PRIM, sec_raft=SEC_RAFT, sec_col=SEC_COL):
    res = build(sec_prim, sec_raft, sec_col)
    Hchar, Fr = {}, {}
    for d in 'NSEW':
        H, Ftot, Hr, Ht = bracing.distribute(d); Hchar[d] = H; Fr[d] = (Ftot, Hr, Ht, H)
    bays = {d: bracing.bay_forces({k: 1.5*v for k, v in Hchar[d].items()}) for d in 'NSEW'}
    steel = sum(sec(s['section'])['w']*s['L'] for s in res['spans']) + sum(sec(sec_col)['w']*L_col(COLS[c][1]) for c in COLS)
    seis = bracing.seismic_check(res['roof_area'], 1.1*steel)
    X, Y, R, dx = res['grid']; xc = float((X*R).sum()/R.sum()); yc = float((Y*R).sum()/R.sum())
    H4 = {'x': bracing.distribute_point(seis['Fb'], xc, yc, 'x'), 'y': bracing.distribute_point(seis['Fb'], xc, yc, 'y')}
    beams = beam_checks(res)
    cols, cases, base_env = column_checks(res, Hchar, H4)
    pur = purlin_checks(res)
    return dict(res=res, bays=bays, Fr=Fr, Hchar=Hchar, H4=H4, seis=seis, beams=beams, cols=cols, cases=cases, base_env=base_env, purlins=pur)

if __name__ == '__main__':
    out = run()
    print('BEAMS'); 
    for r in out['beams']:
        print('%-10s %-8s %-8s L=%5.2f M=%6.1f Mu=%6.1f V=%5.1f MbG=%5.1f MbU=%5.1f Lu=%.2f d=%5.1f | u=%.2f (%s)' % (
            r['id'], r['span'], r['section'], r['L'], r['M_Ed'], r['Mu_Ed'], r['V_Ed'], r['MbG'], r['MbU'], r['Lu'], r['d'], r['umax'], r['gov']))
    print('COLUMNS')
    for r in out['cols']:
        e = out['base_env'][r['id']]
        print('%-4s %s keyB=%-12s Nc=%6.1f(%s) Nt=%6.1f(%s) Vt=%5.1f(%s) base %.2f %s %s | zreq %d u800/700/600 %.2f/%.2f/%.2f Nmax %.0f' % (
            r['id'], e['orient'], ','.join(e['keyB']) or '-', e['Nc'][0], e['Nc'][1], e['Nt'][0], e['Nt'][1], e['Vt'][0], e['Vt'][1], e['umax'][0], e['umax'][1], e['umax'][2], e['zreq'], e['u_zone'][800], e['u_zone'][700], e['u_zone'][600], e['Nmax']))
    print('seismic', out['seis'], out['H4'])
    print('PURLINS', out['purlins'])
    for d in 'NSEW':
        print(d, {k: (round(v['H'],1), round(v['T'],1), round(v['N'],1), round(v['sway'],2)) for k, v in out['bays'][d].items()})
