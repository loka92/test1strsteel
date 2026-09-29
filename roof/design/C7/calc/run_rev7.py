"""Design Rev 7 (reduced roofed area). Writes members_C7.csv, reactions_C7.csv, framing_C7.png, view3d_C7.png and
summary_C7.json (input to write_report_rev7.py).  Run: python3 run_rev7.py   (SENS=tag: sensitivity run, summary only)"""
import csv, json, os, math
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import *
from model import NORTH_JOG_X, WIND_POSTS, UNUSED, COLS_ALL, SLAB_ENV, SLAB_NOTCH, SLAB_OPEN, SCHEME, TOS0
from bracing import ECON
from connections import KEYPAIR
from loads import *
from sections import sec, Nb_Rd, Mb_Rd
import members, bracing, connections, struts_rev7
from bracing import DIAG, ROD

OUT = os.path.join(HERE, '..'); SENS = os.environ.get('SENS', '')
o = members.run()
res, beams, cols, cases, base_env, bays, Fr, pur, seis, H4 = o['res'], o['beams'], o['cols'], o['cases'], o['base_env'], o['bays'], o['Fr'], o['purlins'], o['seis'], o['H4']
SP, SR, SC = res['sections']['prim'], res['sections']['raft'], res['sections']['col']
BAYC = {b['id']: b['c'] for b in BAYS}

# ---------------- bracing
bay_env = {}
for b in BAYS:
    i = b['id']; H = max(bays[d][i]['H'] for d in 'NSEW'); dmax = max((bays[d][i]['H'], d) for d in 'NSEW')[1]
    bf = bays[dmax][i]; chk = bracing.check_diagonal(bf['T']); g = connections.gusset_bolts(bf['T'])
    sway = max(bays[d][i]['sway'] for d in 'NSEW')/1.5 + 2.0
    Hs = max(H4['x'][i], H4['y'][i])
    if Hs > H:
        w_, h_, Ld_, _, _ = bay_geom(b); bf = dict(H=Hs, T=Hs*Ld_/w_, N=Hs*h_/w_, w=w_, h=h_, Ld=Ld_, sway=Hs/bracing.bay_stiffness()[i]*1000)
        chk = bracing.check_diagonal(bf['T']); g = connections.gusset_bolts(bf['T']); dmax = 'seismic'; H = Hs
    bay_env[i] = dict(H=H, T=bf['T'], N=bf['N'], w=bf['w'], h=bf['h'], Ld=bf['Ld'], dir=dmax, util=chk['util'], util_bolt=max(g.values()),
                      NtRd=chk['NtRd'], sway=sway, sway_lim=bf['h']*1000/150, H4=Hs, wind=max(bays[d][i]['H'] for d in 'NSEW'))
H_uls_max = {i: bay_env[i]['H'] for i in bay_env}
trusses = bracing.roof_truss_forces(H_uls_max)
def _maxM(pred): return max([max(abs(sp['M']['G'][0]), abs(sp['M']['G'][1])) for sp in res['spans'] if pred(dict(id=sp['id'], kind=sp['kind'], section=sp['section']))] + [0.0])   # G-only moment (1.0 G + E)
Mact = dict(rafter_chord=_maxM(lambda r: r['id'] in ('R68', 'R72', 'R90', 'R95')), rafter_strut=_maxM(lambda r: r['kind'] == 'raft'),
            primary_chord=_maxM(lambda r: r['id'] in ('P_K8K9', 'P_K9K10', 'P_K10K11', 'P_K11K12', 'P_K12K13', 'P_K13K14')),
            eave=_maxM(lambda r: r['kind'] == 'eave' and r['section'] == SP['name']), R78=_maxM(lambda r: r['id'] == 'R78'), purlin=pur['worst']['gravity'][0])
