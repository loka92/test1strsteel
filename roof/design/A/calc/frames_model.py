"""Alternative A - analysis of the 7 portal frames (2D, first order + amplified sway).
Run:  python3 frames_model.py   -> results_frames.pkl, frames_A.png, prints summary.
Design sections are set in DESIGN (also imported by the check scripts).
"""
import os, pickle, math
import numpy as np
from frame2d import Frame2D
from sections import sec, haunch_props
import loads as L

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..')

# ---------------------------------------------------------------- design choice (iterated by the checks)
DESIGN = dict(
    rafter={'F1': 'IPE300', 'F2': 'IPE300', 'F3': 'IPE300', 'F4': 'IPE300', 'F5': 'IPE300', 'F6': 'IPE300', 'F7': 'IPE300'},
    column_default='HEA200',
    column={},                       # exceptions per column id, none: one column section for all 27
    haunch={'F1': 1.3, 'F2': 1.3, 'F3': 1.3, 'F4': 1.3, 'F5': 1.3, 'F6': 1.3, 'F7': 1.3},   # m each side of column, one cutting detail
    girder='IPE300',
    haunch_min_bay=3.5,   # bays shorter than this: haunch only at one side (bracket depth by plates)
)


def col_section(k):
    return DESIGN['column'].get(k, DESIGN['column_default'])


# ---------------------------------------------------------------- transfer girder stiffness (F5/F6 prop)
def girder_spring(x_load, sect=None):
    """Vertical stiffness (kN/m) of the 2-span eave girder K21-K22-K23 at x_load."""
    s = sec(sect or DESIGN['girder'])
    g = Frame2D()
    xs = sorted({81.79, 88.88, 95.49, x_load, 87.2, 92.5})
    for i, x in enumerate(xs):
        g.add_node('n%d' % i, x, 0)
    for i in range(len(xs) - 1):
        g.add_member('g%d' % i, 'n%d' % i, 'n%d' % (i + 1), s['A_m2'], s['I_m4'])
    for i, x in enumerate(xs):
        if x in (81.79, 88.88, 95.49):
            g.support('n%d' % i, x == 81.79, True, False)
    g.node_load('n%d' % xs.index(x_load), Fz=-1.0)
    g.solve(2)
    d = -g.displacement('n%d' % xs.index(x_load))[1]
    return 1.0 / d


