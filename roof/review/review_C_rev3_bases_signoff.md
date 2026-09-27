# Alternative C - bases Rev 3: sign-off check

Scripts re-run (`run_all.py`, `write_report.py`): report, members, reactions and `bases_C.md` regenerate byte-identical; R1-R7 are answered in code and note. Units kN, mm.

## Hand checks that agree

- **K19 ULS3S**: N_t 73.1, V (-19.5, 35.1); M = V x 0.085 = 2.98 / 1.66 kNm, e 41 / 23 mm, psi_ec 0.82; cone h_ef 200: N0 101.8, A/A0 1.511, psi_s 0.96 -> 98.5; 73.1/(98.5 x 0.82) = **0.91**; max anchor 34 kN. As stated - but see S1.
- **K23 Key A**: z0 113.5 mm, p_max 0.298 MPa/kN, 25 MPa -> 83.8 kN; 63.7/83.8 = **0.76**. Rigid-post bound for pressure with the cantilever bound (85 mm) for the anchor moment: inconsistent but conservative both ways.
- **K14 Key B**: c1 250: V0 70.3, A/A0 0.667, psi_h 1.22 -> 38.2; bar bearing 37.2 governs; 18.3/37.2 = **0.49**; no torque.
- **K21 saddle**: plate cantilever 150, t 15: 6.2 kNm/0.075 = 82.5; 29.3 -> **0.36**.
- **Compressible face**: Key A cannot bear outward and sees only along-axis and inward shear on deep concrete; valid if the strip is fixed before grouting. **psi_ec** per direction with s_cr 600, carried into the max-anchor and T-stub checks: correct.

## Findings

**S1 - BLOCKER - The cone at perimeter bases uses a solid zone the building does not have.** The 800 x 800 zone is centred on the column, but at every perimeter column the slab ends 100 mm from the column centre: the outboard anchor row is 60 mm from a free edge. With that edge (psi_s 0.76): N_Rd,c = 50.4 kN (one edge) / 37.8 (corner). K23 2.16, K19 1.77, K22 1.51, K25 1.28, K18 1.13, K21 (200 mm pier) 1.11, K2 1.00; K16 1.64, K27 1.44, K20 1.39 if the shaft openings are slab openings as modelled. "Min. zone 750" is unachievable there. Fix: the through-bolt fallback becomes the primary detail at these bases, or the anchor group moves inboard (rows >= 250 mm from the edge) with the eccentricity couple designed.

**S2 - MAJOR - Key A shear parallel to the edge.** At the 100 mm-edge bases the pocket wall is 30 mm from the building face; 1.5 f_cd assumes confinement a free face 30-55 mm away does not give. EN 1992-4 7.2.2.5 parallel-to-edge (2 V_Rk,c, c1 55-70): 18.5-23.6 kN against K23 63.7, K27 59.3, K22 59.0, K25 47.0, K18 45.5, K19 35.1. Fix: Key A inboard with the torque resolved (key pair, or anchors in resin-filled holes), or a reinforced edge beam designed for this force.

**S3 - MINOR - Fallback statics.** Rows at 150 / 350 inboard: outer row 73 x 0.35/0.20 = 128 kN (64 per M20), not 91; inner row 55 kN compression; plate 11.0 vs M_el 11.5 kNm: stiffeners or t 30.

**S4 - MINOR** - Acceptance criterion to be one-sided at perimeter heads once S1 is settled.

| ID | Severity | Item | Fix |
|---|---|---|---|
| S1 | BLOCKER | Cone with the real slab edge: K23 2.16, K19 1.77, K22 1.51, K25 1.28, K18 1.13, K21 1.11 | Through-bolts as primary perimeter detail, or anchor group inboard |
| S2 | MAJOR | Key A parallel-edge breakout 18-24 kN vs 34-64 kN | Key A inboard with torque resolved, or reinforced edge beam |
| S3 | MINOR | Fallback row force 128 kN, plate 0.96 | Correct note; stiffeners / t 30 |
| S4 | MINOR | Criterion impossible at perimeter | One-sided criterion |

## Verdict

**NOT ACCEPTABLE.** Interior bases, Key B, saddle and WP1 are fine; the perimeter braced bases fail on the cone with the real edge and on parallel-edge shear at Key A. Make the through-bolt fallback the standard perimeter detail and re-issue.
