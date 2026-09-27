"""Builds members_A.csv, reactions_A.csv and the markdown tables (report_tables.md) from the pickled results."""
import os, csv, pickle
import numpy as np
import loads as L
from frames_model import DESIGN

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..')
CHK = pickle.load(open(os.path.join(HERE, 'results_checks.pkl'), 'rb'))
SEC = pickle.load(open(os.path.join(HERE, 'results_secondary.pkl'), 'rb'))
CON = pickle.load(open(os.path.join(HERE, 'results_connections.pkl'), 'rb'))
RES = pickle.load(open(os.path.join(HERE, 'results_frames.pkl'), 'rb'))

# ------------------------------------------------------------- members_A.csv
rows = []
for m in CHK['members']:
    rows.append(dict(member_id=m['id'], type=m['type'], section=m['section'], length_m=round(m['L'], 2), frm=m['frm'], to=m['to'],
                     N_Ed_kN=round(m['N'], 1), M_Ed_kNm=round(m['M'], 1), V_Ed_kN=round(m['V'], 1), utilisation=round(m['u'], 2),
                     governing_check=m['gov'], combo=m['combo']))
for r in SEC['rows']:
    rows.append(dict(member_id=r['id'], type=r['type'], section=r['section'], length_m=round(r['L'], 2), frm=r['frm'], to=r['to'],
                     N_Ed_kN=round(r.get('N', 0), 1), M_Ed_kNm=round(r.get('M', 0), 1), V_Ed_kN=round(r.get('V', 0), 1),
                     utilisation=round(r['u'], 2), governing_check=r['gov'], combo=''))
c = CON['conn']
rows.append(dict(member_id='knee end-plate connection (all 27 columns)', type='connection', section=c['plate'], length_m='', frm='rafter', to='column',
                 N_Ed_kN=round(c['N'] if 'N' in c else 0, 1), M_Ed_kNm=round(max(c['M_hog'], c['M_sag']), 1), V_Ed_kN=round(c['V'], 1),
                 utilisation=round(max(c['u_hog'], c['u_sag'], c['u_wp']), 2), governing_check='bolt-row tension (uplift, sagging)', combo='ULS3_N K9'))
rows.append(dict(member_id='rafter-to-girder pin F5/F6', type='connection', section='4 x M20 8.8', length_m='', frm='rafter', to='girder',
                 N_Ed_kN=0, M_Ed_kNm=0, V_Ed_kN=round(CON['pin']['R'], 1), utilisation=round(CON['pin']['u'], 2), governing_check='bolt shear', combo='ULS3'))
for k, b in CON['bases'].items():
    rows.append(dict(member_id='base %s (%s)' % (k, b['kind']), type='base', section='300x400x20 + 4 M20 h_ef 300', length_m='', frm='column', to='slab',
                     N_Ed_kN=round(-b['Nt'], 1), M_Ed_kNm=0, V_Ed_kN=round(max(b['Vy'], b['Vx']), 1), utilisation=round(max(b['u'], b['u_bear'], b['u_plate']), 2),
                     governing_check='anchor N+V interaction (EN 1992-4)', combo=b['combo']))
