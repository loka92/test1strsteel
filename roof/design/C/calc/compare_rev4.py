"""Writes rev4_vs_rev3.md: Rev 3 (basis Rev 2) vs Rev 4 (basis Rev 3) from summary_rev3_baseline.json and summary_C.json."""
import json, os, csv
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..')
a = json.load(open(os.path.join(HERE, 'summary_rev3_baseline.json'))); b = json.load(open(os.path.join(HERE, 'summary_C.json')))
f = lambda x, n=1: '%.*f' % (n, float(x))
def colsum(s, t):
    return sum(v[t] for v in s['colloads'].values())
rows = []
def add(item, va, vb, note=''):
    rows.append('| %s | %s | %s | %s |' % (item, va, vb, note))
add('Basis', 'load basis Rev 2', 'load basis Rev 3 (independent load critique)')
add('Services / imposed Q (kN/m2)', '0.20 / 0.60', '0.10 / 0.40')
add('Wall self-weight in G, G_min', '0.30 kN/m2 x height (in both)', 'none (wall mass in the seismic mass only)')
add('Wind q_p (kN/m2) N / S / E / W', '1.30 all directions, z_e 10', '1.25 / 0.75 / 1.05 / 1.05, z_e 9 m, terrain I / III / II / II')
add('Roof zones', 'mono-pitch Table 7.3a theta 180 set (-2.3/-1.3/-0.8) enveloped, e 20', 'flat roof Table 7.2 (-1.8/-1.2/-0.7/-0.2, I +0.2), e 18')
add('Global wall factor', '1.3 (D 0.8 + E 0.5)', '0.98 (0.85 x (0.75 + 0.40))')
add('Roofed area m2', f(a['roof_area']), f(b['roof_area']))
add('Sum G on the bases, char. kN', f(colsum(a, 'G'), 0), f(colsum(b, 'G'), 0), 'no walls, services 0.10')
add('Sum Q, char. kN', f(colsum(a, 'Q'), 0), f(colsum(b, 'Q'), 0))
add('Sum roof uplift W_N / W_S, char. kN', '%s / %s' % (f(colsum(a, 'W_N'), 0), f(colsum(a, 'W_S'), 0)), '%s / %s' % (f(colsum(b, 'W_N'), 0), f(colsum(b, 'W_S'), 0)))
add('Roof-level wind N / S / E / W, char. kN', ' / '.join(f(a['wind_roof'][d]) for d in 'NSEW'), ' / '.join(f(b['wind_roof'][d]) for d in 'NSEW'))
add('Roof-suction horizontal component (S), kN', f(a['roof_comp'][0]), f(b['roof_comp'][0]))
add('Seismic force at roof level, kN', '%s (roof mass, 0.20 g, unamplified)' % f(a['seismic']['Fb']), '%s E-W / %s N-S (two-mass, S_a %s / %s g, q 1.5)' % (f(b['seismic']['Fb_x'], 0), f(b['seismic']['Fb_y'], 0), f(b['seismic']['two_mass']['x']['Sa'], 2), f(b['seismic']['two_mass']['y']['Sa'], 2)))
for i in ('B1', 'B2', 'B3', 'B5', 'B6', 'B7', 'B8'):
    add('Bay %s: governing H_Ed kN (case) / diagonal util.' % i, '%s (%s) / %s' % (f(a['bays'][i]['H']), a['bays'][i]['dir'], f(a['bays'][i]['util'], 2)), '%s (%s) / %s' % (f(b['bays'][i]['H']), b['bays'][i]['dir'], f(b['bays'][i]['util'], 2)))
