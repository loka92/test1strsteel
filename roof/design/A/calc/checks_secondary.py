"""Secondary members, bracing, seismic check-only, steel weight (Alternative A).
Purlins, eaves beams, transfer girder, trimmers, wind posts, roof and wall bracing.
Reads results_checks.pkl (girder prop reactions). Writes results_secondary.pkl.
"""
import os, pickle, math
import numpy as np
from sections import sec, chi, chi_LT, Mcr, curve_z, curve_LT, FY, E
from frame2d import Frame2D
import loads as L

HERE = os.path.dirname(os.path.abspath(__file__))
CHK = pickle.load(open(os.path.join(HERE, 'results_checks.pkl'), 'rb'))
QP = L.QP
rows = []          # member check rows for members_A.csv
notes = {}


def add(idm, typ, section, Lm, frm, to, u, gov, **kw):
    rows.append(dict(id=idm, type=typ, section=section, L=Lm, frm=frm, to=to, u=u, gov=gov, **kw))


def ltb_MRd(s, Lcr_m, C1=1.13):
    Mc = Mcr(s, Lcr_m * 1e3, C1=C1)
    lam = math.sqrt(s['Mpl_y'] / Mc)
    return chi_LT(lam, curve_LT(s)) * s['Mpl_y'], lam


# ------------------------------------------------------------------ 1. purlins Z200x2.0 @ 1.5 m
M_RD_SINGLE, M_RD_SLEEVED, I_PURLIN = 12.5, 16.0, 3.9e6   # basis values (kNm, mm4)
SPANS = {'F1-F2': 4.1, 'F2-F3': 5.7, 'F3-F4': 4.05, 'F4-F5': 5.35, 'F5-F6': 5.3, 'F6-F7': 3.05}
purl = []
for bay, Lp in SPANS.items():
    a = 1.5
    # gravity ULS-1, interior purlin, continuous sleeved: M = wL^2/10 (first interior support)
    w_g = (1.35 * L.G_ROOF + 1.5 * L.Q_ROOF) * a
    M_g = w_g * Lp**2 / 10
    # uplift ULS-3, general zone H (wind N, cpi +0.2): net -(0.8+0.2)*1.3
    w_u = (1.5 * 1.0 * QP - L.G_ROOF_MIN) * a
    M_u = w_u * Lp**2 / 10
    # first purlin from an eave (windward edge F/G strip): 0.45 m of its 1.5 m tributary in the strip
    cpe_edge = 2.3 if bay in ('F1-F2', 'F6-F7') else 1.3   # F at the corners (e/4 = 3 m), G elsewhere
    w_e = (1.5 * ((0.45 * (cpe_edge + 0.2) + 1.05 * 1.0) * QP) - L.G_ROOF_MIN * 1.5)
    M_e = w_e * Lp**2 / 10
    # first purlin along an opening edge (trimmer takes the edge strip itself): treat like the eave case with F
    # single-span end bays (gable bays are the end spans of the sleeved line): use M = wL^2/8 with 12.5
    single = bay in ('F1-F2', 'F6-F7')
    MRd = M_RD_SINGLE if single else M_RD_SLEEVED
    fac = 10 / 8 if single else 1.0
    u = max(M_g, M_u, M_e) * fac / MRd
    d_sls = 5 * (L.G_ROOF + L.Q_ROOF) * a * (Lp * 1e3)**4 / (384 * E * I_PURLIN) * (1 if single else 0.6)
    purl.append(dict(bay=bay, L=Lp, w_g=w_g, M_g=M_g * fac, w_u=w_u, M_u=M_u * fac, M_e=M_e * fac, MRd=MRd, u=u, d=d_sls, dlim=Lp * 1e3 / 150))
    add('purlin %s' % bay, 'purlin', 'Z200x2.0 S350GD', Lp, bay.split('-')[0], bay.split('-')[1], u,
        'uplift edge purlin' if M_e >= max(M_g, M_u) else ('uplift' if M_u > M_g else 'gravity'),
        M=max(M_g, M_u, M_e) * fac, N=0, V=0)

# ------------------------------------------------------------------ 2. eaves beams IPE 200 (N eave and S-W eave)
s200 = sec('IPE200'); s300 = sec('IPE300')
EAVE_SPANS = {'N K6-K5': 4.1, 'N K5-K7': 5.7, 'N K7-K3': 4.1, 'N K3-K1': 5.3, 'N K1-K2': 5.3, 'N K2-K4': 3.05,
              'S K25-K26': 4.0, 'S K26-K24': 2.9, 'S K24-K27': 2.9}
