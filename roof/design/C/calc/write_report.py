"""Composes design_report_C.md (Rev 2) from summary_C.json, members_C.csv and reactions_C.csv (run after run_all.py)."""
import json, csv, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..')
s = json.load(open(os.path.join(HERE, 'summary_C.json')))
mem = list(csv.DictReader(open(os.path.join(OUT, 'members_C.csv'))))
rea = list(csv.DictReader(open(os.path.join(OUT, 'reactions_C.csv'))))
W = s['weight']; L = s['lengths']; b = s['bays']; t = {x['id']: x for x in s['trusses']}; be = s['base_env']
f = lambda x, n=1: ('%.*f' % (n, float(x))) if x not in ('', None) else '-'
BAYC = {'B1': 'K1-K2', 'B2': 'K5-K7', 'B3': 'K22-K23', 'B4': 'K25-K26', 'B5': 'K15-K19', 'B6': 'K14-K18', 'B7': 'K20-K27', 'B8': 'K10-K16', 'B9': 'K18-K23', 'B10': 'K19-K25'}
TDESC = {'RT-N-W': 'N band west, chords y 29.3 / 35.2', 'RT-N-E': 'N band east, chords y 29.3 / 35.7', 'RT-S-E': 'S band east', 'RT-S-W': 'S band west', 'RT-W': 'west edge, chords R68 / R72 (rods over two bays)', 'RT-E': 'east edge, chords R90 / R95 (rods over two bays)', 'RT-JOG': 'jog panel x 77.8-81.9 / y 24.5-29.3, carries the RT-N-E west reaction to B7 via R78'}

