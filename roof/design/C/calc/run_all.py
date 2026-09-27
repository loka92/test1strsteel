"""Runs the whole design for alternative C and writes members_C.csv, reactions_C.csv, framing_C.png and
report_tables.md (tables pasted into design_report_C.md).  Run: python3 run_all.py"""
import csv, json, os, math
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import *
from loads import *
from sections import sec, Nb_Rd, Mb_Rd
import members, bracing, connections
from bracing import DIAG, ROD

OUT = os.path.join(HERE, '..')
o = members.run()
res, beams, cols, reac, bays, Fr, pur = o['res'], o['beams'], o['cols'], o['reac'], o['bays'], o['Fr'], o['purlins']
SP, SR, SC = res['sections']['prim'], res['sections']['raft'], res['sections']['col']

# ---------------- bracing: diagonals, gussets, sway, roof trusses, seismic
bay_env = {}
for b in BAYS:
    i = b['id']; H = max(bays[d][i]['H'] for d in 'NSEW'); dmax = max(d for d in 'NSEW' if bays[d][i]['H'] == H)
    bf = bays[dmax][i]; chk = bracing.check_diagonal(bf['T']); g = connections.gusset_bolts(bf['T'])
    sway = max(bays[d][i]['sway'] for d in 'NSEW')/1.5 + 2.0   # SLS (H/1.5) + 2 mm bolt-slip allowance
    bay_env[i] = dict(H=H, T=bf['T'], N=bf['N'], w=bf['w'], h=bf['h'], Ld=bf['Ld'], dir=dmax, util=chk['util'], util_bolt=max(g.values()),
                      NtRd=chk['NtRd'], sway=sway, sway_lim=bf['h']*1000/150, strut=H)
H_uls_max = {i: bay_env[i]['H'] for i in bay_env}
trusses = bracing.roof_truss_forces(H_uls_max)
steel_prelim = sum(sec(s['section'])['w']*s['L'] for s in res['spans']) + sum(SC['w']*L_col(COLS[c][1]) for c in COLS)
seis = bracing.seismic_check(res['roof_area'], steel_prelim*1.1)
wind_roof = {d: Fr[d][0] for d in 'NSEW'}

# ---------------- connections
Vfin = max(max(r['RA']['ULS1'], r['RB']['ULS1'], -r['RA']['ULS3N'], -r['RB']['ULS3N'], -r['RA']['ULS3S'], -r['RB']['ULS3S'], -r['RA']['ULS3W'], -r['RB']['ULS3W'], -r['RA']['ULS3E'], -r['RB']['ULS3E']) for r in beams if r['kind'] == 'raft')
Vfin_long = max(max(r['RA']['ULS1'], r['RB']['ULS1']) for r in beams if r['kind'] == 'raft' and r['L'] > 8)
fin2 = connections.fin_plate(Vfin, 2, SR['tw']); fin3 = connections.fin_plate(Vfin_long, 3, SR['tw'])
Vprim = max(max(abs(r['RA'][c]) for c in r['RA']) for r in beams if r['kind'] in ('prim', 'eave'))
Nt_cap = max(reac[c]['Nt_ULS'] + (max(bays[d][b['id']]['N'] for d in 'NSEW' for b in BAYS if c in b['c']) if any(c in b['c'] for b in BAYS) else 0) for c in COLS)
# roof uplift only at the cap (bracing vertical enters below the cap through the gusset) -> use the roof-only uplift
Nt_cap_roof = max(-(res['colloads'][c]['Gmin'] + 1.5*min(res['colloads'][c]['W_'+d] for d in 'NSEW')) for c in COLS)
Vh_cap = max(max(t['chord'] for t in trusses), max(bay_env[i]['H'] for i in bay_env))
cap = connections.cap_plate(Nt_cap_roof, Vh_cap)
bases = {}
for c in COLS:
    e = reac[c]
    bases[c] = connections.base_plate(e['Nc_ULS'], e['Nt_ULS'], max(e['Vx_ULS'], e['Vy_ULS']))