# ---------------------------------------------------------------- load cases
def build_frame(fname, prop='spring'):
    F = L.FRAMES[fname]
    rs = sec(DESIGN['rafter'][fname]); hp = haunch_props(rs)
    hr = rs['h'] / 1000
    Lh = DESIGN['haunch'][fname]
    cols = [(k, L.COLS[k][1]) for k in F['cols']]
    y0, y1 = F['y0'], F['y1']
    if F.get('propped'):
        y0 = 20.07
    # haunch extents: at each column, +-Lh (end columns: inside only); short bays: one side only
    hz = []
    for i, (k, y) in enumerate(cols):
        a = y - Lh if i > 0 else y
        b = y + Lh if i < len(cols) - 1 else y
        if i > 0 and (y - cols[i - 1][1]) < DESIGN['haunch_min_bay']:
            a = y
        hz.append((max(a, y0), min(b, y1)))
    # breakpoints
    bp = {y0, y1, y0 + 1.2, y1 - 1.2} | {y for _, y in cols} | {a for a, b in hz} | {b for a, b in hz}
    if fname in ('F3', 'F4'):
        bp |= {L.OPEN_STAIR[0], L.OPEN_STAIR[1], L.OPEN_ELEV[0], L.OPEN_ELEV[1], 20.07}
        if fname == 'F3': bp |= {19.97}
    bp = sorted({round(v, 3) for v in bp if y0 - 1e-9 <= v <= y1 + 1e-9})
    ys = [bp[0]]
    for a, b in zip(bp[:-1], bp[1:]):
        n = max(1, int(math.ceil((b - a) / 0.4)))
        ys += list(np.linspace(a, b, n + 1)[1:])
    f = Frame2D()
    f.meta = dict(name=fname, cols=cols, y0=y0, y1=y1, ys=ys, rafter=rs['name'], hz=hz, Lh=Lh,
                  colsec={k: col_section(k) for k, _ in cols}, propped=bool(F.get('propped')))
    for i, y in enumerate(ys):
        f.add_node('r%d' % i, y, L.TOS(y) - hr / 2)
    for i in range(len(ys) - 1):
        ym = 0.5 * (ys[i] + ys[i + 1])
        inh = any(a - 1e-6 <= ym <= b + 1e-6 for a, b in hz)
        if inh: f.add_member('r%d' % i, 'r%d' % i, 'r%d' % (i + 1), hp['A_m2'], hp['I_m4'], tag=('raf', fname, 'haunch'))
        else:   f.add_member('r%d' % i, 'r%d' % i, 'r%d' % (i + 1), rs['A_m2'], rs['I_m4'], tag=('raf', fname, 'plain'))
    for k, y in cols:
        cs = sec(col_section(k)); ztop = L.TOS(y) - hr / 2
        n = 4
        for j in range(n + 1):
            f.add_node('%s_%d' % (k, j), y, ztop * j / n)
        for j in range(n):
            f.add_member('%s_%d' % (k, j), '%s_%d' % (k, j), '%s_%d' % (k, j + 1), cs['A_m2'], cs['I_m4'], tag=('col', k, j))
        # rigid link column top -> rafter node (same coordinates): merge by using the rafter node as top
        f.support('%s_0' % k, True, True, False)
        # replace top node name in the last column member by the rafter node
        ridx = min(range(len(ys)), key=lambda i: abs(ys[i] - y))
        f.members[-1]['j'] = 'r%d' % ridx
        del f.nodes['%s_%d' % (k, n)]
    if F.get('propped'):
        if prop == 'spring':
            f.spring('r0', kz=girder_spring(F['x']))
        else:
            f.support('r0', False, True, False)
    return f