eave = []
strip = 0.75 + 0.15         # half purlin spacing + panel overhang (m)
for name, Le in EAVE_SPANS.items():
    corner = Le <= 4.1
    cpe_edge = (2.3 if corner else 1.3) if name.startswith('N') else (1.7 if corner else 1.2)   # F or G, wind N / S
    w_g = (1.35 * L.G_ROOF + 1.5 * L.Q_ROOF) * strip + 1.35 * 0.2      # + 0.2 kN/m gutter/flashing
    w_u = 1.5 * (cpe_edge + 0.2) * QP * strip - L.G_ROOF_MIN * strip
    M_g = w_g * Le**2 / 8; M_u = w_u * Le**2 / 8
    MRd_top = s200['Mpl_y']                     # gravity: top flange held by the panel/purlin line
    MRd_u, lam_u = ltb_MRd(s200, min(Le, 2.0))    # uplift: bottom flange, eaves ties to the 1st purlin @ <= 2.0 m
    # axial strut force (roof bracing load path along the eave, ULS): 27.5 kN N-W, 18.3 kN S-W, 27.5 kN E
    N_strut = 27.5 if name in ('N K5-K7', 'N K3-K1', 'N K1-K2') else (18.3 if name.startswith('S') else 0)
    lam_z = Le * 1e3 / (s200['iz'] * 10) / (math.pi * math.sqrt(E / FY)); chi_z = chi(lam_z, curve_z(s200))
    NbRd = chi_z * s200['Npl']
    # horizontal (weak axis) from the wall top: girts -> eaves beam, spanning between eaves ties at 2.0 m
    w_h = 1.5 * (L.CPE_WALL_D + 0.3) * QP * L.wall_height(35.87 if name.startswith('N') else 15.57) / 2
    M_z = w_h * 2.0**2 / 8
    u = max(M_g / MRd_top + M_z / s200['Mpl_z'], M_u / MRd_u + N_strut / NbRd + M_z / s200['Mpl_z'])
    eave.append(dict(name=name, L=Le, M_g=M_g, M_u=M_u, MRd_u=MRd_u, N=N_strut, NbRd=NbRd, Mz=M_z, u=u))
    add('eaves beam %s' % name, 'eaves beam', 'IPE200', Le, name.split()[1].split('-')[0], name.split()[1].split('-')[1], u,
        'uplift LTB + strut' if M_u / MRd_u + N_strut / NbRd > M_g / MRd_top else 'gravity', M=max(M_g, M_u), N=N_strut, V=max(w_g, w_u) * Le / 2)

# ------------------------------------------------------------------ 3. transfer eave girder IPE 300 (y = 20.07)
# 3-span continuous: hanger on F3 rafter (77.8) - K21 (81.79) - K22 (88.88) - K23 (95.49); F5 at 87.2, F6 at 92.5
R5 = CHK['reactions']['girder_F5']; R6 = CHK['reactions']['girder_F6']
gird = {}
for case, P5, P6, wq in (('ULS_grav', R5['Nc_ULS'], R6['Nc_ULS'], (1.35 * L.G_ROOF + 1.5 * L.Q_ROOF) * strip + 1.35 * 0.2),
                         ('ULS_uplift', -R5['Nt_ULS'], -R6['Nt_ULS'], -(1.5 * (1.7 + 0.2) * QP * strip - L.G_ROOF_MIN * strip)),
                         ('SLS_grav', R5['Nc_SLS'], R6['Nc_SLS'], (L.G_ROOF + L.Q_ROOF) * strip + 0.2)):
    g = Frame2D()
    xs = [77.8, 81.79, 87.2, 88.88, 92.5, 95.49]
    for i, x in enumerate(xs): g.add_node('n%d' % i, x, 0)
    for i in range(5): g.add_member('g%d' % i, 'n%d' % i, 'n%d' % (i + 1), s300['A_m2'], s300['I_m4'])
    for i in (0, 1, 3, 5): g.support('n%d' % i, i == 1, True, False)
    for i in range(5): g.member_load(i, 0, -wq)
    g.node_load('n2', Fz=-P5); g.node_load('n4', Fz=-P6)
    g.solve(20)
    Mmax = max(r['M'].max() for r in g.results); Mmin = min(r['M'].min() for r in g.results)
    Vmax = max(np.abs(r['V']).max() for r in g.results)
    dmax = max(np.abs(r['v']).max() for r in g.results) * 1e3
    gird[case] = dict(P5=P5, P6=P6, w=wq, Mmax=Mmax, Mmin=Mmin, Vmax=Vmax, d=dmax,
                      R={n: g.reactions[n][1] for n in ('n0', 'n1', 'n3', 'n5')})