struts = bracing.strut_checks(seis['Fb_x'], seis['Fb_y'], res['roof_area'], trusses, Mact)   # concurrent gravity moments from this run
# eave strut P_K17K18 (13.7 m, IPE 330): RT-E south reaction carried to B3 in-plane; buckling in the vertical plane over 13.7 m
_E = [r for r in beams if r['kind'] == 'eave' and r['id'] in ('P_K17K18', 'P_K17K30', 'P_K30K18')]   # the y 24.46 eave line east of K17: E-W strut for the RT-E reaction
S33 = sec(_E[0]['section']); N_eave = max(t['V'] for t in trusses if t['id'] == 'RT-E'); Nb_eave = Nb_Rd(S33, max(r['L'] for r in _E), 2.9)[0]
M_eave = max(r['M_Ed'] for r in _E)
struts['eave_strut_y24.46'] = dict(N=N_eave, NbRd=Nb_eave, u=N_eave/Nb_eave + M_eave/S33['Mpl_y'])
# T3 chord (IPE 240, 2.88 m): RT-SW panel shear as axial force
N_t3 = max(t['V'] for t in trusses if t['id'] == 'RT-SW'); struts['T3_chord'] = dict(N=N_t3, NbRd=Nb_Rd(SR, 2.88, 2.88)[0], u=N_t3/Nb_Rd(SR, 2.88, 2.88)[0] + 1.0/SR['Mpl_y'])
split = struts_rev7.line_split(seis['Fb_y'], {i: H4['y'][i] for i in H4['y']})
seg_V = {}
for rr in beams:
    if rr['kind'] == 'raft': seg_V[rr['id']] = max(seg_V.get(rr['id'], 0.0), float(rr['RA']['SLS']), float(rr['RB']['SLS']))
if SCHEME == 'ontop':   # rafter on the primary: the strut / chord force passes through M16 bolts in the rafter bottom flange (tf) into the primary top flange
    fins = struts_rev7.strut_table({i: H4['y'][i] for i in H4['y']}, trusses, seg_V, split, tw=SR['tf'], d=16, d0=18, FvRd=0.6*800*157/1.25/1e3, p1=60, e1=30)
    for v in fins: v['V'] = 0.0   # the vertical reaction is carried in bearing, not by the bolts
else:
    fins = struts_rev7.strut_table({i: H4['y'][i] for i in H4['y']}, trusses, seg_V, split, tw=SR['tw'])
drift_eq = struts_rev7.drift_check(trusses, bay_env)
wind_roof = {d: Fr[d][0] for d in 'NSEW'}
drift = {t['id']: t['delta']/1.5 + max(bay_env[i]['sway'] for i in bay_env) for t in trusses if t['id'] in ('RT-E', 'RT-W')}

# ---------------- connections
Vfin = max(max(r['RA']['ULS1'], r['RB']['ULS1'], -min(r['RA'][c] for c in r['RA']), -min(r['RB'][c] for c in r['RB'])) for r in beams if r['kind'] == 'raft')
fin2 = connections.fin_plate(Vfin, 2, SR['tw']) if SCHEME == 'nested' else dict(umax=Vfin/((SP['b'] + 2*SR['tf'] + 2*12)*SR['tw']*275/1e3), gov='rafter web crippling over the primary flange (EN 1993-1-5 6.2, l_y = b_f,prim + 2 t_f + 2 r)')
Nt_cap_roof = max(-(res['colloads'][c]['Gmin'] + 1.5*min(res['colloads'][c]['W_'+d] for d in 'NSEW')) for c in COLS)
Vh_cap = max(max(t['chord'] for t in trusses), max(bay_env[i]['H'] for i in bay_env))
cap = connections.cap_plate(Nt_cap_roof, Vh_cap, tf_beam=SP['tf'], tw_beam=SP['tw'], col_h=SC['h'], col_b=SC['b'])
R = connections.anchor_resistances()
post_N = max(t['post'] for t in trusses); NbR_raft = Nb_Rd(SR, 7.56, 3.07)[0]
ft = res['wall_trib']
N_st2 = 1.5*1.3*QP*wall_h(26.37)*[t for t in ft['K15'] if t[0] == 'W'][0][1]/2; Nb_st2 = Nb_Rd(SR, 4.10, 4.10)[0]
# wind posts WP2, WP3 (S2 face, y 24.36) and WP4 (S1 face, y 21.66): uniaxial, HEA 140, base = centred 60 mm key (c1 250), shear only
wp = {}
for pid, fid in WIND_POSTS.items():
    f = next(ff for ff in FACES if ff['id'] == fid); trib = [t for t in ft[pid] if t[0] == fid][0][1]
    Lp = wall_h(POSTS[pid][1]) - 0.34
    cp = max(abs(wall_cp_net('y-', d, min(abs(POSTS[pid][0] - f['a']), abs(POSTS[pid][0] - f['b']))))*QP_DIR[d] for d in 'NSEW')   # kN/m2 envelope
    w = cp*trib; My = 1.5*w*Lp**2/8; V = 1.5*w*Lp/2
    wp[pid] = dict(L=Lp, trib=trib, q=cp, w=w, My=My, MbRd=Mb_Rd(SC, Lp)[0], u=My/Mb_Rd(SC, Lp)[0], V=V, u_base=V/R['VRd_B_edge250'], face=fid)