worst_base = max(bases, key=lambda c: bases[c]['umax'])
# purlin as strut: not relied on (rafters are the truss posts). Rafter as post: N = V of the truss
post_N = max(t['post'] for t in trusses)
NbR_raft = Nb_Rd(SR, 9.2, 3.07)[0]
# wind post WP1 (HEA 160): both faces
Lwp = wall_h(19.97) - 0.35
ft = res['wall_trib']
My_wp = 1.5*1.1*QP*[t for t in ft['WP1'] if t[0] == 'S2'][0][1]*Lwp**2/8
Mz_wp = 1.5*1.1*QP*[t for t in ft['WP1'] if t[0] == 'EN'][0][1]*Lwp**2/8
u_wp = My_wp/Mb_Rd(SC, Lwp)[0] + Mz_wp/SC['Mpl_z']

# ---------------- members CSV
rows = []
for r in beams:
    rows.append(dict(id=r['id'] + '/' + r['span'], type={'raft': 'rafter', 'prim': 'primary', 'eave': 'eave beam', 'trim': 'trimmer'}[r['kind']],
                     section=r['section'], length=round(r['L'], 2), frm=r['span'].split('-')[0], to=r['span'].split('-')[1],
                     N_Ed=0.0, M_Ed=round(max(r['M_Ed'], r['Mu_Ed']), 1), V_Ed=round(r['V_Ed'], 1),
                     u_M=round(max(r['util']['M'], r['util']['Mu']), 2), u_V=round(r['util']['V'], 2), u_LTB_g=round(r['util']['LTBg'], 2),
                     u_LTB_up=round(r['util']['LTBu'], 2), u_defl=round(r['util']['defl'], 2), utilisation=round(r['umax'], 2), governing=r['gov'],
                     verdict='OK' if r['umax'] <= 1.0 else 'NO'))
for r in cols:
    e = reac[r['id']]
    rows.append(dict(id=r['id'], type='column', section=r['section'], length=round(r['L'], 2), frm='base', to='cap', N_Ed=round(e['Nc_ULS'], 1),
                     M_Ed='%.1f / %.1f' % (r['My'], r['Mz']), V_Ed=round(max(e['Vx_ULS'], e['Vy_ULS']), 1), u_M='', u_V='',
                     u_LTB_g=round(r['util']['N'], 2), u_LTB_up=round(r['util']['NM'], 2), u_defl='', utilisation=round(r['umax'], 2),
                     governing=r['gov'], verdict='OK' if r['umax'] <= 1.0 else 'NO'))
rows.append(dict(id='WP1', type='wind post', section=SC['name'], length=round(Lwp, 2), frm='slab', to='eave', N_Ed=0, M_Ed=round(max(My_wp, Mz_wp), 1), V_Ed='',
                 u_M='', u_V='', u_LTB_g='', u_LTB_up=round(u_wp, 2), u_defl='', utilisation=round(u_wp, 2), governing='6.3.3 biaxial', verdict='OK'))
for i, b in bay_env.items():
    rows.append(dict(id=i, type='wall X-brace', section=DIAG['name'], length=round(b['Ld'], 2), frm=[bb for bb in BAYS if bb['id'] == i][0]['c'][0],
                     to=[bb for bb in BAYS if bb['id'] == i][0]['c'][1], N_Ed=round(b['T'], 1), M_Ed=0, V_Ed='', u_M='', u_V='', u_LTB_g='', u_LTB_up='',
                     u_defl=round(b['sway']/b['sway_lim'], 2), utilisation=round(max(b['util'], b['util_bolt']), 2),
                     governing='6.2.3 net section' if b['util'] >= b['util_bolt'] else 'gusset bolts', verdict='OK'))
for t in trusses:
    rows.append(dict(id=t['id'], type='roof X-brace', section=ROD['name'], length=round(t['Ld'], 2), frm='', to='', N_Ed=round(t['T'], 1), M_Ed=0, V_Ed='',
                     u_M='', u_V='', u_LTB_g='', u_LTB_up='', u_defl='', utilisation=round(t['util'], 2), governing='rod tension', verdict='OK'))