MRd_g, lam_g = ltb_MRd(s300, 5.41)            # compression flange restrained at supports and rafter connections
M_g_max = max(abs(gird['ULS_grav']['Mmax']), abs(gird['ULS_grav']['Mmin']), abs(gird['ULS_uplift']['Mmax']), abs(gird['ULS_uplift']['Mmin']))
# weak axis: wall-top wind reaction (girts and K22 post top, 13 kN ULS) carried into the roof plane by eaves ties
# to the first purlin line at <= 2.0 m spacing (one tie at x = 88.88 under the K22 post); girder horizontal span 2.0 m
w_hg = 1.5 * (L.CPE_WALL_D + 0.3) * QP * L.wall_height(20.07) / 2
Mz_g = w_hg * 2.0**2 / 8 + (1.5 * (L.CPE_WALL_D + 0.3) * QP * L.WALL_TRIB['K22'][0] * L.wall_height(20.07) / 2) * 2.0 / 4
u_g = M_g_max / MRd_g + Mz_g / s300['Mpl_z']
gird['check'] = dict(MRd=MRd_g, Mz=Mz_g, u=u_g, dlim=7090 / 200, V=max(gird['ULS_grav']['Vmax'], gird['ULS_uplift']['Vmax']))
add('transfer girder K21-K22-K23 (+hanger to F3)', 'girder', 'IPE300', 17.7, 'F3 rafter', 'K23', u_g, 'LTB (L 5.4 m) + weak-axis wind (eaves ties @ 2 m)',
    M=M_g_max, N=0, V=gird['check']['V'])

# ------------------------------------------------------------------ 4. trimmers IPE 200 at the openings (4.05 m F3-F4)
Lt = 4.05
w_tg = (1.35 * L.G_ROOF + 1.5 * L.Q_ROOF) * 0.75 + 1.35 * (L.UPSTAND + 0.2)
w_tu = 1.5 * 3.3 * 0.75 - L.G_ROOF_MIN * 0.75            # basis: -3.3 kN/m2 at opening edges
M_tg = w_tg * Lt**2 / 8; M_tu = w_tu * Lt**2 / 8
MRd_t, lam_t = ltb_MRd(s200, Lt)
u_t = max(M_tg / s200['Mpl_y'], M_tu / MRd_t)
trim = dict(w_g=w_tg, w_u=w_tu, M_g=M_tg, M_u=M_tu, MRd_u=MRd_t, u=u_t, d=5 * ((L.G_ROOF + L.Q_ROOF) * 0.75 + 0.5) * 4050**4 / (384 * E * s200['Iy'] * 1e4))
for yy in (20.17, 24.16, 29.37, 35.37):
    add('trimmer y=%.2f' % yy, 'trimmer', 'IPE200', Lt, 'F3', 'F4', u_t, 'uplift LTB (L 4.05 m)', M=max(M_tg, M_tu), N=0, V=max(w_tg, w_tu) * Lt / 2)

# ------------------------------------------------------------------ 5. wind posts IPE 200 (notch corner 77.89, 87.2, 92.5) and eave posts K24, K22 HEA 200
posts = []
for name, trib, Hp, sname in (('wind post x=77.89 (notch corner)', 1.95, 4.4, 'IPE200'), ('wind post x=87.2', 3.55, 4.6, 'IPE200'),
                              ('wind post x=92.5', 3.30, 4.6, 'IPE200'), ('eave post K24', 2.90, 4.6, 'HEA200'), ('eave post K22', 2.65, 4.6, 'HEA200')):
    sp = sec(sname)
    w = 1.5 * (L.CPE_WALL_D + 0.3) * QP * trib
    M = w * Hp**2 / 8; V = w * Hp / 2
    d = 5 * (w / 1.5) * (Hp * 1e3)**4 / (384 * E * sp['Iy'] * 1e4)
    # eave posts also carry the eaves beam / girder reaction (compression)
    N = {'eave post K24': 12.0, 'eave post K22': gird['ULS_grav']['R']['n3']}.get(name, 0.0)
    lam_z = Hp * 1e3 / (sp['iz'] * 10) / (math.pi * math.sqrt(E / FY)); chi_z = chi(lam_z, curve_z(sp))
    MRd_p, _ = ltb_MRd(sp, Hp, C1=1.13)
    u = N / (chi_z * sp['Npl']) + M / MRd_p
    posts.append(dict(name=name, sec=sname, trib=trib, H=Hp, w=w, M=M, V=V, N=N, d=d, dlim=Hp * 1e3 / 150, u=u))
    add(name, 'post', sname, Hp, 'slab', 'girder/eave', u, 'wind bending (pinned-pinned)', M=M, N=N, V=V)

