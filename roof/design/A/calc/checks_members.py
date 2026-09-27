"""EN 1993-1-1 member checks for the portal frames (columns and rafters), deflections and sway.
Reads results_frames.pkl (from frames_model.py). Writes members_A.csv (frame members part),
reactions_frames.pkl and prints tables used in the report.
"""
import os, pickle, math, csv
import numpy as np
from sections import sec, haunch_props, chi, chi_LT, Mcr, C1_from_psi, curve_y, curve_z, curve_LT, MN_Rd, annexB_k, FY, E
import loads as L
from frames_model import DESIGN, COMBOS

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..')
RES = pickle.load(open(os.path.join(HERE, 'results_frames.pkl'), 'rb'))
FLY = {'F1': 3.0, 'F2': 3.0, 'F3': 3.0, 'F4': 3.0, 'F5': 3.0, 'F6': 3.0, 'F7': 3.0}   # fly-brace spacing (m), every 2nd purlin
ULS = [c for c in COMBOS if c.startswith('ULS')]


def frame_keys(fname):
    return [k for k in RES if k == fname or k.startswith(fname + '_')]


# ------------------------------------------------------------------ helpers to extract forces
def column_forces(res, k):
    """Return dict with N (compression +), M_top, M_max, V_max for column k in one combo result."""
    Ns, Ms, Vs = [], [], []
    Mtop = 0
    for m, r in zip(res['members'], res['results']):
        if m['tag'][0] == 'col' and m['tag'][1] == k:
            Ns += list(-r['N']); Ms += list(r['M']); Vs += list(r['V'])
            if m['tag'][2] == 3: Mtop = r['M'][-1]
    return dict(N=max(Ns), Nmin=min(Ns), M=max(np.abs(Ms)), Mtop=Mtop, V=max(np.abs(Vs)))


def rafter_profile(res):
    """Concatenate rafter results into arrays along y: y, M, V, N, haunch flag, deflection dz."""
    ys, Ms, Vs, Ns, hs, dz = [], [], [], [], [], []
    nodes = res['nodes']
    for m, r in zip(res['members'], res['results']):
        if m['tag'][0] != 'raf': continue
        xi, zi = nodes[m['i']]; xj, zj = nodes[m['j']]
        c = (xj - xi) / r['L']
        ys += list(xi + r['x'] * c); Ms += list(r['M']); Vs += list(r['V']); Ns += list(r['N'])
        hs += [m['tag'][2] == 'haunch'] * len(r['x'])
        ui = res['disp'][m['i']]; uj = res['disp'][m['j']]
        dz += list(np.interp(r['x'], [0, r['L']], [ui[1], uj[1]]))
    o = np.argsort(ys)
    return (np.array(ys)[o], np.array(Ms)[o], np.array(Vs)[o], np.array(Ns)[o], np.array(hs)[o], np.array(dz)[o])


