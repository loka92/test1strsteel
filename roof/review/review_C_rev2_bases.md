# Alternative C Rev 2 - focused review of the bases and anchors

Scope: `bases_C.md`, `reactions_C.csv` (595 rows), `calc/`, basis Rev 2. Scripts re-run: all outputs regenerate byte-identical. Units kN, mm, MPa.

## 1. Rev 1 fixes confirmed in the code

F1: `members.py` puts 1.5 (V_wall + V_brace) at every base, concurrent per wind case. F2: no anchor shear, cone k = 7.2 cracked. F3: struts and wall rail deleted, full H per base. F4: `bracing.py` adds the roof-suction component (39.1 kN char.; S-wind roof force 148.3 kN), no friction. Bays B1-B10 match the base rows (B8 57.3, B7 50.9, B6 42.4, B9 38.1, B5 35.1, B10 33.1 kN ULS); paired bays on one line act in parallel, so the split is right ("in series" is a misnomer). B8 is an interior X in the hall, not a wall bay.

## 2. Verified by hand

- Cone, h_ef 250: N0 142.3, A_c,N/A0 1.138, psi_s 0.908 -> N_Rd,c 98.0; bond 237. K19 0.75, K12 0.68 as stated.
- Plate 25 mm: mode 1 934 / mode 2 ~370 kN per row vs <= 37 kN; bearing K22 0.10.
- Key: bearing 125 kN; bending 12.8 kNm/133 mm = 96 kN, K23 0.71.
- Reactions table: 22 rows per column plus WP1, concurrent N/V_x/V_y, near-edge flags, ULS-4, SLS wind: complete.

## 3. Findings

**R1 - MAJOR - The 60 kN "column cage" resistance for shear towards a free edge is not demonstrable.** It is 3 dia14 dowels at 50 % (21.7 kN each, 1.3 d^2 sqrt(f_cd f_yd)) plus one dia6 stirrup. The dowel formula needs several bar diameters of concrete on the loaded side; here the bars push on their own 30 mm cover, which spalls: nothing. The stirrup legs in the shear direction are 157 mm from the key, beyond 0.75 c1 (c1 = 55 mm), which EN 1992-4 7.2.2.6 excludes, and a stirrup may not exist in the joint. Plain-concrete edge breakout of a stiff 60 mm element (7.2.2.5, cracked): 5.6 kN at c1 55, 28 at 155, 36 at 205 mm. Demands: K21 29.3, K19 26.8, K22 26.1, K23 24.6, K14 18.3, K6 16.3, K25 15.7, K1 15.3, K4 14.8, K8 14.4, K3 13.6, K15 13.1 kN (15 bases). Fix: key inboard so c1 >= 250 (36-42 kN) with the torsion resolved, or a slab-edge clamp (horizontal through-bolt to a plate on the edge-beam face, once cores show a beam), or drilled-in hairpins designed per 7.2.2.6 for the whole force. No credit for the cage.

**R2 - MAJOR - Key moment on the anchor group is ignored.** The key delivers V at 40 + 250/3 = 123 mm below the plate; under uplift that moment goes into the anchors (eccentric tension, psi_ec,N) unless the key is shown to carry it by toe bearing. With psi_ec: K19 ULS3S (73.1 kN, V 40.2) 0.94, K23 ULS3E (59.3, V_x 62.8 across the 80 mm spacing) 0.94, K23 ULS3S 0.87, K22 0.82, K16 0.79 against 0.75 / 0.61 / 0.63 / 0.53 / 0.60; max anchor tension 59 kN (steel OK). "No N-V interaction" does not hold for the group. Fix: include psi_ec, shorten the lever (stub lug 150 deep), or design the key for the moment with a toe-bearing check.

**R3 - MAJOR - Tension capacity is the assumed solid zone and nothing else.** The group cone fills the 800 x 800 zone, so N_Rd,c is 98-100 kN for any h_ef from 200 to 300, 71.7 kN at 700 x 700 (K19 1.02) and 50.3 kN at 600 x 600 (K9, K10, K12, K13, K16, K19, K20, K22, K23 at 1.04-1.45). Fix: core acceptance criterion (solid >= 750 x 750 x 250, C25, every head) and a pre-designed through-bolt fallback at those nine columns.

**R4 - MAJOR - Drilling into the column head buys nothing and will hit bars.** h_ef 200 in the slab alone gives 98.5 kN (bond 158) and respects a typical ETA h_min = h_ef + 2 d0 = 248 <= 250. The anchors at (40, 140) are 24 mm centre-to-centre from the corner dia14 bars (5-6 mm clear); the 90 mm core is 5-11 mm from the middle bars, removes 45 % of the column width over its top 100 mm and cuts the slab's hogging bars over the support. Fix: anchors h_ef 200 and key pocket <= 200 deep in the slab only (bearing 11.3 MPa at 68 kN, M 7.3 kNm), pocket placed by scan, 100-110 mm core for a 20-25 mm grout annulus, anchors set after grouting.

**R5 - MINOR** - f_y 335 for the 60 mm bar (V <= 90.7 kN). No key edge check beyond 0.25 m; at c1 255-355 the plain value is 40-42 kN vs outward shears <= 27 kN - state it.

**R6 - MINOR** - WP1: a 200 x 200 plate centred on the notch corner overhangs both slab edges; 2 M16 (h_ef 120) carry 11.8 kN towards the edge of an unconfirmed edge beam. Offset >= 150 mm inboard, detail as R1.

**R7 - MINOR** - Table: add the 280 mm spacing orientation, key moment / max anchor tension, minimum solid zone per column.

## 4. Verdict for the bases

**NOT ACCEPTABLE as presented; the concept (tension-only anchors + grouted key) is right and becomes acceptable with R1-R4.** Superstructure detailing may start. Base detailing may not start until cores and scans meet the R3 criterion, the outward-shear path at the 15 near-edge bases is redesigned without the cage, and the key moment is removed or carried. No coring into a column head before R4 is settled.

## 5. Findings table

| ID | Severity | Item | Mine vs theirs | Fix |
|---|---|---|---|---|
| R1 | MAJOR | Near-edge shear via column cage | 5.6-36 kN vs 60 kN; K21 needs 29.3 | Key inboard (c1 >= 250) / edge clamp / designed hairpins |
| R2 | MAJOR | Key moment on anchors under uplift | K19 0.94, K23 0.94, K22 0.82 vs 0.75 / 0.61 / 0.53 | Include psi_ec or design key for the moment; shorter lug |
| R3 | MAJOR | Solid-zone dependence | 700 x 700 -> K19 1.02; 600 -> 9 bases fail | Core criterion + through-bolt fallback |
| R4 | MAJOR | Coring/drilling into column head | 5-11 mm to bars; h_ef 200 gives same 98 kN | Anchors and key in the slab only |
| R5 | MINOR | Key f_y; edge check beyond 0.25 m | 90.7 vs 95.9 kN | Update note |
| R6 | MINOR | WP1 at the slab corner | plate overhangs | Offset inboard |
| R7 | MINOR | Table fields | - | Add orientation, key moment, min. zone |