# ------------------------------------------------------------------ 6. bracing (E-W wind) and seismic check
Hw_avg = 0.5 * (L.wall_height(15.57) + L.wall_height(35.87))
A_gable = 20.3 * Hw_avg                                    # projected W elevation (E elevation similar incl. notch wall)
F_ew_k = 1.3 * QP * A_gable                                # characteristic total (cpe,D - cpe,E + friction)
F_roof_k = 0.5 * F_ew_k                                    # to roof level (columns span slab - roof)
F_roof_d = 1.5 * F_roof_k
brace = dict(A_gable=A_gable, F_ew_k=F_ew_k, F_roof_k=F_roof_k, F_roof_d=F_roof_d)
# wall bays: two (N) or three (S) bays in series per wing; each side of the wing takes half of the gable load
BAYS = {('K6', 'K5'): (4.10, 'N', 2), ('K5', 'K7'): (5.70, 'N', 2), ('K25', 'K26'): (4.00, 'S', 3), ('K26', 'K24'): (2.90, 'S', 3),
        ('K24', 'K27'): (2.90, 'S', 3), ('K3', 'K1'): (5.30, 'N', 2), ('K1', 'K2'): (5.29, 'N', 2), ('K21', 'K22'): (7.09, 'S', 2),
        ('K22', 'K23'): (6.61, 'S', 2)}
vb = {}
base_brace = {}       # column -> dict(Vx=horizontal at base (ULS), Nv=vertical +-)
for (a, b), (Lb, side, nser) in BAYS.items():
    H = F_roof_d / 2 / nser
    h = L.TOS(35.77 if side == 'N' else (15.87 if a in ('K25', 'K26', 'K24') else 20.07))
    theta = math.atan(h / Lb); Ld = math.hypot(h, Lb)
    T = H / math.cos(theta); Vv = H * math.tan(theta)
    NtRd_rod = 0.9 * 245 * 800 / 1.25 / 1e3          # M20 8.8 threaded rod, F_t,Rd of the basis
    vb['%s-%s' % (a, b)] = dict(L=Lb, h=h, H=H, T=T, Vv=Vv, u=T / NtRd_rod, Ld=Ld)
    for c in (a, b):
        r = base_brace.setdefault(c, dict(Vx=0.0, Nv=0.0))
        r['Vx'] = max(r['Vx'], H); r['Nv'] += Vv * (1 if c == a else -1)
    add('wall bracing %s-%s' % (a, b), 'wall bracing', 'rod M20 8.8 (X)', Ld, a, b, T / NtRd_rod, 'tension rod', N=T, M=0, V=0)
# columns shared by two bays in series: vertical components cancel (one bay lifts, the other pushes down);
# report the net absolute value plus the un-cancelled one where only one bay meets (corner / end columns)
for c, r in base_brace.items():
    n_b = sum(1 for (a, b) in BAYS if c in (a, b))
    single = [(a, b) for (a, b) in BAYS if c in (a, b)]
    r['Nv_abs'] = max(abs(vb['%s-%s' % (a, b)]['Vv']) for (a, b) in single) if n_b == 1 else abs(r['Nv'])
# roof bracing: horizontal truss in the gable bay, depth = frame spacing, panels = rafter bays
s_chs = dict(name='CHS 76.3x3.2', A=735.0, i=25.9, mass=5.75)
NtRd_chs = s_chs['A'] * FY / 1e3
roofb = {}
for name, depth, panels, F in (('W bay 68.0-72.1', 4.1, [5.9, 4.6, 3.0, 5.8], F_roof_d),
                               ('E bay 92.5-95.55', 3.05, [4.4, 4.8, 6.4], F_roof_d),
                               ('E bay 81.85-87.2 (diaphragm tie)', 5.35, [4.4, 4.8, 6.4], 0.5 * F_roof_d),
                               ('mid panel 77.8-81.85 (y 24.2-29.3)', 4.05, [5.2], 0.25 * F_roof_d)):
    Vsh = F / 2                                        # end-panel shear (load spread along the gable, exits at both ends)
    Lp = max(panels); Ld = math.hypot(Lp, depth)
    D = Vsh / (depth / Ld)                             # tension-only diagonal
    chord = F * sum(panels) / 8 / depth
    roofb[name] = dict(depth=depth, Ld=Ld, D=D, chord=chord, u=D / NtRd_chs)
    add('roof bracing %s' % name, 'roof bracing', s_chs['name'], Ld, '-', '-', D / NtRd_chs, 'tension-only diagonal', N=D, M=0, V=0)
