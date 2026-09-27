# Alternative C - Rev 2 base and anchor design note (bases_C.md)

Self-contained note for the base reviewer. Loads from `calc/run_all.py` (reactions_C.csv has every column and load case); anchorage basis = `../load_basis.md` Rev 2 (anchors through the slab into the column heads). Units kN, mm, MPa.

## 1. One base detail for all 27 columns

- Base plate **300 x 400 x 25 S275** (long side along the concrete column's 400 mm axis), on **40 mm non-shrink grout** over the slab solid zone; HEA 160 column welded a = 6 all round, web across the concrete column's short axis (i.e. normal to the wall it supports).
- **4 M20 8.8 resin anchors at 80 x 280** (all four inside the 200 x 400 concrete column core: 60 mm from each column face, 13 mm clear of the corner dia14 bars at the nominal cover - **rebar scan before drilling**), drilled through the 250 mm slab solid zone into the column head, **h_ef = 300 mm** (>= 50 mm into the column). Holes in the plate 26 mm (clearance) so the anchors carry tension only.
- **Grouted shear key**: 60 mm round bar S355, 330 mm long, welded to the underside of the plate with an 8 mm fillet all round, in a **90 mm cored pocket 350 mm deep** (250 slab + 100 into the column head, centred on the column, clear of the middle dia14 bars by 11 mm nominal - scan), grouted with the same non-shrink grout. The key carries the whole base shear in both directions; no anchor shear towards or parallel to a slab edge.
- Erection: level on shims, set the key and anchors in resin/grout, torque the anchor nuts to snug + 1/4 turn only (no preload relied on).

## 2. Resistances (EN 1992-4 with the basis values, EN 1993-1-8 for the plate and key)

| Item | Formula / factors | Value |
|---|---|---|
| Anchor steel tension, per anchor | N_Rk,s 196 / gamma_Ms 1.4 | 140.0 kN (4 anchors 560.0 kN) |
| Concrete cone, single (slab solid zone) | k 7.2 (cracked) sqrt(25) h_ef^1.5, h_ef = 250 | N0_Rk,c = 142.3 kN |
| Cone group factors | s_cr,N 750, c_cr,N 375; group 80 x 280 in the 800 x 800 solid zone (boundary as free edges): A_c,N/A0 = 800 x 800 / 750^2 = 1.138; psi_s,N = 0.7 + 0.3 x 260/375 = 0.91; psi_re = psi_ec = 1 | N_Rk,c,g = 147.0 kN |
| **Cone group design** | / gamma_Mc 1.5 | **N_Rd,c = 98.0 kN** |
| Bond, single | pi x 20 x 300 x tau_Rk 10 MPa (cracked) | N0_Rk,p = 188.5 kN |
| Bond group factors | s_cr,Np = 7.3 d sqrt(tau) = 462 <= 3 h_ef; A_p,N/A0 = 1.88; psi_s,Np = 1.00; psi_g,Np taken 1.0 | N_Rk,p,g = 355.3 kN |
| Bond group design | / gamma_Mp 1.5 | N_Rd,p = 236.9 kN |
| **Group tension resistance** | min(steel, cone, bond) | **98.0 kN (cone)** |
| Bearing under the plate (compression) | effective area c = t sqrt(f_y/3 f_jd) = 76 mm -> A_eff = 934 cm2 at f_jd = 10 MPa (0.6 f_cd on the slab) | 934 kN |
| Plate T-stub under uplift (per anchor row of 2) | cantilever from the flange tips m = 55 mm, l_eff 300, t 25: F_T,1,Rd = 4 M_pl/m | 934 kN |
| Key bearing on the grout/concrete | triangular over the 250 mm slab depth, sigma_max = 2V/(60 x 250) <= f_cd 16.7 | V <= 125.0 kN |
| Key bending at the plate | lever 250/3 + 50 = 133 mm, W_pl = d^3/6, f_y 355 -> M_Rd 12.8 kNm | **V <= 95.9 kN** |
| Key weld | a = 8 fillet, 188 mm | 352 kN |
| Key shear **towards a free slab edge < 0.25 m from the column centre** | concrete in front of the key = 50 mm cover strip of the column head; resistance from the column cage only (3 dia14 dowels at 50 % = 33 kN + one dia6 stirrup 2 legs 24 kN, f_yd 435): 57 -> | **V_Rd,edge = 60 kN** (requires the rebar scan to confirm 6 dia14 + dia6/200) |

Tension and shear are carried by different elements (anchors / key), so no N-V interaction applies to the anchors; the key is checked for shear only. The slab solid zone (>= 800 x 800) and the column-head reinforcement are assumptions to be confirmed by cores and a rebar scan at 3 heads before drilling.

## 3. Governing actions and utilisation, every base (ULS envelope, concurrent values; full table in reactions_C.csv)

| Col | Type | Bays | Near edges (< 0.25 m) | N_c max kN (case) | N_t max kN (case) | V max kN (case) | Governing check | Util. |
|---|---|---|---|---|---|---|---|---|
| K1 | B braced-bay | B1 | +y | 54.7 (ULS2E) | 34.0 (ULS3N) | 33.5 (ULS2W) | key shear | **0.35** |
| K2 | B braced-bay | B1 | +y | 46.9 (ULS2W) | 36.1 (ULS3N) | 34.4 (ULS2E) | anchor tension (cone governs) | **0.37** |
| K3 | P perimeter | - | +y | 31.1 (ULS1) | 15.1 (ULS3N) | 15.0 (ULS2N) | edge shear +y (cage) | **0.23** |
| K4 | P perimeter | - | +x,+y | 19.8 (ULS1) | 14.6 (ULS3E) | 14.8 (ULS2N) | edge shear +x (cage) | **0.23** |
| K5 | B braced-bay | B2 | - | 57.6 (ULS2E) | 42.1 (ULS3W) | 41.6 (ULS2W) | key shear | **0.43** |
| K6 | P perimeter | - | -x | 25.2 (ULS1) | 18.0 (ULS3W) | 16.3 (ULS2N) | edge shear -x (cage) | **0.25** |
| K7 | B braced-bay | B2 | +x | 52.0 (ULS2W) | 26.4 (ULS3E) | 41.6 (ULS2E) | key shear | **0.43** |
| K8 | P perimeter | - | -x | 30.1 (ULS1) | 26.4 (ULS3W) | 15.8 (ULS2W) | anchor tension (cone governs) | **0.27** |
| K9 | I interior | - | - | 57.2 (ULS1) | 52.2 (ULS3N) | 0.0 (ULS1) | anchor tension (cone governs) | **0.53** |
| K10 | B braced-bay | B8 | +x,+y | 78.8 (ULS2S) | 58.1 (ULS3N) | 33.2 (ULS2N) | anchor tension (cone governs) | **0.59** |
| K11 | P perimeter | - | +y | 43.6 (ULS1) | 33.9 (ULS3N) | 0.0 (ULS1) | anchor tension (cone governs) | **0.35** |
| K12 | I interior | - | - | 70.5 (ULS1) | 66.7 (ULS3N) | 0.0 (ULS1) | anchor tension (cone governs) | **0.68** |
| K13 | I interior | - | - | 55.7 (ULS1) | 54.0 (ULS3N) | 0.0 (ULS1) | anchor tension (cone governs) | **0.55** |
| K14 | B braced-bay | B6 | +x | 56.7 (ULS2S) | 30.1 (ULS3E) | 30.8 (ULS2N) | key shear | **0.32** |
| K15 | B braced-bay | B5 | -x | 43.6 (ULS2S) | 16.7 (ULS3N) | 23.5 (ULS2N) | key shear | **0.25** |
| K16 | B braced-bay | B8 | +x | 43.8 (ULS2N) | 58.4 (ULS3S) | 57.3 (ULS2S) | key shear | **0.60** |
| K17 | P perimeter | - | - | 23.2 (ULS1) | 15.7 (ULS3S) | 0.0 (ULS1) | anchor tension (cone governs) | **0.16** |
| K18 | B braced-bay | B6,B9 | +x | 54.2 (ULS2S) | 39.5 (ULS3S) | 45.5 (ULS2S) | key shear | **0.47** |
| K19 | B braced-bay | B5,B10 | -x | 79.9 (ULS2S) | 73.1 (ULS3S) | 40.2 (ULS2S) | anchor tension (cone governs) | **0.75** |
| K20 | B braced-bay | B7 | +x | 82.3 (ULS2S) | 64.0 (ULS3N) | 29.5 (ULS2N) | anchor tension (cone governs) | **0.65** |
| K21 | P perimeter | - | +y,-y | 39.8 (ULS1) | 19.8 (ULS3S) | 29.3 (ULS2W) | edge shear -y (cage) | **0.49** |
| K22 | B braced-bay | B3 | -y | 90.6 (ULS2E) | 56.3 (ULS3S) | 59.0 (ULS2W) | key shear | **0.62** |
| K23 | B braced-bay | B3,B9 | +x,-y | 73.2 (ULS2W) | 62.1 (ULS3S) | 68.4 (ULS2E) | key shear | **0.71** |
| K24 | P perimeter | - | - | 23.9 (ULS1) | 23.6 (ULS3S) | 16.4 (ULS2E) | anchor tension (cone governs) | **0.24** |
| K25 | B braced-bay | B4,B10 | -x | 54.6 (ULS2E) | 42.6 (ULS3W) | 47.0 (ULS2S) | key shear | **0.49** |
| K26 | B braced-bay | B4 | - | 50.1 (ULS2W) | 30.5 (ULS3E) | 26.7 (ULS2E) | anchor tension (cone governs) | **0.31** |
| K27 | B braced-bay | B7 | +x | 38.8 (ULS2N) | 44.1 (ULS3S) | 59.3 (ULS2S) | key shear | **0.62** |

Worst base: **K19, 0.75 at anchor tension (cone governs) (ULS3S)**. All 27 bases <= 1.0 with the single detail above.

## 4. Worked check, three representative bases

**K12 (I interior, bays -, near edges none)** - max compression 70.5 kN (ULS1): bearing 0.08; max uplift 66.7 kN (ULS3N): anchors 66.7/4 = 16.7 kN each, group 66.7/98.0 = **0.68**, plate row 33.3/934 = 0.04; max shear 0.0 kN (ULS1): key 0.0/95.9 = 0.00.

**K23 (B braced-bay, bays B3,B9, near edges +x,-y)** - max compression 73.2 kN (ULS2W): bearing 0.08; max uplift 62.1 kN (ULS3S): anchors 62.1/4 = 15.5 kN each, group 62.1/98.0 = **0.63**, plate row 31.0/934 = 0.03; max shear 68.4 kN (ULS2E): key 68.4/95.9 = 0.71; the component towards the near edge is checked against 60 kN in reactions_C.csv.

**K19 (B braced-bay, bays B5,B10, near edges -x)** - max compression 79.9 kN (ULS2S): bearing 0.09; max uplift 73.1 kN (ULS3S): anchors 73.1/4 = 18.3 kN each, group 73.1/98.0 = **0.75**, plate row 36.6/934 = 0.04; max shear 40.2 kN (ULS2S): key 40.2/95.9 = 0.42; the component towards the near edge is checked against 60 kN in reactions_C.csv.

## 5. Load path summary

- Gravity: column -> plate -> grout -> slab solid zone -> concrete column (centred, no eccentricity).
- Uplift (ULS-3 roof suction + bracing tension diagonal): column and bracing gusset -> plate -> 4 anchors in tension -> bond over 300 mm and concrete cone in the slab solid zone (cracked). Max 73.1 kN at K19 vs 98.0 kN.
- Shear (bracing bay shear at the tension-diagonal base + wall wind wL/2 of the column, concurrent, same wind case): plate -> welded key -> grout -> slab solid zone / column head. Bay shears are arranged so that at no braced-bay base the bay shear points towards a free edge closer than 0.25 m (three N-S bracing lines x 68.0 / 77.8 / 95.5, two bays in series each); wall shear towards the near edge (<= 29 kN) is carried by the column cage.
- Wind post WP1 (notch corner, no concrete column): base plate 200 x 200 x 15 with 2 M16 resin anchors (h_ef 120) in the notch edge beam, shear 11.8 / 8.8 kN (E-W / N-S), no uplift (slotted top connection). Edge beam presence at the notch corner to be confirmed by a core.

## 6. Site verification before anchor installation

1. Cores at 3 column heads: slab thickness, solid-zone extent (>= 800 x 800 assumed), concrete grade (C25 assumed).
2. Rebar scan at every column head: 6 dia14 + dia6/200 stirrups, cover; adjust the 80 x 280 pattern and the key pocket to clear bars (tolerance +/- 20 mm in the pattern is covered: cone/bond group factors change < 3 %).
3. Pull-out test on 3 sacrificial anchors (h_ef 300) to 1.3 x N_Ed = 100 kN before production drilling; anchor supplier's ETA group verification (basis open item).