with open(os.path.join(OUT, 'members_A.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# ------------------------------------------------------------- reactions_A.csv
react = []
for k in L.COLS:
    b = CON['bases'][k]
    react.append(dict(column=k, x=L.COLS[k][0], y=L.COLS[k][1], position=b['kind'],
                      Nc_ULS_kN=round(b['Nc'], 1), Nt_ULS_kN=round(b['Nt'], 1), Vx_ULS_kN=round(b['Vx'], 1), Vy_ULS_kN=round(b['Vy'], 1),
                      Vy_toward_edge_ULS_kN=round(b['Vout'], 1),
                      Nc_SLS_kN=round(b['Nc_s'], 1), Nt_SLS_kN=round(b['Nt_s'], 1), Vx_SLS_kN=round(b['Vx_s'], 1), Vy_SLS_kN=round(b['Vy_s'], 1),
                      combo_Nc=b['comboC'], combo_Nt=b['comboT'], anchor_util=round(b['u'], 2)))
with open(os.path.join(OUT, 'reactions_A.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(react[0].keys())); w.writeheader(); w.writerows(react)

# ------------------------------------------------------------- markdown tables
md = []
md.append('## per-frame envelopes\n')
md.append('| Frame | rafter | columns | alpha_cr ULS-1 | alpha_cr min (combo) | alpha_cr H/V | M_sag max (kNm) | M_hog max at column face (kNm) | V max (kN) | N rafter (kN) | col M_top max (kNm) | col N max (kN) |')
md.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
for fname, pf in CHK['per_frame'].items():
    env = pf['env']; a = pf['alpha']
    cmin = min(a, key=a.get)
    Msag = max(e['Mmax'] for e in env.values()); Mhog = min(e['Mmin'] for e in env.values()); Vm = max(e['Vmax'] for e in env.values())
    Nmin = min(e['Nmin'] for e in env.values()); Nmax = max(e['Nmax'] for e in env.values())
    colM = max(v['M'] for e in env.values() for v in e['cols'].values()); colN = max(v['N'] for e in env.values() for v in e['cols'].values())
    meta = RES[fname if fname not in ('F5', 'F6') else fname + '_spring']['_meta']
    md.append('| %s | %s | %s | %.1f | %.1f (%s) | %.1f | %.0f | %.0f | %.0f | %.0f / +%.0f | %.0f | %.0f |' %
              (fname, meta['rafter'], 'HEA 200', a['ULS1+'], a[cmin], cmin, pf['alpha_HV'], Msag, Mhog, Vm, Nmin, Nmax, colM, colN))
md.append('\n## knee moments per column (kNm, at column face)\n')
md.append('| column | M hog (combo) | M sag (combo) | V (kN) | dM panel (kNm) |'); md.append('|---|---|---|---|---|')
for k, v in c['knee'].items():
    md.append('| %s | %.0f (%s) | %.0f (%s) | %.0f | %.0f |' % (k, v['M_hog'], v['combo_hog'], v['M_sag'], v['combo_sag'], v['V'], v['dM']))
md.append('\n## member checks\n')
md.append('| member | section | L (m) | N_Ed (kN) | M_Ed (kNm) | Mz (kNm) | V_Ed (kN) | class | M+N 6.2.9 | shear | haunch Mel | buckling 6.3.3 | LTB | u | governing (combo) |')
md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for m in CHK['members']:
    if m['type'] == 'column':
        md.append('| %s | %s | %.2f | %.0f | %.0f | %.0f | %.0f | %d | %.2f | %.2f | - | %.2f | - | **%.2f** | %s (%s) |' %
                  (m['id'], m['section'], m['L'], m['N'], m['M'], m['Mz'], m['V'], m['cls'], m['u_cs'], m['u_v'], max(m['u_b1'], m['u_b2']), m['u'], m['gov'], m['combo']))
    else:
        md.append('| %s | %s | %.2f | %.0f | %.0f | - | %.0f | %d | %.2f | %.2f | %.2f | - | %.2f (L %.1f, C1 %.2f, chi %.2f) | **%.2f** | %s (%s) |' %
                  (m['id'], m['section'], m['L'], m['N'], m['M'], m['V'], m['cls'], m['u_cs'], m['u_v'], m['u_h'], m['u_lt'], m['Lcr'], m['C1'], m['xLT'], m['u'], m['gov'], m['combo']))
md.append('\n## secondary members\n')
md.append('| member | section | L (m) | N (kN) | M (kNm) | V (kN) | u | governing |'); md.append('|---|---|---|---|---|---|---|---|')
for r in SEC['rows']:
    md.append('| %s | %s | %.2f | %.0f | %.1f | %.0f | **%.2f** | %s |' % (r['id'], r['section'], r['L'], r.get('N', 0), r.get('M', 0), r.get('V', 0), r['u'], r['gov']))
md.append('\n## deflections (SLS G+Q; Q only in brackets)\n')
md.append('| frame | bay | L (m) | delta G+Q (mm) | delta Q (mm) | limit L/200 (mm) | ratio |'); md.append('|---|---|---|---|---|---|---|')
seen = set()
for d in CHK['defl']:
    if d['case'] != 'G+Q' or (d['frame'], d['bay']) in seen: continue
    seen.add((d['frame'], d['bay']))
    dq = [x for x in CHK['defl'] if x['case'] == 'Q' and x['frame'] == d['frame'] and x['bay'] == d['bay']][0]
    md.append('| %s | %s | %.2f | %.1f | %.1f | %.0f | L/%.0f |' % (d['frame'], d['bay'], d['L'], d['d'], dq['d'], d['lim'], d['L'] * 1e3 / max(d['d'], 0.1)))
md.append('\n## sway (SLS G + W)\n')
md.append('| frame | column | u (mm) | h (m) | ratio | combo |'); md.append('|---|---|---|---|---|---|')
for fname in L.FRAMES:
    w = max([x for x in CHK['sway'] if x['frame'] == fname], key=lambda x: x['ratio'])
    md.append('| %s | %s | %.1f | %.2f | h/%.0f | %s |' % (fname, w['col'], abs(w['u']), w['h'] / 1e3, 1 / max(w['ratio'], 1e-9), w['combo']))
md.append('\n## reactions\n')
md.append('| column | position | Nc ULS | Nt ULS | Vx ULS | Vy ULS | Vy to edge | Nc SLS | Nt SLS | Vx SLS | Vy SLS | anchor u (h_ef 300) | anchor u (h_ef 170) |')
md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for r in react:
    b1 = CON['bases_170'][r['column']]
    md.append('| %s | %s | %.0f | %.0f | %.0f | %.0f | %.0f | %.0f | %.0f | %.0f | %.0f | %.2f | %.2f |' %
              (r['column'], r['position'], r['Nc_ULS_kN'], r['Nt_ULS_kN'], r['Vx_ULS_kN'], r['Vy_ULS_kN'], r['Vy_toward_edge_ULS_kN'],
               r['Nc_SLS_kN'], r['Nt_SLS_kN'], r['Vx_SLS_kN'], r['Vy_SLS_kN'], r['anchor_util'], b1['u']))
md.append('\n## weight\n')
md.append('| item | kg |'); md.append('|---|---|')
for k, v in SEC['weight']['items'].items():
    md.append('| %s | %.0f |' % (k, v))
md.append('| **total** | **%.0f** |' % SEC['weight']['total'])
open(os.path.join(HERE, 'report_tables.md'), 'w').write('\n'.join(md))
print('\n'.join(md))
print('\nmax utilisation frame members: %.2f' % max(m['u'] for m in CHK['members']))
print('files written: members_A.csv (%d rows), reactions_A.csv (%d rows), report_tables.md' % (len(rows), len(react)))