def member_table():
    keep = [m for m in mem if m['type'] in ('rafter', 'primary', 'eave beam', 'trimmer', 'roof truss post')]
    rows = ['| Member (span) | Section | L m | M_Ed kNm | V_Ed kN | 6.2.5 M | 6.2.6 V | 6.3.2 LTB gravity | 6.3.2 LTB uplift | SLS L/200 | Util. | Governs | Verdict |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    n = 0
    for m in sorted(keep, key=lambda m: -float(m['utilisation'])):
        if float(m['utilisation']) < 0.10 and float(m['length']) < 6: n += 1; continue
        rows.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | **%s** | %s | %s |' % (m['id'], m['section'], f(m['length'], 2), m['M_Ed'], m['V_Ed'], m['u_M'], m['u_V'], m['u_LTB_g'], m['u_LTB_up'], m['u_defl'], m['utilisation'], m['governing'], m['verdict']))
    rows.append(('| %d further spans (eave beams, trimmers, short edge-beam spans, ST2) | ' + s['secs']['prim'] + ' / ' + s['secs']['raft'] + ' | 2.7-5.9 | <= 15 | <= 11 | | | | | | <= 0.10 | - | OK |') % n)
    return '\n'.join(rows)

def column_table():
    rows = ['| Column | Section | L m | N_Ed,c kN (case) | N_Ed,t kN (case) | M_y,Ed / M_z,Ed kNm | k_zy (B.2) | 6.3.1 N/N_b,Rd | 6.3.3 | Util. | Verdict |', '|---|---|---|---|---|---|---|---|---|---|---|']
    cols = [m for m in mem if m['type'] == 'column']
    for m in sorted(cols, key=lambda m: -float(m['utilisation']))[:10]:
        e = be[m['id']]; c = s['cols'][m['id']]
        rows.append('| %s | %s | %s | %s (%s) | %s (%s) | %s | %s | %s | %s | **%s** | %s |' % (m['id'], m['section'], f(m['length'], 2), f(e['Nc'][0]), e['Nc'][1], f(max(e['Nt'][0], 0)), e['Nt'][1], m['M_Ed'], f(c['kzy'], 2), m['u_LTB_g'], m['u_LTB_up'], m['utilisation'], m['verdict']))
    rest = sorted(cols, key=lambda m: -float(m['utilisation']))[10:]
    rows.append('| other %d columns | %s | %s-%s | <= %s | <= %s | <= %s | 0.97-1.00 | <= %s | <= %s | <= %s | OK |' % (len(rest), s['secs']['col'], f(min(float(m['length']) for m in rest), 2), f(max(float(m['length']) for m in rest), 2), f(max(be[m['id']]['Nc'][0] for m in rest), 0), f(max(max(be[m['id']]['Nt'][0], 0) for m in rest), 0), f(max(max(float(v) for v in str(m['M_Ed']).split('/')) for m in rest), 0), f(max(float(m['u_LTB_g']) for m in rest), 2), f(max(float(m['u_LTB_up']) for m in rest), 2), f(max(float(m['utilisation']) for m in rest), 2)))
    return '\n'.join(rows)

def reaction_table():
    rows = ['| Col | Type | Bays | Near edges | Keys | N_c max kN (case) | N_t max kN (case) | V max kN (case) | N_c SLS | N_t SLS | Base governs | Util. | Min. zone |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for c, e in be.items():
        rc = [r for r in rea if r['column'] == c]
        sls_c = max(float(r['N_kN']) for r in rc if r['case'].startswith('SLS')); sls_t = max(-float(r['N_kN']) for r in rc if r['case'].startswith('SLS'))
        rows.append('| %s | %s | %s | %s | %s | %s (%s) | %s (%s) | %s (%s) | %s | %s | %s | **%s** | %s |' % (
            c, e['btype'], rc[0]['braced_bays'], rc[0]['near_edges'], rc[0]['keys'], f(e['Nc'][0]), e['Nc'][1], f(max(e['Nt'][0], 0)), e['Nt'][1], f(e['Vt'][0]), e['Vt'][1], f(sls_c), f(max(sls_t, 0)), e['umax'][2].split(' (')[0], f(e['umax'][0], 2), (e['zreq'] or '-') if e['btype'] == 'B1' else 'head scanned; slab solid at keys'))
    w = s['wp1']
    rows.append('| WP1 (offset 280 inboard) | post | - | +x,-y | B centred | %s (self weight) | 0 | %s (ULS2 E / S) | - | - | key edge breakout c1 250 | %s | - |' % (f(0.3*w['L']*1.35), f(max(w['V'])), f(max(w['V'])/R['VRd_B_edge250'], 2)))
    return '\n'.join(rows)

def bay_table():
    rows = ['| Bay | Columns | w m | h m | Governing case | H_Ed kN (ULS, governing) | H seismic (1.0 E, amplified) | T_Ed diag. kN | N col. +/- kN | T_Rd L70x7 kN | Util. angle | Util. bolts | Sway SLS mm | h/150 mm |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for k, v in b.items():
        rows.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (k, BAYC[k], f(v['w'], 2), f(v['h'], 2), v['dir'], f(v['H']), f(v['H4']), f(v['T']), f(v['N']), f(v['NtRd']), f(v['util'], 2), f(v['util_bolt'], 2), f(v['sway']), f(v['sway_lim'])))
    return '\n'.join(rows)

def truss_table():
    rows = ['| Roof truss | Wind | Span m | Depth m | Panels | Shear V kN | Diagonal T kN (M24, 203) | Chord kN | Post kN | Util. rod | Truss defl. ULS mm |', '|---|---|---|---|---|---|---|---|---|---|---|']
    desc = TDESC
    for k, v in t.items():
        rows.append('| %s (%s) | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (k, desc[k], 'N-S' if k not in ('RT-W', 'RT-E') else 'E-W', f(v['L']), f(v['D']), v.get('npanels', 1), f(v['V']), f(v['T']), f(v['chord']), f(v.get('post', v['V'])), f(v['util'], 2), f(v['delta'])))
    return '\n'.join(rows)

def weight_table():
    rows = ['| Item | Section | Length m | Weight t |', '|---|---|---|---|']
    for k, sec_, ln in (('Rafters / edge beams / trimmers / posts ST1-ST2', s['secs']['raft'], 'rafters'), ('Primaries / eave beams', s['secs']['prim'], 'primaries'), ('Columns (27) + wind post WP1', s['secs']['col'], 'columns')):
        rows.append('| %s | %s | %s | %s |' % (k, sec_, f(L[ln]), f(W[ln]/1000, 2)))
    rows.append('| Plates, stiffeners, keys, bolts (BOM take-off) | S275 / S355 keys | - | %s |' % f(W['plates_bolts_keys']/1000, 2))
    rows.append('| **Hot-rolled total** | | | **%s** |' % f(W['hot_rolled_total']/1000, 1))
    rows.append('| Wall bracing, 10 bays x 2 diagonals | L 70x7 | %s | %s |' % (f(L['wall_bracing']), f(W['wall_bracing']/1000, 2)))
    rows.append('| Roof bracing, %d panels x 2 diagonals | M24 rods 8.8 | %s | %s |' % (s['n_roof_panels'], f(L['roof_bracing']), f(W['roof_bracing']/1000, 2)))
    rows.append('| Purlins %s m + girts %s m (BOM lengths) | Z 200x2.0 S350GD | %s | %s |' % (f(L['purlins'], 0), f(L['girts'], 0), f(L['purlins'] + L['girts'], 0), f(W['purlins_girts_Z200']/1000, 2)))
    rows.append('| Calculation take-off | | | %s |' % f(W['total']/1000, 1))
    rows.append('| **BOM total (S06, for cost)** | | | **%s t** (%s kg/m2 of footprint 486 m2, %s kg/m2 of roofed %s m2) |' % (f(W['BOM_total']/1000, 1), f(W['BOM_total']/486, 0), f(W['BOM_total']/float(s['roof_area']), 0), f(s['roof_area'], 0)))
    return '\n'.join(rows)

cap, fin2, fin3, R, pu, seis, wr = s['cap'], s['fin2'], s['fin3'], s['R'], s['purlins'], s['seismic'], s['wind_roof']
worst = max(be, key=lambda c: be[c]['umax'][0]); wb = be[worst]
kw = dict(member_table=member_table(), column_table=column_table(), reaction_table=reaction_table(), bay_table=bay_table(), truss_table=truss_table(), weight_table=weight_table(),
          Vfin=f(s['Vfin']), Vfin_long=f(s['Vfin_long']), fin2=f(fin2['umax'], 2), fin3=f(fin3['umax'], 2),
          fin2_bs=f(fin2['util']['bolt shear'], 2), fin2_bp=f(fin2['util']['bearing plate'], 2), fin2_ps=f(fin2['util']['plate shear'], 2), fin2_pb=f(fin2['util']['plate bending'], 2), fin2_w=f(fin2['util']['weld'], 2), fin2_bt=f(fin2['util']['web block tearing'], 2),
          Nt_cap=f(s['Nt_cap']), Vh_cap=f(s['Vh_cap']), cap_bt=f(cap['util']['bolt tension'], 2), cap_bi=f(cap['util']['bolt interaction'], 2), cap_ts=f(cap['util']['beam flange T-stub'], 2), cap_w=f(cap['util']['weld'], 2),
          NRd_c=f(R['NRd_c']), NRd_p=f(R['NRd_p']), NRd_g=f(R['NRd_g']), VRd_A=f(R['VRd_A']), VRd_B=f(R['VRd_B_edge250']), Aeff=f(R['Aeff']/100, 0), ratio_c=f(R['ratio_c'], 2), N0c=f(R['N0c']), N0p=f(R['N0p']),
          nkeyB=sum(1 for e in be.values() if e['keyB']), nb1=sum(1 for e in be.values() if e['btype'] == 'B1'), nb2=sum(1 for e in be.values() if e['btype'] == 'B2'), b1list=', '.join(c for c, e in be.items() if e['btype'] == 'B1'), b2list=', '.join(c for c, e in be.items() if e['btype'] == 'B2'), nE=sum(1 for e in be.values() if e['btype'] == 'E'), Elist=', '.join(c for c, e in be.items() if e['btype'] == 'E'), VRd_A_e=f(R['VRd_A_edge255']), z750=', '.join(c for c, e in be.items() if e['zreq'] == 750), z700=', '.join(c for c, e in be.items() if e['zreq'] == 700),
          K19u=f(be['K19']['umax'][0], 2), K23u=f(be['K23']['umax'][0], 2), K22u=f(be['K22']['umax'][0], 2), K16u=f(be['K16']['umax'][0], 2), K12u=f(be['K12']['umax'][0], 2),
          worst=worst, wb_u=f(wb['umax'][0], 2), wb_gov=wb['umax'][2], wb_case=wb['umax'][1], Ntmax=f(max(e['Nt'][0] for e in be.values())), Ntmax_col=max(be, key=lambda c: be[c]['Nt'][0]),
          Vmax=f(max(e['Vt'][0] for e in be.values())), Vmax_col=max(be, key=lambda c: be[c]['Vt'][0]),
          Mg=f(pu['Mg']), Mu=f(pu['Mu']), Lp=f(pu['Lmax'], 2), dp=f(pu['d']), dplim=f(pu['dlim']), Mu_where='x %.1f-%.1f, y %.1f' % tuple(pu['Mu_where'][:3]),
          seisW=f(seis['W'], 0), Fb=f(seis['Fb']), wN=f(wr['N']), wS=f(wr['S']), wE=f(wr['E']), wW=f(wr['W']), wEW_comp='', roofc=f(s['roof_comp'][0]), roofx=f(s['roof_comp'][1]), roofy=f(s['roof_comp'][2]),
          wS_uls=f(1.5*wr['S']), wE_uls=f(1.5*wr['E']), H4max=f(max(s['H4']['x'].values())), H4maxy=f(max(s['H4']['y'].values())),
          roof_area=f(s['roof_area']), Wtot=f(W['total']/1000, 1), Whot=f(W['hot_rolled_total']/1000, 1), n_panels=s['n_roof_panels'],
          maxbeam=f(s['max_util']['beams'], 2), maxcol=f(s['max_util']['cols'], 2), maxbase=f(s['max_util']['bases'], 2), postN=f(s['post']['N']), postNb=f(s['post']['NbRd'], 0),
          st1=f(s['st']['N1']), st1b=f(s['st']['Nb1'], 0), st2=f(s['st']['N2']), st2b=f(s['st']['Nb2'], 0),
          wpL=f(s['wp1']['L'], 2), wpMy=f(s['wp1']['My']), wpMz=f(s['wp1']['Mz']), wpu=f(s['wp1']['u'], 2), wpV=f(max(s['wp1']['V'])),
          driftE=f(s['drift']['RT-E']), driftW=f(s['drift']['RT-W']), K12=s['colloads']['K12'], K19=s['colloads']['K19'],
          sumWN=f(s['colsum']['W_N'], 0), SaX=f(s['seismic']['two_mass']['x']['Sa'], 2), SaY=f(s['seismic']['two_mass']['y']['Sa'], 2), FbX=f(s['seismic']['Fb_x'], 0), FbY=f(s['seismic']['Fb_y'], 0), TaX=f(s['seismic']['two_mass']['x']['Ta'], 2), TaY=f(s['seismic']['two_mass']['y']['Ta'], 2), kX=f(s['seismic']['two_mass']['x']['k'], 0), T1X=f(s['seismic']['two_mass']['x']['T1'], 2),
          B3s=f(s['bay_gov']['B3']['seis']), B3w=f(s['bay_gov']['B3']['wind']), MK19=f(next(m['M_Ed'] for m in mem if m['id'].startswith('P_K19K20'))), dK19=f(s['thermal']['keff']*0 + float(next(m['u_defl'] for m in mem if m['id'].startswith('P_K19K20')))*9790/200, 1), LK19=f(200/float(next(m['u_defl'] for m in mem if m['id'].startswith('P_K19K20'))), 0),
          uten_max=f(max(e['uten'] for e in be.values()), 2), K19t=f(be['K19']['uten'], 2), K23t=f(be['K23']['uten'], 2), K12t=f(be['K12']['uten'], 2), ukey_max=f(max(e['ukey'] for e in be.values()), 2), ukey_col=max(be, key=lambda c: be[c]['ukey']),
          udiag_max=f(max(v['util'] for v in b.values()), 2), udiag_bay=max(b, key=lambda k: b[k]['util']), ubolt_max=f(max(v['util_bolt'] for v in b.values()), 2),
          Lrod=f(L['roof_bracing'], 0), Wbr=f((W['roof_bracing'] + W['wall_bracing'])/1000, 2), urod=f(max(x['util'] for x in s['trusses']), 2), Wsave=f((2.26e3 - W['roof_bracing'] - W['wall_bracing'])/1000, 2), Wbom5=f((W['BOM_total'] - (2.26e3 - W['roof_bracing'] - W['wall_bracing']))/1000, 1),
          Npurlin=f(s['struts']['purlin']['N']), upurlin=f(s['struts']['purlin']['u'], 2), Nchord=f(s['struts']['rafter_chord']['N']), uchord_r=f(s['struts']['rafter_chord']['u'], 2), Nchordp=f(s['struts']['primary_chord']['N']), uchord=f(s['struts']['primary_chord']['u'], 2), Neave=f(s['struts']['eave_strut']['N']), ueave=f(s['struts']['eave_strut']['u'], 2), Nraftstrut=f(s['struts']['rafter_strut']['N']), uraftstrut=f(s['struts']['rafter_strut']['u'], 2), NR78=f(s['struts']['R78_strut']['N']), uR78=f(s['struts']['R78_strut']['u'], 2),
          NR68=f(s['split']['R68']), NR82=f(s['split']['R82']), NR95=f(s['split']['R95']), ufin_max=f(max(v['umax'] for v in s['fins']), 2), ufin_mem=max(s['fins'], key=lambda v: v['umax'])['member'],
          uR78f=f(next(v['umax'] for v in s['fins'] if v['member'] == 'R78'), 2), uR82f=f(next(v['umax'] for v in s['fins'] if v['member'] == 'R82'), 2), NR68f=f(next(v['N'] for v in s['fins'] if v['member'] == 'R68')), NR95f=f(next(v['N'] for v in s['fins'] if v['member'] == 'R95')),
          drW=f(s['drift_eq']['west wall (RT-W + B4/B2)']['dr_nu']), drWl=f(s['drift_eq']['west wall (RT-W + B4/B2)']['lim']), drE=f(s['drift_eq']['east wall (RT-E + B3/B1)']['dr_nu']), drEl=f(s['drift_eq']['east wall (RT-E + B3/B1)']['lim']), dr778=f(s['drift_eq']['x 77.8 line (jog + R78 + B7)']['dr_nu']), dr778l=f(s['drift_eq']['x 77.8 line (jog + R78 + B7)']['lim']),
          sNWa=f(s['split']['actual']['RT_N_W'][0]), sNWb=f(s['split']['actual']['RT_N_W'][1]), sJ=f(s['split']['actual']['RT_JOG']), sNEa=f(s['split']['actual']['RT_N_E'][0]), sNEb=f(s['split']['actual']['RT_N_E'][1]),
          SP=s['secs']['prim'], SR=s['secs']['raft'], SC=s['secs']['col'], twR=f(s['secs']['tw_raft']), tfP=f(s['secs']['tf_prim']),
          MplR=f(next(x['Mpl'] for x in s['beam_top'] if x['section'] == s['secs']['raft']), 0), MplP=f(next(x['Mpl'] for x in s['beam_top'] if x['section'] == s['secs']['prim']), 0),
          B19u=f(next(x['umax'] for x in s['beam_top'] if x['id'] == 'P_K19K20'), 2), K19gov=next(x['gov'] for x in s['beam_top'] if x['id'] == 'P_K19K20'), K19ltb=f(next(x['u']['LTBg'] for x in s['beam_top'] if x['id'] == 'P_K19K20'), 2),
          K19d=f(next(x['d'] for x in s['beam_top'] if x['id'] == 'P_K19K20')), K19dc=next(x['dcase'] for x in s['beam_top'] if x['id'] == 'P_K19K20'), K19L=f(9790/next(x['d'] for x in s['beam_top'] if x['id'] == 'P_K19K20'), 0), K19M=f(next(x['M'] for x in s['beam_top'] if x['id'] == 'P_K19K20')),
          R92u=f(max(x['umax'] for x in s['beam_top'] if x['L'] > 9 and x['section'] == s['secs']['raft']), 2), R92gov=max((x for x in s['beam_top'] if x['L'] > 9 and x['section'] == s['secs']['raft']), key=lambda x: x['umax'])['gov'], R92M=f(max(x['u']['M'] for x in s['beam_top'] if x['L'] > 9 and x['section'] == s['secs']['raft']), 2), R92ltb=f(max(x['u']['LTBu'] for x in s['beam_top'] if x['L'] > 9 and x['section'] == s['secs']['raft']), 2),
          R92d=f(max(x['d'] for x in s['beam_top'] if x['L'] > 9 and x['section'] == s['secs']['raft'])), R92L=f(9200/max(x['d'] for x in s['beam_top'] if x['L'] > 9 and x['section'] == s['secs']['raft']), 0), R92dc=max((x for x in s['beam_top'] if x['L'] > 9 and x['section'] == s['secs']['raft']), key=lambda x: x['d'])['dcase'],
          NbMin=f(min(c['NbRd'] for c in s['cols'].values()), 0), NbMax=f(max(c['NbRd'] for c in s['cols'].values()), 0), LcMin=f(min(c['L'] for c in s['cols'].values()), 2), LcMax=f(max(c['L'] for c in s['cols'].values()), 2),
          K25case=s['cols']['K25']['case'], K25My=f(s['cols']['K25']['My']), K25Mz=f(s['cols']['K25']['Mz']), K25N=f(s['cols']['K25']['N_Ed']), K25kzy=f(s['cols']['K25']['kzy'], 2),
          clN=f(s['clear']['cap_nuts'], 2), clP=f(s['clear']['primary_bottom'], 2), clR=f(s['clear']['rafter_N'], 2), clW=f(s['clear']['west_cap_nuts'], 2),
          FbRd2=f(next(x['FbRd'] for x in s['fins'] if x['cols'] == 1)), FbRd4=f(next(x['FbRd'] for x in s['fins'] if x['cols'] == 2)), capCant=f(s['cap']['util']['cap plate cantilever'], 2), tpB=str(int(s['R'].get('tp', 20))) if isinstance(s['R'], dict) and 'tp' in s['R'] else '20',
          Wbom6=f(W['BOM_total']/1000, 1), Wcol=f(W['columns']/1000, 2), Wraf=f(W['rafters']/1000, 2), Wpri=f(W['primaries']/1000, 2), Wplates=f(W['plates_bolts_keys']/1000, 2),
          st1u=f(s['st']['N1']/s['st']['Nb1'], 2), st2u=f(s['st']['N2']/s['st']['Nb2'], 2), uplate_max=f(max(e['uplate'] for e in be.values()), 2),
          Wcost='{:,.0f}'.format(W['BOM_total']/1000*2040), ustrip=f(max([e['umax'][0] for e in be.values() if 'plate strip' in e['umax'][2]] + [0.0]), 2),
          flC=f(s['clear']['flange_clear']*1000), flT=f(s['clear']['flange_clear_tip']*1000), finR=f(s['clear']['fin_margin_raft'], 0), finP=f(s['clear']['fin_margin_prim'], 0),
          LK1=f(s['clear']['L_K1'], 3), LK6=f(s['clear']['L_K6'], 3), LcK19=f(s['clear']['L_K19'], 3), LK25=f(s['clear']['L_K25'], 3), P13sec=next(x['section'] for x in s['beam_top'] if x['id'] == 'P_K19K20'), WP13=f(W['L_p13']*(49.1 - 42.2)/1000, 2),
          R92dq=f(max(x['dq'] for x in s['beam_top'] if x['L'] > 9 and x['section'] == s['secs']['raft'])), R92Lq=f(9200/max(x['dq'] for x in s['beam_top'] if x['L'] > 9 and x['section'] == s['secs']['raft']), 0), K19b=f(be['K19']['umax'][0], 2),
          k_eff=f(s['thermal']['keff'], 1), F_s=f(s['thermal']['F_s'], 0), F_e=f(s['thermal']['F_e'], 0), F_uw=f(s['thermal']['F_uls_wind'], 0), F_ue=f(s['thermal']['F_uls_erect'], 0),
          cleatR=f(s['cleat']['R']), jogT=f(t['RT-JOG']['T']), jogV=f(t['RT-JOG']['V']), Lraft=f(L['rafters'], 0),
          sumG=f(sum(v['G'] for v in s['colloads'].values()), 0), sumQ=f(sum(v['Q'] for v in s['colloads'].values()), 0), sumWS=f(sum(v['W_S'] for v in s['colloads'].values()), 0),
          B8H=f(b['B7']['H']), B8T=f(b['B7']['T']), B8N=f(b['B7']['N']), B3H=f(b['B3']['H']), K25c=f(s['cols']['K25']['umax'], 2), K23c=f(s['cols']['K23']['umax'], 2), K22c=f(s['cols']['K22']['umax'], 2))
report = open(os.path.join(HERE, 'report_text.md')).read().format(**kw)
open(os.path.join(OUT, 'design_report_C.md'), 'w').write(report)
body = [l for l in report.splitlines() if not l.startswith('|')]
print('report written; words excl. tables:', len(' '.join(body).split()))