# ------------------------------------------------------------------ column check
def check_column(k, fname, meta, combos_res):
    s = sec(meta['colsec'][k]); y = L.COLS[k][1]
    h = L.TOS(y) - sec(meta['rafter'])['h'] / 2000     # column length to rafter centreline
    rows = []
    # buckling parameters (non-sway lengths: sway captured by alpha_cr >= 10 / amplification)
    Lcr_y, Lcr_z = h, h
    lam_y = Lcr_y * 1e3 / (s['iy'] * 10) / (math.pi * math.sqrt(E / FY))
    lam_z = Lcr_z * 1e3 / (s['iz'] * 10) / (math.pi * math.sqrt(E / FY))
    chi_y = chi(lam_y, curve_y(s)); chi_z = chi(lam_z, curve_z(s))
    Mc = Mcr(s, h * 1e3, C1=C1_from_psi(0.0))          # triangular moment 0 at base -> M at top
    lam_LT = math.sqrt(s['Mpl_y'] / Mc); xLT = chi_LT(lam_LT, curve_LT(s))
    wall_ns = k in L.WALL_SIDE
    Cmy = 0.9 if wall_ns else 0.6                       # Table B.3 (uniform load + end moment / triangular)
    CmLT = Cmy
    ew_trib = L.WALL_TRIB.get(k, (0, 0))[1]
    worst = dict(u=0)
    for combo, res in combos_res:
        cf = column_forces(res, k)
        N, M = cf['N'], cf['M']
        # out-of-plane bending from E/W wall wind (only in the along-ridge wind combos, max with cpi -0.3)
        Mz = 0.0
        if ew_trib > 0 and combo.endswith('_R'):
            cpi = L.CPI['m'] if 'ULS2' in combo else L.CPI['p']
            wz = 1.5 * (L.CPE_WALL_D - cpi) * L.QP * ew_trib
            Mz = wz * h**2 / 8
        # brace vertical force in braced bays (E-W wind), added axial
        Nbr = 30.0 if (combo.endswith('_R') and k in L.BRACED_COLS) else 0.0   # vertical component of the wall bracing (checks_secondary)
        N = max(N + Nbr, 0.0)
        cls = max(s['class_bending'], s.web_class_MN(N))
        u_cs = M / MN_Rd(s, N) + (Mz / s['Mpl_z'] if Mz else 0)     # 6.2.9 (linear sum, conservative)
        u_v = cf['V'] / s['Vpl']
        kyy, kyz, kzy, kzz = annexB_k(s, N, chi_y, chi_z, lam_y, lam_z, Cmy, 0.9, CmLT)
        u_b1 = N / (chi_y * s['Npl']) + kyy * M / (xLT * s['Mpl_y']) + kyz * Mz / s['Mpl_z']
        u_b2 = N / (chi_z * s['Npl']) + kzy * M / (xLT * s['Mpl_y']) + kzz * Mz / s['Mpl_z']
        u = max(u_cs, u_v, u_b1, u_b2)
        if u > worst['u']:
            worst = dict(u=u, combo=combo, N=N, M=M, Mz=Mz, V=cf['V'], u_cs=u_cs, u_v=u_v, u_b1=u_b1, u_b2=u_b2,
                         cls=cls, Nmin=cf['Nmin'])
    gov = max([('6.2.9 M+N', worst['u_cs']), ('shear', worst['u_v']), ('6.3.3 (6.61)', worst['u_b1']), ('6.3.3 (6.62)', worst['u_b2'])],
              key=lambda t: t[1])[0]
    return dict(id='%s (%s)' % (k, fname), type='column', section=s['name'], L=h, frm='base', to='knee',
                N=worst['N'], M=worst['M'], Mz=worst['Mz'], V=worst['V'], combo=worst['combo'], cls=worst['cls'],
                u_cs=worst['u_cs'], u_v=worst['u_v'], u_b1=worst['u_b1'], u_b2=worst['u_b2'], u=worst['u'], gov=gov,
                lam_y=lam_y, lam_z=lam_z, chi_y=chi_y, chi_z=chi_z, lam_LT=lam_LT, xLT=xLT, Mcr=Mc)