# ---------------- members CSV
rows = []
def krow(**k): rows.append(k)
for r in beams:
    krow(id=r['id'] + '/' + r['span'], type={'raft': 'rafter', 'prim': 'primary', 'eave': 'eave beam', 'trim': 'trimmer/chord'}[r['kind']],
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
for pid, v in wp.items():
    krow(id=pid, type='wind post', section=SC['name'], length=round(v['L'], 2), frm='slab', to='eave', N_Ed=0, M_Ed=round(v['My'], 1), V_Ed=round(v['V'], 1),
         u_M='', u_V='', u_LTB_g='', u_LTB_up=round(v['u'], 2), u_defl='', utilisation=round(max(v['u'], v['u_base']), 2), governing='6.3.2 LTB / base key %.2f' % v['u_base'], verdict='OK' if max(v['u'], v['u_base']) <= 1 else 'NO')
krow(id='ST2', type='roof truss post', section=SR['name'], length=4.10, frm='K15', to='R72', N_Ed=round(N_st2, 1), M_Ed=0, V_Ed='', u_M='', u_V='',
     u_LTB_g=round(N_st2/Nb_st2, 2), u_LTB_up='', u_defl='', utilisation=round(N_st2/Nb_st2, 2), governing='6.3.1', verdict='OK')
for i, b in bay_env.items():
    krow(id=i, type='wall X-brace', section=DIAG['name'], length=round(b['Ld'], 2), frm=BAYC[i][0], to=BAYC[i][1], N_Ed=round(b['T'], 1), M_Ed=0, V_Ed='',
         u_M='', u_V='', u_LTB_g='', u_LTB_up='', u_defl=round(b['sway']/b['sway_lim'], 2), utilisation=round(max(b['util'], b['util_bolt']), 2),
         governing=('6.2.3 net section' if b['util'] >= b['util_bolt'] else 'gusset bolts') + ' (%s)' % b['dir'], verdict='OK' if max(b['util'], b['util_bolt']) <= 1 else 'NO')
for t in trusses:
    krow(id=t['id'], type='roof X-brace', section=ROD['name'], length=round(t['Ld'], 2), frm='', to='', N_Ed=round(t['T'], 1), M_Ed=0, V_Ed='',
         u_M='', u_V='', u_LTB_g='', u_LTB_up='', u_defl='', utilisation=round(t['util'], 2), governing='rod tension (seismic)', verdict='OK' if t['util'] <= 1 else 'NO')
for k, v in struts.items():
    krow(id='strut ' + k, type='diaphragm strut/chord', section={'purlin': 'Z200x2.0', 'rafter_chord': SR['name'], 'rafter_strut': SR['name'], 'R78_strut': SR['name'], 'T3_chord': SR['name'], 'eave_strut_y24.46': _E[0]['section']}.get(k, SP['name']), length='', frm='', to='', N_Ed=round(v['N'], 1), M_Ed='', V_Ed='',
         u_M='', u_V='', u_LTB_g='', u_LTB_up='', u_defl='', utilisation=round(v['u'], 2), governing='N + M interaction', verdict='OK' if v['u'] <= 1 else 'NO')
for v in fins:
    krow(id='fin ' + v['member'], type='strut/chord fin plates', section='%s on %s web' % (v['bolts'], SR['name']), length='', frm=v['where'], to='', N_Ed=round(v['N'], 1), M_Ed='', V_Ed=round(v['V'], 1),
         u_M='', u_V=round(v['u_bolt'], 2), u_LTB_g='', u_LTB_up='', u_defl='', utilisation=round(v['umax'], 2), governing='web bearing %.2f' % v['u_bearing'], verdict='OK' if v['umax'] <= 1 else 'NO')

# ---------------- reactions CSV
rrows = []
for c in COLS:
    ed = edge_distances(*COLS[c])
    for cs in cases[c]:
        Ns = [('N', cs['N'])] + ([('Nt', cs['Nt'])] if 'Nt' in cs else [])
        for tag, N in Ns:
            bc = None
            if 'base' in cs: bc = next((b for n, b in cs['base'] if abs(n - N) < 1e-9), None)
            rrows.append(dict(column=c, x=COLS[c][0], y=COLS[c][1], braced_bays=','.join(bb['id'] for bb in BAYS if c in bb['c']) or '-',
                              case=cs['case'] + ('' if tag == 'N' else ' (uplift side)'), N_kN=round(N, 1), Vx_kN=round(cs['V'][0], 1), Vy_kN=round(cs['V'][1], 1),
                              Vcross_x=round(cs['Vc'][0], 1), Vcross_y=round(cs['Vc'][1], 1), V_total=round(bc['Vt'], 1) if bc else round(math.hypot(*cs['V']), 1),
                              base_util=round(bc['umax'], 2) if bc else '', base_gov=bc['gov'] if bc else '',
                              near_edges=','.join(k for k, v in ed.items() if v < NEAR_EDGE) or '-',
                              base_type='E', keys=('A-pair' if c in KEYPAIR else 'A' + (',B' + ','.join(base_env[c]['keyB']) if base_env[c]['keyB'] else '')),
                              max_anchor_kN=round(bc['Nmax'], 1) if bc else ''))
for pid, v in wp.items():
    rrows.append(dict(column=pid, x=POSTS[pid][0], y=POSTS[pid][1] + (0.28 if v['face'] in ('S1', 'S2') else 0.0), braced_bays='-', case='ULS2 (wind post, shear only, no uplift)', N_kN=round(SC['w']*v['L']*1.35, 1),
                      Vx_kN=0.0, Vy_kN=round(v['V'], 1), Vcross_x=0, Vcross_y=0, V_total=round(v['V'], 1), base_util=round(v['u_base'], 2), base_gov='centred 60 mm key, c1 250 (post 280 mm inboard of the face)', near_edges='-y',
                      base_type='post', keys='B (centred)', max_anchor_kN=0))

# ---------------- weight and lengths
L_raft = sum(s['L'] for s in res['spans'] if s['section'] == SR['name']) + sum((r['y1'] - r['sup'][-1][0]) + (r['sup'][0][0] - r['y0']) for r in RAFTERS) + 4.10
L_prim_all = [(s['id'], s['L'], s['section']) for s in res['spans'] if s['kind'] in ('prim', 'eave')]
L_by_sec = {}
for i, L, sc in L_prim_all: L_by_sec[sc] = L_by_sec.get(sc, 0.0) + L
L_p330 = L_by_sec.get('IPE 330', 0.0); L_p300 = sum(L for sc, L in L_by_sec.items() if sc != 'IPE 330')   # 'p300' = primaries in the standard primary section (SP)
L_col_tot = sum(L_col(COLS[c][1], c) for c in COLS); L_wp = sum(v['L'] for v in wp.values())
L_wall_brace = sum(2*bay_env[i]['Ld'] for i in bay_env)
L_roof_brace, n_panels = bracing.roof_bracing_length()
L_purlin = round(res['roof_area']/1.5*1.03)
def girt_rows(Lbay): return 1.5 if Lbay <= 5.3 else (1.2 if Lbay <= 6.0 else 1.0)
L_girt = 0.0
for f in FACES:
    pos = [POSTS[p][1 if f['normal'][0] == 'x' else 0] for p in f['posts']]
    hw = wall_h(f['c'] if f['normal'][0] == 'y' else 0.5*(f['a'] + f['b']))
    for a, bb in zip(pos, pos[1:]): L_girt += (bb - a)*math.ceil(hw/girt_rows(bb - a))
    L_girt += (pos[0] - f['a'] + f['b'] - pos[-1])*math.ceil(hw/1.5)
L_girt = round(L_girt)
W = dict(rafters=L_raft*SR['g'], primaries=sum(L*sec(sc)['g'] for sc, L in L_by_sec.items()), columns=(L_col_tot + L_wp)*SC['g'],
         wall_bracing=L_wall_brace*DIAG['kg'], roof_bracing=L_roof_brace*ROD['kg'])
W['plates_bolts_keys'] = 3270.0*(L_raft + L_p300 + L_p330 + L_col_tot + L_wp)/400.1   # scaled from the Rev 6a BOM (3.27 t on 400 m of hot-rolled members)
W['hot_rolled_total'] = W['rafters'] + W['primaries'] + W['columns'] + W['plates_bolts_keys']
W['purlins_Z200'] = L_purlin*5.9; W['girts_Z200'] = L_girt*5.9
W['total_offer'] = W['hot_rolled_total'] + W['wall_bracing'] + W['roof_bracing'] + W['purlins_Z200']      # girts excluded (wall system open)
W['total_with_girts'] = W['total_offer'] + W['girts_Z200']
W['sections_hot_rolled'] = W['rafters'] + W['primaries'] + W['columns']
lengths = dict(rafters=L_raft, primaries_std=L_p300, primaries_IPE330=L_p330, primaries_by_section=L_by_sec, columns=L_col_tot, wind_posts=L_wp, wall_bracing=L_wall_brace, roof_bracing=L_roof_brace, purlins=L_purlin, girts=L_girt)

# ---------------- clear heights and summary
PT = PRIM_TOP_OFFSET
clear = dict(cap_nuts=TOS(35.77) + PT - SP['h']/1000 - 0.04, south_west_edge=TOS(21.66), south_east_edge=TOS(24.36), north_eave=TOS(35.87), L_K19=L_col(21.76, 'K19'), L_K17=L_col(24.46, 'K17'), L_K6=L_col(35.17, 'K6'), L_K1=L_col(35.77, 'K1'))
thermal = o['thermal']
beam_top = [dict(id=x['id'], span=x['span'], section=x['section'], L=x['L'], umax=x['umax'], gov=x['gov'], d=x['d'], dlim=x['dlim'], u=x['util'], M=x['M_Ed'], Mpl=x['Mpl']) for x in sorted(beams, key=lambda x: -x['umax'])[:14]]
summary = dict(rev=(('8a' if not wp else '8') if SCHEME == 'ontop' else '7b'), scheme=SCHEME, econ=ECON, TOS0=TOS0, Mact=Mact, sections=dict(prim=SP['name'], raft=SR['name'], col=SC['name'], brace=DIAG['name'], rod=ROD['name'], spans=SPAN_SECTION), beam_top=beam_top,
               roof_area=res['roof_area'], wind_roof=wind_roof, seismic=seis, H4=H4, bays=bay_env, trusses=trusses, drift=drift,
               fin2=fin2, Vfin=Vfin, cap=cap, Nt_cap=Nt_cap_roof, Vh_cap=Vh_cap,
               base_env={c: dict(Nc=e['Nc'], Nt=e['Nt'], Vt=e['Vt'], umax=e['umax'], keyB=e['keyB'], Nmax=e['Nmax'], uten=e['uten'], ukey=e['ukey'], uplate=e['uplate'], pair=(c in KEYPAIR)) for c, e in base_env.items()},
               purlins=dict(Mg=pur['worst']['gravity'][0], Mg_where=pur['worst']['gravity'][1], Mu=pur['worst']['uplift'][0], Mu_where=pur['worst']['uplift'][1], Lmax=pur['Lmax'], d=pur['d'], dlim=pur['dlim']),
               post=dict(N=post_N, NbRd=NbR_raft), st2=dict(N=N_st2, Nb=Nb_st2), wp=wp, weight=W, lengths=lengths, n_roof_panels=n_panels, clear=clear, thermal=thermal,
               struts=struts, split=split, fins=fins, drift_eq=drift_eq, unused_columns=UNUSED,
               bay_gov={i: dict(wind=bay_env[i]['wind'], seis=bay_env[i]['H4'], gov=('seismic' if bay_env[i]['H4'] > bay_env[i]['wind'] else 'wind')) for i in bay_env},
               colsum={t: float(sum(v[t] for v in res['colloads'].values())) for t in ('G', 'Gmin', 'Q', 'W_N', 'W_S', 'W_E', 'W_W', 'W_D')},
               max_util=dict(beams=max(r['umax'] for r in beams), cols=max(r['umax'] for r in cols), bases=max(e['umax'][0] for e in base_env.values()), bays=max(max(b['util'], b['util_bolt']) for b in bay_env.values()), rods=max(t['util'] for t in trusses), wp=max([max(v['u'], v['u_base']) for v in wp.values()] + [0.0]), struts=max(v['u'] for v in struts.values()), fins=max(v['umax'] for v in fins)),
               colloads=res['colloads'], cols={r['id']: dict(NbRd=r['NbRd'], N_Ed=r['N_Ed'], L=r['L'], umax=r['umax'], My=r['My'], Mz=r['Mz'], case=r['case'], util=r['util'], bays=r['bays']) for r in cols},
               env=dict(QP_SCALE=os.environ.get('QP_SCALE', '1.0'), E_ZONE=os.environ.get('E_ZONE', '18.0'), G_WALL_SEIS=os.environ.get('G_WALL_SEIS', '0.30')))
def conv(x):
    if isinstance(x, dict): return {str(k): conv(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [conv(v) for v in x]
    if isinstance(x, (np.floating, np.integer)): return float(x)
    return x
json.dump(conv(summary), open(os.path.join(HERE, 'summary_C7%s.json' % ('_' + SENS if SENS else '')), 'w'), indent=1)
print('SENS=%s area %.1f' % (SENS, res['roof_area']), 'max util', {k: round(v, 2) for k, v in summary['max_util'].items()})
print('weight kg', {k: round(v) for k, v in W.items()}); print('lengths', {k: (round(v, 1) if not isinstance(v, dict) else {a: round(b, 1) for a, b in v.items()}) for k, v in lengths.items()})
print('bays', {i: (round(b['H'], 1), round(b['T'], 1), round(b['N'], 1), round(b['util'], 2), b['dir']) for i, b in bay_env.items()})
print('trusses', [(t['id'], round(t['V'], 1), round(t['T'], 1), round(t['util'], 2), round(t['delta'], 1)) for t in trusses])
print('seismic W %.1f Fb %.1f' % (seis['W'], seis['Fb_x']), 'wind roof', {d: round(v, 1) for d, v in wind_roof.items()})
print('wp', {k: (round(v['My'], 1), round(v['u'], 2), round(v['V'], 1), round(v['u_base'], 2)) for k, v in wp.items()}, 'ST2 %.2f' % (N_st2/Nb_st2), 'fin2 %.2f cap %.2f' % (fin2['umax'], cap['umax']))
print('worst bases', [(c, round(base_env[c]['umax'][0], 2), base_env[c]['umax'][2][:30]) for c in sorted(base_env, key=lambda c: -base_env[c]['umax'][0])[:5]])
if SENS: raise SystemExit
with open(os.path.join(OUT, 'members_C7.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(OUT, 'reactions_C7.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rrows[0].keys())); w.writeheader(); w.writerows(rrows)

# ---------------- framing plan
fig, ax = plt.subplots(figsize=(14, 10.5))
cmap = plt.get_cmap('RdYlGn_r'); norm = plt.Normalize(0, 1)
E, N = SLAB_ENV, SLAB_NOTCH
ax.plot([E['x0'], NORTH_JOG_X, NORTH_JOG_X, E['x1'], E['x1'], N['x0'], N['x0'], E['x0'], E['x0']], [35.37, 35.37, E['y1'], E['y1'], N['y1'], N['y1'], E['y0'], E['y0'], 35.37], color='0.6', lw=0.8, ls=':', label='existing slab edge')
ax.plot([ENV['x0'], NORTH_JOG_X, NORTH_JOG_X, ENV['x1'], ENV['x1'], NOTCH['x0'], NOTCH['x0'], ENV['x0'], ENV['x0']], [35.37, 35.37, ENV['y1'], ENV['y1'], NOTCH['y1'], NOTCH['y1'], ENV['y0'], ENV['y0'], 35.37], 'k--', lw=1.0, label='roof edge Rev 7')
for k, op in SLAB_OPEN.items():
    ax.add_patch(plt.Rectangle((op['x0'], op['y0']), op['x1'] - op['x0'], op['y1'] - op['y0'], fc='0.92', ec='k', hatch='//', lw=0.6))
    ax.text(0.5*(op['x0'] + op['x1']), 0.5*(op['y0'] + op['y1']), k + ('\nopening' if k == 'STAIR' else '\nlight well\n(outside roof)'), ha='center', va='center', fontsize=7.5)
ax.text(72.9, 18.0, 'open terrace\n(existing slab, not roofed)', ha='center', fontsize=8, color='0.4'); ax.text(88.5, 22.2, 'open terrace with skylight (not roofed)', ha='center', fontsize=8, color='0.4')
for r in beams:
    if r['axis'] == 'y':
        x = next(rr['x'] for rr in RAFTERS if rr['id'] == r['id']); ax.plot([x, x], [r['a'], r['b']], color=cmap(norm(r['umax'])), lw=2.5)
        ax.text(x + 0.12, 0.5*(r['a'] + r['b']), '%.2f' % r['umax'], fontsize=6.5, rotation=90, va='center', color='0.2')
    else:
        y = next(pp['y'] for pp in PRIMARIES if pp['id'] == r['id']); ax.plot([r['a'], r['b']], [y, y], color=cmap(norm(r['umax'])), lw=4 if r['kind'] in ('prim', 'eave') else 2.5)
        ax.text(0.5*(r['a'] + r['b']), y + 0.15, '%s %.2f' % (r['section'] if r['section'] != SP['name'] else '', r['umax']), fontsize=6.5, ha='center', color='0.2')
ax.plot([67.99, 72.09], [26.37, 26.37], color=cmap(norm(N_st2/Nb_st2)), lw=2.5); ax.text(70.0, 26.52, 'ST2 %.2f' % (N_st2/Nb_st2), fontsize=6.5, ha='center', color='0.2')
for c, (x, y) in COLS.items():
    u = next(r['umax'] for r in cols if r['id'] == c); ub = base_env[c]['umax'][0]
    ax.add_patch(plt.Rectangle((x - 0.2, y - 0.2), 0.4, 0.4, fc=cmap(norm(u)), ec='k', lw=0.8, zorder=5))
    ax.text(x + 0.25, y - 0.45, '%s %.2f / base %.2f' % (c, u, ub), fontsize=6, color='darkred')
for c in UNUSED:
    x, y = COLS_ALL[c]; ax.add_patch(plt.Rectangle((x - 0.2, y - 0.2), 0.4, 0.4, fc='w', ec='0.5', lw=0.6, zorder=4)); ax.text(x + 0.25, y - 0.45, c + ' (no steel column)', fontsize=5.5, color='0.4')
for pid, v in wp.items():
    ax.plot(*POSTS[pid], 's', ms=6, mfc='w', mec='k'); ax.text(POSTS[pid][0] + 0.2, POSTS[pid][1] - 0.5, '%s %.2f' % (pid, max(v['u'], v['u_base'])), fontsize=6, color='darkred')
for b in BAYS:
    (x1, y1), (x2, y2) = COLS[b['c'][0]], COLS[b['c'][1]]
    ax.plot([x1, x2], [y1, y2], color='red', lw=6, alpha=0.35, solid_capstyle='butt')
    ax.text(0.5*(x1 + x2) + (0.35 if b['dir'] == 'y' else 0), 0.5*(y1 + y2) + (0.45 if b['dir'] == 'x' else 0), '%s %.2f' % (b['id'], bay_env[b['id']]['util']), color='red', fontsize=8, ha='center', fontweight='bold', rotation=0 if b['dir'] == 'x' else 90)
for t in bracing.ROOF_TRUSSES:
    for (x0, x1, y0, y1) in t['panels']:
        ax.plot([x0, x1], [y0, y1], 'g--', lw=0.7, alpha=0.7); ax.plot([x0, x1], [y1, y0], 'g--', lw=0.7, alpha=0.7)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm); sm.set_array([]); cb = plt.colorbar(sm, ax=ax, fraction=0.03, pad=0.01); cb.set_label('utilisation (governing check)')
ax.set_aspect('equal'); ax.set_xlim(66.5, 99.0); ax.set_ylim(14, 37.5); ax.set_xlabel('x (m)'); ax.set_ylabel('y (m)'); ax.grid(alpha=0.25); ax.legend(loc='lower right', fontsize=7)
ax.set_title('Design C Rev %s - reduced roofed area (%.0f m2), %s - framing plan coloured by utilisation\n%s primaries%s, %s rafters, %s columns %s; red = wall X-bracing B1, B2, B3, B5, B6, B7 (%s); green dashed = roof %s, %d panels\ncolumn label = member / base utilisation; roof plane TOS = %.2f + 0.06 (35.87 - y), falling north to the gutter' % (('8a' if not wp else '8') if SCHEME == 'ontop' else '7b', res['roof_area'], 'continuous rafters on the primaries' if SCHEME == 'ontop' else 'light section set', SP['name'], (' (%s: IPE 330)' % ', '.join(SPAN_SECTION)) if SPAN_SECTION else '', SR['name'], SC['name'], ('K1-K20 + K28-K30' if not wp else 'K1-K20 + wind posts WP2-WP4'), DIAG['name'], ROD['name'], n_panels, TOS0), fontsize=8.6)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'framing_C7.png'), dpi=150); plt.close(fig)

