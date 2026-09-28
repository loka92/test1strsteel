"""S06 bill of materials from members_C.csv + plates and bolts estimate."""
import math
from common import *
from geom import *
OX, OY = 310.0, 8.0
def bom_rows():
    rows = []; raft_ct = {}
    for m in members_csv():
        t, sec, L, mid = m['type'], m['section'], float(m['length']), m['id']
        if t in ('rafter', 'trimmer', 'eave beam', 'primary'):
            line = mid.split('/')[0]
            if t == 'rafter':
                raft_ct[line] = raft_ct.get(line, 0) + 1; mark = '%s.%d' % (RMARK[line], raft_ct[line])
            elif t == 'trimmer': mark = line
            else: mark = PMARK[line]
            rows.append((mark, t, sec, L, 1, mid.split('/')[1] if '/' in mid else ''))
        elif t == 'column': rows.append(('C' + mid[1:], 'column', sec, L, 1, mid))
        elif t == 'wind post': rows.append(('WP1', 'wind post', sec, L, 1, 'notch corner'))
        elif t == 'roof truss post': rows.append((mid, 'truss post', sec, L, 1, 'R9-R11' if mid == 'ST1' else 'R1-R3'))
        elif t == 'wall X-brace': rows.append((mid, 'wall X-brace', sec, L, 2, '%s-%s' % (m['frm'], m['to'])))
    for tid, panels in ROOF_TRUSSES:
        for i, (x0, x1, y0, y1) in enumerate(panels):
            rows.append(('%s.%d' % (tid, i+1), 'roof X-brace', 'M24 rod 8.8', round(math.hypot(x1-x0, y1-y0), 2), 2, 'panel x %.1f-%.1f' % (x0, x1)))
    return rows
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S06', 'BILL OF MATERIALS', 'Lengths in m from members_C.csv Rev 3; weights nominal (kg/m x length), plates by volume x 7850')
    rows = bom_rows()
    tab = []; tot = {}
    for mark, t, sec, L, q, note in rows:
        kg = SEC[sec]['kg'] * L * q; tot[sec] = tot.get(sec, [0, 0, 0]); tot[sec][0] += L*q; tot[sec][1] += kg; tot[sec][2] += q
        tab.append([mark, sec, '%.2f' % L, q, '%.0f' % kg, note])
    cols = [('Mark', 1.5), ('Section', 1.7), ('L m', 0.9), ('n', 0.5), ('kg', 0.8), ('between', 2.4)]
    n = len(tab); per = math.ceil(n / 3)
    for i in range(3):
        sh.table(0.5 + i*8.3, 29.0, cols, tab[i*per:(i+1)*per], 0.36, 0.14, title='MEMBERS (%d-%d of %d)' % (i*per+1, min((i+1)*per, n), n))
    # purlins / girts / eave rail
    pur = sum(b - a for y, a, b in purlin_segments()); pur_n = len(purlin_segments())
    girt = 0.0; girt_n = 0
    for f in FACES:
        for p, q in zip(f['posts'][:-1], f['posts'][1:]):
            (x1, y1), (x2, y2) = POSTXY[p], POSTXY[q]; L = math.hypot(x2-x1, y2-y1); s = girt_spacing(p, q)
            zmax = (prim_top(f['c']) - 0.33 if f['normal'][0] == 'y' else TOS(min(y1, y2)) - 0.27) - 0.15
            k = int((zmax - 0.5)/s) + 1; girt += k*L; girt_n += k
    cf = [('Item', 6.0), ('Section / size', 3.2), ('Qty', 1.2), ('Total m', 1.4), ('kg', 1.2)]
    cf_rows = []
    for sec in ('IPE 330', 'IPE 270', 'HEA 160', 'L 70x7', 'M24 rod 8.8'):
        L, kg, q = tot[sec]; cf_rows.append(['Hot-rolled / bracing members above', sec, '%d' % q, '%.1f' % L, '%.0f' % kg])
    zk = SEC['Z200x2.0']['kg']
    cf_rows += [['Purlins Z200x2.0 @ 1.5 m (%d pieces, 14 rows) + anti-sag' % pur_n, 'Z200x2.0', '%d' % pur_n, '%.1f' % pur, '%.0f' % (pur*zk*1.05)],
                ['Girts Z200x2.0 S350GD (%d pieces) incl. sleeves' % girt_n, 'Z200x2.0', '%d' % girt_n, '%.1f' % girt, '%.0f' % (girt*zk*1.08)],
                ['Eave rails C200x60x2.5 (G-W 10.0 + G-E 13.9) + well header 2 x 3.9', 'C200x60x2.5', '4', '31.7', '%.0f' % (31.7*6.9)], ['Sill rail C100x50x3 (wall base, D11)', 'C100x50x3', '-', '101', '%.0f' % (101*4.0)],
                ['Upstand framing C100x50x3 (both wells)', 'C100x50x3', '-', '90', '%.0f' % (90*4.0)]]
    y2 = sh.table(0.5, 29.0 - (per+1)*0.36 - 0.9, cf, cf_rows, 0.36, 0.15, title='COLD-FORMED AND TOTALS BY SECTION')
    # plates and bolts
    n_raft_ends = 2*sum(1 for r in rows if r[1] in ('rafter', 'trimmer', 'truss post')) + 1
    pl = [('Fin plates 100x150x10 (D1)', n_raft_ends - 8, 0.1*0.15*0.01), ('Fin plates 100x220x10 (D1, 9.2 m rafters)', 8, 0.1*0.22*0.01),
          ('Cap plates 200x280x20 (D2)', 27, 0.2*0.28*0.02), ('Tie plates 140x400x10 (D3, rows F and B)', 8, 0.14*0.40*0.01),
          ('Base plates 300x400x25 (B1 x7 + K21)', 8, 0.3*0.4*0.025), ('Base plates 350x400x25 (B1 edge heads)', 6, 0.35*0.4*0.025), ('Base plates 800x550x30 + 2 stiffeners 120x10 (B2 standard)', 9, 0.8*0.55*0.03 + 2*0.12*0.45*0.01), ('Base plates K7 / K23 / K25 / K27 (500x1000, 1000x550, 550x900, 600x900 x30)', 4, 0.52*0.03 + 2*0.12*0.45*0.01), ('Under-slab plates 400x200x25 (B2)', 13, 0.4*0.2*0.025), ('Key A SHS 90x90x8 x 205 S355 (B1 13 + B2 pairs 26)', 39, 0.00258*0.205), ('Key B dia 60 x 205 S355 (K3, K4 x2, K6 x2, K8, K14) + WP1 key', 8, math.pi*0.03**2*0.205), ('K21 saddle plates 400x150x15', 2, 0.4*0.15*0.015),
          ('Bracing gussets 10 mm ~350x420 (D4)', 40, 0.35*0.42*0.01*0.6), ('Rod gussets 8 mm ~250x250 (D5)', 96, 0.25*0.25*0.008*0.6),
          ('Purlin cleats 120x160x8 (D8)', pur_n*2, 0.12*0.16*0.008), ('Girt cleats L100x100x8 x150 (D9)', girt_n*2, 0.0015*0.15*1.0),
          ('WP1 base plate 250x250x15 + head cleat', 1, 0.25*0.25*0.015 + 0.12*0.2*0.01)]
    pl_rows = [[a, n, '%.1f' % (n*v*7850)] for a, n, v in pl]
    pl_kg = sum(n*v*7850 for a, n, v in pl)
    y3 = sh.table(14.0, y2 - 0.8, [('Plates and fittings', 6.5), ('Qty', 1.0), ('kg', 1.0)], pl_rows, 0.36, 0.15, title='PLATES (S275 unless noted) - estimate')
    bolts = [['M20 8.8 x 60 (fin plates, incl. slotted rows)', n_raft_ends*2 + 8], ['M20 8.8 x 70 (cap plates + tie plates)', 27*4], ['M20 8.8 x 60 (bracing gussets, 2 per angle end)', 80],
             ['M16 8.8 (bracing crossing clips)', 10], ['M24 8.8 rods with turnbuckle, nuts + lock nuts', 48], ['M12 8.8 (purlin / girt cleats, fly braces, eave rail)', (pur_n + girt_n)*4 + 200],
             ['M20 8.8 resin anchors h_ef 200 (B1, 13 bases x 4)', 52], ['M24 8.8 through-bolts x 420 + 60x6 washers (B2, 13 bases x 2)', 26], ['M16 8.8 resin anchors h_ef 400 (K21 pier, pattern by scan)', 4], ['M12 anchors (WP1 location)', 2], ['M8 resin anchors sill rail @ 600 (D11)', 170], ['Key A SHS 90x90x8 x 205 in 140 pockets x 200 (B1 13 + B2 26)', 39], ['Key B dia 60 x 205 in 110 pockets x 200 (7) + WP1 key (1)', 8], ['K21 saddle plates 400x150x15', 2], ['Ceiling openings ~600x600 for the B2 under-slab plates', 13]]
    sh.table(23.5, y2 - 0.8, [('Bolts and anchors (add 5 % spare)', 7.5), ('Qty', 1.2)], bolts, 0.36, 0.15, title='BOLTS AND ANCHORS - estimate')
    hot = tot['IPE 330'][1] + tot['IPE 270'][1] + tot['HEA 160'][1]
    grand = hot + pl_kg + tot['L 70x7'][1] + tot['M24 rod 8.8'][1] + pur*zk*1.05 + girt*zk*1.08 + 31.7*6.9 + 101*4.0 + 360
    sh.note_block(0.5, y2 - 0.8, 'TOTALS', ['Hot-rolled members %.1f t + plates %.1f t = %.1f t' % (hot/1e3, pl_kg/1e3, (hot+pl_kg)/1e3),
        'Wall bracing %.2f t, roof rods %.2f t' % (tot['L 70x7'][1]/1e3, tot['M24 rod 8.8'][1]/1e3), 'Cold-formed Z/C %.1f t' % ((pur*zk*1.05 + girt*zk*1.08 + 31.7*6.9 + 101*4.0 + 360)/1e3),
        'GRAND TOTAL approx. %.1f t (%.0f kg/m2 of 486 m2 footprint, %.0f kg/m2 of 439 m2 roofed)' % (grand/1e3, grand/486, grand/439), 'Report Rev 3 s.10: 24.9 t (BOM before the Rev 4b base plates, sill rail, header).',
        'Galvanising: hot-dip all members and plates; Z/C S350GD Z275.', 'Bases per bases_C.md Rev 4b (B1 13, B2 13, P 1).'], 0.16, 0.3)
    return sh
