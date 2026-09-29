"""S01a enlarged partial plans (2x) of the dense areas."""
from common import *
from geom import *
from plan import Plan, inside
from s01 import dbubble
OX, OY = 360.0, 8.0
def partial(sh, R, lx0, ly0, title, tag):
    pl = Plan(sh, R[0], R[1], lx0, ly0, 2.0, R); W, H = (R[2]-R[0])*2, (R[3]-R[1])*2
    sh.rect(lx0, ly0, lx0+W, ly0+H, 'S-TITLE', owner=tag, lineweight=35); sh.text(lx0, ly0+H+0.35, title, TH_TITLE, 'S-TEXT-NOTE', allowed=(tag,), owner=tag)
    pl.existing(); pl.openings(label=False); pl.purlins(); pl.members(); pl.columns(); pl.bracing(); pl.gutters()
    pl.mark_members(with_sections=True); pl.mark_bracing(sections=True)
    return pl
def fin_marks(sh, pl):
    """FP1 / FP2 at every rafter-primary junction inside the region; RG / RG-C rod gusset marks at panel corners."""
    for r in RAFTERS:
        for (y, sup) in r['sup']:
            if not inside(r['x'], y, pl.R): continue
            fp = FIN2.get(r['mark'], 'FP1')
            bnd = (pl.lx0, pl.ly0, pl.lx0 + (pl.R[2]-pl.R[0])*2, pl.ly0 + (pl.R[3]-pl.R[1])*2)
            sh.label(fp, *pl.L(r['x'], y), h=TH_DIM, layer='S-TEXT-DIM', cands=[(0.25, 0.25, 'LEFT'), (-0.25, 0.25, 'RIGHT'), (0.25, -0.45, 'LEFT'), (-0.25, -0.45, 'RIGHT'), (0.8, 0.6, 'LEFT'), (-0.8, 0.6, 'RIGHT'), (0.8, -0.8, 'LEFT'), (-0.8, -0.8, 'RIGHT')], allowed=(r['mark'],), bounds=bnd)
    nodes = rod_gusset_nodes(); comb = {KXY[k] for k in COMBINED_GUSSETS}
    for (x, y) in nodes:
        if not inside(x, y, pl.R): continue
        bnd = (pl.lx0, pl.ly0, pl.lx0 + (pl.R[2]-pl.R[0])*2, pl.ly0 + (pl.R[3]-pl.R[1])*2)
        s = 'RG-C' if any(abs(x-cx) < 0.15 and abs(y-cy) < 0.15 for cx, cy in comb) else 'RG'
        sh.label(s, *pl.L(x, y), h=TH_DIM, layer='S-TEXT-DIM', cands=[(-0.25, -0.45, 'RIGHT'), (0.25, -0.45, 'LEFT'), (-0.25, 0.25, 'RIGHT'), (0.25, 0.25, 'LEFT'), (-0.9, -0.9, 'RIGHT'), (0.9, -0.9, 'LEFT'), (-0.9, 0.7, 'RIGHT'), (0.9, 0.7, 'LEFT')], bounds=bnd)
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S01a', 'ENLARGED PARTIAL PLANS EP-A TO EP-D (2x)', 'Partial plans at 2x (1 m model = 500 mm); dimension text in mm (dimlfac 500)')
    sh.legend_block([('S-PRIM','line','Primaries IPE 300'), ('S-RAFT','line','Rafters IPE 240'), ('S-COL','box','Columns HEA 140'), ('S-BRACE','dash','Roof rods M24'), ('S-TEXT-DIM','line','FP1/FP2 fin plates, RG gussets')], 28.6, 3.4, 12.6)
    # EP-A east bay + NE corner
    A = partial(sh, (89.3, 28.5, 96.3, 36.3), 1.0, 12.0, 'EP-A  EAST BAY R9-R11 + NE CORNER', 'EPA'); fin_marks(sh, A)
    for a, b in ((89.90, 92.48), (92.48, 95.55)): sh.dimh(*A.L(a, 28.5)[:1], *A.L(b, 28.5)[:1], A.L(0, 28.5)[1], -0.5, 'S-MM2')
    sh.dimv(A.L(0, 29.27)[1], A.L(0, 35.77)[1], A.L(96.3, 0)[0], 0.5, 'S-MM2'); sh.dimv(A.L(0, 35.77)[1], A.L(0, 35.87)[1], A.L(96.3, 0)[0], 1.1, 'S-MM2', loc=A.L(96.95, 36.45))
    sh.text(*A.L(89.5, 29.0), 'both rod sets in the corner cell (RT-N-E panel 3 + RT-E panel 3); combined gussets RG-C at C2, C4, C13, C14 (D5)', TH_DIM, 'S-TEXT-NOTE', allowed=('EPA',), owner='EPA') if False else None
    # EP-B jog panel
    B = partial(sh, (77.3, 23.8, 82.4, 29.8), 17.4, 14.4, 'EP-B  JOG PANEL, T2, P12', 'EPB'); fin_marks(sh, B)
    sh.dimh(B.L(77.78, 23.8)[0], B.L(81.85, 23.8)[0], B.L(0, 23.8)[1], -0.5, 'S-MM2'); sh.dimv(B.L(0, 24.09)[1], B.L(0, 24.46)[1], B.L(82.4, 0)[0], 0.5, 'S-MM2', loc=B.L(83.2, 24.9)); sh.dimv(B.L(0, 24.46)[1], B.L(0, 29.27)[1], B.L(82.4, 0)[0], 0.5, 'S-MM2')
    # EP-C notch corner
    C = partial(sh, (77.2, 19.5, 82.5, 21.6), 17.4, 7.2, 'EP-C  NOTCH CORNER, WP1, K21', 'EPC'); fin_marks(sh, C)
    sh.dimh(C.L(77.89, 19.5)[0], C.L(WP1[0], 19.5)[0], C.L(0, 19.5)[1], -0.5, 'S-MM2', loc=C.L(77.0, 19.15)); sh.dimv(C.L(0, 19.97)[1], C.L(0, WP1[1])[1], C.L(77.2, 0)[0], -0.5, 'S-MM2', loc=C.L(76.6, 20.8))
    sh.dimh(C.L(WP1[0], 19.5)[0], C.L(81.85, 19.5)[0], C.L(0, 19.5)[1], -0.5, 'S-MM2')
    # EP-D north jog / well header / return
    D = partial(sh, (77.2, 34.7, 82.5, 36.2), 1.0, 5.2, 'EP-D  NORTH JOG, HEADER, RETURN', 'EPD'); fin_marks(sh, D)
    sh.dimv(D.L(0, 35.37)[1], D.L(0, 35.87)[1], D.L(82.5, 0)[0], 0.5, 'S-MM2', loc=D.L(83.3, 35.95)); sh.dimh(D.L(77.89, 34.7)[0], D.L(81.79, 34.7)[0], D.L(0, 34.7)[1], -0.5, 'S-MM2')
    sh.dimv(D.L(0, 35.22)[1], D.L(0, 35.37)[1], D.L(77.2, 0)[0], -0.5, 'S-MM2', loc=D.L(76.5, 35.6))
    # notes column
    sh.note_block(28.6, 27.5, 'NOTES TO THE PARTIAL PLANS', [
        'FP1: fin plate 100 x 150 x 10, 2 M20 8.8 (pitch 70, e1 = e2 = 40), bolt line 50 from the primary web, welds 2 x a6 (D1). FP2: 160 x 150 x 10, 2 x 2 M20 (p2 60) at the strip-chord splices of R1 / R3 / R9 / R11 (D1). R5 strut fin: FP1 (2 M20, 0.55).',
        'RG: rod gusset 8 mm shop-welded to the primary web, bolted 2 M16 to the rafter web, at every corner of the 13 rod panels (D5). RG-C: combined gusset at C2, C4, C13, C14 where the north strip and the east strip share the NE corner cell (both rod sets, D5).',
        'Rods M24 8.8 with turnbuckles; on RT-W (R1/R3) and RT-E (R9/R11) the rods span two rafter cells and pass R2 / R10 through a bolted web clip (D5).',
        'EP-C: WP1 at (77.61, 20.25); P14 IPE 300 eave beam from R5 (fin plate) to C21; K21 pier 200 thick between the notch edge y 19.97 and the shaft opening y 20.17 (base P, S05).',
        'EP-D: the stair well is open to the north face; wall header 2 x C200x60x2.5 boxed between C7 and the return post; 0.5 m wall return at x 81.79 on brackets from C3; gutter G-W stops at x 77.89, G-E starts at x 81.79 (stop ends + overflow spouts).',
        'Marks: Rn rafters IPE 240, Pn primaries IPE 300 (P13 IPE 330), Cn/Kn columns HEA 140 on concrete column Kn, RT-* rod strips, Bn wall X bays. Sections and lengths on S06.'], TH_DIM, 12.6)
    return sh