# ---------------- 3D view (wireframe, for the offer)
from mpl_toolkits.mplot3d import Axes3D  # noqa
fig = plt.figure(figsize=(14, 9)); ax = fig.add_subplot(111, projection='3d')
def seg(p, q, **kw): ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], **kw)
# existing slab outline + unused columns
ax.plot([E['x0'], NORTH_JOG_X, NORTH_JOG_X, E['x1'], E['x1'], N['x0'], N['x0'], E['x0'], E['x0']], [35.37, 35.37, E['y1'], E['y1'], N['y1'], N['y1'], E['y0'], E['y0'], 35.37], [0]*9, color='0.55', lw=1.0)
for k, op in SLAB_OPEN.items(): ax.plot([op['x0'], op['x1'], op['x1'], op['x0'], op['x0']], [op['y0'], op['y0'], op['y1'], op['y1'], op['y0']], [0]*5, color='0.55', lw=0.6)
for c in UNUSED: ax.plot([COLS_ALL[c][0]], [COLS_ALL[c][1]], [0], 's', color='0.6', ms=4)
for c, (x, y) in COLS.items(): seg((x, y, 0), (x, y, L_col(y, c)), color='#1f3a5f', lw=2.2)
for pid, v in wp.items(): seg((POSTS[pid][0], POSTS[pid][1], 0), (POSTS[pid][0], POSTS[pid][1], v['L']), color='#1f3a5f', lw=1.4, ls='--')
for p in PRIMARIES:
    z = TOS(p['y']) + PT - (0.165 if SPAN_SECTION.get(p['id']) == 'IPE 330' else (SR['h']/2000 if p['kind'] == 'trim' else SP['h']/2000)) - (SR['h']/1000 if (SCHEME == 'ontop' and p['kind'] == 'trim') else 0)
    seg((p['x0'], p['y'], z), (p['x1'], p['y'], z), color='#c0392b', lw=2.6 if p['kind'] != 'trim' else 1.6)
