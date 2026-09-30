"""Steel section cost from the supplier quotation (Al-Salama Industrial Steel Trading, pro-forma 11486, 29/09/2026):
unit prices per stock bar -> LYD/m and LYD/t; Rev 7 section bill priced with a 12 m bar-cutting plan (first-fit decreasing)."""
import sys, os, json, math, csv
OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # .../roof, wherever the repo is checked out
sys.path.insert(0, OUT + '/design/C7/calc')
import model as M
from sections import sec
# ---- invoice items: (item no, description, bar length m, qty, unit price LYD)
INV = [(1596, 'HEA 140 x 133, 12 m, imported', 12, 8, 3375.0), (85, 'IPE 300, 12 m, imported', 12, 7, 3750.0), (83, 'IPE 330, 12 m, imported', 12, 1, 4650.0),
       (81, 'IPE 240, 12 m, imported', 12, 17, 2725.0), (2707, 'Galvanised purlin 200, 6 m', 6, 95, 285.0), (341, 'Angle 75 x 75 x 7, 12 m', 12, 13, 720.0),
       (1351, 'Threaded bolt M24 x 60 cm', 0.6, 1, 29.0), (1985, 'HEA 140 x 133, 6 m, imported', 6, 1, 1690.0)]
inv_total = sum(q*p for _, _, _, q, p in INV)
KG = {'HEA 140': 24.7, 'IPE 300': 42.2, 'IPE 330': 49.1, 'IPE 240': 30.7, 'IPE 200': 22.4, 'IPE 180': 18.8, 'IPE 160': 15.8, 'Z200': 5.9, 'L75x7': 7.94, 'L60x6': 5.42, 'M24': 3.55, 'M20': 2.47}
IPE_T = 7400.0   # LYD/t: IPE 240 and IPE 300 both price at 7,400 LYD/t on the invoice -> used for the IPE sizes not quoted
RATE = {  # LYD per metre from the invoice (sizes not on the invoice by weight at the invoice rate of the same family)
 'HEA 140': 3375.0/12, 'IPE 300': 3750.0/12, 'IPE 330': 4650.0/12, 'IPE 240': 2725.0/12, 'IPE 200': 22.4*IPE_T/1000, 'IPE 180': 18.8*IPE_T/1000, 'IPE 160': 15.8*IPE_T/1000,
 'Z200': 285.0/6, 'L75x7': 720.0/12, 'L60x6': 5.42*720.0/12/7.94, 'M24': 29.0/0.6, 'M20': 29.0/0.6*2.47/3.55}
NOTQ = {'IPE 200', 'IPE 180', 'IPE 160', 'L60x6', 'M20'}
# ---- Rev 7 cut lengths
SEC_R, SEC_P, SEC_C = M.SEC_RAFT, M.SEC_PRIM, M.SEC_COL
from bracing import ECON as _ECON
ANG = 'L60x6' if _ECON else 'L75x7'; RODN = 'M20' if _ECON else 'M24'
pieces = {SEC_C: [], SEC_P: [], SEC_R: [], ANG: []}
for _s in M.SPAN_SECTION.values(): pieces.setdefault(_s, [])
for c, (x, y) in M.COLS.items(): pieces[SEC_C].append(M.L_col(y, c))
for pid in M.WIND_POSTS: pieces[SEC_C].append(M.wall_h(M.POSTS[pid][1]) - 0.34)
for r in M.RAFTERS:
    ys = [s[0] for s in r['sup']]; L = [b - a for a, b in zip(ys[:-1], ys[1:])]
    L[0] += ys[0] - r['y0']; L[-1] += r['y1'] - ys[-1]
    if M.SCHEME == 'ontop': pieces[SEC_R].append(sum(L))       # continuous rafter: one piece per line (spliced only where longer than 12 m)
    else: pieces[SEC_R] += L
pieces[SEC_R] += [4.10]                                        # ST2 (T3 is a primary entry with kind trim)
for p in M.PRIMARIES:
    L = p['x1'] - p['x0']; s = M.SPAN_SECTION.get(p['id'], SEC_R if p['kind'] == 'trim' else SEC_P); pieces[s].append(L)