def apply_case(f, case, factor, horiz_scale=1.0):
    """Add the loads of one characteristic case times factor. case in
    G, Gmin, Q, W_<dir>_<cpi> (dir N/S/R/S0, cpi p/m)."""
    fname = f.meta['name']; F = L.FRAMES[fname]
    rs = sec(f.meta['rafter']); hp = haunch_props(rs)
    ys = f.meta['ys']; cols = f.meta['cols']
    gable = F['gable'] is not None
    for mi, m in enumerate(f.members):
        tag = m['tag']
        if tag[0] == 'raf':
            i = int(m['name'][1:]); ya, yb = ys[i], ys[i + 1]; ym = 0.5 * (ya + yb)
            w_tr = L.trib_roof(fname, ym)
            sw = (hp['mass'] if tag[2] == 'haunch' else rs['mass']) * 9.81e-3 * (1 + L.ALLOW_PLATES)
            if case == 'G':
                wz = -(L.G_ROOF * w_tr + sw + (L.UPSTAND if L.on_opening_edge(fname, ym) else 0))
                f.member_load(mi, 0, factor * wz)
            elif case == 'Gmin':
                f.member_load(mi, 0, -factor * (L.G_ROOF_MIN * w_tr + sw))
            elif case == 'Q':
                f.member_load(mi, 0, -factor * L.Q_ROOF * w_tr)
            elif case.startswith('W'):
                _, d, cpi_key = case.split('_'); cpi = L.CPI[cpi_key]
                if d == 'N': cpe = L.roof_cpe('N', f.meta['y1'] - ym, gable)
                elif d == 'S': cpe = L.roof_cpe('S', ym - f.meta['y0'], gable)
                elif d == 'S0': cpe = 0.0 if cpi < 0 else L.roof_cpe('S', ym - f.meta['y0'], gable)
                else: cpe = L.ROOF_CPE_RIDGE[fname]
                p = (cpe - cpi) * L.QP          # positive = pressure (downwards)
                f.member_load(mi, 0, -factor * p * w_tr)
        else:
            k = tag[1]; cs = sec(f.meta['colsec'][k]); y = L.COLS[k][1]
            if case in ('G', 'Gmin'):
                f.member_load(mi, 0, -factor * cs['mass'] * 9.81e-3 * (1 + L.ALLOW_PLATES))
            if case.startswith('W') and k in L.WALL_SIDE:
                _, d, cpi_key = case.split('_'); cpi = L.CPI[cpi_key]
                dd = 'S' if d == 'S0' else d
                cp = L.wall_cp(dd, L.WALL_SIDE[k], cpi)
                # force direction: pressure on the N wall pushes south (-x); on the S wall pushes north (+x)
                sgn = -1 if L.WALL_SIDE[k] == 'N' else +1
                f.member_load(mi, factor * horiz_scale * sgn * cp * L.QP * L.WALL_TRIB[k][0], 0)
    # wall dead load and roof-level wind at propped ends
    for k, y in cols:
        if k in L.WALL_TRIB and case == 'G':
            wt = max(L.WALL_TRIB[k])
            ridx = min(range(len(ys)), key=lambda i: abs(ys[i] - y))
            f.node_load('r%d' % ridx, Fz=-factor * L.G_WALL * L.wall_height(y) * wt)
    if f.meta['propped'] and case.startswith('W'):
        _, d, cpi_key = case.split('_'); cpi = L.CPI[cpi_key]; dd = 'S' if d == 'S0' else d
        cp = L.wall_cp(dd, 'S', cpi)
        Hw = L.wall_height(20.07)
        f.node_load('r0', Fx=factor * horiz_scale * cp * L.QP * L.POST_TRIB[fname] * Hw / 2)
        if case == 'G':
            f.node_load('r0', Fz=-factor * L.G_WALL * Hw * L.POST_TRIB[fname] / 2)


COMBOS = {
    'ULS1+': [('G', 1.35), ('Q', 1.5)], 'ULS1-': [('G', 1.35), ('Q', 1.5)],
    'ULS2_N': [('G', 1.35), ('W_N_m', 1.5)], 'ULS2_S': [('G', 1.35), ('W_S_m', 1.5)],
    'ULS2_S0': [('G', 1.35), ('W_S0_m', 1.5)], 'ULS2_R': [('G', 1.35), ('W_R_m', 1.5)],
    'ULS3_N': [('Gmin', 1.0), ('W_N_p', 1.5)], 'ULS3_S': [('Gmin', 1.0), ('W_S_p', 1.5)],
    'ULS3_R': [('Gmin', 1.0), ('W_R_p', 1.5)],
    'SLS_D': [('G', 1.0), ('Q', 1.0)], 'SLS_Q': [('Q', 1.0)], 'SLS_G': [('G', 1.0)],
    'SLS_WN': [('G', 1.0), ('W_N_m', 1.0)], 'SLS_WS': [('G', 1.0), ('W_S0_m', 1.0)],
    'SLS_WNp': [('Gmin', 1.0), ('W_N_p', 1.0)], 'SLS_WR': [('G', 1.0), ('W_R_m', 1.0)],
}
EHF_SIGN = {'ULS1+': +1, 'ULS1-': -1, 'ULS2_N': -1, 'ULS2_S': +1, 'ULS2_S0': +1, 'ULS2_R': +1,
            'ULS3_N': -1, 'ULS3_S': +1, 'ULS3_R': +1}


