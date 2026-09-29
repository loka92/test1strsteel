"""Writes bracing_rev5.md and bracing_rev5.png (Rev 5 bracing rationalisation), from summary_C.json and summary_rev4_baseline.json."""
import json, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from model import COLS, BAYS, RAFTERS, PRIMARIES, ENV, NOTCH, OPEN, NORTH_JOG_X, POSTS
from bracing import ROOF_TRUSSES, ROD, DIAG, roof_bracing_length
SPn, SRn = b_secs = None, None
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..')
a = json.load(open(os.path.join(HERE, 'summary_rev4_baseline.json'))); b = json.load(open(os.path.join(HERE, 'summary_C.json')))
SPn, SRn, twR = b['secs']['prim'], b['secs']['raft'], b['secs']['tw_raft']
f = lambda x, n=1: '%.*f' % (n, float(x))
Lrod, npan = roof_bracing_length()
L = ['# Design C Rev 5a bracing (rationalised, review Z1-Z6 closed) - figures re-run at Rev 6 with the IPE 300 / IPE 240 / HEA 140 sections\n',
     'Forces: design roof-level seismic %s kN E-W / %s kN N-S (two-mass, q 1.5) and wind %s-%s kN char. (x 1.5); every bay and strip is seismic-governed.\n' % (f(b['seismic']['Fb_x'], 0), f(b['seismic']['Fb_y'], 0), f(min(b['wind_roof'].values())), f(max(b['wind_roof'].values()))),
     '## 1. Before / after\n', '| Item | Rev 4 | Rev 5 | Reason |', '|---|---|---|---|',
     '| Roof-plane braced panels (X of M24 rods) | 24 (every rafter cell of both bands, both wings, plus the edge strips and the jog) | **%d** in five strips: north strip west (2), north strip east (3), jog (1), west strip (4), east strip (3) | south bands deleted: the rafters carry the south-half inertia as N-S struts to the y 29.3 chord; north-band rods now span two rafter cells with posts at the column lines |' % npan,
     '| Rods / gussets | 48 rods, 96 gussets, %s m | **%d rods, %d gussets, %s m** | |' % (f(a['lengths']['roof_bracing'], 0), 2*npan, 4*npan, f(Lrod, 0)),
     '| Wall bays (L70x7 X) | 10: B1-B10 | **8: B1, B2, B3, B4 (E-W), B5, B6, B7, B9 (N-S)** | B8 (K10-K16, the interior X in the hall) and B10 (K19-K25) removed: B7 alone carries the x 77.8 line (66.8 kN), B5 alone the x 68 line (49 kN); every remaining base passes with its Rev 5a keys and rebars |',
     '| Truss posts ST1 (y 24.46, R90-R95) / ST2 (y 26.37, R68-R72) | 2 | **2, kept** | they carry the E-wall (K18) and W-wall (K15) column-top loads into the edge trusses; without them the R95 / R68 chords bend about their weak axis (32 / 24 kNm vs 26.7) |',
     '| Bracing tonnage (rods + angles) | %s + %s = %s t | **%s + %s = %s t** | -%s t (plus 44 gussets and 4 bracing base gussets) |' % (f(a['weight']['roof_bracing']/1000, 2), f(a['weight']['wall_bracing']/1000, 2), f((a['weight']['roof_bracing'] + a['weight']['wall_bracing'])/1000, 2), f(b['weight']['roof_bracing']/1000, 2), f(b['weight']['wall_bracing']/1000, 2), f((b['weight']['roof_bracing'] + b['weight']['wall_bracing'])/1000, 2), f((a['weight']['roof_bracing'] + a['weight']['wall_bracing'] - b['weight']['roof_bracing'] - b['weight']['wall_bracing'])/1000, 2)),
     '| Worst bay diagonal / roof rod / base | %s / %s / %s | **%s / %s / %s** | seismic-governed everywhere |' % (f(max(v['util'] for v in a['bays'].values()), 2), f(max(t['util'] for t in a['trusses']), 2), f(a['max_util']['bases'], 2), f(max(v['util'] for v in b['bays'].values()), 2), f(max(t['util'] for t in b['trusses']), 2), f(b['max_util']['bases'], 2)),
     '\n## 2. Diaphragm analysis (strips as horizontal trusses; end shear = the bay force of the line it delivers to, seismic envelope)\n',
     '| Strip | Chords | Posts | Span m | Depth m | Delivers to | Shear V kN | Rod T kN (M24 203) | Chord kN | Post kN | Rod util. | Deflection mm (ULS) |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
desc = {'RT-N-W': ('primaries y 29.3 / y 35.2 (' + SPn + ')', 'rafters R68, R72, R78', 'B5 (x 68), B7 (x 77.8 via R78 strut)'), 'RT-N-E': ('primaries y 29.3 / y 35.7', 'rafters R82, R87, R92, R95', 'B7 (via jog), B6 + B9 (x 95.5)'),
        'RT-JOG': ('primaries y 24.5 / y 29.3', 'rafters R78, R82', 'B7 through R78'), 'RT-W': ('rafters R68 / R72 (' + SRn + ')', 'primaries y 15.9, 21.8, 29.3, 35.2 + ST2', 'B4 (y 15.9), B2 (y 35.2)'), 'RT-E': ('rafters R90 / R95', 'primaries y 20.1, 29.3, 35.7 + ST1', 'B3 (y 20.1), B1 (y 35.7)')}
for t in b['trusses']:
    d = desc[t['id']]
    L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (t['id'], d[0], d[1], f(t['L']), f(t['D']), d[2], f(t['V']), f(t['T']), f(t['chord']), f(t['post']), f(t['util'], 2), f(t['delta'])))