for b in M.BAYS: pieces[ANG] += [M.bay_geom(b)[2]]*2
L_purlin = 217.0; L_rod = 167.8
def pack(lengths, bar=12.0, kerf=0.01):
    bars = []
    for L in sorted(lengths, reverse=True):
        for b in bars:
            if b['left'] >= L + kerf: b['cuts'].append(L); b['left'] -= L + kerf; break
        else: bars.append(dict(cuts=[L], left=bar - L - kerf))
    return bars
rows = []; total = 0.0; tot_kg = 0.0
for s in pieces:
    Ls = pieces[s]; net = sum(Ls)
    if s == 'IPE 330':   # 13.7 m eave beam: one 12 m bar + 1.7 m from a second bar (bolted splice), or a 14 m special length; 9.8 m beam from the second bar
        bars = math.ceil(net/12.0); note = '13.7 m beam: 12 m bar + 1.7 m piece (splice) or one 14 m special length; the 9.8 m beam uses the rest of the second bar'
    elif s == SEC_R and M.SCHEME == 'ontop':
        cut = []
        for L in Ls: cut += ([L] if L <= 12.0 else [12.0, L - 12.0])   # 13.7 / 11.5 m continuous rafters: one bolted splice at a low-moment point in the lines longer than 12 m
        bars = len(pack(cut)); note = '%d rafter lines up to %.2f m: continuous, %d spliced at a low-moment point (over 12 m)' % (len(Ls) - 1, max(Ls), sum(1 for L in Ls if L > 12))
    else:
        bars = len(pack(Ls)); note = '%d pieces, longest %.2f m' % (len(Ls), max(Ls))
    if s in NOTQ: note += '; not on the quotation, priced by weight at the invoice rate'
    cost = bars*RATE[s]*12; kg = bars*12*KG[s]; total += cost; tot_kg += kg
    rows.append(dict(section=s, net_m=net, bars=bars, bar_m=bars*12, kg=kg, rate_m=RATE[s], rate_t=RATE[s]*1000/KG[s], cost=cost, note=note))
n_pur = math.ceil(L_purlin/6); cost = n_pur*285.0; kg = n_pur*6*KG['Z200']; total += cost; tot_kg += kg
rows.append(dict(section='Z200 purlin, 6 m bars', net_m=L_purlin, bars=n_pur, bar_m=n_pur*6, kg=kg, rate_m=RATE['Z200'], rate_t=RATE['Z200']*1000/KG['Z200'], cost=cost, note='gauge 2.0 mm S350GD to confirm with the supplier'))
cost = L_rod*RATE[RODN]; kg = L_rod*KG[RODN]; total += cost; tot_kg += kg
rows.append(dict(section='%s threaded rod' % RODN, net_m=L_rod, bars=None, bar_m=L_rod, kg=kg, rate_m=RATE[RODN], rate_t=RATE[RODN]*1000/KG[RODN], cost=cost, note='priced from the 60 cm M24 bolt (29 LYD) by weight; ask for rod in 3 m lengths'))
S7 = json.load(open(OUT + '/design/C7/calc/summary_C7%s.json' % os.environ.get('SUMMARY_TAG', '')))
REV = S7.get('rev', '7')
_net = S7['weight']['sections_hot_rolled'] + S7['weight']['wall_bracing']*KG[ANG]/(5.42 if ANG == 'L60x6' else 7.38) + S7['weight']['roof_bracing'] + S7['weight']['purlins_Z200']
plates_kg = S7['weight']['plates_bolts_keys']; plate_rate = 7500.0; plates_cost = plates_kg/1000*plate_rate
res = dict(invoice_total=inv_total, rows=rows, sections_cost=total, sections_kg=tot_kg, plates_kg=plates_kg, plate_rate=plate_rate, plates_cost=plates_cost,
           avg_rate_t=total/tot_kg*1000)
json.dump(res, open(OUT + '/offer/sections_cost_invoice%s.json' % ('_rev' + REV if REV != '7' else ''), 'w'), indent=1)
f = lambda x: '{:,.0f}'.format(x)
md = ['# Steel section cost from the supplier quotation (29 Sep 2026) - design Rev %s\n' % REV,
      'Source: pro-forma invoice 11486, Al-Salama Industrial Steel Trading (محلات السلامة لتجارة الحديد الصناعي), total %s LYD. Its quantities are the **Rev 6a** sections list (8 x 12 m + 1 x 6 m HEA 140, 7 x IPE 300, 1 x IPE 330, 17 x IPE 240, 95 x 6 m purlins, 13 x angle): supply of sections only, no plates, bolts, fabrication, coating or erection.\n' % f(inv_total),
      '## 1. Unit rates from the invoice\n', '| Item | Bar | Price LYD | LYD / m | kg / m | LYD / tonne |', '|---|---|---|---|---|---|']