for r in RAFTERS: seg((r['x'], r['y0'], TOS(r['y0']) - SR['h']/2000), (r['x'], r['y1'], TOS(r['y1']) - SR['h']/2000), color='#1e8449', lw=1.8)
seg((67.99, 26.37, TOS(26.37) - 0.12), (72.09, 26.37, TOS(26.37) - 0.12), color='#1e8449', lw=1.6)
for yy in np.arange(35.87 - 0.3, 21.66, -1.5):
    xs = [x for x in np.arange(ENV['x0'], ENV['x1'] + 0.01, 0.25) if roofed(min(x, ENV['x1'] - 0.01), yy)]
    runs = []
    for x in xs:
        if runs and x - runs[-1][1] <= 0.26: runs[-1][1] = x
        else: runs.append([x, x])
    for a, b in runs:
        if b - a > 0.5: seg((a, yy, TOS(yy) + 0.1), (b, yy, TOS(yy) + 0.1), color='0.6', lw=0.5)
for b in BAYS:
    (x1, y1), (x2, y2) = COLS[b['c'][0]], COLS[b['c'][1]]
    for (p, q) in (((x1, y1, 0.05), (x2, y2, L_col(y2, b['c'][1]))), ((x2, y2, 0.05), (x1, y1, L_col(y1, b['c'][0])))): seg(p, q, color='#8e44ad', lw=1.3)
