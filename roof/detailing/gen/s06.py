"""S06 bill of materials from members_C.csv Rev 6 (P13 as IPE 330) + plates, bolts, anchors, cold-formed."""
import math
from common import *
from geom import *
OX, OY = 310.0, 8.0
def bom_rows():
    rows = []; raft_ct = {}
    for m in members_csv():
        t, sec, mid = m['type'], m['section'], m['id']
        if t in ('diaphragm strut/chord', 'strut/chord fin plates'): continue
        L = float(m['length']) if m['length'] else 0.0
        if t in ('rafter', 'trimmer', 'eave beam', 'primary'):
            line = mid.split('/')[0]
            if t == 'rafter': raft_ct[line] = raft_ct.get(line, 0) + 1; mark = '%s.%d' % (RMARK[line], raft_ct[line])
            elif t == 'trimmer': mark = line
            else: mark = PMARK[line]
            if mark == 'P13': sec = 'IPE 330'
            rows.append((mark, t, sec, L, 1, mid.split('/')[1] if '/' in mid else ''))
        elif t == 'column': rows.append(('C' + mid[1:], 'column', sec, L, 1, mid))
        elif t == 'wind post': rows.append(('WP1', 'wind post', sec, L, 1, 'notch corner'))
        elif t == 'roof truss post': rows.append((mid, 'truss post', sec, L, 1, 'R9-R11' if mid == 'ST1' else 'R1-R3'))
        elif t == 'wall X-brace': rows.append((mid, 'wall X-brace', sec, L, 2, '%s-%s' % (m['frm'], m['to'])))
    for tid, panels in ROOF_TRUSSES:
        for i, (x0, x1, y0, y1) in enumerate(panels): rows.append(('%s.%d' % (tid, i+1), 'roof X-brace', 'M24 rod 8.8', round(math.hypot(x1-x0, y1-y0), 2), 2, 'panel x %.1f-%.1f' % (x0, x1)))
    return rows
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S06', 'BILL OF MATERIALS', 'Lengths in m from members_C.csv Rev 6a; weights nominal (kg/m x length), plates by volume x 7850')
    rows = bom_rows(); tab = []; tot = {}
    for mark, t, sec, L, q, note in rows:
        kg = SEC[sec]['kg'] * L * q; tot[sec] = tot.get(sec, [0, 0, 0]); tot[sec][0] += L*q; tot[sec][1] += kg; tot[sec][2] += q
        tab.append([mark, sec, '%.2f' % L, q, '%.0f' % kg, note])
    cols = [('Mark', 1.4), ('Section', 1.6), ('L m', 0.85), ('n', 0.5), ('kg', 0.8), ('between', 2.5)]
    n = len(tab); per = math.ceil(n / 3)
    for i in range(3): sh.table(0.5 + i*8.1, 28.9, cols, tab[i*per:(i+1)*per], 0.36, 0.14, title='MEMBERS (%d-%d of %d)' % (i*per+1, min((i+1)*per, n), n))
    pur = sum(b - a for y, a, b in purlin_segments()); pur_n = len(purlin_segments()); girt = 0.0; girt_n = 0
    for f in FACES:
        for p, q in zip(f['posts'][:-1], f['posts'][1:]):
            (x1, y1), (x2, y2) = POSTXY[p], POSTXY[q]; L = math.hypot(x2-x1, y2-y1); s = girt_spacing(p, q)
            zmax = (prim_top(f['c']) - 0.30 if f['normal'][0] == 'y' else TOS(min(y1, y2)) - 0.24) - 0.15
            k = int((zmax - 0.5)/s) + 1; girt += k*L; girt_n += k
    zk = SEC['Z200x2.0']['kg']
    cf = [('Item', 6.6), ('Section', 2.0), ('Qty', 0.9), ('Total m', 1.2), ('kg', 1.0)]
    cf_rows = [['Hot-rolled / bracing members above', s, '%d' % tot[s][2], '%.1f' % tot[s][0], '%.0f' % tot[s][1]] for s in ('IPE 300', 'IPE 330', 'IPE 240', 'HEA 140', 'L 70x7', 'M24 rod 8.8') if s in tot]
    cf_rows += [['Purlins Z200x2.0 @ 1.5 m (%d pcs) + anti-sag' % pur_n, 'Z200x2.0', '%d' % pur_n, '%.1f' % pur, '%.0f' % (pur*zk*1.05)],
                ['Girts Z200x2.0 (%d pcs) incl. sleeves' % girt_n, 'Z200x2.0', '%d' % girt_n, '%.1f' % girt, '%.0f' % (girt*zk*1.08)],
                ['Eave rails C200 (G-W 10.0 + G-E 13.9) + well header 2 x 3.9', 'C200x60x2.5', '4', '31.7', '%.0f' % (31.7*6.9)],
                ['Sill rail C100x50x3 (D11)', 'C100x50x3', '-', '101', '%.0f' % (101*4.0)], ['Upstand framing C100x50x3 (both wells)', 'C100x50x3', '-', '90', '360']]
    y2 = sh.table(0.5, 28.9 - (per+1)*0.36 - 0.9, cf, cf_rows, 0.36, 0.14, title='COLD-FORMED AND TOTALS BY SECTION')
    nraft = sum(1 for r in rows if r[1] in ('rafter', 'trimmer', 'truss post')); nfp2 = 4*4
    pl = [('Fin plates FP1 100x150x10 (D1)', 2*nraft + 1 - nfp2, 0.1*0.15*0.01), ('Fin plates FP2 160x150x10 (D1, chord splices)', nfp2, 0.16*0.15*0.01),
          ('Cap plates 200x280x20 (D2)', 27, 0.2*0.28*0.02), ('Tie plates 140x400x10 (D3, rows F and B)', 8, 0.14*0.40*0.01),
          ('Base plates 300x400x20 (type E x13 + K21)', 14, 0.3*0.4*0.02), ('Key-pair plates 800x400x20 (K1, K2, K5, K10, K22)', 5, 0.8*0.4*0.02), ('Key-pair plates 400x800x20 (K15, K18, K19, K20)', 4, 0.4*0.8*0.02),
          ('Key-pair plates K7 400x950, K23 1000x400, K25 / K27 400x850 x20', 4, 0.36*0.02), ('Key A SHS 90x90x8 x 205 S355 (14 + 13 pairs)', 40, 0.00258*0.205), ('Key B dia 60 x 205 S355 (K3, K4 x2, K6 x2, K8, K14) + WP1', 8, math.pi*0.03**2*0.205),
          ('K21 saddle plates 400x150x15', 2, 0.4*0.15*0.015), ('Bracing gussets 10 mm ~350x420 (D4)', 32, 0.35*0.42*0.01*0.6), ('Rod gussets 8 mm ~250x250 (D5, 13 panels)', 52, 0.25*0.25*0.008*0.6),
          ('Purlin cleats 120x160x8 (D8)', pur_n*2, 0.12*0.16*0.008), ('Girt cleats L100x100x8 x150 (D9)', girt_n*2, 0.0015*0.15), ('WP1 base plate 250x250x15 + head cleat', 1, 0.25*0.25*0.015 + 0.12*0.2*0.01)]
    pl_rows = [[a, n_, '%.1f' % (n_*v*7850)] for a, n_, v in pl]; pl_kg = sum(n_*v*7850 for a, n_, v in pl)
    sh.table(14.2, y2 - 0.8, [('Plates and fittings (S275 unless noted)', 7.2), ('Qty', 0.9), ('kg', 1.0)], pl_rows, 0.36, 0.14, title='PLATES - estimate')
    bolts = [['M20 8.8 x 60 (fin plates FP1 / FP2)', 2*nraft*2 + 2*nfp2], ['M20 8.8 x 70 (cap + tie plates)', 27*4], ['M20 8.8 x 60 (bracing gussets, 2 per angle end)', 64], ['M16 8.8 (rod gussets 2 per rafter leg; crossing clips)', 52*2 + 8],
             ['M24 8.8 rods with turnbuckle, nuts + lock nuts', 26], ['M12 8.8 (purlin / girt cleats, fly braces, eave rail)', (pur_n + girt_n)*4 + 200],
             ['dia 16 B500 post-installed bars M16 threaded, EAD 330087 injection (27 bases x 4)', 108], ['M12 anchors (WP1 location)', 2], ['M8 resin anchors sill rail @ 600 (D11)', 170],
             ['Key A pockets 140 x 200 cored; Key B pockets 110 x 200', 40 + 8], ['Pilot holes 10 x 600 + production holes 20 x 600 (bars)', 108]]
    sh.table(24.0, y2 - 0.8, [('Bolts, bars and anchors (add 5 % spare)', 9.4), ('Qty', 1.0)], bolts, 0.36, 0.14, title='BOLTS AND ANCHORS - estimate')
    hot = sum(tot[s][1] for s in ('IPE 300', 'IPE 330', 'IPE 240', 'HEA 140') if s in tot); brac = tot['L 70x7'][1] + tot['M24 rod 8.8'][1]; cold = pur*zk*1.05 + girt*zk*1.08 + 31.7*6.9 + 101*4.0 + 360
    grand = hot + pl_kg + brac + cold
    sh.note_block(0.5, y2 - 0.8, 'TOTALS', ['Hot-rolled members %.1f t + plates %.1f t = %.1f t' % (hot/1e3, pl_kg/1e3, (hot+pl_kg)/1e3), 'Wall bracing + roof rods %.2f t; cold-formed Z/C %.1f t' % (brac/1e3, cold/1e3),
        'STEEL WEIGHT %.1f t (%.0f kg/m2 of 486 m2 footprint, %.0f kg/m2 of 439 m2 roofed)' % (grand/1e3, grand/486, grand/439), 'Design report Rev 6a s.10: BOM basis 22.1 t (P13 IPE 330 + 70 kg).',
        'Galvanising: hot-dip all members and plates; Z/C S350GD Z275. Bases per bases_C.md Rev 8 (type E, P at K21).'], 0.16, 13.0)
    return sh
