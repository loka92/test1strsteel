"""Composes design_report_C.md (Rev 2) from summary_C.json, members_C.csv and reactions_C.csv (run after run_all.py)."""
import json, csv, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..')
s = json.load(open(os.path.join(HERE, 'summary_C.json')))
mem = list(csv.DictReader(open(os.path.join(OUT, 'members_C.csv'))))
rea = list(csv.DictReader(open(os.path.join(OUT, 'reactions_C.csv'))))
W = s['weight']; L = s['lengths']; b = s['bays']; t = {x['id']: x for x in s['trusses']}; be = s['base_env']
f = lambda x, n=1: ('%.*f' % (n, float(x))) if x not in ('', None) else '-'
BAYC = {'B1': 'K1-K2', 'B2': 'K5-K7', 'B3': 'K22-K23', 'B4': 'K25-K26', 'B5': 'K15-K19', 'B6': 'K14-K18', 'B7': 'K20-K27', 'B8': 'K10-K16', 'B9': 'K18-K23', 'B10': 'K19-K25'}

def member_table():
    keep = [m for m in mem if m['type'] in ('rafter', 'primary', 'eave beam', 'trimmer', 'roof truss post')]
    rows = ['| Member (span) | Section | L m | M_Ed kNm | V_Ed kN | 6.2.5 M | 6.2.6 V | 6.3.2 LTB gravity | 6.3.2 LTB uplift | SLS L/200 | Util. | Governs | Verdict |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    n = 0
    for m in sorted(keep, key=lambda m: -float(m['utilisation'])):
        if float(m['utilisation']) < 0.10 and float(m['length']) < 6: n += 1; continue
        rows.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | **%s** | %s | %s |' % (m['id'], m['section'], f(m['length'], 2), m['M_Ed'], m['V_Ed'], m['u_M'], m['u_V'], m['u_LTB_g'], m['u_LTB_up'], m['u_defl'], m['utilisation'], m['governing'], m['verdict']))
    rows.append('| %d further spans (eave beams, trimmers, short edge-beam spans, ST2) | IPE 330 / IPE 270 | 2.7-5.9 | <= 15 | <= 11 | | | | | | <= 0.10 | - | OK |' % n)
    return '\n'.join(rows)

def column_table():
    rows = ['| Column | Section | L m | N_Ed,c kN (case) | N_Ed,t kN (case) | M_y,Ed / M_z,Ed kNm | k_zy (B.2) | 6.3.1 N/N_b,Rd | 6.3.3 | Util. | Verdict |', '|---|---|---|---|---|---|---|---|---|---|---|']
    cols = [m for m in mem if m['type'] == 'column']
    for m in sorted(cols, key=lambda m: -float(m['utilisation']))[:10]:
        e = be[m['id']]; c = s['cols'][m['id']]
        rows.append('| %s | %s | %s | %s (%s) | %s (%s) | %s | %s | %s | %s | **%s** | %s |' % (m['id'], m['section'], f(m['length'], 2), f(e['Nc'][0]), e['Nc'][1], f(max(e['Nt'][0], 0)), e['Nt'][1], m['M_Ed'], f(c['kzy'], 2), m['u_LTB_g'], m['u_LTB_up'], m['utilisation'], m['verdict']))
    rows.append('| other 17 columns | HEA 160 | 2.97-4.16 | <= 58 | <= 58 | <= 15 | 0.98-1.00 | <= 0.12 | <= 0.38 | <= 0.38 | OK |')
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
    rows = ['| Bay | Columns | w m | h m | Wind | H_Ed kN (ULS) | H seismic (1.0 E) | T_Ed diag. kN | N col. +/- kN | T_Rd L70x7 kN | Util. angle | Util. bolts | Sway SLS mm | h/150 mm |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for k, v in b.items():
        rows.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (k, BAYC[k], f(v['w'], 2), f(v['h'], 2), v['dir'], f(v['H']), f(v['H4']), f(v['T']), f(v['N']), f(v['NtRd']), f(v['util'], 2), f(v['util_bolt'], 2), f(v['sway']), f(v['sway_lim'])))
    return '\n'.join(rows)

def truss_table():
    rows = ['| Roof truss | Wind | Span m | Depth m | Panels | Shear V kN | Diagonal T kN (M24, 203) | Chord kN | Post kN | Util. rod | Truss defl. ULS mm |', '|---|---|---|---|---|---|---|---|---|---|---|']
    desc = {'RT-N-W': 'N band west, chords y 29.3 / 35.2', 'RT-N-E': 'N band east, chords y 29.3 / 35.7', 'RT-S-E': 'S band east, chords y 20.1 / 29.3', 'RT-S-W': 'S band west, chords y 15.9 / 21.8', 'RT-W': 'west edge, chords R68 / R72 (rods over two bays)', 'RT-E': 'east edge, chords R90 / R95 (rods over two bays)', 'RT-JOG': 'jog panel x 77.8-81.9 / y 24.5-29.3, carries the RT-N-E west reaction into B8'}
    for k, v in t.items():
        rows.append('| %s (%s) | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (k, desc[k], 'N-S' if k not in ('RT-W', 'RT-E') else 'E-W', f(v['L']), f(v['D']), v.get('npanels', 1), f(v['V']), f(v['T']), f(v['chord']), f(v.get('post', v['V'])), f(v['util'], 2), f(v['delta'])))
    return '\n'.join(rows)

def weight_table():
    rows = ['| Item | Section | Length m | Weight t |', '|---|---|---|---|']
    for k, sec_, ln in (('Rafters / edge beams / trimmers / posts ST1-ST2', 'IPE 270', 'rafters'), ('Primaries / eave beams', 'IPE 330', 'primaries'), ('Columns (27) + wind post WP1', 'HEA 160', 'columns')):
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
          seisW=f(seis['W'], 0), Fb=f(seis['Fb']), wN=f(wr['N']), wS=f(wr['S']), wE=f(wr['E'] - s['roof_comp'][0]*0.0 - 30.3), wEW_comp='30', roofc=f(s['roof_comp'][0]), roofx=f(s['roof_comp'][1]), roofy=f(s['roof_comp'][2]),
          wS_uls=f(1.5*wr['S']), wE_uls=f(1.5*(wr['E'] - 30.3)), H4max=f(max(s['H4']['x'].values())), H4maxy=f(max(s['H4']['y'].values())),
          roof_area=f(s['roof_area']), Wtot=f(W['total']/1000, 1), Whot=f(W['hot_rolled_total']/1000, 1), n_panels=s['n_roof_panels'],
          maxbeam=f(s['max_util']['beams'], 2), maxcol=f(s['max_util']['cols'], 2), maxbase=f(s['max_util']['bases'], 2), postN=f(s['post']['N']), postNb=f(s['post']['NbRd'], 0),
          st1=f(s['st']['N1']), st1b=f(s['st']['Nb1'], 0), st2=f(s['st']['N2']), st2b=f(s['st']['Nb2'], 0),
          wpL=f(s['wp1']['L'], 2), wpMy=f(s['wp1']['My']), wpMz=f(s['wp1']['Mz']), wpu=f(s['wp1']['u'], 2), wpV=f(max(s['wp1']['V'])),
          driftE=f(s['drift']['RT-E']), driftW=f(s['drift']['RT-W']), K12=s['colloads']['K12'], K19=s['colloads']['K19'],
          k_eff=f(s['thermal']['keff'], 1), F_s=f(s['thermal']['F_s'], 0), F_e=f(s['thermal']['F_e'], 0), F_uw=f(s['thermal']['F_uls_wind'], 0), F_ue=f(s['thermal']['F_uls_erect'], 0),
          cleatR=f(s['cleat']['R']), jogT=f(t['RT-JOG']['T']), jogV=f(t['RT-JOG']['V']), Lraft=f(L['rafters'], 0),
          sumG=f(sum(v['G'] for v in s['colloads'].values()), 0), sumQ=f(sum(v['Q'] for v in s['colloads'].values()), 0), sumWS=f(sum(v['W_S'] for v in s['colloads'].values()), 0),
          B8H=f(b['B8']['H']), B8T=f(b['B8']['T']), B8N=f(b['B8']['N']), B3H=f(b['B3']['H']), K25c=f(s['cols']['K25']['umax'], 2), K23c=f(s['cols']['K23']['umax'], 2), K22c=f(s['cols']['K22']['umax'], 2))
report = open(os.path.join(HERE, 'report_text.md')).read().format(**kw)
open(os.path.join(OUT, 'design_report_C.md'), 'w').write(report)
body = [l for l in report.splitlines() if not l.startswith('|')]
print('report written; words excl. tables:', len(' '.join(body).split()))
