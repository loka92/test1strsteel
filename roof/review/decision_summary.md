# Independent review stage - decision summary

Two independent reviewers re-ran both calculation packages (all numbers reproduced) and hand-checked the governing members, connections and anchors.

## Verdicts
| | A: Portal frames | C: Post-and-beam braced |
|---|---|---|
| Verdict | NOT ACCEPTABLE as submitted | NOT ACCEPTABLE as submitted |
| Blockers / majors / minors | 1 / 6 / 7 | 1 / 3 / 11 |
| Steel superstructure | Sound; passes after the wind corrections (knee 0.90 -> 0.81, girder 0.81, F5 sway h/163) | Sound; all hand checks agree (K19-K20 primary 0.74, 9.2 m rafters 0.52, columns 0.68, bracing 0.36-0.72) |
| The blocker | Bases rely on 300 mm anchor embedment that does not exist in a 250 mm slab; with the basis 170 mm value and corrected wind, 6-7 bases fail (K22 1.95, K9 1.02-1.1, K6, K26, K12, K13); 80-110 kN uplift at interior bases | Braced-bay bases: wall base shear was wrongly diverted to a wall rail and bracing shear was shared through a bolted strut; restored, K21 is at 1.4-2.1, K22/K23 1.0-1.5; interior uplift 66-76 kN |
| Other majors | 3.0 m clear at the north eave lost to the 680 mm knee end plate (2.89 m); gutter uplift omitted; perimeter thrust into the unverified slab edge; thermal lock-up between the two braced wings | Cracked-concrete edge shear value must be used (34 not 48 kN); base strut load sharing unproven; roof-suction horizontal component missing (+34 % on south-wind force; B8 diagonal 68 -> 92 kN, still OK) |
| Load-basis errors (my responsibility, now corrected in load_basis.md Rev 2) | Wind direction labels swapped (mattered for A: uplift +10-25 %), zone size e = 20 m not 12 m (edge purlins 0.67 -> 0.9), roof-suction horizontal component missing | Same three; C had enveloped the wind directions so only the last two matter |

## The common root cause
Both alternatives stand on drilled resin anchors in a 250 mm hollow-block slab over 200 x 400 columns that must not be touched. Every wind case turns into 60-110 kN of uplift and 25-75 kN of shear per base, and a 4 x M20 group at 170 mm embedment inside a 200 x 400 solid zone resists only about 50-60 kN in tension and 34 kN of shear towards a free edge. This is not a superstructure problem; it is an anchorage concept problem, and it has to be settled before either alternative can be detailed.

## Ways to resolve the anchorage (need a client decision)
1. **Through-bolts with a bearing plate under the slab** (recommended). 4 x M20 threaded rods pass through the slab in the solid zone beside the column head, with a 300 x 400 x 15 steel plate on the soffit. Uplift and shear go into the solid concrete in bearing, independent of drilling depth or cracked-concrete cone capacity. Needs access to the ceiling below at 27 points (ceiling tiles opened, one night each), and trial cores first to confirm the solid zone.
2. **Deepen anchors into the column heads** (300 mm). Works structurally for most bases but drills 300 mm into the concrete columns and needs a rebar scan at every head, which conflicts with "no changes to the existing columns". Only if the client waives that rule.
3. **Reduce base forces at source** and keep 170 mm anchors: in C, double the braced bays (about 14-16 bays) and add ballast or tie-down beams; in A, change the F5/F6 propped scheme and add wind posts. Still leaves interior uplift of 60-80 kN per base, which 170 mm anchors cannot take in a 200 x 400 solid zone; so this only works combined with 1 or 2.

## Recommendation
- Carry forward **Alternative C**. Its superstructure passed every hand check, its base forces are 20-30 % lower than A's, its remaining majors are small (use the cracked edge value, drop the unproven base strut, add the roof-suction component), and it keeps the simplicity the client asked for. A's fixes are larger (north-eave headroom, thermal lock-up, thrust into the slab edge, propped frames) and its uplift is the highest.
- Adopt **through-bolt bases (option 1)** at every base, with trial cores at 3 column heads before detailing.
- Re-run the C design with load basis Rev 2 and the review fixes, re-review the bases only, then proceed to detailing.

## What the client needs to confirm now
1. Alternative C (or A) to proceed.
2. Through-bolt bases with ceiling access below (option 1), or permission to drill into the column heads (option 2).
3. Trial cores at 3 column heads to confirm slab thickness and the solid-zone extent.
4. The 8 braced bays B1-B8 are door-free and can be closed with wall panels (list in design_report_C.md section 8).
5. Local rainfall intensity and wind speed for the city.
