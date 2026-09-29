"""S00 general notes: sheet index, load basis Rev 3, materials, bolts, welding, galvanising, tolerances, erection, site verification, open items; isometric key view."""
import math
from common import *
from geom import *
OX, OY = 10.0, 8.0
SHEETS = [('S00', 'General notes, sheet index, isometric key view'), ('S01', 'Roof framing plan'), ('S01a', 'Enlarged partial plans EP-A to EP-D (2x)'), ('S02', 'Column schedule and wall elevations'),
          ('S03', 'Typical sections A-A, B-B, C-C'), ('S04', 'Connection details D1-D8'), ('S04a', 'Connection details D9-D11 and connection notes'), ('S05', 'Base details type E / P / WP1 and schedule'), ('S06', 'Bill of materials')]
def iso(sh, x0, y0, s=0.36):
    """Simplified 3D wireframe (columns, primaries, rafters, wall bays, roof rods) projected to an isometric from the north-east."""
    o = 'iso'; ang = math.radians(30)
    def P(x, y, z):
        u = x - 67.89; v = y - 15.57                 # view from the NE: east to the left, north towards the viewer (down)
        return (x0 + (v - u)*math.cos(ang)*s + 27.8*math.cos(ang)*s, y0 + (48.1 - (u + v))*math.sin(ang)*s + z*s)
    def L(a, b, layer, lw=13): sh.line(*P(*a), *P(*b), layer, owner=o, lineweight=lw)
    pts = [(67.89,15.57), (77.89,15.57), (77.89,19.97), (95.69,19.97), (95.69,35.87), (81.79,35.87), (81.79,35.37), (67.89,35.37)]
    for a, b in zip(pts, pts[1:] + pts[:1]): L((a[0], a[1], 0), (b[0], b[1], 0), 'S-EXIST', 15)
    for k, c in COLS.items(): L((c['cx'], c['cy'], 0), (c['cx'], c['cy'], col_top(c['cy'])), 'S-COL', 25)
    L((WP1[0], WP1[1], 0), (WP1[0], WP1[1], TOS(19.97)-0.3), 'S-COL', 25)
    for p in PRIMARIES: L((p['x0'], p['y'], prim_top(p['y'])), (p['x1'], p['y'], prim_top(p['y'])), 'S-PRIM', 35)
    for st in POSTS: L((st['x0'], st['y'], TOS(st['y'])), (st['x1'], st['y'], TOS(st['y'])), 'S-RAFT', 18)
    for r in RAFTERS: L((r['x'], r['y0'], TOS(r['y0'])), (r['x'], r['y1'], TOS(r['y1'])), 'S-RAFT', 25)
    for tid, panels in ROOF_TRUSSES:
        for (xa, xb, ya, yb) in panels: L((xa, ya, TOS(ya)-0.12), (xb, yb, TOS(yb)-0.12), 'S-BRACE', 13); L((xa, yb, TOS(yb)-0.12), (xb, ya, TOS(ya)-0.12), 'S-BRACE', 13)
    for b, d, (a, c) in BAYS:
        (x1, y1), (x2, y2) = KXY[a], KXY[c]; L((x1, y1, 0.15), (x2, y2, col_top(y2)+0.15), 'S-BRACE', 13); L((x1, y1, col_top(y1)+0.15), (x2, y2, 0.15), 'S-BRACE', 13)
    sh.text(x0, y0 + 11.3, 'KEY VIEW - isometric from the NE, panel and purlins hidden; renders in roof/3d/iso_NE_no_panel.png', 0.16, 'S-TEXT-NOTE', allowed=(o,), owner=o)
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S00', 'GENERAL NOTES AND SHEET INDEX', 'Not to scale; all sheets 42 x 30 m frames side by side in model space (y 8-38)')
    sh.table(0.5, 29.0, [('Sheet', 1.2), ('Title', 8.4)], [[a, b] for a, b in SHEETS], 0.36, 0.16, title='SHEET INDEX')
    y = sh.note_block(0.5, 25.2, 'GENERAL NOTES (numbered)', [
        'Design basis: EN 1990 / 1991-1-1 / 1991-1-4 / 1993-1-1 / 1993-1-8 / 1998-1, EN 1992-1-1 8.4 and EN 1992-4 for the anchorage. Site Tripoli, Libya. Design report C Rev 6a, load basis Rev 3, bases_C.md Rev 8, bracing Rev 5a. Roof: one plane at 6 % falling north, TOS(y) = 3.33 + 0.06 (35.87 - y); primary top TOS + 0.03; column top TOS - 0.29; clear height 3.03 m under the cap-plate nuts at C1/C2, 3.07 m under the eave primary.',
        'Load basis Rev 3: panel 0.12, purlins 0.05, services 0.10 kN/m2 (permanent); imposed category H q_k 0.40 kN/m2 (psi 0), Q_k 1.0 kN; no wall weight in G (wall mass 0.30 kN/m2 in the seismic mass); G_min 0.17 + steel; gutter 0.25 / -0.50 kN/m; upstands 0.30 kN/m. Wind v_b 27 m/s, q_p by direction: N 1.25, E / W 1.05, S 0.75 kN/m2 (flat-roof coefficients, e = 18 m, z_e 9 m), c_pi +0.2 / -0.3. Seismic a_g 0.10 g, S 1.2, q 1.5, two-mass floor amplification MANDATORY: design roof-level force 133 kN E-W / 134 kN N-S (bays and bases seismic-governed). Temperature +/-30 K service, +45/-25 K erection. Combinations EN 1990 6.10.',
        'Materials: hot-rolled S275 J0 (EN 10025-2); shear keys SHS 90x90x8 and Key B bars S355; plates S275; cold-formed Z200x2.0 / C sections S350GD+Z275; PIR sandwich panel 50 mm; BoardX wall panels (0.30 kN/m2, product data to be confirmed); non-shrink cementitious grout C50 class; post-installed bars dia 16 B500 with an EAD 330087 injection system.',
        'Bolts: 8.8 (EN 15048 / ISO 4014-4032) hot-dip galvanised, snug tight + 1/4 turn where noted, no preload relied upon; M20 in 22 round holes, M16 in 18, M12 in 14, M24 rods in 26 with turnbuckles and lock nuts; NO slotted holes (thermal path designed for).',
        'Welding: shop fillet welds a5-a8 as detailed (E42 consumables, EN 1090-2 EXC2); no site welding on galvanised steel; rod gussets shop-welded to the primaries and bolted to the rafters.',
        'Galvanising: hot-dip EN ISO 1461 (85 um) after fabrication for all members, plates and gussets; site touch-up zinc-rich; Z / C sections Z275.',
        'Tolerances (EN 1090-2 class 1): base position +/- 10 mm, plumb h/300 (max 10 mm), primary level +/- 5 mm at the cap, rafter TOS +/- 10 mm; bar pattern +/- 15 mm from the scan, never closer than 20 mm to a bar; grout bed 25 +/- 5 mm; column lengths NOMINAL - cut to the surveyed plate-top level.',
        'Erection sequence: (1) slab-top survey (datum), scans, cores, proof tests, acceptance per head; (2) core the key pockets, set shims and level; (3) columns C1-C27 and WP1 on the keys, grout pockets and beds, drill and set the bars through the plates, cure, nuts snug + 1/4 turn; (4) primaries P1-P19 on the cap plates (4 M20, tie plates rows F and B), temporary guys; (5) rafters R1-R11, T2, ST1/ST2 on fin plates FP1/FP2; (6) wall bays B1-B7, B9 and the 13 rod panels (turnbuckles snug, lock nuts), release guys; (7) TEMPORARY PLAN BRACING (crossed wire ropes or angles) in one rafter cell of each south band (west wing R2-R3 / y 15.9-21.8, east wing R7-R8 / y 20.1-29.3) or guyed wall columns, kept until the panels and the purlin bridging are complete; (8) purlins, fly braces, eave rails, girts, anti-sag rows; (9) roof panels from the south (high) edge north, well upstands and flashings, gutters and downpipes, wall panels and sills. No panel before all permanent bracing is in.',
        'Site verification before any drilling: slab-top level survey; cover-meter scan of all four faces of every column head (top 600 mm: bars, links, cover); GPR from above at all 27 heads (slab solid and 300 mm thick under the plates and pockets, slab top bars); 3-6 cores for the concrete grade; 10 mm pilot drills with feed monitoring; proof tests of 3 bars to >= 60 kN (2 min, <= 1 mm); scan sheet with the final pattern filed per head (S05).',
        'Existing structure: the roof adds about 257 kN characteristic gravity (+ 116 kN if the walls are counted), 62 kN characteristic roof-level wind and 133 / 134 kN design seismic force into the 27 pinned 20 x 40 concrete columns and foundations; as-built drawings, the adequacy statement of the existing columns / foundations and the roof survey are client / structural open items to be closed before the permit.',
        'Open items: v_b 27 m/s and the terrain sectors to be confirmed (LNMC); purlin uplift capacity >= 9 kNm and sleeved girt capacities (supplier); BoardX data and drift limit; ambient-vibration period of the existing building (seismic amplification); door-free bays B1-B7, B9 and R6 over the shaft east wall (client); gutter manufacturer data, yard gullies, well outlets and hall-side well walls (architect / mechanical); notch edge beam at WP1 (GPR); client option B1 for the 7 interior columns (bases_C.md appendix).'], 0.16, 26.0, numbered=True)
    iso(sh, 26.8, 4.4)
    sh.legend_block([('S-PRIM','line','Primaries IPE 300 (P13 IPE 330)'), ('S-RAFT','line','Rafters IPE 240'), ('S-COL','line','Columns HEA 140'), ('S-BRACE','dash','Wall bays / roof rods'), ('S-EXIST','line','Existing slab outline')], 28.5, 17.0, 12.6)
    return sh
