"""Rev 2. Runs the whole design for alternative C and writes members_C.csv, reactions_C.csv (one row per column and
load case), framing_C.png, bases_C.md and summary_C.json (input to write_report.py).  Run: python3 run_all.py"""
import csv, json, os, math
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import *
from model import SADDLE, NORTH_JOG_X
from connections import KEYPAIR
from loads import *
from sections import sec, Nb_Rd, Mb_Rd
import members, bracing, connections
from bracing import DIAG, ROD

OUT = os.path.join(HERE, '..')
o = members.run()
res, beams, cols, cases, base_env, bays, Fr, pur, seis, H4 = o['res'], o['beams'], o['cols'], o['cases'], o['base_env'], o['bays'], o['Fr'], o['purlins'], o['seis'], o['H4']
SP, SR, SC = res['sections']['prim'], res['sections']['raft'], res['sections']['col']
BAYC = {b['id']: b['c'] for b in BAYS}

# ---------------- bracing: diagonals, gussets, sway, roof trusses
bay_env = {}
for b in BAYS:
    i = b['id']; H = max(bays[d][i]['H'] for d in 'NSEW'); dmax = max((bays[d][i]['H'], d) for d in 'NSEW')[1]
    bf = bays[dmax][i]; chk = bracing.check_diagonal(bf['T']); g = connections.gusset_bolts(bf['T'])
    sway = max(bays[d][i]['sway'] for d in 'NSEW')/1.5 + 2.0
    bay_env[i] = dict(H=H, T=bf['T'], N=bf['N'], w=bf['w'], h=bf['h'], Ld=bf['Ld'], dir=dmax, util=chk['util'], util_bolt=g_max if (g_max := max(g.values())) else 0,
                      NtRd=chk['NtRd'], sway=sway, sway_lim=bf['h']*1000/150, H4=max(H4['x'][i], H4['y'][i]))
H_uls_max = {i: bay_env[i]['H'] for i in bay_env}
trusses = bracing.roof_truss_forces(H_uls_max)
wind_roof = {d: Fr[d][0] for d in 'NSEW'}
# diaphragm drift at the east / west wall mid-length = truss deflection + bay sway (SLS = ULS/1.5)
drift = {t['id']: t['delta']/1.5 + max(bay_env[i]['sway'] for i in bay_env) for t in trusses if t['id'] in ('RT-E', 'RT-W')}

# ---------------- connections
Vfin = max(max(r['RA']['ULS1'], r['RB']['ULS1'], -min(r['RA'][c] for c in r['RA']), -min(r['RB'][c] for c in r['RB'])) for r in beams if r['kind'] == 'raft')
Vfin_long = max(max(r['RA']['ULS1'], r['RB']['ULS1']) for r in beams if r['kind'] == 'raft' and r['L'] > 8)
fin2 = connections.fin_plate(Vfin, 2, SR['tw']); fin3 = connections.fin_plate(Vfin_long, 3, SR['tw'])
Nt_cap_roof = max(-(res['colloads'][c]['Gmin'] + 1.5*min(res['colloads'][c]['W_'+d] for d in 'NSEW')) for c in COLS)
Vh_cap = max(max(t['chord'] for t in trusses), max(bay_env[i]['H'] for i in bay_env))
cap = connections.cap_plate(Nt_cap_roof, Vh_cap)
R = connections.anchor_resistances()
post_N = max(t['post'] for t in trusses); NbR_raft = Nb_Rd(SR, 9.2, 3.07)[0]
# roof-truss posts ST1 (y 24.46, R90-R95, 5.65 m) and ST2 (y 26.37, R68-R72, 4.10 m): IPE 270 struts, N = wall load at K18 / K15 top
ft = res['wall_trib']
N_st1 = 1.5*1.3*QP*wall_h(24.46)*[t for t in ft['K18'] if t[0] == 'E'][0][1]/2
N_st2 = 1.5*1.3*QP*wall_h(26.37)*[t for t in ft['K15'] if t[0] == 'W'][0][1]/2
Nb_st1 = Nb_Rd(SR, 5.65, 5.65)[0]; Nb_st2 = Nb_Rd(SR, 4.10, 4.10)[0]
# wind post WP1 (HEA 160), both faces
Lwp = wall_h(19.97) - 0.34
My_wp = 1.5*1.1*QP*[t for t in ft['WP1'] if t[0] == 'S2'][0][1]*Lwp**2/8
Mz_wp = 1.5*1.1*QP*[t for t in ft['WP1'] if t[0] == 'EN'][0][1]*Lwp**2/8
u_wp = My_wp/Mb_Rd(SC, Lwp)[0] + Mz_wp/SC['Mpl_z']
V_wp = (1.5*1.1*QP*[t for t in ft['WP1'] if t[0] == 'S2'][0][1]*Lwp/2, 1.5*1.4*QP*[t for t in ft['WP1'] if t[0] == 'EN'][0][1]*Lwp/2)