add('Thermal locked-in force B1/B2, ULS with wind / erection, kN', '%s / %s' % (f(a['thermal']['F_uls_wind'], 0), f(a['thermal']['F_uls_erect'], 0)), '%s / %s' % (f(b['thermal']['F_uls_wind'], 0), f(b['thermal']['F_uls_erect'], 0)))
add('Sections (primaries / rafters / columns)', 'IPE 330 / IPE 270 / HEA 160', 'IPE 330 / IPE 270 / HEA 160 (kept; IPE 300 / IPE 240 / HEA 140 passes at 0.82 / 0.69 / 0.79, not adopted)')
add('Max beam utilisation (K19-K20)', f(a['max_util']['beams'], 2), f(b['max_util']['beams'], 2), 'now LTB under the flat-roof pressure case')
add('Max column utilisation (K25)', f(a['max_util']['cols'], 2), f(b['max_util']['cols'], 2))
add('Purlin uplift M_Ed, kNm (3.07 m corner span)', f(a['purlins']['Mu']), f(b['purlins']['Mu']))
add('Cap-plate uplift, max kN', f(a['Nt_cap']), f(b['Nt_cap']))
for c in ('K19', 'K12', 'K23', 'K22', 'K20', 'K10', 'K7'):
    ea, eb = a['base_env'][c], b['base_env'][c]
    add('%s: uplift max kN (case) / compression max kN / shear max kN' % c, '%s (%s) / %s / %s' % (f(ea['Nt'][0]), ea['Nt'][1], f(ea['Nc'][0]), f(ea['Vt'][0])), '%s (%s) / %s / %s' % (f(eb['Nt'][0]), eb['Nt'][1], f(eb['Nc'][0]), f(eb['Vt'][0])))
add('Base utilisation: tension max / key max / worst base', '%s / %s / %s (%s)' % (f(max(e['uten'] for e in a['base_env'].values()), 2), f(max(e['ukey'] for e in a['base_env'].values()), 2), f(a['max_util']['bases'], 2), max(a['base_env'], key=lambda c: a['base_env'][c]['umax'][0])),
    '%s / %s / %s (%s)' % (f(max(e['uten'] for e in b['base_env'].values()), 2), f(max(e['ukey'] for e in b['base_env'].values()), 2), f(b['max_util']['bases'], 2), max(b['base_env'], key=lambda c: b['base_env'][c]['umax'][0])), 'seismic-governed E-W bay bases')
add('Weight (BOM t / calc take-off t)', '%s / %s' % (f(a['weight']['BOM_total']/1000), f(a['weight']['total']/1000)), '%s / %s' % (f(b['weight']['BOM_total']/1000), f(b['weight']['total']/1000)), 'unchanged sections')
add('Existing-structure loads: G char. / roof-level wind char. / roof-level seismic design', '%s kN / %s kN / %s kN' % (f(colsum(a, 'G'), 0), f(max(a['wind_roof'].values())), f(a['seismic']['Fb'])), '%s kN (+116 if the walls are counted) / %s kN / %s kN E-W, %s kN N-S' % (f(colsum(b, 'G'), 0), f(max(b['wind_roof'].values())), f(b['seismic']['Fb_x'], 0), f(b['seismic']['Fb_y'], 0)))
md = ['# Design C: Rev 4 (load basis Rev 3) versus Rev 3 (load basis Rev 2) - one-page comparison\n',
      'Both columns come from the same scripts (`calc/run_all.py`); Rev 3 values from `calc/summary_rev3_baseline.json`, Rev 4 from `calc/summary_C.json`. ULS values unless stated; kN, kNm, mm.\n',
      '| Item | Rev 3 | Rev 4 | Note |', '|---|---|---|---|'] + rows + [
      '\nWhat did not change: geometry (north-face jog, TOS 3.33, 11 rafter lines), sections, bracing layout (10 bays), roof-plane rods, connections, the base detail (type E post-installed rebar at all 27 columns, keys and plates), the detailing package. What changed: every load-derived number above, the governing case of every braced bay (seismic, two-mass), and the base and bay utilisations.']
open(os.path.join(OUT, 'rev4_vs_rev3.md'), 'w').write('\n'.join(md) + '\n')
print('rev4_vs_rev3.md written')
