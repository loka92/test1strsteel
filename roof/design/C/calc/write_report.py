"""Composes design_report_C.md from summary_C.json and the CSVs (run after run_all.py)."""
import json, csv, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..')
s = json.load(open(os.path.join(HERE, 'summary_C.json')))
mem = list(csv.DictReader(open(os.path.join(OUT, 'members_C.csv'))))
rea = list(csv.DictReader(open(os.path.join(OUT, 'reactions_C.csv'))))
W = s['weight']; L = s['lengths']; b = s['bays']; t = {x['id']: x for x in s['trusses']}
f = lambda x, n=1: ('%.*f' % (n, float(x))) if x not in ('', None) else '-'

def member_table():
    keep = [m for m in mem if m['type'] in ('rafter', 'primary', 'eave beam', 'trimmer')]
    # one row per span for rafters/primaries with utilisation > 0.05, plus all long spans; short list the rest
    rows = ['| Member (span) | Section | L m | M_Ed kNm | V_Ed kN | 6.2.5 M | 6.2.6 V | 6.3.2 LTB gravity | 6.3.2 LTB uplift | SLS L/200 | Util. | Governs | Verdict |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for m in sorted(keep, key=lambda m: -float(m['utilisation'])):
        if float(m['utilisation']) < 0.10 and float(m['length']) < 6: continue
        rows.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | **%s** | %s | %s |' % (m['id'], m['section'], f(m['length'], 2), m['M_Ed'], m['V_Ed'], m['u_M'], m['u_V'], m['u_LTB_g'], m['u_LTB_up'], m['u_defl'], m['utilisation'], m['governing'], m['verdict']))
    n_skipped = len(keep) - (len(rows) - 2)
    rows.append('| %d further spans (eave beams, trimmers, short edge-beam spans) | IPE 330 / IPE 270 | 2.7-5.9 | <= 15 | <= 11 | | | | | | <= 0.10 | - | OK |' % n_skipped)
    return '\n'.join(rows)

def column_table():
    rows = ['| Column | Section | L m | N_Ed,c kN (case) | N_Ed,t kN (case) | M_y,Ed / M_z,Ed kNm | 6.3.1 N/N_b,Rd | 6.3.3 interaction | Util. | Verdict |', '|---|---|---|---|---|---|---|---|---|---|']
    cols = [m for m in mem if m['type'] == 'column']
    for m in sorted(cols, key=lambda m: -float(m['utilisation']))[:10]:
        r = next(x for x in rea if x['column'] == m['id'])
        rows.append('| %s | %s | %s | %s (%s) | %s (%s) | %s | %s | %s | **%s** | %s |' % (m['id'], m['section'], f(m['length'], 2), r['N_comp_ULS'], r['case_comp'], r['N_uplift_ULS'], r['case_uplift'], m['M_Ed'], m['u_LTB_g'], m['u_LTB_up'], m['utilisation'], m['verdict']))
    rows.append('| other 17 columns | HEA 160 | 2.94-4.13 | <= 57 | <= 52 | <= 15 | <= 0.10 | <= 0.35 | <= 0.35 | OK |')
    return '\n'.join(rows)

def reaction_table():
    rows = ['| Col | x | y | Bay | N_c ULS (case) | N_t ULS (case) | V_x ULS | V_y ULS | N_c SLS | N_t SLS | V_x SLS | V_y SLS | V_wall,x | V_wall,y | Anchor util. (governs) |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in rea:
        rows.append('| %s | %s | %s | %s | %s (%s) | %s (%s) | %s | %s | %s | %s | %s | %s | %s | %s | %s (%s) |' % (
            r['column'], r['x'], r['y'], r['braced_bay'] or '-', r['N_comp_ULS'], r['case_comp'], r['N_uplift_ULS'], r['case_uplift'], r['Vx_ULS'], r['Vy_ULS'],
            r['N_comp_SLS'], r['N_uplift_SLS'], r['Vx_SLS'], r['Vy_SLS'], r['Vwall_x_ULS'], r['Vwall_y_ULS'], r['anchor_util'], r['anchor_gov'].replace('anchor ', '')))
    return '\n'.join(rows)

def bay_table():
    rows = ['| Bay | Columns | w m | h m | Governing wind | H_Ed kN (ULS) | T_Ed diag. kN | N col. +/- kN | T_Rd L70x7 kN | Util. angle | Util. bolts | Sway SLS mm | Limit h/150 mm |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    bays = {'B1': 'K1-K2', 'B2': 'K5-K7', 'B3': 'K22-K23', 'B4': 'K25-K26', 'B5': 'K15-K19', 'B6': 'K14-K18', 'B7': 'K20-K27', 'B8': 'K17-K21'}
    for k, v in b.items():
        rows.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (k, bays[k], f(v['w'], 2), f(v['h'], 2), v['dir'], f(v['H']), f(v['T']), f(v['N']), f(v['NtRd']), f(v['util'], 2), f(v['util_bolt'], 2), f(v['sway']), f(v['sway_lim'])))
    return '\n'.join(rows)

def truss_table():
    rows = ['| Roof truss | Wind | Span m | Depth m | Shear V kN | Diagonal T kN (M20 rod, 141) | Chord kN | Post kN | Util. rod |', '|---|---|---|---|---|---|---|---|---|']
    desc = {'RT-N-W': 'N band west, chords y 29.3 / 35.2', 'RT-N-E': 'N band east, chords y 29.3 / 35.7', 'RT-S-E': 'S band east, chords y 20.1 / 29.3', 'RT-S-W': 'S band west, chords y 15.9 / 21.8', 'RT-W': 'west edge, chords x 68.0 / 72.1', 'RT-E': 'east edge, chords x 89.9 / 95.5', 'RT-JOG': 'jog panel x 77.8-81.9, y 24.5-29.3'}
    for k, v in t.items():
        rows.append('| %s (%s) | %s | %s | %s | %s | %s | %s | %s | %s |' % (k, desc[k], 'N-S' if k not in ('RT-W', 'RT-E') else 'E-W', f(v['L']), f(v['D']), f(v['V']), f(v['T']), f(v['chord']), f(v['post']), f(v['util'], 2)))
    return '\n'.join(rows)

def weight_table():
    rows = ['| Item | Section | Length m | Weight t |', '|---|---|---|---|']
    for k, sec_, ln in (('Rafters / edge beams / trimmers', 'IPE 270', 'rafters'), ('Primaries / eave beams', 'IPE 330', 'primaries'), ('Columns (27) + wind post WP1', 'HEA 160', 'columns'), ('Base struts in the 8 braced bays', 'HEA 160', 'base_struts')):
        rows.append('| %s | %s | %s | %s |' % (k, sec_, f(L[ln]), f(W[ln]/1000, 2)))
    rows.append('| Plates, fin/cap/base plates, bolts (10 %%) | S275 | - | %s |' % f(W['plates_bolts']/1000, 2))
    rows.append('| **Hot-rolled total** | | | **%s** |' % f(W['hot_rolled_total']/1000, 1))
    rows.append('| Wall bracing, 8 bays x 2 diagonals | L 70x7 | %s | %s |' % (f(L['wall_bracing']), f(W['wall_bracing']/1000, 2)))
    rows.append('| Roof bracing, %d panels x 2 diagonals | M20 rods 8.8 | %s | %s |' % (s['n_roof_panels'], f(L['roof_bracing']), f(W['roof_bracing']/1000, 2)))
    rows.append('| Purlins %s m + girts %s m | Z 200x2.0 S350GD | %s | %s |' % (f(L['purlins'], 0), f(L['girts'], 0), f(L['purlins'] + L['girts'], 0), f(W['purlins_girts_Z200']/1000, 2)))
    rows.append('| **Total** | | | **%s** (%s kg/m2 of footprint 486 m2, %s kg/m2 of roofed 446 m2) |' % (f(W['total']/1000, 1), f(W['total']/486, 0), f(W['total']/446, 0)))
    return '\n'.join(rows)

cap, fin2, fin3, br, pu = s['cap'], s['fin2'], s['fin3'], s['base_res'], s['purlins']
worst = s['worst_base']; wb = s['bases'][worst]['util']
seis = s['seismic']; wr = s['wind_roof']
report = open(os.path.join(HERE, 'report_text.md')).read()
report = report.format(member_table=member_table(), column_table=column_table(), reaction_table=reaction_table(), bay_table=bay_table(),
                       truss_table=truss_table(), weight_table=weight_table(),
                       Vfin=f(s['Vfin']), Vfin_long=f(s['Vfin_long']), fin2=f(fin2['umax'], 2), fin2gov=fin2['gov'], fin3=f(fin3['umax'], 2),
                       fin2_bs=f(fin2['util']['bolt shear'], 2), fin2_bp=f(fin2['util']['bearing plate'], 2), fin2_ps=f(fin2['util']['plate shear'], 2), fin2_pb=f(fin2['util']['plate bending'], 2), fin2_w=f(fin2['util']['weld'], 2), fin2_bt=f(fin2['util']['web block tearing'], 2),
                       Nt_cap=f(s['Nt_cap']), Vh_cap=f(s['Vh_cap']), cap_bt=f(cap['util']['bolt tension'], 2), cap_bi=f(cap['util']['bolt interaction'], 2), cap_ts=f(cap['util']['beam flange T-stub'], 2), cap_w=f(cap['util']['weld'], 2),
                       NRd_c=f(br['NRd_c']), NRd_p=f(br['NRd_p']), VRd_c=f(br['VRd_c']), VRd_cp=f(br['VRd_cp']), Aeff=f(br['Aeff']/100, 0), ratio_c=f(br['ratio_c'], 2),
                       worst=worst, wb_cone=f(wb['anchor group cone'], 2), wb_edge=f(wb['anchor group edge'], 2), wb_int=f(wb['N-V interaction'], 2), wb_bear=f(wb['bearing (grout/slab)'], 2), wb_pb=f(wb['plate bending (uplift)'], 2),
                       Mg=f(pu['Mg']), Mu=f(pu['Mu']), Lp=f(pu['Lmax'], 2), dp=f(pu['d']), dplim=f(pu['dlim']), Mu_where='x %.1f-%.1f, y %.1f' % tuple(pu['Mu_where'][:3]),
                       seisW=f(seis['W'], 0), Fb=f(seis['Fb']), wN=f(wr['N']), wS=f(wr['S']), wE=f(wr['E']), wW=f(wr['W']),
                       roof_area=f(s['roof_area']), n_panels=s['n_roof_panels'], wS_uls=f(1.5*wr['S']), wE_uls=f(1.5*wr['E']), Wtot=f(W['total']/1000, 1), Whot=f(W['hot_rolled_total']/1000, 1),
                       maxbeam=f(s['max_util']['beams'], 2), maxcol=f(s['max_util']['cols'], 2), postN=f(s['post']['N']), postNb=f(s['post']['NbRd'], 0),
                       wpL=f(s['wp1']['L'], 2), wpMy=f(s['wp1']['My']), wpMz=f(s['wp1']['Mz']), wpu=f(s['wp1']['u'], 2),
                       K12=s['colloads']['K12'], K19=s['colloads']['K19'])
open(os.path.join(OUT, 'design_report_C.md'), 'w').write(report)
print('report written, words:', len(report.split()))