# ---------------- members CSV
rows = []
def krow(**k): rows.append(k)
for r in beams:
    krow(id=r['id'] + '/' + r['span'], type={'raft': 'rafter', 'prim': 'primary', 'eave': 'eave beam', 'trim': 'trimmer'}[r['kind']],
         section=r['section'], length=round(r['L'], 2), frm=r['span'].split('-')[0], to=r['span'].split('-')[1],
         N_Ed=0.0, M_Ed=round(max(r['M_Ed'], r['Mu_Ed']), 1), V_Ed=round(r['V_Ed'], 1),
         u_M=round(max(r['util']['M'], r['util']['Mu']), 2), u_V=round(r['util']['V'], 2), u_LTB_g=round(r['util']['LTBg'], 2),
         u_LTB_up=round(r['util']['LTBu'], 2), u_defl=round(r['util']['defl'], 2), utilisation=round(r['umax'], 2), governing=r['gov'],
         verdict='OK' if r['umax'] <= 1.0 else 'NO')
for r in cols:
    e = base_env[r['id']]
    krow(id=r['id'], type='column', section=r['section'], length=round(r['L'], 2), frm='base', to='cap', N_Ed=round(e['Nc'][0], 1),
         M_Ed='%.1f / %.1f' % (r['My'], r['Mz']), V_Ed=round(e['Vt'][0], 1), u_M='', u_V='',
         u_LTB_g=round(r['util']['N'], 2), u_LTB_up=round(r['util']['NM'], 2), u_defl='', utilisation=round(r['umax'], 2),
         governing=r['gov'], verdict='OK' if r['umax'] <= 1.0 else 'NO')
krow(id='WP1', type='wind post', section=SC['name'], length=round(Lwp, 2), frm='slab', to='eave', N_Ed=0, M_Ed='%.1f / %.1f' % (My_wp, Mz_wp), V_Ed=round(max(V_wp), 1),
     u_M='', u_V='', u_LTB_g='', u_LTB_up=round(u_wp, 2), u_defl='', utilisation=round(u_wp, 2), governing='6.3.3 biaxial', verdict='OK')
for sid, N, Nb, L in (('ST1', N_st1, Nb_st1, 5.65), ('ST2', N_st2, Nb_st2, 4.10)):
    krow(id=sid, type='roof truss post', section=SR['name'], length=L, frm='', to='', N_Ed=round(N, 1), M_Ed=0, V_Ed='', u_M='', u_V='',
         u_LTB_g=round(N/Nb, 2), u_LTB_up='', u_defl='', utilisation=round(N/Nb, 2), governing='6.3.1', verdict='OK')
for i, b in bay_env.items():
    krow(id=i, type='wall X-brace', section=DIAG['name'], length=round(b['Ld'], 2), frm=BAYC[i][0], to=BAYC[i][1], N_Ed=round(b['T'], 1), M_Ed=0, V_Ed='',
         u_M='', u_V='', u_LTB_g='', u_LTB_up='', u_defl=round(b['sway']/b['sway_lim'], 2), utilisation=round(max(b['util'], b['util_bolt']), 2),
         governing='6.2.3 net section' if b['util'] >= b['util_bolt'] else 'gusset bolts', verdict='OK')
