"""Steel section cost from the supplier quotation (Al-Salama Industrial Steel Trading, pro-forma 11486, 29/09/2026):
unit prices per stock bar -> LYD/m and LYD/t; Rev 7 section bill priced with a 12 m bar-cutting plan (first-fit decreasing)."""
import sys, json, math, csv
sys.path.insert(0, '/home/user/test1strsteel/roof/design/C7/calc')
import model as M
from sections import sec
OUT = '/home/user/test1strsteel/roof'
# ---- invoice items: (item no, description, bar length m, qty, unit price LYD)
INV = [(1596, 'HEA 140 x 133, 12 m, imported', 12, 8, 3375.0), (85, 'IPE 300, 12 m, imported', 12, 7, 3750.0), (83, 'IPE 330, 12 m, imported', 12, 1, 4650.0),
       (81, 'IPE 240, 12 m, imported', 12, 17, 2725.0), (2707, 'Galvanised purlin 200, 6 m', 6, 95, 285.0), (341, 'Angle 75 x 75 x 7, 12 m', 12, 13, 720.0),
       (1351, 'Threaded bolt M24 x 60 cm', 0.6, 1, 29.0), (1985, 'HEA 140 x 133, 6 m, imported', 6, 1, 1690.0)]
inv_total = sum(q*p for _, _, _, q, p in INV)
KG = {'HEA 140': 24.7, 'IPE 300': 42.2, 'IPE 330': 49.1, 'IPE 240': 30.7, 'Z200': 5.9, 'L75x7': 7.94, 'M24': 3.55}
RATE = {  # LYD per metre from the invoice
 'HEA 140': 3375.0/12, 'IPE 300': 3750.0/12, 'IPE 330': 4650.0/12, 'IPE 240': 2725.0/12, 'Z200': 285.0/6, 'L75x7': 720.0/12, 'M24': 29.0/0.6}
# ---- Rev 7 cut lengths
pieces = {'HEA 140': [], 'IPE 300': [], 'IPE 330': [], 'IPE 240': [], 'L75x7': []}
for c, (x, y) in M.COLS.items(): pieces['HEA 140'].append(M.L_col(y, c))
for pid in M.WIND_POSTS: pieces['HEA 140'].append(M.wall_h(M.POSTS[pid][1]) - 0.34)
for r in M.RAFTERS:
    ys = [s[0] for s in r['sup']]; L = [b - a for a, b in zip(ys[:-1], ys[1:])]
    L[0] += ys[0] - r['y0']; L[-1] += r['y1'] - ys[-1]; pieces['IPE 240'] += L
pieces['IPE 240'] += [4.10]                                    # ST2 (T3 is a primary entry with kind trim)
for p in M.PRIMARIES:
    L = p['x1'] - p['x0']; s = M.SPAN_SECTION.get(p['id'], 'IPE 240' if p['kind'] == 'trim' else 'IPE 300'); pieces[s].append(L)
for b in M.BAYS: pieces['L75x7'] += [M.bay_geom(b)[2]]*2
L_purlin = 217.0; L_rod = 167.8
def pack(lengths, bar=12.0, kerf=0.01):
    bars = []
    for L in sorted(lengths, reverse=True):
        for b in bars:
            if b['left'] >= L + kerf: b['cuts'].append(L); b['left'] -= L + kerf; break
        else: bars.append(dict(cuts=[L], left=bar - L - kerf))
    return bars
rows = []; total = 0.0; tot_kg = 0.0
for s in ('HEA 140', 'IPE 300', 'IPE 330', 'IPE 240', 'L75x7'):
    Ls = pieces[s]; net = sum(Ls)
    if s == 'IPE 330':   # 13.7 m eave beam: one 12 m bar + 1.7 m from a second bar (bolted splice), or a 14 m special length
        bars = 2; note = '13.7 m beam: 12 m bar + 1.7 m piece (splice) or one 14 m special length'
    else:
        bars = len(pack(Ls)); note = '%d pieces, longest %.2f m' % (len(Ls), max(Ls))
    cost = bars*RATE[s]*12; kg = bars*12*KG[s]; total += cost; tot_kg += kg
    rows.append(dict(section=s, net_m=net, bars=bars, bar_m=bars*12, kg=kg, rate_m=RATE[s], rate_t=RATE[s]*1000/KG[s], cost=cost, note=note))
n_pur = math.ceil(L_purlin/6); cost = n_pur*285.0; kg = n_pur*6*KG['Z200']; total += cost; tot_kg += kg
rows.append(dict(section='Z200 purlin, 6 m bars', net_m=L_purlin, bars=n_pur, bar_m=n_pur*6, kg=kg, rate_m=RATE['Z200'], rate_t=RATE['Z200']*1000/KG['Z200'], cost=cost, note='gauge 2.0 mm S350GD to confirm with the supplier'))
cost = L_rod*RATE['M24']; kg = L_rod*KG['M24']; total += cost; tot_kg += kg
rows.append(dict(section='M24 threaded rod', net_m=L_rod, bars=None, bar_m=L_rod, kg=kg, rate_m=RATE['M24'], rate_t=RATE['M24']*1000/KG['M24'], cost=cost, note='priced from the 60 cm bolt (29 LYD); ask for rod in 3 m lengths'))
S7 = json.load(open('/home/user/test1strsteel/roof/design/C7/calc/summary_C7.json'))
plates_kg = S7['weight']['plates_bolts_keys']; plate_rate = 7500.0; plates_cost = plates_kg/1000*plate_rate
res = dict(invoice_total=inv_total, rows=rows, sections_cost=total, sections_kg=tot_kg, plates_kg=plates_kg, plate_rate=plate_rate, plates_cost=plates_cost,
           avg_rate_t=total/tot_kg*1000)