with open(os.path.join(OUT, 'members_C.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# ---------------- reactions CSV
rrows = []
for c in COLS:
    e = reac[c]; b = bases[c]
    rrows.append(dict(column=c, x=COLS[c][0], y=COLS[c][1], braced_bay=','.join(bb['id'] for bb in BAYS if c in bb['c']),
                      N_comp_ULS=round(e['Nc_ULS'], 1), case_comp=e['case_c'], N_uplift_ULS=round(e['Nt_ULS'], 1), case_uplift=e['case_t'],
                      Vx_ULS=round(e['Vx_ULS'], 1), Vy_ULS=round(e['Vy_ULS'], 1), N_comp_SLS=round(e['Nc_SLS'], 1), N_uplift_SLS=round(e['Nt_SLS'], 1),
                      Vx_SLS=round(e['Vx_SLS'], 1), Vy_SLS=round(e['Vy_SLS'], 1),
                      Vwall_x_ULS=round(e.get('Vwall_x', 0), 1), Vwall_y_ULS=round(e.get('Vwall_y', 0), 1),
                      anchor_util=round(b['umax'], 2), anchor_gov=b['gov']))
with open(os.path.join(OUT, 'reactions_C.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rrows[0].keys())); w.writeheader(); w.writerows(rrows)

# ---------------- weight
L_raft = sum(s['L'] for s in res['spans'] if s['section'] == SR['name']) + sum((r['y1'] - r['sup'][-1][0]) + (r['sup'][0][0] - r['y0']) for r in RAFTERS)
L_prim = sum(s['L'] for s in res['spans'] if s['section'] == SP['name'])
L_col_tot = sum(L_col(COLS[c][1]) for c in COLS) + Lwp
L_strut = sum(bay_env[i]['w'] for i in bay_env)
L_wall_brace = sum(2*bay_env[i]['Ld'] for i in bay_env)
L_roof_brace, n_panels = bracing.roof_bracing_length()
L_purlin = res['roof_area']/1.5 + 0.25*res['roof_area']/1.5      # purlins + 25 % for eave/opening extra rows
def girt_rows(Lbay):   # girt row spacing rule from the girt check (report section 4): 1.5 m <= 5.3 m, 1.2 m <= 6.0 m, 1.0 m above
    return 1.5 if Lbay <= 5.3 else (1.2 if Lbay <= 6.0 else 1.0)
L_girt = 0.0
for f in FACES:
    pos = [POSTS[p][1 if f['normal'][0] == 'x' else 0] for p in f['posts']]
    hw = wall_h(f['c'] if f['normal'][0] == 'y' else 0.5*(f['a'] + f['b']))
    for a, bb in zip(pos, pos[1:]): L_girt += (bb - a)*math.ceil(hw/girt_rows(bb - a))
    L_girt += (pos[0] - f['a'] + f['b'] - pos[-1])*math.ceil(hw/1.5)
W = dict(rafters=L_raft*SR['g'], primaries=L_prim*SP['g'], columns=L_col_tot*SC['g'], base_struts=L_strut*SC['g'],
         wall_bracing=L_wall_brace*7.38, roof_bracing=L_roof_brace*ROD['kg'])
W['plates_bolts'] = 0.10*(W['rafters'] + W['primaries'] + W['columns'] + W['base_struts'])
W['hot_rolled_total'] = sum(v for k, v in W.items() if k in ('rafters', 'primaries', 'columns', 'base_struts', 'plates_bolts'))
W['purlins_girts_Z200'] = (L_purlin + L_girt)*5.9
W['total'] = W['hot_rolled_total'] + W['wall_bracing'] + W['roof_bracing'] + W['purlins_girts_Z200']
lengths = dict(rafters=L_raft, primaries=L_prim, columns=L_col_tot, base_struts=L_strut, wall_bracing=L_wall_brace, roof_bracing=L_roof_brace, purlins=L_purlin, girts=L_girt)

# ---------------- framing plan coloured by utilisation
fig, ax = plt.subplots(figsize=(14, 10.5))
cmap = plt.get_cmap('RdYlGn_r'); norm = plt.Normalize(0, 1)
bx = [ENV['x0'], ENV['x1'], ENV['x1'], NOTCH['x0'], NOTCH['x0'], ENV['x0'], ENV['x0']]
by = [ENV['y1'], ENV['y1'], NOTCH['y1'], NOTCH['y1'], ENV['y0'], ENV['y0'], ENV['y1']]
ax.plot(bx, by, 'k--', lw=0.8)
for k, op in OPEN.items():
    ax.add_patch(plt.Rectangle((op['x0'], op['y0']), op['x1'] - op['x0'], op['y1'] - op['y0'], fc='0.9', ec='k', hatch='//', lw=0.8))
    ax.text(0.5*(op['x0'] + op['x1']), 0.5*(op['y0'] + op['y1']), k + '\nopening', ha='center', va='center', fontsize=8)
for r in beams:
    sp = next(s for s in res['spans'] if s['id'] == r['id'] and abs(s['L'] - r['L']) < 1e-6 and s['a'] == r['a'])
    if r['axis'] == 'y':
        x = next(rr['x'] for rr in RAFTERS if rr['id'] == r['id']); ax.plot([x, x], [r['a'], r['b']], color=cmap(norm(r['umax'])), lw=2.5 if r['kind'] == 'raft' else 2)
        ax.text(x + 0.12, 0.5*(r['a'] + r['b']), '%.2f' % r['umax'], fontsize=6.5, rotation=90, va='center', color='0.2')
    else:
        y = next(pp['y'] for pp in PRIMARIES if pp['id'] == r['id']); ax.plot([r['a'], r['b']], [y, y], color=cmap(norm(r['umax'])), lw=4 if r['kind'] in ('prim', 'eave') else 2.5)
        ax.text(0.5*(r['a'] + r['b']), y + 0.15, '%.2f' % r['umax'], fontsize=6.5, ha='center', color='0.2')
for c, (x, y) in COLS.items():
    u = next(r['umax'] for r in cols if r['id'] == c)
    ax.add_patch(plt.Rectangle((x - 0.2, y - 0.2), 0.4, 0.4, fc=cmap(norm(u)), ec='k', lw=0.8, zorder=5))
    ax.text(x + 0.25, y - 0.45, '%s %.2f' % (c, u), fontsize=6.5, color='darkred')
ax.plot(*POSTS['WP1'], 's', ms=6, mfc='w', mec='k'); ax.text(POSTS['WP1'][0] + 0.2, POSTS['WP1'][1] - 0.5, 'WP1', fontsize=6.5, color='darkred')
for b in BAYS:
    (x1, y1), (x2, y2) = COLS[b['c'][0]], COLS[b['c'][1]]
    ax.plot([x1, x2], [y1, y2], color='red', lw=6, alpha=0.35, solid_capstyle='butt')
    ax.text(0.5*(x1 + x2), 0.5*(y1 + y2) + (0.45 if b['dir'] == 'x' else 0), '%s %.2f' % (b['id'], bay_env[b['id']]['util']), color='red', fontsize=8, ha='center', fontweight='bold')
for t in bracing.ROOF_TRUSSES:
    for (x0, x1, y0, y1) in t['panels']:
        ax.plot([x0, x1], [y0, y1], 'g--', lw=0.7, alpha=0.7); ax.plot([x0, x1], [y1, y0], 'g--', lw=0.7, alpha=0.7)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm); sm.set_array([]); cb = plt.colorbar(sm, ax=ax, fraction=0.03, pad=0.01); cb.set_label('utilisation (governing check)')
ax.set_aspect('equal'); ax.set_xlim(66.5, 97.5); ax.set_ylim(14, 37.5); ax.set_xlabel('x (m)'); ax.set_ylabel('y (m)'); ax.grid(alpha=0.25)
ax.set_title('Alternative C - framing plan coloured by utilisation: %s primaries (E-W), %s rafters (N-S, 11 lines), %s columns;\n'
             'red = wall X-bracing bays B1-B8 (L70x7), green dashed = roof-plane X bracing (M20 rods); values = governing utilisation' % (SP['name'], SR['name'], SC['name']), fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'framing_C.png'), dpi=150); plt.close(fig)

# ---------------- summary JSON + markdown tables for the report
summary = dict(sections=dict(prim=SP['name'], raft=SR['name'], col=SC['name'], brace=DIAG['name'], rod=ROD['name']),
               roof_area=res['roof_area'], wind_roof=wind_roof, seismic=seis, bays=bay_env, trusses=trusses,
               fin2=fin2, fin3=fin3, Vfin=Vfin, Vfin_long=Vfin_long, Vprim=Vprim, cap=cap, Nt_cap=Nt_cap_roof, Vh_cap=Vh_cap,
               bases={c: dict(umax=bases[c]['umax'], gov=bases[c]['gov'], util=bases[c]['util']) for c in bases}, worst_base=worst_base,
               base_res=dict(NRd_c=bases[worst_base]['NRd_c'], NRd_p=bases[worst_base]['NRd_p'], VRd_c=bases[worst_base]['VRd_c'], VRd_cp=bases[worst_base]['VRd_cp'], Aeff=bases[worst_base]['Aeff'], ratio_c=bases[worst_base]['ratio_c']),
               purlins=dict(Mg=pur['worst']['gravity'][0], Mg_where=pur['worst']['gravity'][1], Mu=pur['worst']['uplift'][0], Mu_where=pur['worst']['uplift'][1], Lmax=pur['Lmax'], d=pur['d'], dlim=pur['dlim']),
               post=dict(N=post_N, NbRd=NbR_raft), wp1=dict(L=Lwp, My=My_wp, Mz=Mz_wp, u=u_wp),
               weight=W, lengths=lengths, n_roof_panels=n_panels,
               max_util=dict(beams=max(r['umax'] for r in beams), cols=max(r['umax'] for r in cols)),
               colloads=res['colloads'], reac=reac, Fr={d: dict(Ftot=Fr[d][0], rigid=Fr[d][1], trib=Fr[d][2]) for d in 'NSEW'})
def conv(x):
    if isinstance(x, dict): return {str(k): conv(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [conv(v) for v in x]
    if isinstance(x, (np.floating, np.integer)): return float(x)
    return x
json.dump(conv(summary), open(os.path.join(HERE, 'summary_C.json'), 'w'), indent=1)
print('max beam util %.2f, max column util %.2f, worst base %s %.2f (%s)' % (summary['max_util']['beams'], summary['max_util']['cols'], worst_base, bases[worst_base]['umax'], bases[worst_base]['gov']))
print('weight', {k: round(v/1000, 2) for k, v in W.items()})
print('lengths', {k: round(v, 1) for k, v in lengths.items()})
print('bays', {i: (round(b['H'], 1), round(b['T'], 1), round(b['N'], 1), round(b['util'], 2), round(b['sway'], 1)) for i, b in bay_env.items()})
print('trusses', [(t['id'], round(t['V'], 1), round(t['T'], 1), round(t['chord'], 1), round(t['util'], 2)) for t in trusses])
print('seismic', seis, 'wind roof', wind_roof)
print('fin2', fin2['umax'], fin2['gov'], Vfin, 'fin3', fin3['umax'], fin3['gov'], Vfin_long, 'cap', cap['umax'], cap['gov'], Nt_cap_roof, Vh_cap)
print('purlins', summary['purlins']); print('post', post_N, NbR_raft, 'WP1', u_wp)
for c in sorted(bases, key=lambda c: -bases[c]['umax'])[:6]: print(c, round(bases[c]['umax'], 2), bases[c]['gov'], {k: round(v, 2) for k, v in bases[c]['util'].items()})