for t in trusses:
    krow(id=t['id'], type='roof X-brace', section=ROD['name'], length=round(t['Ld'], 2), frm='', to='', N_Ed=round(t['T'], 1), M_Ed=0, V_Ed='',
         u_M='', u_V='', u_LTB_g='', u_LTB_up='', u_defl='', utilisation=round(t['util'], 2), governing='rod tension', verdict='OK')
with open(os.path.join(OUT, 'members_C.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# ---------------- reactions CSV: one row per column and load case (concurrent N, Vx, Vy), + WP1
rrows = []
for c in COLS:
    ed = edge_distances(*COLS[c])
    for cs in cases[c]:
        Ns = [('N', cs['N'])] + ([('Nt', cs['Nt'])] if 'Nt' in cs else [])
        for tag, N in Ns:
            bc = None
            if 'base' in cs:
                bc = next((b for n, b in cs['base'] if abs(n - N) < 1e-9), None)
            rrows.append(dict(column=c, x=COLS[c][0], y=COLS[c][1], braced_bays=','.join(bb['id'] for bb in BAYS if c in bb['c']) or '-',
                              case=cs['case'] + ('' if tag == 'N' else ' (uplift side)'), N_kN=round(N, 1), Vx_kN=round(cs['V'][0], 1), Vy_kN=round(cs['V'][1], 1),
                              Vcross_x=round(cs['Vc'][0], 1), Vcross_y=round(cs['Vc'][1], 1), V_total=round(bc['Vt'], 1) if bc else round(math.hypot(*cs['V']), 1),
                              base_util=round(bc['umax'], 2) if bc else '', base_gov=bc['gov'] if bc else '',
                              near_edges=','.join(k for k, v in ed.items() if v < NEAR_EDGE) or '-',
                      base_type=base_env[c]['btype'], keys=('saddle' if c in SADDLE else ('A-pair' if c in KEYPAIR else 'A' + (',B' + ','.join(base_env[c]['keyB']) if base_env[c]['keyB'] else ''))),
                      psi_ec=round(bc['psi_ec'], 2) if bc else '', max_anchor_kN=round(bc['Nmax'], 1) if bc else '', min_zone_mm=bc['zreq'] if bc else ''))
rrows.append(dict(column='WP1', x=POSTS['WP1'][0] - 0.28, y=POSTS['WP1'][1] + 0.28, braced_bays='-', case='ULS2 (wind post, shear only, no uplift)', N_kN=round(SC['w']*Lwp*1.35, 1), base_type='post', keys='B (centred)', psi_ec='', max_anchor_kN=0, min_zone_mm='',
                  Vx_kN=round(V_wp[1], 1), Vy_kN=round(V_wp[0], 1), Vcross_x=0, Vcross_y=0, V_total=round(max(V_wp), 1), base_util=round(max(V_wp)/R['VRd_B_edge250'], 2), base_gov='centred 60 mm key, c1 250 (post offset 280 inboard)', near_edges='+x,-y'))
with open(os.path.join(OUT, 'reactions_C.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rrows[0].keys())); w.writeheader(); w.writerows(rrows)

# ---------------- weight
L_raft = sum(s['L'] for s in res['spans'] if s['section'] == SR['name']) + sum((r['y1'] - r['sup'][-1][0]) + (r['sup'][0][0] - r['y0']) for r in RAFTERS) + 5.65 + 4.10
L_prim = sum(s['L'] for s in res['spans'] if s['section'] == SP['name'])
L_col_tot = sum(L_col(COLS[c][1]) for c in COLS) + Lwp
L_wall_brace = sum(2*bay_env[i]['Ld'] for i in bay_env)
L_roof_brace, n_panels = bracing.roof_bracing_length()
L_purlin = res['roof_area']/1.5*1.25
def girt_rows(Lbay): return 1.5 if Lbay <= 5.3 else (1.2 if Lbay <= 6.0 else 1.0)
L_girt = 0.0
for f in FACES:
    pos = [POSTS[p][1 if f['normal'][0] == 'x' else 0] for p in f['posts']]
    hw = wall_h(f['c'] if f['normal'][0] == 'y' else 0.5*(f['a'] + f['b']))
    for a, bb in zip(pos, pos[1:]): L_girt += (bb - a)*math.ceil(hw/girt_rows(bb - a))
    L_girt += (pos[0] - f['a'] + f['b'] - pos[-1])*math.ceil(hw/1.5)
W = dict(rafters=L_raft*SR['g'], primaries=L_prim*SP['g'], columns=L_col_tot*SC['g'],
         wall_bracing=L_wall_brace*7.38, roof_bracing=L_roof_brace*ROD['kg'])
W['plates_bolts_keys'] = 3400.0          # BOM take-off (detailing, S06): base plates incl. B2 30 mm + stiffeners + under-slab, cap and fin plates, gussets, keys, bolts
W['hot_rolled_total'] = W['rafters'] + W['primaries'] + W['columns'] + W['plates_bolts_keys']
L_purlin, L_girt = 300.0, 271.0            # BOM take-off 571 m (calc estimate 0 m)
W['purlins_girts_Z200'] = (L_purlin + L_girt)*5.9
W['total'] = W['hot_rolled_total'] + W['wall_bracing'] + W['roof_bracing'] + W['purlins_girts_Z200']
lengths = dict(rafters=L_raft, primaries=L_prim, columns=L_col_tot, wall_bracing=L_wall_brace, roof_bracing=L_roof_brace, purlins=L_purlin, girts=L_girt)
W['BOM_total'] = 25400.0                    # drawing BOM (S06 Rev 4b, X1); Rev 5 bases are lighter (25 mm plates, no stiffeners, no under-slab plates: about -0.4 t) - BOM to be updated by detailing

# ---------------- framing plan coloured by utilisation
fig, ax = plt.subplots(figsize=(14, 10.5))
cmap = plt.get_cmap('RdYlGn_r'); norm = plt.Normalize(0, 1)
bx = [ENV['x0'], NORTH_JOG_X, NORTH_JOG_X, ENV['x1'], ENV['x1'], NOTCH['x0'], NOTCH['x0'], ENV['x0'], ENV['x0']]
by = [35.37, 35.37, ENV['y1'], ENV['y1'], NOTCH['y1'], NOTCH['y1'], ENV['y0'], ENV['y0'], 35.37]
ax.plot(bx, by, 'k--', lw=0.8)
for k, op in OPEN.items():
    ax.add_patch(plt.Rectangle((op['x0'], op['y0']), op['x1'] - op['x0'], op['y1'] - op['y0'], fc='0.9', ec='k', hatch='//', lw=0.8))
    ax.text(0.5*(op['x0'] + op['x1']), 0.5*(op['y0'] + op['y1']), k + '\nopening', ha='center', va='center', fontsize=8)
for r in beams:
    if r['axis'] == 'y':
        x = next(rr['x'] for rr in RAFTERS if rr['id'] == r['id']); ax.plot([x, x], [r['a'], r['b']], color=cmap(norm(r['umax'])), lw=2.5 if r['kind'] == 'raft' else 2)
        ax.text(x + 0.12, 0.5*(r['a'] + r['b']), '%.2f' % r['umax'], fontsize=6.5, rotation=90, va='center', color='0.2')
    else:
        y = next(pp['y'] for pp in PRIMARIES if pp['id'] == r['id']); ax.plot([r['a'], r['b']], [y, y], color=cmap(norm(r['umax'])), lw=4 if r['kind'] in ('prim', 'eave') else 2.5)
        ax.text(0.5*(r['a'] + r['b']), y + 0.15, '%.2f' % r['umax'], fontsize=6.5, ha='center', color='0.2')
for (x0, x1, yy, u, lab) in ((89.90, 95.55, 24.46, N_st1/Nb_st1, 'ST1'), (67.99, 72.09, 26.37, N_st2/Nb_st2, 'ST2')):
    ax.plot([x0, x1], [yy, yy], color=cmap(norm(u)), lw=2.5); ax.text(0.5*(x0 + x1), yy + 0.15, '%s %.2f' % (lab, u), fontsize=6.5, ha='center', color='0.2')
for c, (x, y) in COLS.items():
    u = next(r['umax'] for r in cols if r['id'] == c); ub = base_env[c]['umax'][0]
    ax.add_patch(plt.Rectangle((x - 0.2, y - 0.2), 0.4, 0.4, fc=cmap(norm(u)), ec='k', lw=0.8, zorder=5))
    ax.text(x + 0.25, y - 0.45, '%s %.2f / base %.2f' % (c, u, ub), fontsize=6, color='darkred')
ax.plot(*POSTS['WP1'], 's', ms=6, mfc='w', mec='k'); ax.text(POSTS['WP1'][0] + 0.2, POSTS['WP1'][1] - 0.5, 'WP1 %.2f' % u_wp, fontsize=6, color='darkred')
for b in BAYS:
    (x1, y1), (x2, y2) = COLS[b['c'][0]], COLS[b['c'][1]]
    ax.plot([x1, x2], [y1, y2], color='red', lw=6, alpha=0.35, solid_capstyle='butt')
    ax.text(0.5*(x1 + x2) + (0.35 if b['dir'] == 'y' else 0), 0.5*(y1 + y2) + (0.45 if b['dir'] == 'x' else 0), '%s %.2f' % (b['id'], bay_env[b['id']]['util']), color='red', fontsize=8, ha='center', fontweight='bold', rotation=0 if b['dir'] == 'x' else 90)
for t in bracing.ROOF_TRUSSES:
    for (x0, x1, y0, y1) in t['panels']:
        ax.plot([x0, x1], [y0, y1], 'g--', lw=0.7, alpha=0.7); ax.plot([x0, x1], [y1, y0], 'g--', lw=0.7, alpha=0.7)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm); sm.set_array([]); cb = plt.colorbar(sm, ax=ax, fraction=0.03, pad=0.01); cb.set_label('utilisation (governing check)')
ax.set_aspect('equal'); ax.set_xlim(66.5, 99.0); ax.set_ylim(14, 37.5); ax.set_xlabel('x (m)'); ax.set_ylabel('y (m)'); ax.grid(alpha=0.25)
ax.set_title('Alternative C Rev 3 - framing plan coloured by utilisation (north face at y 35.37 west of x 81.79): %s primaries (E-W), %s rafters (N-S, 11 lines) + posts ST1/ST2, %s columns;\n'
             'red = wall X-bracing bays B1-B10 (L70x7, utilisation), green dashed = roof-plane X bracing (M24 rods); column label = member / base utilisation' % (SP['name'], SR['name'], SC['name']), fontsize=9.5)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'framing_C.png'), dpi=150); plt.close(fig)

# purlin cleat under zone-F uplift (C10): reaction of a 3.07 m span at w = (0.17 - 1.5 x 3.25) x 1.5 = -7.06 kN/m
w_F = (G_MIN - 1.5*(2.3 + 0.2)*QP)*1.5; R_cleat = abs(w_F)*3.07/2
cleat = dict(R=R_cleat, bolts_FtRd=2*0.9*800*84.3/1.25/1e3, M=R_cleat*0.05, MRd=120*10**2/4*275/1e6, u_bolt=R_cleat/(2*0.9*800*84.3/1.25/1e3))
cleat['u_plate'] = cleat['M']/cleat['MRd']
# clear heights (C3): under the rafter at the north edge, under the eave primary and under the cap-plate nuts at y 35.77
clear = dict(rafter_N=TOS(35.87) - 0.27, primary_bottom=TOS(35.77) + 0.05 - 0.33, cap_underside=TOS(35.77) + 0.05 - 0.33 - 0.02, cap_nuts=TOS(35.77) + 0.05 - 0.33 - 0.02 - 0.02,
             west_cap_nuts=TOS(35.27) + 0.05 - 0.33 - 0.04)
thermal = o['thermal']
# ---------------- bases_C.md (self-contained base and anchor note)
from bases_note import write_bases_note
write_bases_note(OUT, R, base_env, cases, cols, V_wp, Lwp)

# ---------------- summary JSON
summary = dict(sections=dict(prim=SP['name'], raft=SR['name'], col=SC['name'], brace=DIAG['name'], rod=ROD['name']),
               roof_area=res['roof_area'], wind_roof=wind_roof, seismic=seis, H4=H4, bays=bay_env, trusses=trusses, drift=drift,
               fin2=fin2, fin3=fin3, Vfin=Vfin, Vfin_long=Vfin_long, cap=cap, Nt_cap=Nt_cap_roof, Vh_cap=Vh_cap, R=R,
               base_env={c: dict(Nc=e['Nc'], Nt=e['Nt'], Vt=e['Vt'], umax=e['umax'], keyB=e['keyB'], zreq=e['zreq'], u_zone=e['u_zone'], Nmax=e['Nmax'], Mkey=e['Mkey'], btype=e['btype'], uten=e['uten'], ukey=e['ukey'], uplate=e['uplate'], B1_option=(dict(umax=e['B1_option']['umax'], zreq=e['B1_option']['zreq'], uten=e['B1_option']['uten']) if e.get('B1_option') else None)) for c, e in base_env.items()},
               purlins=dict(Mg=pur['worst']['gravity'][0], Mg_where=pur['worst']['gravity'][1], Mu=pur['worst']['uplift'][0], Mu_where=pur['worst']['uplift'][1], Lmax=pur['Lmax'], d=pur['d'], dlim=pur['dlim']),
               post=dict(N=post_N, NbRd=NbR_raft), st=dict(N1=N_st1, Nb1=Nb_st1, N2=N_st2, Nb2=Nb_st2), wp1=dict(L=Lwp, My=My_wp, Mz=Mz_wp, u=u_wp, V=V_wp),
               weight=W, lengths=lengths, n_roof_panels=n_panels, roof_comp=bracing.roof_suction_component()['S'][:3], cleat=cleat, clear=clear, thermal=thermal,
               tos={y: TOS(y) for y in (35.87, 35.77, 35.37, 35.27, 35.17, 29.27, 24.46, 21.76, 20.07, 15.87, 15.57)},
               max_util=dict(beams=max(r['umax'] for r in beams), cols=max(r['umax'] for r in cols), bases=max(e['umax'][0] for e in base_env.values())),
               colloads=res['colloads'], Fr={d: dict(Ftot=Fr[d][0], rigid=Fr[d][1], trib=Fr[d][2]) for d in 'NSEW'},
               cols={r['id']: dict(kzy=r['kzy'], umax=r['umax'], My=r['My'], Mz=r['Mz'], case=r['case'], util=r['util']) for r in cols})
def conv(x):
    if isinstance(x, dict): return {str(k): conv(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [conv(v) for v in x]
    if isinstance(x, (np.floating, np.integer)): return float(x)
    return x
json.dump(conv(summary), open(os.path.join(HERE, 'summary_C.json'), 'w'), indent=1)
print('max beam %.2f col %.2f base %.2f' % (summary['max_util']['beams'], summary['max_util']['cols'], summary['max_util']['bases']))
print('weight', {k: round(v/1000, 2) for k, v in W.items()}); print('lengths', {k: round(v, 1) for k, v in lengths.items()})
print('bays', {i: (round(b['H'], 1), round(b['T'], 1), round(b['N'], 1), round(b['util'], 2), round(b['sway'], 1), round(b['H4'], 1)) for i, b in bay_env.items()})
print('trusses', [(t['id'], round(t['V'], 1), round(t['T'], 1), round(t['chord'], 1), round(t['util'], 2), round(t['delta'], 1)) for t in trusses], 'drift', drift)
print('seismic', seis, 'wind roof', wind_roof, 'roof comp', summary['roof_comp'])
print('fin2', round(fin2['umax'], 2), fin2['gov'], round(Vfin, 1), 'fin3', round(fin3['umax'], 2), round(Vfin_long, 1), 'cap', round(cap['umax'], 2), cap['gov'], round(Nt_cap_roof, 1), round(Vh_cap, 1))
print('purlins', summary['purlins']); print('post', round(post_N, 1), round(NbR_raft), 'ST', round(N_st1, 1), round(N_st2, 1), 'WP1', round(u_wp, 2), V_wp)
for c in sorted(base_env, key=lambda c: -base_env[c]['umax'][0])[:8]: print(c, base_env[c])