# ------------------------------------------------------------------ rafter checks
def check_rafter(fname, meta, combos_res):
    s = sec(meta['rafter']); hp = haunch_props(s)
    cols = meta['cols']; y0, y1 = meta['y0'], meta['y1']
    fb = FLY[fname]
    # restraint points of the bottom flange: columns, haunch tips, fly braces at fb intervals from haunch tips
    restr = set()
    for (a, b), (k, y) in zip(meta['hz'], cols):
        restr |= {round(a, 3), round(b, 3), round(y, 3)}
    tips = [(a, b) for a, b in meta['hz']]
    if meta['propped']: tips = [(y0, y0)] + tips
    for i in range(len(tips) - 1):
        a = tips[i][1]; b = tips[i + 1][0]
        n = int(math.floor((b - a) / fb + 1e-6))
        for j in range(1, n + 1):
            restr.add(round(a + j * fb, 3))
        restr.add(round(b, 3))
    restr |= {round(y0, 3), round(y1, 3)}
    restr = sorted(restr)
    # segments = bays (between columns) + cantilevers
    supports = [y for _, y in cols]
    if meta['propped']: supports = [y0] + supports
    seg_bounds = [(y0, supports[0])] + [(supports[i], supports[i + 1]) for i in range(len(supports) - 1)] + [(supports[-1], y1)]
    rows = []
    for si, (ya, yb) in enumerate(seg_bounds):
        Lseg = yb - ya
        if Lseg < 0.05: continue
        canti = si == 0 or si == len(seg_bounds) - 1
        name = '%s rafter %s' % (fname, ('cant S' if si == 0 else 'cant N') if canti else 'bay %d' % si)
        if canti and Lseg < 0.35: continue
        worst = dict(u=0); ltb = dict(u=0); hnch = dict(u=0)
        for combo, res in combos_res:
            y, M, V, N, hz, dz = rafter_profile(res)
            sel = (y >= ya - 1e-6) & (y <= yb + 1e-6)
            plain = sel & ~hz; haun = sel & hz
            Nc = max(0.0, -N[sel].min())
            # cross-section (plain part) M+N and shear
            if plain.any():
                Mp = np.abs(M[plain]).max()
                u_cs = Mp / MN_Rd(s, Nc)
            else:
                Mp = 0; u_cs = 0
            u_v = np.abs(V[sel]).max() / s['Vpl']
            # haunch: elastic check at column face with the haunched section (class 3 treatment)
            if haun.any():
                Mh = np.abs(M[haun]).max()
                u_h = Mh / hp['Mel'] + Nc / (hp['A'] * 100 * FY / 1e3)
            else:
                Mh = 0; u_h = 0
            # LTB: bottom flange in compression (M < 0) between restraints
            u_lt, Lcr_g, Mneg_g, C1_g = 0, 0, 0, 1
            for ra, rb in zip(restr[:-1], restr[1:]):
                if rb <= ya + 1e-6 or ra >= yb - 1e-6: continue
                seg = (y >= ra - 1e-6) & (y <= rb + 1e-6)
                if not seg.any(): continue
                Mseg = M[seg]
                Mneg = -Mseg.min()
                if Mneg <= 0: continue
                Lcr = rb - ra
                # C1: if the peak negative moment is at a segment end use the end ratio, else uniform (C1 = 1.0 ... 1.13)
                iend = np.argmin(Mseg); yseg = y[seg]
                at_end = abs(yseg[iend] - ra) < 1e-3 or abs(yseg[iend] - rb) < 1e-3
                if at_end:
                    Mother = Mseg[-1] if abs(yseg[iend] - ra) < 1e-3 else Mseg[0]
                    C1 = C1_from_psi(max(-1.0, min(1.0, Mother / Mseg.min())))
                else:
                    C1 = 1.13
                Mc = Mcr(s, Lcr * 1e3, C1=C1)
                lam_LT = math.sqrt(s['Mpl_y'] / Mc); xLT = chi_LT(lam_LT, curve_LT(s))
                lam_z = Lcr * 1e3 / (s['iz'] * 10) / (math.pi * math.sqrt(E / FY)); chi_z = chi(lam_z, curve_z(s))
                # 6.3.3 with N (rafter axial small); haunch region uses plain rafter properties conservatively
                kzy = annexB_k(s, Nc, 1.0, chi_z, 0.5, lam_z, 0.9, 0.9, 0.9)[2]
                in_haunch = hz[seg].mean() > 0.5   # boundary points are shared with the plain element
                MRd = hp['Mel'] if in_haunch else s['Mpl_y']   # haunch: elastic modulus of the deepened section, chi_LT of the rafter
                u = Nc / (chi_z * s['Npl']) + kzy * Mneg / (xLT * MRd)
                if u > u_lt:
                    u_lt, Lcr_g, Mneg_g, C1_g, xLT_g, lamLT_g = u, Lcr, Mneg, C1, xLT, lam_LT
            uu = max(u_cs, u_v, u_h, u_lt)
            if uu > worst['u']:
                worst = dict(u=uu, combo=combo, Mp=Mp, Mh=Mh, N=Nc, V=np.abs(V[sel]).max(), u_cs=u_cs, u_v=u_v, u_h=u_h,
                             u_lt=u_lt, Lcr=Lcr_g, Mneg=Mneg_g, C1=C1_g, xLT=(xLT_g if u_lt else 1.0), lamLT=(lamLT_g if u_lt else 0))
        w = worst
        gov = max([('6.2.9 M+N', w['u_cs']), ('shear', w['u_v']), ('haunch Mel', w['u_h']), ('LTB 6.3.2/6.3.3', w['u_lt'])], key=lambda t: t[1])[0]
        rows.append(dict(id=name, type='rafter', section=s['name'] + (' + haunch' if w['Mh'] else ''), L=Lseg,
                         frm='y=%.2f' % ya, to='y=%.2f' % yb, N=w['N'], M=max(w['Mp'], w['Mneg']), Mh=w['Mh'], V=w['V'], combo=w['combo'],
                         u_cs=w['u_cs'], u_v=w['u_v'], u_h=w['u_h'], u_lt=w['u_lt'], Lcr=w['Lcr'], C1=w['C1'], xLT=w['xLT'],
                         lamLT=w['lamLT'], u=w['u'], gov=gov, cls=s['class_bending']))
    return rows