def run_combo(f, combo):
    """Two-pass: (1) loads -> reactions, alpha_cr; (2) add EHF, amplify sway if alpha_cr < 10."""
    f.clear_loads()
    for case, fac in COMBOS[combo]:
        apply_case(f, case, fac)
    f.solve(10)
    alpha = f.alpha_cr() if combo.startswith('ULS') else None
    if not combo.startswith('ULS'):
        return snapshot(f, combo, None, 1.0, {})
    Vcol = {k: max(f.reactions['%s_0' % k][1], 0.0) for k, _ in f.meta['cols']}
    hmean = np.mean([L.TOS(y) for _, y in f.meta['cols']])
    phi = L.ehf_phi(hmean, len(f.meta['cols']))
    amp = 1.0 / (1 - 1 / alpha) if alpha < 10 else 1.0
    f.clear_loads()
    for case, fac in COMBOS[combo]:
        apply_case(f, case, fac, horiz_scale=amp)
    ys = f.meta['ys']
    ehf = {}
    for k, y in f.meta['cols']:
        ridx = min(range(len(ys)), key=lambda i: abs(ys[i] - y))
        ehf[k] = EHF_SIGN[combo] * phi * Vcol[k] * amp
        f.node_load('r%d' % ridx, Fx=ehf[k])
    f.solve(10)
    return snapshot(f, combo, alpha, amp, ehf)


def snapshot(f, combo, alpha, amp, ehf):
    ys = f.meta['ys']
    disp = {n: f.displacement(n).copy() for n in f.nodes}
    return dict(combo=combo, alpha_cr=alpha, amp=amp, ehf=ehf,
                results=[dict(r) for r in f.results],
                members=[dict(name=m['name'], i=m['i'], j=m['j'], tag=m['tag'], A=m['A'], I=m['I']) for m in f.members],
                reactions={n: v.copy() for n, v in f.reactions.items()},
                disp=disp, nodes=dict(f.nodes))


def hv_alpha_cr(f, combo):
    """Cross-check: simplified alpha_cr = (H/V)(h/delta) with a 1 kN horizontal load per column top."""
    f.clear_loads()
    for case, fac in COMBOS[combo]:
        apply_case(f, case, fac)
    f.solve(4)
    V = sum(max(f.reactions['%s_0' % k][1], 0) for k, _ in f.meta['cols'])
    hcol = {k: L.TOS(y) - sec(f.meta['rafter'])['h'] / 2000 for k, y in f.meta['cols']}
    h = sum(hcol[k] * max(f.reactions['%s_0' % k][1], 0) for k, _ in f.meta['cols']) / V
    f.clear_loads()
    ys = f.meta['ys']
    for k, y in f.meta['cols']:
        ridx = min(range(len(ys)), key=lambda i: abs(ys[i] - y))
        f.node_load('r%d' % ridx, Fx=1.0)
    f.solve(2)
    H = len(f.meta['cols'])
    d = np.mean([f.displacement('r%d' % min(range(len(ys)), key=lambda i: abs(ys[i] - y)))[0] for k, y in f.meta['cols']])
    return H / V * h / d


def run_all(verbose=True):
    out = {}
    for fname in L.FRAMES:
        props = ['spring', 'pin'] if L.FRAMES[fname].get('propped') else ['none']
        for prop in props:
            f = build_frame(fname, prop)
            key = fname if prop == 'none' else '%s_%s' % (fname, prop)
            res = {c: run_combo(f, c) for c in COMBOS}
            res['_meta'] = dict(f.meta); res['_meta']['prop'] = prop
            res['_meta']['alpha_HV'] = hv_alpha_cr(f, 'ULS1+')
            out[key] = res
            if verbose:
                a = min(res[c]['alpha_cr'] for c in COMBOS if c.startswith('ULS'))
                Mmax = max(np.abs(r['M']).max() for r in res['ULS1+']['results'])
                print('%-10s rafter %s cols %s  alpha_cr(min ULS) %.1f  alpha_HV %.1f  |M|max ULS1 %.1f kNm' %
                      (key, f.meta['rafter'], ','.join(sorted(set(f.meta['colsec'].values()))), a,
                       res['_meta']['alpha_HV'], Mmax))
    pickle.dump(out, open(os.path.join(HERE, 'results_frames.pkl'), 'wb'))
    return out