for no, d, bl, q, p in INV:
    key = {1596: 'HEA 140', 1985: 'HEA 140', 85: 'IPE 300', 83: 'IPE 330', 81: 'IPE 240', 2707: 'Z200', 341: 'L75x7', 1351: 'M24'}[no]
    md.append('| %d %s | %g m | %s | %.1f | %.2f | %s |' % (no, d, bl, f(p), p/bl, KG[key], f(p/bl*1000/KG[key])))
md += ['', 'Supply-only section prices are 7,400-7,900 LYD/t for IPE, about 11,400 LYD/t for HEA 140, 8,050 LYD/t for the purlin (if 2.0 mm) and 7,560 LYD/t for the angle. **The 6,950 LYD/t used so far as an all-in rate (supplied, fabricated, erected) is below the bare material price**, so the cost build-up changes: material at invoice prices plus fabrication, coating and erection as separate items.\n',
       '## 2. Rev %s section bill at invoice prices (12 m stock bars, first-fit cutting plan, 10 mm kerf)\n' % REV, '| Section | Net m | Bars | Bought m | kg | LYD / m | Cost LYD | Cutting note |', '|---|---|---|---|---|---|---|---|']
for r in rows: md.append('| %s | %.1f | %s | %.1f | %s | %.1f | %s | %s |' % (r['section'], r['net_m'], r['bars'] if r['bars'] else '-', r['bar_m'], f(r['kg']), r['rate_m'], f(r['cost']), r['note']))
md += ['| **Sections total** | | | | **%s** | | **%s** | average %s LYD/t on bought weight |' % (f(tot_kg), f(total), f(res['avg_rate_t'])),
       '| Plates, keys, rebars, bolts (%.1f t, not on the invoice) | | | | %s | | %s | assumed %s LYD/t, to be quoted |' % (plates_kg/1000, f(plates_kg), f(plates_cost), f(plate_rate)),
       '| **Material total** | | | | **%s** | | **%s** | |' % (f(tot_kg + plates_kg), f(total + plates_cost)), '',
       'Waste: bought %.0f kg against a net take-off of %.0f kg (%.0f %% offcuts); the offcuts of the rafter and column bars are usable for T3, ST2, the wind posts and stiffeners.\n' % (tot_kg, _net, (tot_kg/_net - 1)*100),
       '## 3. Notes on the quotation\n',
       '- The IPE 330 eave beam K17-K18 is 13.7 m; the stock length is 12 m. Either a 14 m bar is ordered (ask the supplier) or the beam is spliced with a bolted end-plate splice near a rafter, about 3 m from K18.' if 'IPE 330' in pieces else '- No IPE 330: the eave beams bear on the existing columns K28, K29 and K30 (Rev 8a), all primaries in one section.',
       '- The angle offered is 75 x 75 x 7 (7.94 kg/m); the design uses %s (priced by weight at the same rate).' % ANG,
       '- Purlin "galvanised 200, 6 m": confirm Z (not C) profile, 2.0 mm, S350GD, Z275; the design needs sleeved laps at the rafters, so 6 m bars suit the 2.6-4.1 m rafter spacing with one lap per two bays.',
       '- HEA 140 columns: %d columns of about 3.0-3.8 m cut from %d x 12 m bars (three pieces per bar); the 6 m bar is not needed.' % (len(pieces[SEC_C]), rows[0]['bars']),
       '- The M24 item is a 60 cm bolt; the roof rods need about 168 m of threaded rod with turnbuckles, to be quoted as rod.',
       '- Prices are dated 29/09/2026 and imported stock; keep the 15-day offer validity.']
open(OUT + '/cost_sections_invoice%s.md' % ('_rev' + REV if REV != '7' else ''), 'w', encoding='utf-8').write('\n'.join(md) + '\n')   # utf-8: the supplier's name is in Arabic
print('\n'.join(md))