for t in bracing.ROOF_TRUSSES:
    for (x0, x1, y0, y1) in t['panels']:
        seg((x0, y0, TOS(y0)), (x1, y1, TOS(y1)), color='#d68910', lw=1.0); seg((x0, y1, TOS(y1)), (x1, y0, TOS(y0)), color='#d68910', lw=1.0)
ax.set_box_aspect((27.8, 20.3, 6)); ax.view_init(elev=32, azim=-128)
ax.set_xlim(67.5, 96); ax.set_ylim(15.5, 36); ax.set_zlim(0, 6); ax.set_axis_off()
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0], [0], color='#1f3a5f', lw=2.2, label='%s columns %s' % (SC['name'], 'K1-K20, K28-K30' if not wp else 'K1-K20 (dashed: wind posts WP2-WP4)')), Line2D([0], [0], color='#c0392b', lw=2.6, label='%s primaries / eave beams%s' % (SP['name'], (' (%s IPE 330)' % ', '.join(SPAN_SECTION)) if SPAN_SECTION else '')),
                   Line2D([0], [0], color='#1e8449', lw=1.8, label='%s rafters, T3, ST2 (6 %% slope, falling north)' % SR['name']), Line2D([0], [0], color='0.6', lw=0.5, label='Z200 purlins @ 1.5 m'),
                   Line2D([0], [0], color='#8e44ad', lw=1.3, label='%s wall X-bracing, 6 bays' % DIAG['name']), Line2D([0], [0], color='#d68910', lw=1.0, label='%s roof rods, 12 panels' % ROD['name']), Line2D([0], [0], color='0.55', lw=1.0, label='existing slab edge, wells, unused columns')],
          loc='lower left', fontsize=8, frameon=False)
ax.set_title('Steel roof, design Rev %s - reduced roofed area (%.0f m2): view from the south-west, roof panels hidden' % (('8a' if not wp else '8') if SCHEME == 'ontop' else '7b', res['roof_area']), fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'view3d_C7.png'), dpi=150); plt.close(fig)
print('written members_C7.csv, reactions_C7.csv, framing_C7.png, view3d_C7.png, summary_C7.json')
