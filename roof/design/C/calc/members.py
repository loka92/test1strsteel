"""Member checks to EN 1993-1-1: beams (6.2.5, 6.2.6, 6.3.2 LTB gravity/uplift, SLS L/200), columns (6.3.1/6.3.3),
purlins vs basis capacities, plus the column/base reaction envelope.  kN, m, kNm."""
import numpy as np, math
from model import *
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
    """Return (strong_normal, weak_normal): the wall face normal resisted by the strong axis (web normal to that wall)."""
    faces = ft.get(cid, [])
    if not faces: return None, None
    faces = sorted(faces, key=lambda f: -f[1])
    strong = faces[0][2]
    weak = next((f[2] for f in faces if f[2][0] != strong[0]), None)
    return strong, weak

def column_checks(res, bays_uls):
    """bays_uls: {d: {bay: dict(H,T,N,...)}} at ULS (1.5 W). Returns rows and the reaction envelope."""
    SC = res['sections']['col']; ft = res['wall_trib']
    rows, reac = [], {}
    NbR, xy, xz, ly, lz = None, None, None, None, None
    for cid, (cx, cy) in COLS.items():
        L = L_col(cy); v = res['colloads'][cid]
        NbR, xy, xz, ly, lz = Nb_Rd(SC, L, L)
        MbR, xlt, llt = Mb_Rd(SC, L)
        strong, weak = column_orientation(cid, ft)
        # bracing membership
        mybays = [b for b in BAYS if cid in b['c']]
        best = None
        env = dict(Nc_ULS=0, Nt_ULS=0, Vx_ULS=0, Vy_ULS=0, Nc_SLS=0, Nt_SLS=0, Vx_SLS=0, Vy_SLS=0, case_c='', case_t='')
        # ULS-1 (gravity, no wind)
        N1 = 1.35*v['G'] + 1.5*v['Q']; env['Nc_ULS'] = N1; env['case_c'] = 'ULS1'
        env['Nc_SLS'] = v['G'] + v['Q']
        cands = [dict(case='ULS1', N=N1, My=0.0, Mz=0.0)]
        for d in 'NSEW':
            # wall wind line loads on this column (kN/m) per face, worst net cp
            My = Mz = 0.0; Vw = dict(x=0.0, y=0.0)
            for fid, trib, normal in ft.get(cid, []):
                f = next(ff for ff in FACES if ff['id'] == fid)
                # distance from the windward corner along the face (for zones A/B/C)
                along = cy if normal[0] == 'x' else cx
                if d in 'NS':  corner = f['b'] if d == 'N' else f['a']
                else:          corner = f['b'] if d == 'E' else f['a']
                s = abs(along - corner) if normal[0] != {'N':'y','S':'y','E':'x','W':'x'}[d] else 0.0
                cp = wall_cp_net(normal, d, s)
                w = 1.5*abs(cp)*QP*trib               # ULS line load kN/m on the column
                M = w*L**2/8
                if normal == strong: My += M
                else: Mz += M
                Vw[normal[0]] += w*L/2               # base shear from the wall (ULS)
            Nb = 0.0; Hb = dict(x=0.0, y=0.0)
            for b in mybays:
                bf = bays_uls[d][b['id']]; Nb = max(Nb, bf['N']); Hb[b['dir']] = max(Hb[b['dir']], bf['H'])
            # ULS-2: gravity + downward wind + bracing compression (leeward column)
            N2 = 1.35*v['G'] + 1.5*v['W_D'] + Nb
            cands.append(dict(case='ULS2' + d, N=N2, My=My, Mz=Mz))
            # ULS-3: uplift + bracing tension (windward column)
            N3 = 1.0*v['Gmin'] + 1.5*v['W_' + d] - Nb
            cands.append(dict(case='ULS3' + d, N=N3, My=My, Mz=Mz))
            if N2 > env['Nc_ULS']: env['Nc_ULS'], env['case_c'] = N2, 'ULS2' + d
            if -N3 > env['Nt_ULS']: env['Nt_ULS'], env['case_t'] = -N3, 'ULS3' + d
            env['Nt_SLS'] = max(env['Nt_SLS'], -(v['Gmin'] + v['W_' + d] - Nb/1.5))
            env['Nc_SLS'] = max(env['Nc_SLS'], v['G'] + v['W_D'] + Nb/1.5)
            for ax in 'xy':   # bay shear shared by the two bases through the HEA 160 base strut; wall base shear
                Vt = Hb[ax]/2  # goes to the slab through the anchored wall base rail (reported separately)
                env['V%s_ULS' % ax] = max(env['V%s_ULS' % ax], Vt); env['V%s_SLS' % ax] = max(env['V%s_SLS' % ax], Vt/1.5)
                env['Vwall_%s' % ax] = max(env.get('Vwall_%s' % ax, 0.0), Vw[ax])
        # 6.3.3 interaction (Annex B method 2, class 1, Cm = 0.95 pinned-pinned UDL)
        best = None
        for c in cands:
            N = max(c['N'], 0.0); My, Mz = c['My'], c['Mz']
            Npl = SC['Npl']; ny = N/(xy*Npl); nz = N/(xz*Npl)
            Cm = 0.95
            kyy = min(Cm*(1 + (ly - 0.2)*ny), Cm*(1 + 0.8*ny))
            kzz = min(Cm*(1 + (2*lz - 0.6)*nz), Cm*(1 + 1.4*nz))
            kzy = 0.6*kyy; kyz = 0.6*kzz
            u1 = N/(xy*Npl) + kyy*My/MbR + kyz*Mz/SC['Mpl_z']
            u2 = N/(xz*Npl) + kzy*My/MbR + kzz*Mz/SC['Mpl_z']
            uxs = abs(c['N'])/Npl + My/SC['Mpl_y'] + Mz/SC['Mpl_z']
            u = max(u1, u2, uxs)
            if best is None or u > best['u']: best = dict(u=u, u1=u1, u2=u2, uxs=uxs, **c)
        rows.append(dict(id=cid, section=SC['name'], L=L, N_Ed=best['N'], My=best['My'], Mz=best['Mz'], case=best['case'],
                         NbRd=NbR, MbRd=MbR, util=dict(N=env['Nc_ULS']/NbR, NM=best['u'], Nt=env['Nt_ULS']/SC['Npl']),
                         umax=max(env['Nc_ULS']/NbR, best['u']), gov='6.3.3' if best['u'] > env['Nc_ULS']/NbR else '6.3.1',
                         chi_y=xy, chi_z=xz, lam_z=lz, orient=strong, bays=[b['id'] for b in mybays]))
        reac[cid] = env
    return rows, reac

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
    bays = {}; Fr = {}
    for d in 'NSEW':
        H, Ftot, Hr, Ht = bracing.distribute(d)
        bays[d] = bracing.bay_forces({k: 1.5*v for k, v in H.items()}); Fr[d] = (Ftot, Hr, Ht, H)
    beams = beam_checks(res)
    cols, reac = column_checks(res, bays)
    pur = purlin_checks(res)
    return dict(res=res, bays=bays, Fr=Fr, beams=beams, cols=cols, reac=reac, purlins=pur)