json.dump(res, open(OUT + '/offer/sections_cost_invoice.json', 'w'), indent=1)
f = lambda x: '{:,.0f}'.format(x)
md = ['# Steel section cost from the supplier quotation (29 Sep 2026)\n',
      'Source: pro-forma invoice 11486, Al-Salama Industrial Steel Trading (محلات السلامة لتجارة الحديد الصناعي), total %s LYD. Its quantities are the **Rev 6a** sections list (8 x 12 m + 1 x 6 m HEA 140, 7 x IPE 300, 1 x IPE 330, 17 x IPE 240, 95 x 6 m purlins, 13 x angle): supply of sections only, no plates, bolts, fabrication, coating or erection.\n' % f(inv_total),
      '## 1. Unit rates from the invoice\n', '| Item | Bar | Price LYD | LYD / m | kg / m | LYD / tonne |', '|---|---|---|---|---|---|']
for no, d, bl, q, p in INV:
    key = {1596: 'HEA 140', 1985: 'HEA 140', 85: 'IPE 300', 83: 'IPE 330', 81: 'IPE 240', 2707: 'Z200', 341: 'L75x7', 1351: 'M24'}[no]
    md.append('| %d %s | %g m | %s | %.1f | %.2f | %s |' % (no, d, bl, f(p), p/bl, KG[key], f(p/bl*1000/KG[key])))
md += ['', 'Supply-only section prices are 7,400-7,900 LYD/t for IPE, about 11,400 LYD/t for HEA 140, 8,050 LYD/t for the purlin (if 2.0 mm) and 7,560 LYD/t for the angle. **The 6,950 LYD/t used so far as an all-in rate (supplied, fabricated, erected) is below the bare material price**, so the cost build-up changes: material at invoice prices plus fabrication, coating and erection as separate items.\n',
       '## 2. Rev 7 section bill at invoice prices (12 m stock bars, first-fit cutting plan, 10 mm kerf)\n', '| Section | Net m | Bars | Bought m | kg | LYD / m | Cost LYD | Cutting note |', '|---|---|---|---|---|---|---|---|']
for r in rows: md.append('| %s | %.1f | %s | %.1f | %s | %.1f | %s | %s |' % (r['section'], r['net_m'], r['bars'] if r['bars'] else '-', r['bar_m'], f(r['kg']), r['rate_m'], f(r['cost']), r['note']))
md += ['| **Sections total** | | | | **%s** | | **%s** | average %s LYD/t on bought weight |' % (f(tot_kg), f(total), f(res['avg_rate_t'])),
       '| Plates, keys, rebars, bolts (%.1f t, not on the invoice) | | | | %s | | %s | assumed %s LYD/t, to be quoted |' % (plates_kg/1000, f(plates_kg), f(plates_cost), f(plate_rate)),
       '| **Material total** | | | | **%s** | | **%s** | |' % (f(tot_kg + plates_kg), f(total + plates_cost)), '',
       'Waste: bought %.0f kg against a net take-off of %.0f kg (%.0f %% offcuts); the offcuts of the IPE 240 and HEA 140 bars are usable for T3, ST2, the wind posts and stiffeners.\n' % (tot_kg, S7['weight']['sections_hot_rolled'] + S7['weight']['wall_bracing']*7.94/7.38 + S7['weight']['roof_bracing'] + S7['weight']['purlins_Z200'], (tot_kg/(S7['weight']['sections_hot_rolled'] + S7['weight']['wall_bracing']*7.94/7.38 + S7['weight']['roof_bracing'] + S7['weight']['purlins_Z200']) - 1)*100),
       '## 3. Notes on the quotation\n',
       '- The IPE 330 eave beam K17-K18 is 13.7 m; the stock length is 12 m. Either a 14 m bar is ordered (ask the supplier) or the beam is spliced with a bolted end-plate splice near a rafter, about 3 m from K18.',
       '- The angle offered is 75 x 75 x 7 (7.94 kg/m) instead of the designed 70 x 70 x 7: acceptable, slightly stronger; gusset holes at the 40 mm gauge stay.',
       '- Purlin "galvanised 200, 6 m": confirm Z (not C) profile, 2.0 mm, S350GD, Z275; the design needs sleeved laps at the rafters, so 6 m bars suit the 2.6-4.1 m rafter spacing with one lap per two bays.',
       '- HEA 140 columns: 20 columns of 3.0-3.84 m and 3 posts of about 4.0 m cut from 8 x 12 m bars (three pieces per bar); the 6 m bar is not needed for Rev 7.',
       '- The M24 item is a 60 cm bolt; the roof rods need about 168 m of threaded rod with turnbuckles, to be quoted as rod.',
       '- Prices are dated 29/09/2026 and imported stock; keep the 15-day offer validity.']
open(OUT + '/cost_sections_invoice.md', 'w').write('\n'.join(md) + '\n')
print('\n'.join(md))