s = b['struts']; sp = b['split']; fins = b['fins']; dr = b['drift_eq']
L += ['\nStruts and chords (axial + bending): purlin lines as E-W struts %s kN (Z200x2.0, N_b,Rd %s kN) -> %s; rafter chords R68/R72/R90/R95 %s kN -> %s (with the 7.5 m gravity moment); primaries y 29.3 as chords %s kN -> %s; eave primaries as struts to B1-B4 %s kN -> %s; rafters as N-S struts (south-half inertia to the y 29.3 chord) %s kN -> %s; R78 as the N-S strut from the north strips down to B7 %s kN -> %s. The strut and chord forces pass through the rafter fin plates: checked in 2b (web bearing governs, not the 188 kN bolt shear).\n' % (
    f(s['purlin']['N']), f(s['purlin']['NbRd'], 0), f(s['purlin']['u'], 2), f(s['rafter_chord']['N']), f(s['rafter_chord']['u'], 2), f(s['primary_chord']['N']), f(s['primary_chord']['u'], 2), f(s['eave_strut']['N']), f(s['eave_strut']['u'], 2), f(s['rafter_strut']['N']), f(s['rafter_strut']['u'], 2), f(s['R78_strut']['N']), f(s['R78_strut']['u'], 2)),
      '### 2a. Actual strip end shears and line forces (Z4)\n',
      'The rod design above takes V_end = the enveloped force of the line each strip delivers to (conservative, kept). The actual split, from the tributary N-S inertia of each block (roof grid) scaled per line so that the line totals equal the enveloped bay forces: RT-N-W %s kN to x 68 (R68 -> B5) and %s kN to x 77.8; jog panel %s kN to x 77.8; RT-N-E %s kN to x 77.8 (R82 -> jog -> R78) and %s kN to x 95.5 (R95 -> B6 + B9). Line forces: **R68 %s kN, R78 %s kN (= B7, not the sum of the strip end shears), R82 %s kN, R95 %s kN**.\n' % (f(sp['actual']['RT_N_W'][0]), f(sp['actual']['RT_N_W'][1]), f(sp['actual']['RT_JOG']), f(sp['actual']['RT_N_E'][0]), f(sp['actual']['RT_N_E'][1]), f(sp['R68']), f(sp['R78']), f(sp['R82']), f(sp['R95'])),
      '### 2b. Strut / chord forces through the rafter fin plates (Z1)\n',
      'N = envelope of E_y + 0.3 E_x and E_x + 0.3 E_y (strut = N-S line force, chord = strip chord force at the splice); V = gravity end shear of the segment (G + Q, psi_2 = 0 in the seismic combination). Fin plate 10 mm S275, M20 8.8 (pitch 70, e1 = e2 = 40), bolt line 50 mm from the primary web; the strip-chord splices use two rows (2 x 2 M20, p2 60, plate 160 x 150) because the ' + SRn + ' web (190 mm clear) takes no 3-bolt row. Bearing on the %s mm ' % twR + SRn + ' web governs: %s kN per bolt with one row, %s kN with two rows (lesser of the two force directions), bolt shear 94 kN, plate net section, weld a 6 both sides; the force passes through the ' % (f(next(x['FbRd'] for x in fins if x['cols'] == 1)), f(next(x['FbRd'] for x in fins if x['cols'] == 2))) + SPn + ' primary web plate-weld-web-weld-plate (web in through-thickness bearing, < 0.05).\n',
      '| Member | Fin plates at | N strut kN | N chord kN | N design kN | V kN | Bolts | Web bearing | Bolt shear | Plate net | Weld | Note |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
for v in fins:
    L.append('| %s | %s | %s | %s | %s | %s | %s | **%s** | %s | %s | %s | %s |' % (v['member'], v['where'], f(v['N_strut']), f(v['N_chord']), f(v['N']), f(v['V']), v['bolts'], f(v['u_bearing'], 2), f(v['u_bolt'], 2), f(v['u_net'], 2), f(v['u_weld'], 2), v['note']))
L += ['\nWith a single row of 2 M20 the chord rafters R68 / R95 would exceed 0.6 in web bearing, so their splices (and R72 / R90, the other strip chords) get the 2 x 2 M20 plate; R78 stays at 2 M20 (%s <= 0.6).' % f(next(x['umax'] for x in fins if x['member'] == 'R78'), 2) + ' Purlin lines: 3.4 kN through the 2 M12 cleats (bearing on the 2.0 mm Z flange 2 x 16 kN, 0.11). Eave and row-F primaries: %s kN through the 4 M20 of the cap plate (bolt shear + tension interaction %s). Bracing gussets at the NE corner (K2, K4, K13, K14): both rod sets concurrently, E_x + 0.3 E_y - rod forces %s + 0.3 x %s kN on a 10 mm gusset, 2 M20 per rod end (crossings and the R92 web clip to be drawn on S04 by detailing).\n' % (f(s['eave_strut']['N']), f(b['cap']['util']['bolt interaction'], 2), f(max(t['T'] for t in b['trusses'] if t['id'] == 'RT-E')), f(max(t['T'] for t in b['trusses'] if t['id'] == 'RT-N-E'))),
      '### 2c. Seismic drift, EN 1998-1 4.4.3.2 (Z3)\n',
      'd_e = roof-truss deflection at the wall mid-length under the design (q 1.5) force + bay sway (+ strut strain); d_r = q d_e; nu = 0.5; limit 0.005 h for brittle cladding, h = TOS at the location.\n',
      '| Line | d_e mm | nu d_r mm | 0.005 h mm | Ratio |', '|---|---|---|---|---|']
for k, v in dr.items(): L.append('| %s | %s | %s | %s | %s |' % (k, f(v['de']), f(v['dr_nu']), f(v['lim']), f(v['u'], 2)))
L += ['\nPasses everywhere; the west wall (13.3 vs 19.7 mm) governs.\n',
      '### 2d. Erection (Z5) and purlin data (Z6)\n',
      '- The south bands have no plan bracing until the sandwich panels are fixed: the erector shall place temporary plan bracing (crossed wire ropes or angles) in one rafter cell of each south band (west wing R70-R72 / y 15.9-21.8, east wing R85-R87 / y 20.1-29.3) or guy the wall columns, and keep it until the roof panels and the purlin bridging are complete - to be written into the S05 sequence by detailing. The permanent strips (north bands, jog, west / east edge) are erected and pinned with the first rafters of each block.',
      '- Purlin strut check: Z200x2.0 S350GD, A 7.4 cm2, i_min 20 mm (principal minor axis; catalogue values 21-23 mm for Z200x65x2.0), buckling length 3.07 m between rafters - the supplier is to confirm A and i_min; with the sheeting fixed to the top flange the real length is the bridging spacing, so the 0.41 (mostly gravity bending) is an upper bound.\n',
      '## 3. Wall bays: why each remaining bay is needed\n',
      '| Bay | Columns | H_Ed kN (seismic / wind ULS) | Diagonal | Why it stays |', '|---|---|---|---|---|']
why = {'B1': 'only E-W bay on the east north wall: the y 35.7 eave line cannot pass the stair-well jog to B2', 'B2': 'only E-W bay on the west north wall; north support of the west strip RT-W and of the thermal path', 'B3': 'only E-W bay on the south (notch) wall; south support of the east strip RT-E', 'B4': 'only E-W bay on the west-wing south wall; south support of RT-W (the y 15.9 and y 20.1 eave lines are linked only through the weak axis of R78)',
       'B5': 'the x 68 line now has one bay: takes the west strip reaction (49 kN); K15 / K19 keys and rebars pass (0.36)', 'B6': 'east wall line with B9: K14 has Key A only and its parallel-edge value (44 kN at c1 155) needs the line force shared', 'B7': 'the x 77.8 line now has one bay: takes the east reactions of both north strips through R78 (66.8 kN); K20 / K27 key pairs 0.48 / 0.52', 'B9': 'shares the x 95.5 line with B6 (35.5 kN each) and keeps the net uplift at K18 near zero'}
for i, v in b['bays'].items():
    L.append('| %s | %s | %s / %s | %s | %s |' % (i, '-'.join(next(bb['c'] for bb in BAYS if bb['id'] == i)), f(b['bay_gov'][i]['seis']), f(b['bay_gov'][i]['wind']), f(v['util'], 2), why[i]))
L += ['\nRemoved: **B8 (K10-K16)** - the interior X in the hall; its role (west support of the jog panel) is taken by R78 as a strut down to B7. **B10 (K19-K25)** - added at Rev 2 only to keep the net uplift off K19 when the S-wind uplift was 73 kN; with the Rev 3 loads K19 sees 49 kN (rebar 0.36) and B5 alone carries the line.\n',
      '## 4. Rules respected\n',
      '- No bay shear towards a free slab edge without a key: every remaining braced-bay base keeps its Rev 5a key pair (K1, K2, K5, K7, K15, K18, K19, K20, K22, K23, K25, K27) or Key A + B (K14); no base type changed.',
      '- Torsion of the L-shape with 5 % eccentricity: rigid-diaphragm and tributary distributions enveloped with the 8 bays (bay forces in the table).',
      '- DCL, q 1.5, tension-only X, L70x7 unchanged; door-free bays for the client: B1 K1-K2, B2 K5-K7, B3 K22-K23, B4 K25-K26, B5 K15-K19, B6 K14-K18, B7 K20-K27, B9 K18-K23 (no interior bay any more).',
      '- Both openings: the stair well is passed by the jog panel (y 24.5-29.3) and R78; the elevator opening lies south of the jog and below the west/east strips - no strip crosses it.',
      '- Thermal path B2 - RT-N-W - y 29.3 - RT-N-E - B1: k_eff %s kN/mm, %s / %s kN ULS (wind / erection) on B1, B2 - not governing.\n' % (f(b['thermal']['keff'], 1), f(b['thermal']['F_uls_wind'], 0), f(b['thermal']['F_uls_erect'], 0)),
      '- North-east corner: the last panel of the north strip east (x 92.5-95.5) and the first panel of the east strip (y 29.3-35.7) share the corner cell; both rod sets are kept (different chord/post pairs), gussets combined at K2, K4, K13, K14.\n',
      'Figure: bracing_rev5.png (columns, primaries, rafters thin; braced strips and wall bays bold).']
open(os.path.join(OUT, 'bracing_rev5.md'), 'w').write('\n'.join(L) + '\n')
# ---- figure
fig, ax = plt.subplots(figsize=(13, 9.5))
bx = [ENV['x0'], NORTH_JOG_X, NORTH_JOG_X, ENV['x1'], ENV['x1'], NOTCH['x0'], NOTCH['x0'], ENV['x0'], ENV['x0']]
by = [35.37, 35.37, ENV['y1'], ENV['y1'], NOTCH['y1'], NOTCH['y1'], ENV['y0'], ENV['y0'], 35.37]
ax.plot(bx, by, 'k-', lw=0.8)
for k, op in OPEN.items():
    ax.add_patch(plt.Rectangle((op['x0'], op['y0']), op['x1'] - op['x0'], op['y1'] - op['y0'], fc='0.93', ec='0.4', hatch='//', lw=0.6))
for r in RAFTERS: ax.plot([r['x'], r['x']], [r['y0'], r['y1']], color='0.6', lw=0.8)
for p in PRIMARIES: ax.plot([p['x0'], p['x1']], [p['y'], p['y']], color='0.3', lw=1.6)
for (x0, x1, yy) in ((89.90, 95.55, 24.46), (67.99, 72.09, 26.37)): ax.plot([x0, x1], [yy, yy], color='0.3', lw=1.6)
for t in ROOF_TRUSSES:
    for (x0, x1, y0, y1) in t['panels']:
        ax.plot([x0, x1], [y0, y1], color='tab:green', lw=2.2); ax.plot([x0, x1], [y1, y0], color='tab:green', lw=2.2)
        ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fc='none', ec='tab:green', lw=1.0, ls=':'))
    p = t['panels'][len(t['panels'])//2]; ax.text(0.5*(p[0] + p[1]), 0.5*(p[2] + p[3]) + 0.35, t['id'], color='darkgreen', fontsize=8, ha='center', fontweight='bold')
for bb in BAYS:
    (x1, y1), (x2, y2) = COLS[bb['c'][0]], COLS[bb['c'][1]]
    ax.plot([x1, x2], [y1, y2], color='red', lw=7, alpha=0.5, solid_capstyle='butt')
    ax.text(0.5*(x1 + x2) + (0.4 if bb['dir'] == 'y' else 0), 0.5*(y1 + y2) + (0.5 if bb['dir'] == 'x' else 0), bb['id'], color='red', fontsize=9, ha='center', fontweight='bold', rotation=0 if bb['dir'] == 'x' else 90)
for c, (x, y) in COLS.items():
    ax.add_patch(plt.Rectangle((x - 0.2, y - 0.2), 0.4, 0.4, fc='k', ec='k', zorder=5)); ax.text(x + 0.25, y - 0.5, c, fontsize=6.5, color='0.2')
ax.text(78.3, 22.5, 'R78 strut\nto B7', fontsize=7, color='darkgreen'); ax.text(87.5, 26.5, 'rafters as N-S struts\n(south band unbraced)', fontsize=7, color='0.3', ha='center')
ax.set_aspect('equal'); ax.set_xlim(66.5, 97.5); ax.set_ylim(14, 37.5); ax.set_xlabel('x (m)'); ax.set_ylabel('y (m)')
ax.set_title('Design C Rev 6 (Rev 5a bracing, IPE 300 / IPE 240 sections) - 5 roof strips (%d X panels, M24 rods, green) and 8 wall bays (L70x7, red); ST1 / ST2 kept as truss posts' % npan, fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'bracing_rev5.png'), dpi=150); plt.close(fig)
print('bracing_rev5 written')