# ------------------------------------------------------------------ deflections and sway
def deflections(fname, meta, res_D, res_Q):
    cols = meta['cols']; y0, y1 = meta['y0'], meta['y1']
    supports = [y for _, y in cols]
    if meta['propped']: supports = [y0] + supports
    out = []
    for name, res in (('G+Q', res_D), ('Q', res_Q)):
        y, M, V, N, hz, dz = rafter_profile(res)
        for i in range(len(supports) - 1):
            a, b = supports[i], supports[i + 1]
            sel = (y >= a) & (y <= b)
            da, db = np.interp(a, y, dz), np.interp(b, y, dz)
            chord = np.interp(y[sel], [a, b], [da, db])
            d = (dz[sel] - chord).min() * 1e3
            out.append(dict(frame=fname, case=name, bay='%.2f-%.2f' % (a, b), L=b - a, d=-d, lim=(b - a) * 1e3 / 200))
        # cantilevers
        for a, b, tag in ((y0, supports[0], 'cant S'), (supports[-1], y1, 'cant N')):
            if b - a > 0.35:
                yc = y0 if tag == 'cant S' else y1; ysup = supports[0] if tag == 'cant S' else supports[-1]
                d = (np.interp(yc, y, dz) - np.interp(ysup, y, dz)) * 1e3
                out.append(dict(frame=fname, case=name, bay=tag, L=b - a, d=-d, lim=(b - a) * 1e3 / 100))
    return out


def sway(fname, meta, combos_res):
    out = []
    for combo, res in combos_res:
        for k, y in meta['cols']:
            ridx = min(range(len(meta['ys'])), key=lambda i: abs(meta['ys'][i] - y))
            u = res['disp']['r%d' % ridx][0] * 1e3
            h = L.TOS(y) * 1e3
            out.append(dict(frame=fname, combo=combo, col=k, u=u, h=h, ratio=abs(u) / h))
    return out