def plot_frames(out):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(7, 1, figsize=(13, 26))
    for ax, fname in zip(axes, L.FRAMES):
        key = fname if not L.FRAMES[fname].get('propped') else fname + '_spring'
        res = out[key]; meta = res['_meta']
        for combo, col, lab in (('ULS1+', 'tab:red', 'ULS-1 1.35G+1.5Q (+EHF)'), ('ULS3_N', 'tab:blue', 'ULS-3 G_min+1.5W (N, cpi+0.2)')):
            r = res[combo]; nodes = r['nodes']
            for m, mr in zip(r['members'], r['results']):
                xi, zi = nodes[m['i']]; xj, zj = nodes[m['j']]
                Lm = mr['L']; c, s = (xj - xi) / Lm, (zj - zi) / Lm
                sc = 0.012   # m per kNm
                xs = xi + mr['x'] * c; zs = zi + mr['x'] * s
                # plot M on the tension side: for a horizontal member sagging (M>0) -> below
                px = xs + mr['M'] * sc * s; pz = zs - mr['M'] * sc * c
                ax.fill(np.r_[xs, px[::-1]], np.r_[zs, pz[::-1]], color=col, alpha=0.25, lw=0)
                ax.plot(px, pz, color=col, lw=0.8)
            # peak annotations
            allM = [(abs(v), v, nodes[m['i']], mr, m) for m, mr in zip(r['members'], r['results']) for v in (mr['M'].max(), mr['M'].min())]
            allM.sort(key=lambda t: -t[0])
            ann = []
            for a, v, (xi, zi), mr, m in allM:
                if all(abs(xi - q) > 1.5 for q in ann) and a > 5:
                    ax.text(xi, zi + (0.55 if combo == 'ULS1+' else -0.55), '%.0f' % v, color=col, fontsize=7, ha='center')
                    ann.append(xi)
                if len(ann) >= 6: break
        nodes = res['ULS1+']['nodes']
        for m in res['ULS1+']['members']:
            xi, zi = nodes[m['i']]; xj, zj = nodes[m['j']]
            ax.plot([xi, xj], [zi, zj], 'k-', lw=3 if m['tag'][-1] == 'haunch' else 1.5)
        for k, y in meta['cols']:
            ax.plot(y, 0, 'ko', ms=6, mfc='w'); ax.text(y, -0.55, k, ha='center', fontsize=8)
            ax.text(y + 0.15, 1.2, meta['colsec'][k], rotation=90, fontsize=7)
        if meta['propped']:
            ax.plot(meta['y0'], nodes['r0'][1], '^', color='tab:green', ms=9, mfc='w')
            ax.text(meta['y0'], nodes['r0'][1] + 0.5, 'pin on\ngirder', color='tab:green', fontsize=7, ha='center')
        a1 = res['ULS1+']['alpha_cr']; a3 = min(res[c]['alpha_cr'] for c in res if c.startswith('ULS'))
        ax.set_title('%s (x = %.2f): rafter %s, haunches %.1f m  |  alpha_cr ULS-1 = %.1f (min all ULS %.1f), EHF+amplified sway  '
                     '(red: ULS-1, blue: ULS-3 wind N; kNm)' % (fname, L.FRAMES[fname]['x'], meta['rafter'], meta['Lh'], a1, a3), fontsize=9)
        ax.set_xlim(14.5, 37); ax.set_ylim(-1.2, 7.0); ax.set_aspect('equal'); ax.grid(alpha=0.3)
        ax.set_xlabel('y (m)  south <-  -> north'); ax.set_ylabel('z (m)')
    fig.suptitle('Alternative A - portal frames: bending moment diagrams (ULS-1 red, ULS-3 uplift blue), sections per design_report_A.md', fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.99))
    fig.savefig(os.path.join(OUT, 'frames_A.png'), dpi=110)


if __name__ == '__main__':
    out = run_all()
    plot_frames(out)
    print('girder spring at F5: %.0f kN/m, F6: %.0f kN/m' % (girder_spring(87.2), girder_spring(92.5)))