if __name__ == '__main__':
    out = run()
    print('BEAMS'); 
    for r in out['beams']:
        print('%-10s %-8s %-8s L=%5.2f M=%6.1f Mu=%6.1f V=%5.1f MbG=%5.1f MbU=%5.1f Lu=%.2f d=%5.1f | u=%.2f (%s)' % (
            r['id'], r['span'], r['section'], r['L'], r['M_Ed'], r['Mu_Ed'], r['V_Ed'], r['MbG'], r['MbU'], r['Lu'], r['d'], r['umax'], r['gov']))
    print('COLUMNS')
    for r in out['cols']:
        e = out['reac'][r['id']]
        print('%-4s L=%.2f N=%6.1f My=%5.1f Mz=%5.1f %-6s NbRd=%5.0f u=%.2f | Nc=%6.1f(%s) Nt=%6.1f(%s) Vx=%5.1f Vy=%5.1f' % (
            r['id'], r['L'], r['N_Ed'], r['My'], r['Mz'], r['case'], r['NbRd'], r['umax'], e['Nc_ULS'], e['case_c'], e['Nt_ULS'], e['case_t'], e['Vx_ULS'], e['Vy_ULS']))
    print('PURLINS', out['purlins'])
    for d in 'NSEW':
        print(d, {k: (round(v['H'],1), round(v['T'],1), round(v['N'],1), round(v['sway'],2)) for k, v in out['bays'][d].items()})