# ------------------------------------------------------------------ main
def main():
    members, defl, sw, per_frame = [], [], [], {}
    reactions = {}
    for fname in L.FRAMES:
        keys = frame_keys(fname)
        meta = RES[keys[0]]['_meta']
        combos_res = [(c, RES[k][c]) for k in keys for c in ULS]
        for k, y in meta['cols']:
            members.append(check_column(k, fname, meta, combos_res))
        members += check_rafter(fname, meta, combos_res)
        for k in keys:
            defl += deflections(fname, meta, RES[k]['SLS_D'], RES[k]['SLS_Q'])
            sw += sway(fname, meta, [(c, RES[k][c]) for c in ('SLS_WN', 'SLS_WS', 'SLS_WNp', 'SLS_WR')])
        # reactions (frame plane): Rz > 0 compression on base, Rx = horizontal reaction on the structure (+ north)
        for k, y in meta['cols']:
            rec = reactions.setdefault(k, dict(Nc_ULS=0, Nt_ULS=0, Vy_ULS=0, Nc_SLS=0, Nt_SLS=0, Vy_SLS=0, comboC='', comboT='', comboV=''))
            for kk in keys:
                for c in COMBOS:
                    R = RES[kk][c]['reactions']['%s_0' % k]
                    tag = 'ULS' if c.startswith('ULS') else 'SLS'
                    if R[1] > rec['Nc_' + tag]: rec['Nc_' + tag] = R[1]; rec['combo' + ('C' if tag == 'ULS' else 'Cs')] = c
                    if -R[1] > rec['Nt_' + tag]: rec['Nt_' + tag] = -R[1]; rec['combo' + ('T' if tag == 'ULS' else 'Ts')] = c
                    if abs(R[0]) > rec['Vy_' + tag]: rec['Vy_' + tag] = abs(R[0]); rec['combo' + ('V' if tag == 'ULS' else 'Vs')] = c
        # girder prop reactions
        if meta['propped']:
            rec = reactions.setdefault('girder_' + fname, dict(Nc_ULS=0, Nt_ULS=0, Vy_ULS=0, Nc_SLS=0, Nt_SLS=0, Vy_SLS=0))
            for kk in keys:
                for c in COMBOS:
                    R = RES[kk][c]['reactions'].get('r0', np.zeros(3))
                    tag = 'ULS' if c.startswith('ULS') else 'SLS'
                    rec['Nc_' + tag] = max(rec['Nc_' + tag], R[1]); rec['Nt_' + tag] = max(rec['Nt_' + tag], -R[1])
        # per-frame envelope summary for the report
        pf = dict(alpha={c: min(RES[k][c]['alpha_cr'] for k in keys) for c in ULS}, alpha_HV=meta['alpha_HV'])
        env = {}
        for k in keys:
            for c in ULS:
                y, M, V, N, hz, dz = rafter_profile(RES[k][c])
                e = env.setdefault(c, dict(Mmax=-1e9, Mmin=1e9, Vmax=0, Nmin=0, Nmax=0))
                e['Mmax'] = max(e['Mmax'], M.max()); e['Mmin'] = min(e['Mmin'], M.min()); e['Vmax'] = max(e['Vmax'], np.abs(V).max())
                e['Nmin'] = min(e['Nmin'], N.min()); e['Nmax'] = max(e['Nmax'], N.max())
                for kc, yc in meta['cols']:
                    cf = column_forces(RES[k][c], kc)
                    e.setdefault('cols', {}).setdefault(kc, dict(N=0, M=0, V=0))
                    e['cols'][kc]['N'] = max(e['cols'][kc]['N'], cf['N']); e['cols'][kc]['M'] = max(e['cols'][kc]['M'], cf['M'])
                    e['cols'][kc]['V'] = max(e['cols'][kc]['V'], cf['V'])
        pf['env'] = env
        per_frame[fname] = pf
    pickle.dump(dict(members=members, defl=defl, sway=sw, reactions=reactions, per_frame=per_frame),
                open(os.path.join(HERE, 'results_checks.pkl'), 'wb'))
    # ---- print
    print('\n=== MEMBER CHECKS (frame members) ===')
    print('%-22s %-16s %5s %7s %7s %6s %6s | %5s %5s %5s %5s %5s | %5s  %s' %
          ('member', 'section', 'L', 'N_Ed', 'M_Ed', 'Mz', 'V_Ed', 'M+N', 'V', 'haun', 'buckl', 'LTB', 'u', 'governing / combo'))
    for m in members:
        if m['type'] == 'column':
            print('%-22s %-16s %5.2f %7.1f %7.1f %6.1f %6.1f | %5.2f %5.2f %5s %5.2f %5s | %5.2f  %s %s' %
                  (m['id'], m['section'], m['L'], m['N'], m['M'], m['Mz'], m['V'], m['u_cs'], m['u_v'], '-', max(m['u_b1'], m['u_b2']), '-', m['u'], m['gov'], m['combo']))
        else:
            print('%-22s %-16s %5.2f %7.1f %7.1f %6s %6.1f | %5.2f %5.2f %5.2f %5s %5.2f | %5.2f  %s %s (Lcr %.1f C1 %.2f chiLT %.2f)' %
                  (m['id'], m['section'], m['L'], m['N'], m['M'], '-', m['V'], m['u_cs'], m['u_v'], m['u_h'], '-', m['u_lt'], m['u'], m['gov'], m['combo'], m['Lcr'], m['C1'], m['xLT']))
    print('\n=== DEFLECTIONS (mm) ===')
    for d in defl:
        flag = 'OK' if d['d'] <= d['lim'] else 'EXCEEDS'
        if d['case'] == 'G+Q' or d['d'] > 0.5 * d['lim']:
            print('%s %-5s bay %-12s L %5.2f  d %6.1f  limit %6.1f  %s' % (d['frame'], d['case'], d['bay'], d['L'], d['d'], d['lim'], flag))
    print('\n=== SWAY (SLS wind) worst per frame ===')
    for fname in L.FRAMES:
        w = max([x for x in sw if x['frame'] == fname], key=lambda x: x['ratio'])
        print('%s  u = %5.1f mm at %s (h %.2f m)  1/%.0f  %s  [%s]' % (fname, w['u'], w['col'], w['h'] / 1e3, 1 / max(w['ratio'], 1e-9), 'OK' if w['ratio'] <= 1 / 150 else 'EXCEEDS', w['combo']))
    print('\n=== alpha_cr per frame (min over ULS combos) ===')
    for fname, pf in per_frame.items():
        print(fname, ' '.join('%s:%.1f' % (c, a) for c, a in pf['alpha'].items()), ' H/V-method(ULS1): %.1f' % pf['alpha_HV'])
    print('\n=== REACTIONS (frame plane) ===')
    for k, r in reactions.items():
        print('%-10s Nc_ULS %6.1f  Nt_ULS %6.1f  Vy_ULS %5.1f | Nc_SLS %6.1f Nt_SLS %6.1f Vy_SLS %5.1f' %
              (k, r['Nc_ULS'], r['Nt_ULS'], r['Vy_ULS'], r['Nc_SLS'], r['Nt_SLS'], r['Vy_SLS']))
    return members


if __name__ == '__main__':
    main()