# seismic (check only): base shear vs wind
W_seis = (L.G_ROOF + 0.20) * 446 + L.G_WALL * 96.2 * Hw_avg / 2
seis = dict(W=W_seis, Fb_EW=2.5 * 0.10 * 1.2 / 1.5 * W_seis, Fb_NS=2.5 * 0.10 * 1.2 / 4.0 * W_seis,
            wind_EW_k=F_ew_k, wind_NS_k=1.3 * QP * (27.8 * L.wall_height(35.87)))

# ------------------------------------------------------------------ 7. steel weight
cos_s = math.cos(math.atan(0.06))
raf_len = sum((L.FRAMES[f]['y1'] - (20.07 if L.FRAMES[f].get('propped') else L.FRAMES[f]['y0'])) / cos_s for f in L.FRAMES)
n_haunch_sides = 0
for f in L.FRAMES:
    cols = L.FRAMES[f]['cols']
    for i, k in enumerate(cols):
        n_haunch_sides += (1 if i in (0, len(cols) - 1) else 2)
haunch_mass = 0.5 * s300['mass'] / 2 * 1.3          # tapered cutting from half an IPE 300 over 1.3 m (kg per side)
col_len = sum(L.TOS(L.COLS[k][1]) for k in L.COLS)  # 27 columns incl. K24, K22 posts
wt = {
    'rafters IPE 300 (%.0f m)' % raf_len: raf_len * s300['mass'],
    'haunch cuttings (%d)' % n_haunch_sides: n_haunch_sides * haunch_mass,
    'columns HEA 200 (27, %.0f m)' % col_len: col_len * sec('HEA200')['mass'],
    'eaves beams IPE 200 (37.8 m)': 37.8 * s200['mass'],
    'transfer girder IPE 300 (17.7 m)': 17.7 * s300['mass'],
    'trimmers IPE 200 (4 x 4.05 m)': 16.2 * s200['mass'],
    'wind posts IPE 200 (3 x 4.5 m)': 13.5 * s200['mass'],
    'roof bracing CHS 76.3x3.2 (approx. 150 m)': 150 * s_chs['mass'],
    'wall bracing rods M20 (9 bays, approx. 110 m)': 110 * 2.5,
    'eaves ties, fly braces, sag rods (allowance)': 250,
}
primary = sum(wt.values())
wt['end plates, stiffeners, base plates, bolts (+12 %)'] = 0.12 * primary
wt['purlins Z200x2.0 @ 1.5 m (approx. 300 m incl. sleeves)'] = 300 * 6.5
wt['girts Z150x1.5 (perimeter 96 m x 3 rows)'] = 290 * 4.5
total = sum(wt.values())
weight = dict(items=wt, primary=primary * 1.12, total=total, per_m2_footprint=total / 486, per_m2_roofed=total / 446)

pickle.dump(dict(rows=rows, purlins=purl, eaves=eave, girder=gird, trimmer=trim, posts=posts, brace=brace, wall_bays=vb,
                 base_brace=base_brace, roof_bracing=roofb, seismic=seis, weight=weight),
            open(os.path.join(HERE, 'results_secondary.pkl'), 'wb'))

if __name__ == '__main__':
    print('PURLINS'); [print('  %s' % p) for p in purl]
    print('EAVES'); [print('  %s' % e) for e in eave]
    print('GIRDER'); [print('  %s: %s' % (k, v)) for k, v in gird.items()]
    print('TRIMMER', trim)
    print('POSTS'); [print('  %s' % p) for p in posts]
    print('BRACING', brace); [print('  %s: %s' % (k, v)) for k, v in vb.items()]
    print('BASE BRACE'); [print('  %s: %s' % (k, v)) for k, v in base_brace.items()]
    print('ROOF BRACING'); [print('  %s: %s' % (k, v)) for k, v in roofb.items()]
    print('SEISMIC', seis)
    print('WEIGHT'); [print('  %-55s %7.0f kg' % (k, v)) for k, v in wt.items()]
    print('  total %.1f t = %.1f kg/m2 footprint, %.1f kg/m2 roofed; primary %.1f t' % (total / 1e3, weight['per_m2_footprint'], weight['per_m2_roofed'], weight['primary'] / 1e3))
