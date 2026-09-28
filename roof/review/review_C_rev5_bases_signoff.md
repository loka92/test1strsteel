# Alternative C - bases Rev 5 (no through-bolts, slab 300 mm): focused sign-off

Scripts re-run: report, reactions and `bases_C.md` regenerate byte-identical. Rows: K19 E tension 0.28 (N_t 73.2), K23 key pair 0.80, K12 B1 cone 0.69, K7 0.76. Units kN, mm.

## 1. The "lap with the column bars" model

- **Concept right, framework wrong.** A threaded rod M16 at h_ef 550 (34 d) and 70 mm pitch (4.4 d) is outside every standard anchor ETA (h_ef <= 20 d = 320, s_min ~ 5 d), so the 257 kN "bond with narrow-member factor" (EN 1992-4, tau_Rk 10) has no product behind it. What is described is a **post-installed rebar connection** (EAD 330087): dia 16 B500 with threaded ends, designed to EN 1992-1-1 8.4 / 8.7 with the product's f_bd. That framework is valid here and passes: f_bd(C25) 2.7 MPa; K19 sigma_sd = 18.3/201 = 91 MPa -> l_b,rqd 135, l_0 = 1.5 x 135 = 203 < l_0,min = 15 d = **240 <= 250 provided** (tight); column-part capacity 4 x pi x 16 x 250 x 2.7 = **136 kN -> K19 0.54**, K23 0.46. Each rod laps 1:1 with its corner dia14 (11 mm clear, "close" lap): 268 kN receiving capacity; d < 20, minimum links suffice (8.7.4). Splitting is covered by the EC2 cover rules in this framework; EN 1992-4 7.2.1.7 applied with c = 65 would give ~52 kN and is not the right check.
- **Slab part.** Ignoring 300 mm of bond is not conservative: the stiff resin loads the top of the rod first, into the edge-slab cone (50 kN one edge / 38 corner), near its limit at service (48 kN at K19); the column lap takes over only after that cone cracks. Fix: **debond the top 300 mm** (sleeve), inject the column part only.
- Steel 323 kN: fine. The 70 mm pitch (54 mm clear) is admissible under the rebar framework; cracked concrete throughout is correct.

## 2. Keys and plates with the 300 mm slab

Pockets 200 deep leave 100 mm; breakout bodies with h = 300: c1 255 -> 45.5 kN, c1 250 (d 60) -> 41.9 kN, reproduced; K23 0.80, K25 0.83, K7 0.76. Without a lever the 25 mm plates carry only in-plane shear to keys 300-700 mm away and concentric uplift (T-stub m 55): no stiffeners needed. Rigid-post key-moment model retained.

## 3. Constructability

Clearance from a rod at (35, 140) to the corner bar at (57, 157) is **11 mm** with a 20 mm hole; drill wander over 550 mm ~5 mm; GPR from above through 300 mm of reinforced slab locates column bars to +/-15-20 mm: hit risk about one hole in two. Procedure: cover-meter scan of the column faces below the slab (+/-3-5 mm), projected to the top; pattern **70 x 240** (26 mm clear); 10 mm pilot with feed monitoring, relocate within +/-15 mm on steel contact; plate holes match-drilled or 30 mm oversize with 10 mm washers; proof tests of 3 rods to >= 60 kN with displacement, not 25 kN.

## 4. Criterion and B1

An 800 x 800 solid head is plausible on a ribbed slab and GPR sees blocks reliably: B1 with the tabulated minima (K12 / K16 700; 0.95 at 700, 1.35 at 600) is verifiable, E fallback stated. The 300 mm criterion matches the checks.

## 5. Findings

| ID | Severity | Item | Fix |
|---|---|---|---|
| V1 | MAJOR | M16 rod at h_ef 550 / 70 pitch outside anchor ETAs; 257 kN unsupported | Post-installed rebar (EAD 330087), dia 16 threaded end, EC2 lap: 250 >= 240, 136 kN (K19 0.54) |
| V2 | MAJOR | Slab bond loads the edge-slab cone (50 kN) first | Debond the top 300 mm; inject the column part only |
| V3 | MAJOR | 11 mm clearance to corner bars; from-above scan +/-15-20 mm | 70 x 240; face scan from below; pilot drill; relocate; match-drilled plate holes |
| V4 | MINOR | Proof test 25 kN proves nothing | 3 rods to >= 60 kN with displacement |
| V5 | MINOR | Lap 250 vs l_0,min 240 | Embed 300 into the column where possible |
| V6 | MINOR | B1 depends on the 800 solid zone | GPR all heads; E fallback |

## 6. Verdict

**ACCEPTABLE WITH FIXES** (V1-V3 before the base drawings are re-issued; no member or key changes). **Recommendation: build all 27 bases as type E** (dia 16 post-installed rebar, 70 x 240, h_ef 550-600, debonded through the slab): one base detail, no slab-cone check and no solid-zone criterion anywhere, for 28 more scanned holes.
