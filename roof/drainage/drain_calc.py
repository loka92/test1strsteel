"""Rainwater drainage calc + drawings for the north-eave gutter (EN 12056-3)."""
import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

OUT = "/home/user/test1strsteel/roof/drainage"

# ---------------- geometry (m) ----------------
X0, X1 = 67.89, 95.69
Y_S = 15.57                       # high (south) edge
Y_NW, Y_NE = 35.37, 35.87         # north outer faces: west part (x<81.79) / east part
X_JOG = 81.79
NOTCH = dict(x0=77.89, x1=95.69, y0=15.57, y1=19.97)
STAIR = dict(x0=77.89, x1=81.79, y0=29.37, y1=35.37)
ELEV = dict(x0=77.89, x1=81.99, y0=20.17, y1=24.16)
SLOPE = 0.06
r100, r150 = 100/3600, 150/3600   # l/s.m2

# ---------------- catchment split ----------------
# West wing x 67.89-77.89, y 15.57-35.37 (no openings)
A_west_wing = (77.89-X0)*(Y_NW-Y_S)
# strip x 77.89-81.79 between the openings (diverted by the stair cricket 50/50 W/E)
A_strip = (STAIR["x1"]-STAIR["x0"])*(STAIR["y0"]-ELEV["y1"])
# sliver south of the elevator (0.2 m) -> 50/50 by the mini-saddle flashing
A_sliv_S = (ELEV["x1"]-ELEV["x0"])*(ELEV["y0"]-NOTCH["y1"])
# east block x 81.79-95.69, y 19.97-35.87 less the elevator part east of 81.79
A_east_blk = (X1-X_JOG)*(Y_NE-NOTCH["y1"]) - (ELEV["x1"]-X_JOG)*(ELEV["y1"]-ELEV["y0"])
A_stair = (STAIR["x1"]-STAIR["x0"])*(STAIR["y1"]-STAIR["y0"])
A_elev = (ELEV["x1"]-ELEV["x0"])*(ELEV["y1"]-ELEV["y0"])
A_footprint = (X1-X0)*(Y_NE-Y_S) - (NOTCH["x1"]-NOTCH["x0"])*(NOTCH["y1"]-NOTCH["y0"]) - (X_JOG-X0)*(Y_NE-Y_NW)
A_roofed = A_footprint - A_stair - A_elev
div = 0.5*(A_strip + A_sliv_S)      # diverted to each side by the crickets
A_W = A_west_wing + div
A_E = A_east_blk + div
print(f"footprint {A_footprint:.1f} roofed {A_roofed:.1f} west {A_W:.1f} east {A_E:.1f} check {A_W+A_E:.1f}")
print(f"strip {A_strip:.1f} sliver {A_sliv_S:.2f} stair {A_stair:.1f} elev {A_elev:.1f}")

# EN 12056-3 4.2 effective area with wind: A = (L + H/2) B  -> factor (L + 0.03L)/L
kW = (1 + SLOPE/2)   # rise/2 relative to plan length: H/2 = 0.03 L
print("wind factor", kW)

# ---------------- downpipes ----------------
# West gutter run x 67.89-77.89 at y 35.37; East run x 81.79-95.69 at y 35.87
DP = [dict(id="DP1", x=68.7, run="W"), dict(id="DP2", x=77.3, run="W"),
      dict(id="DP3", x=85.3, run="E"), dict(id="DP4", x=92.0, run="E")]
hpW = (68.7+77.3)/2       # 73.0 high point between outlets (expansion joint)
hpE = (85.3+92.0)/2       # 88.65
bW = Y_NW - Y_S           # 19.8 m slope length west wing
bE = Y_NE - NOTCH["y1"]   # 15.9 m east block

def reach(x_a, x_b, b, extra=0.0):
    L = abs(x_b-x_a); A = L*b + extra
    return L, A

reaches = []
# West
reaches.append(("DP1 west end", "DP1") + reach(X0, 68.7, bW))
reaches.append(("DP1 east (to high pt)", "DP1") + reach(68.7, hpW, bW))
reaches.append(("DP2 west (from high pt)", "DP2") + reach(hpW, 77.3, bW))
reaches.append(("DP2 east end + cricket W", "DP2") + reach(77.3, 77.89, bW, div))
# East (elevator sliver east of 81.79 removed from DP3-west)
elev_east = (ELEV["x1"]-X_JOG)*(ELEV["y1"]-ELEV["y0"])
reaches.append(("DP3 west end + cricket E", "DP3") + reach(X_JOG, 85.3, bE, div-elev_east))
reaches.append(("DP3 east (to high pt)", "DP3") + reach(85.3, hpE, bE))
reaches.append(("DP4 west (from high pt)", "DP4") + reach(hpE, 92.0, bE))
reaches.append(("DP4 east end", "DP4") + reach(92.0, X1, bE))

print("\nReach  L(m)  A(m2)  Aeff  Q100  Q150")
tot = {}
for name, dp, L, A in reaches:
    Ae = A*kW; q1 = Ae*r100; q2 = Ae*r150
    tot.setdefault(dp, [0, 0, 0]); tot[dp][0] += Ae; tot[dp][1] += q1; tot[dp][2] += q2
    print(f"{name:28s} {L:5.2f} {A:6.1f} {Ae:6.1f} {q1:5.2f} {q2:5.2f}")
print("\nper downpipe:", {k: [round(v[0],1), round(v[1],2), round(v[2],2)] for k, v in tot.items()})
print("total", sum(v[1] for v in tot.values()), sum(v[2] for v in tot.values()))

# ---------------- gutter capacity EN 12056-3 cl. 5 ----------------
def QN(A_mm2): return 2.78e-5*A_mm2**1.25
for name, A in [("HR 125", math.pi*62.5**2/2), ("HR 150", math.pi*75**2/2), ("HR 200", math.pi*100**2/2),
                ("box 150x100", 150*100), ("box 160x100", 160*100)]:
    Fd = 1.0 if name.startswith("HR") else 0.95
    print(f"{name:12s} A={A:6.0f} QN={QN(A):.2f}  QL=0.9*QN*Fd={0.9*QN(A)*Fd:.2f} l/s")

# outlet, sharp-edged round, weir regime EN 12056-3 cl. 7
def Qo(D, h): return 7.5e-5*D*h**1.5
for h in (40, 50, 58, 60):
    print(f"outlet D100 h={h}: {Qo(100,h):.2f} l/s")
# head needed
for q in (2.9, 3.07, 3.3, 4.95):
    print(f"Q={q}: h={ (q/(7.5e-5*100))**(2/3):.1f} mm")
# RWP capacity EN 12056-3 cl. 6 (Wyly-Eaton), f = 0.33, kb = 0.25 mm
def Qrwp(d, f=0.33, kb=0.25): return 2.5e-4*kb**-0.167*d**2.667*f**1.667
print("RWP 75/100/125:", [round(Qrwp(d), 1) for d in (75, 100, 125)])
# gutter water depth ratio in the longest reach (Q/QN)^(1/1.25)
for q in (2.44, 3.66):
    print(f"reach Q={q}: depth ratio {(q/QN(15000))**(1/1.25):.2f}")
# thermal
for L in (10.0, 13.9):
    print(f"L={L}: alu {L*24e-6*40*1000:.1f} mm, steel {L*12e-6*40*1000:.1f} mm")
# loads
w_water = 0.15*0.10*9.81   # kN/m
print("water kN/m", w_water)

# ---------------- drainage_loads.json ----------------
loads = {
  "units": "kN, m, mm",
  "gutter": "external box gutter 150 wide x 100 deep, hung on brackets outside the north outer face (y 35.37 west run x 67.89-77.89; y 35.87 east run x 81.79-95.69)",
  "gutter_line_load_kN_per_m": 0.25,
  "gutter_line_load_note": "characteristic, gutter brim-full of water (0.15) + gutter, brackets and fascia trim (0.10); applied 0.20 m outside the fascia line -> add eccentricity moment 0.05 kNm/m on the eave member",
  "gutter_uplift_kN_per_m": -0.50,
  "gutter_uplift_note": "wind zone F on the 0.15 m gutter width (-3.3 kN/m2); brackets and fascia fixings to resist it",
  "maintenance_point_load_kN": 0.5,
  "maintenance_point_load_note": "at any bracket (ladder / person leaning), not combined with wind",
  "bracket_spacing_m": 0.6,
  "load_per_bracket_kN": {"gravity_char": 0.15, "point": 0.5, "uplift": -0.30},
  "fascia_support": "continuous eave rail (eave Z200 purlin or C200x60x2.5) fixed to every rafter end / eave beam; brackets screw to it at 0.6 m",
  "gutter_runs": [
    {"id": "G-W", "x0": 67.89, "x1": 77.89, "y_face": 35.37, "length_m": 10.0, "high_point_x": hpW, "expansion_joint_x": hpW},
    {"id": "G-E", "x0": 81.79, "x1": 95.69, "y_face": 35.87, "length_m": 13.9, "high_point_x": hpE, "expansion_joint_x": hpE}
  ],
  "downpipes": [
    {"id": "DP1", "x": 68.7, "y_face": 35.37, "dia_mm": 100, "Q_100_l_s": round(tot["DP1"][1], 2), "Q_150_l_s": round(tot["DP1"][2], 2), "fixed_to": "north facade beside column K6"},
    {"id": "DP2", "x": 77.3, "y_face": 35.37, "dia_mm": 100, "Q_100_l_s": round(tot["DP2"][1], 2), "Q_150_l_s": round(tot["DP2"][2], 2), "fixed_to": "north facade beside column K7, 0.6 m west of the stair well"},
    {"id": "DP3", "x": 85.3, "y_face": 35.87, "dia_mm": 100, "Q_100_l_s": round(tot["DP3"][1], 2), "Q_150_l_s": round(tot["DP3"][2], 2), "fixed_to": "north facade wall between K3 and K1 (shift to x 82.4 beside K3 if the wall is glazed there)"},
    {"id": "DP4", "x": 92.0, "y_face": 35.87, "dia_mm": 100, "Q_100_l_s": round(tot["DP4"][1], 2), "Q_150_l_s": round(tot["DP4"][2], 2), "fixed_to": "north facade beside column K2"}
  ],
  "outlets": [
    {"id": "O1", "x": 68.7, "run": "G-W", "dia_mm": 100, "type": "conical gutter outlet with wire-balloon strainer"},
    {"id": "O2", "x": 77.3, "run": "G-W", "dia_mm": 100, "type": "conical gutter outlet with wire-balloon strainer"},
    {"id": "O3", "x": 85.3, "run": "G-E", "dia_mm": 100, "type": "conical gutter outlet with wire-balloon strainer"},
    {"id": "O4", "x": 92.0, "run": "G-E", "dia_mm": 100, "type": "conical gutter outlet with wire-balloon strainer"}
  ],
  "overflow_spouts_x": [67.89, 77.89, 81.79, 95.69],
  "openings": {
    "stair": {"upstand_mm": 150, "cricket": "south side y 29.37, apex 2.0 m upslope at x 79.84, ridge 120 mm at the upstand (cross-fall 6 %), upstand 300 mm at the ridge; ~0.05 kN/m2 extra on trimmer T(29.37) and the two rafters 77.89/81.79 over 2 m",
              "well_area_m2": round(A_stair, 1), "well_Q_100_l_s": round(A_stair*r100, 2)},
    "elevator": {"upstand_mm": 150, "cricket": "none possible (roof edge 0.2 m south); south upstand merged with the notch verge flashing, capped 5 % both ways",
                 "well_area_m2": round(A_elev, 1), "well_Q_100_l_s": round(A_elev*r100, 2)}
  },
  "catchment_m2": {"west_run": round(A_W, 1), "east_run": round(A_E, 1), "roofed_total": round(A_roofed, 1), "wind_factor": kW},
  "total_Q_l_s": {"r100": round(sum(v[1] for v in tot.values()), 1), "r150": round(sum(v[2] for v in tot.values()), 1)}
}
with open(f"{OUT}/drainage_loads.json", "w") as f:
    json.dump(loads, f, indent=1)

# ================= drainage_layout.png =================
C = dict(roof="#e8eef5", edge="#2b3a4a", gutter="#1f6fb2", dp="#d1495b", open="#f4e4c1",
         crick="#7aa86a", split="#8a6d3b", text="#2b3a4a", grid="#b8c2cc")
fig, ax = plt.subplots(figsize=(13, 10.5), dpi=150)
ax.set_facecolor("white")
# roof outline (L-shape, with the north jog)
outline = [(X0, Y_S), (77.89, Y_S), (77.89, 19.97), (X1, 19.97), (X1, Y_NE), (X_JOG, Y_NE),
           (X_JOG, Y_NW), (X0, Y_NW)]
ax.add_patch(Polygon(outline, closed=True, fc=C["roof"], ec=C["edge"], lw=2.0, zorder=1))
# catchment split shading
ax.add_patch(Polygon([(X0, Y_S), (77.89, Y_S), (77.89, Y_NW), (X0, Y_NW)], fc="#d8e6f3", ec="none", zorder=1.5, alpha=0.8))
ax.add_patch(Polygon([(X_JOG, 19.97), (X1, 19.97), (X1, Y_NE), (X_JOG, Y_NE)], fc="#dcecdc", ec="none", zorder=1.5, alpha=0.8))
ax.add_patch(Polygon([(77.89, 19.97), (X_JOG, 19.97), (X_JOG, Y_NW), (77.89, Y_NW)], fc="#efe6d2", ec="none", zorder=1.5, alpha=0.9))
# split lines between downpipes
for x, y0, y1 in [(hpW, Y_S, Y_NW), (hpE, 19.97, Y_NE)]:
    ax.plot([x, x], [y0, y1], color=C["split"], ls="--", lw=1.2, zorder=2)
    ax.text(x+0.15, y0+1.2, f"catchment split /\ngutter high point x {x:.2f}", ha="left", va="bottom", fontsize=7.5, color=C["split"])
# openings
for op, nm in [(STAIR, "STAIR WELL\n(not roofed)\n3.9 x 6.0 m\nslab outlet + overflow"),
               (ELEV, "ELEVATOR WELL\n(not roofed)\n4.1 x 4.0 m\nslab outlet + overflow")]:
    ax.add_patch(Rectangle((op["x0"], op["y0"]), op["x1"]-op["x0"], op["y1"]-op["y0"],
                           fc=C["open"], ec="#8a6d3b", lw=1.6, hatch="//", zorder=3))
    ax.text((op["x0"]+op["x1"])/2, (op["y0"]+op["y1"])/2, nm, ha="center", va="center", fontsize=7.5, zorder=4)
    # upstand 150 mm all sides
    ax.add_patch(Rectangle((op["x0"]-0.12, op["y0"]-0.12), op["x1"]-op["x0"]+0.24, op["y1"]-op["y0"]+0.24,
                           fill=False, ec="#8a6d3b", lw=0.8, ls=":", zorder=3))
# stair cricket (saddle on the south side)
apex = (79.84, STAIR["y0"]-2.0)
ax.add_patch(Polygon([(STAIR["x0"], STAIR["y0"]), apex, (STAIR["x1"], STAIR["y0"])], fc=C["crick"], ec="#3f6b32", lw=1.2, alpha=0.75, zorder=3.5))
ax.plot([79.84, 79.84], [STAIR["y0"], apex[1]], color="#3f6b32", lw=1.5, zorder=4)
ax.annotate("cricket: ridge 120 mm at upstand,\napex 2.0 m upslope, valleys 4.3 %",
            xy=(79.84, 28.2), xytext=(84.6, 26.6), fontsize=7.5, ha="left",
            arrowprops=dict(arrowstyle="->", color="#3f6b32"), color="#3f6b32", zorder=5)
# elevator south sliver: mini-saddle flashing
ax.plot([ELEV["x0"], ELEV["x1"]], [19.97+0.1, 19.97+0.1], color="#3f6b32", lw=3, zorder=4)
ax.annotate("0.2 m sliver: verge flashing capped 5 % E/W (no cricket possible)",
            xy=(79.9, 20.07), xytext=(84.6, 21.9), fontsize=7.5, ha="left",
            arrowprops=dict(arrowstyle="->", color="#3f6b32"), color="#3f6b32", zorder=5)
# diverted-flow arrows around the stair well
for x0, dx in [(78.6, -1.1), (81.1, 1.1)]:
    ax.add_patch(FancyArrowPatch((x0, 28.6), (x0+dx, 28.6), arrowstyle="-|>", mutation_scale=12, color="#3f6b32", lw=1.2, zorder=5))
# flow arrows north
for x in (70.0, 75.5, 89.0, 93.5):
    ax.add_patch(FancyArrowPatch((x, 22.5), (x, 32.5), arrowstyle="-|>", mutation_scale=14, color="#5a6b7c", lw=1.0, zorder=2, alpha=0.7))
ax.text(70.0, 22.0, "6 % fall", ha="center", va="top", fontsize=8, color="#5a6b7c")
# gutters (outside the outer face)
gw = 0.35
for (xa, xb, yf, lab) in [(X0, 77.89, Y_NW, "G-W 150x100 box, 10.0 m"), (X_JOG, X1, Y_NE, "G-E 150x100 box, 13.9 m")]:
    ax.add_patch(Rectangle((xa, yf+0.05), xb-xa, gw, fc="#cfe3f5", ec=C["gutter"], lw=1.8, zorder=4))
    ax.text((xa+xb)/2, yf+0.05+gw+0.35, lab, ha="center", va="bottom", fontsize=8.5, color=C["gutter"], fontweight="bold")
    # fall arrows to outlets
# overflow spouts at gutter ends
for x, yf in [(X0, Y_NW), (77.89, Y_NW), (X_JOG, Y_NE), (X1, Y_NE)]:
    ax.plot([x], [yf+0.05+gw/2], marker="s", ms=6, color="#e69f00", zorder=6)
ax.text(64.9, Y_NW+0.05+gw/2, "overflow\nspout", fontsize=7, color="#b07600", va="center")
# outlets + downpipes
for d in DP:
    yf = Y_NW if d["run"] == "W" else Y_NE
    ax.add_patch(Circle((d["x"], yf+0.05+gw/2), 0.22, fc="white", ec=C["dp"], lw=2.2, zorder=7))
    ax.add_patch(Circle((d["x"], yf+0.05+gw/2), 0.08, fc=C["dp"], ec="none", zorder=8))
    q = tot[d["id"]]
    ax.text(d["x"], yf+1.55, f"{d['id']}  x {d['x']:.1f}\nRWP 100 mm\n{q[1]:.1f} l/s (100 mm/h)\n{q[2]:.1f} l/s (150 mm/h)",
            ha="center", va="bottom", fontsize=7.5, color=C["dp"], zorder=8)
# fall arrows in gutters
def fall(xa, xb, yf):
    ax.add_patch(FancyArrowPatch((xa, yf+0.05+gw/2), (xb, yf+0.05+gw/2), arrowstyle="-|>", mutation_scale=10,
                                 color=C["gutter"], lw=0.8, zorder=5))
fall(hpW-0.3, 68.7+0.4, Y_NW); fall(hpW+0.3, 77.3-0.4, Y_NW)
fall(hpE-0.3, 85.3+0.4, Y_NE); fall(hpE+0.3, 92.0-0.4, Y_NE)
ax.text(hpW, Y_NW-0.25, "fall 1:350 to outlets, EJ at high point", ha="center", va="top", fontsize=7, color=C["gutter"])
ax.text(hpE, Y_NE-0.25, "fall 1:350 to outlets, EJ at high point", ha="center", va="top", fontsize=7, color=C["gutter"])
# columns (existing) for reference
cols = json.load(open("/home/user/test1strsteel/roof/geometry.json"))["columns"]
for c in cols:
    ax.add_patch(Rectangle((c["cx"]-c["bx"]/2, c["cy"]-c["by"]/2), c["bx"], c["by"], fc="#555", ec="none", zorder=3))
    ax.text(c["cx"]+0.25, c["cy"]+0.15, c["id"], fontsize=6, color="#555", zorder=3)
# catchment labels
ax.text(72.9, 25.5, f"Catchment W\n{A_west_wing:.0f} m2 + {div:.1f} m2 diverted\n= {A_W:.0f} m2 -> {A_W*kW*r100:.1f} l/s",
        ha="center", va="center", fontsize=8.5, color=C["text"], bbox=dict(fc="white", ec="#9fb4c8", alpha=0.9))
ax.text(89.6, 30.2, f"Catchment E\n{A_east_blk:.0f} m2 + {div:.1f} m2 diverted\n= {A_E:.0f} m2 -> {A_E*kW*r100:.1f} l/s",
        ha="center", va="center", fontsize=8.5, color=C["text"], bbox=dict(fc="white", ec="#9fb4c8", alpha=0.9))
ax.text(79.84, 26.7, f"strip {A_strip:.1f} m2\n-> 50/50 E/W", ha="center", va="center", fontsize=7.5, color="#3f6b32")
# edges labels
ax.text((X0+77.89)/2, Y_S-0.45, "high edge y 15.57 (south)", ha="center", va="top", fontsize=8)
ax.text((X_JOG+X1)/2, 19.97-0.45, "notch edge y 19.97 (verge flashing)", ha="center", va="top", fontsize=8)
ax.annotate("north-wall jog 0.5 m", xy=(X_JOG, (Y_NW+Y_NE)/2), xytext=(79.9, 37.2), fontsize=7.5, ha="center",
            arrowprops=dict(arrowstyle="->", color="#555"), color="#555")
ax.text(64.9, 33.5, "N", fontsize=13, fontweight="bold", ha="center")
ax.add_patch(FancyArrowPatch((64.9, 31.2), (64.9, 33.0), arrowstyle="-|>", mutation_scale=16, color="black", lw=1.5))
ax.set_xlim(64.0, 99.5); ax.set_ylim(13.5, 39.5)
ax.set_aspect("equal")
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
ax.grid(True, color=C["grid"], lw=0.4, alpha=0.6)
ax.set_title("Roof drainage layout - single plane 6 % falling north, external box gutters and 4 downpipes on the north facade\n"
             f"r = 100 mm/h (0.028 l/s.m2); roofed area {A_roofed:.0f} m2; total {sum(v[1] for v in tot.values()):.1f} l/s "
             f"({sum(v[2] for v in tot.values()):.1f} l/s at 150 mm/h)", fontsize=10)
fig.tight_layout()
fig.savefig(f"{OUT}/drainage_layout.png")
plt.close(fig)

# ================= gutter_section.png =================
fig, (axo, axd) = plt.subplots(1, 2, figsize=(15, 8.5), dpi=150, gridspec_kw=dict(width_ratios=[1, 1.9]))
# ---- (a) overview elevation, mm, x = distance from the north outer face (positive outside) ----
ax = axo
ax.add_patch(Rectangle((-300, -4000), 300, 4000, fc="#d9d4cc", ec="#7a7268", lw=1.0, hatch="..."))
ax.add_patch(Rectangle((-1200, -250), 1200, 250, fc="#c9c3ba", ec="#7a7268", lw=1.0, hatch="///"))
ax.text(-750, -125, "existing ribbed slab", ha="center", va="center", fontsize=8)
ax.text(-150, -2000, "existing north facade\n(concrete / block)", ha="center", va="center", fontsize=8, rotation=90)
ax.add_patch(Rectangle((-260, 40), 160, 3020, fc="#9aa9b8", ec="#2b3a4a", lw=1.0))
ax.text(-180, 1500, "new steel column", ha="center", va="center", fontsize=7.5, rotation=90)
ax.add_patch(Rectangle((-60, 40), 60, 3350, fc="#efe3c8", ec="#8a6d3b", lw=0.8))
ax.add_patch(Rectangle((-1200, 3060), 1200, 240, fc="#9aa9b8", ec="#2b3a4a", lw=1.0))
ax.add_patch(Polygon([(-1200, 3450+72), (80, 3450-5), (80, 3500-5), (-1200, 3500+72)], fc="#dfe7ef", ec="#2b3a4a", lw=1.0))
ax.text(-600, 3600, "roof 6 % fall ->", ha="center", fontsize=8)
# gutter box + outlet + downpipe
ax.add_patch(Rectangle((45, 3235), 150, 160, fc="#cfe3f5", ec="#1f6fb2", lw=1.5))
ax.plot([70, 70, 35, 35], [3235, 2950, 2850, -3800], color="#d1495b", lw=2)
ax.plot([170, 170, 135, 135], [3235, 2950, 2850, -3800], color="#d1495b", lw=2)
ax.plot([135, 320, 320], [-3800, -3800, -3900], color="#d1495b", lw=2)
ax.plot([35, 35], [-3800, -3900], color="#d1495b", lw=2)
for y in (2400, 800, -800, -2400):
    ax.plot([0, 30], [y, y], color="#333", lw=2.5)
ax.text(200, 800, "pipe clips <= 2.0 m\ninto concrete wall /\ncolumn", fontsize=7.5, va="center")
ax.text(200, -1600, "rodding access\n1.0 m above ground", fontsize=7.5, va="center")
ax.plot([35, 135], [-3000, -3000], color="#333", lw=2)
ax.plot([-1200, 900], [-4000, -4000], color="k", lw=1.2)
ax.add_patch(Rectangle((250, -4150), 250, 150, fc="#bbb", ec="#333", lw=0.8))
ax.text(375, -4200, "existing surface\ndrain / gully", ha="center", va="top", fontsize=7.5)
ax.annotate("", xy=(-700, 40), xytext=(-700, 3060), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.text(-730, 1550, "3.0 m clear", rotation=90, va="center", ha="right", fontsize=8)
ax.annotate("", xy=(600, -4000), xytext=(600, 3300), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.text(640, -400, "~7.4 m\ndownpipe", va="center", fontsize=8)
ax.text(-1150, 3100, "existing +4.0 m\nassumed", fontsize=7, va="top")
ax.set_xlim(-1300, 1000); ax.set_ylim(-4400, 4000); ax.set_aspect("equal")
ax.set_xlabel("mm from north outer face"); ax.set_ylabel("mm above existing slab")
ax.set_title("(a) Elevation: downpipe 100 dia\nfrom gutter to existing surface drain", fontsize=9.5)
ax.grid(True, color="#d0d6dc", lw=0.4, alpha=0.6)
# ---- (b) eave detail ----
ax = axd
ax.add_patch(Rectangle((-1000, 3060), 1000, 240, fc="#9aa9b8", ec="#2b3a4a", lw=1.2))
ax.text(-500, 3180, "eave beam / rafter end (IPE), TOS on the 6 % plane", ha="center", va="center", fontsize=8)
ax.add_patch(Rectangle((-60, 2700), 60, 690, fc="#efe3c8", ec="#8a6d3b", lw=1.0))
ax.text(-30, 2900, "BoardX wall\non girts", ha="center", va="center", fontsize=7, rotation=90)
ax.add_patch(Rectangle((-360, 3300), 90, 200, fc="#b8c4d0", ec="#2b3a4a", lw=1.0))
ax.text(-315, 3290, "eave purlin Z200", ha="center", va="top", fontsize=7.5)
xp = [-1000, 80]; yp = [3500+0.06*1000, 3500-0.06*80]
ax.add_patch(Polygon([(xp[0], yp[0]-50), (xp[1], yp[1]-50), (xp[1], yp[1]), (xp[0], yp[0])], fc="#dfe7ef", ec="#2b3a4a", lw=1.2))
ax.text(-560, 3585, "PIR sandwich panel 50, 6 % fall ->", ha="center", va="bottom", fontsize=8, rotation=-3.4)
ax.plot([80, 80, 70], [yp[1], yp[1]-90, yp[1]-100], color="#2b3a4a", lw=1.5)
ax.annotate("panel drip flashing\n60 mm into gutter", xy=(80, yp[1]-60), xytext=(250, 3560), fontsize=7.5,
            arrowprops=dict(arrowstyle="->", color="#2b3a4a"))
ax.add_patch(Rectangle((0, 3080), 25, 320, fc="#8d8d8d", ec="#2b3a4a", lw=0.8))
ax.annotate("fascia rail C200x60x2.5 (or eave Z)\nfixed to every rafter end / eave beam", xy=(12, 3120), xytext=(250, 2925),
            fontsize=7.5, arrowprops=dict(arrowstyle="->", color="#333"))
ax.plot([25, 60, 60, 240, 240], [3390, 3390, 3230, 3230, 3345], color="#d1495b", lw=2.5)
ax.annotate("bracket flat 40x5 galv. @ 600\n(0.15 kN gravity + 0.5 kN point,\n0.30 kN uplift per bracket)", xy=(150, 3230), xytext=(400, 3075),
            fontsize=7.5, color="#d1495b", arrowprops=dict(arrowstyle="->", color="#d1495b"))
gx0, gx1, gs = 45, 195, 3235
back_top, front_top = 3395, 3385
ax.plot([gx0-15, gx0, gx0, gx1, gx1, gx1-15], [back_top, back_top, gs, gs, front_top, front_top], color="#1f6fb2", lw=2.4)
ax.add_patch(Rectangle((gx0+2, gs+2), gx1-gx0-4, 58, fc="#bcd8f0", ec="none", alpha=0.9))
ax.plot([gx0+2, gx1-2], [gs+60, gs+60], color="#1f6fb2", lw=0.8, ls="--")
ax.text(gx0+75, gs+28, "water ~60 mm\n(100 mm/h)", ha="center", va="center", fontsize=6.5, color="#0b3d66")
ax.annotate("box gutter 150 x 100, 0.7 mm coated steel\n(or 1.0 mm alu); outer lip 10 mm lower than\nback = whole length overflows outward",
            xy=(gx1, front_top), xytext=(330, 3470), fontsize=7.5, color="#1f6fb2", arrowprops=dict(arrowstyle="->", color="#1f6fb2"))
ax.plot([gx0, gx1], [gs-30, gs-30], color="k", lw=0.6); ax.text((gx0+gx1)/2, gs-40, "150", ha="center", va="top", fontsize=7)
ax.plot([gx1+15, gx1+15], [gs, gs+100], color="k", lw=0.6); ax.text(gx1+22, gs+50, "100", va="center", fontsize=7)
ax.plot([gx0-5, gx0-5], [gs+60, back_top], color="k", lw=0.6); ax.text(gx0-12, gs+110, "40 free-\nboard", va="center", ha="right", fontsize=6.5)
ox = (gx0+gx1)/2
ax.plot([ox-50, ox-50], [gs, gs-130], color="#d1495b", lw=2); ax.plot([ox+50, ox+50], [gs, gs-130], color="#d1495b", lw=2)
ax.plot([ox-75, ox-50], [gs, gs-30], color="#d1495b", lw=1.5); ax.plot([ox+75, ox+50], [gs, gs-30], color="#d1495b", lw=1.5)
th = [i*math.pi/20 for i in range(21)]
ax.plot([ox+60*math.cos(t) for t in th], [gs+60*math.sin(t) for t in th], color="#d1495b", lw=1.0, ls=":")
ax.annotate("outlet 100 dia, conical inlet,\nwire-balloon leaf/sand strainer\n(at DP1-DP4; 2.65 l/s @ 50 mm head,\n3.5 l/s @ 60 mm)",
            xy=(ox+50, gs-80), xytext=(330, 3195), fontsize=7.5, color="#d1495b", arrowprops=dict(arrowstyle="->", color="#d1495b"))
dpc = 85
ax.plot([ox-50, dpc-50, dpc-50], [gs-130, 2930, 2650], color="#d1495b", lw=2)
ax.plot([ox+50, dpc+50, dpc+50], [gs-130, 2990, 2650], color="#d1495b", lw=2)
ax.text(dpc+70, 2800, "2 x 45 deg swan neck,\ndownpipe 100 dia\ncentre 85 mm off the wall", fontsize=7.5, va="center")
ax.plot([gx1, gx1+70], [gs+70, gs+58], color="#e69f00", lw=3, ls="--")
ax.annotate("tell-tale overflow spout 100x30 at each\nstop end, sole +70 (x 67.89 / 77.89 / 81.79 / 95.69)",
            xy=(gx1+60, gs+62), xytext=(330, 3395), fontsize=7.5, color="#b07600", arrowprops=dict(arrowstyle="->", color="#b07600"))
ax.annotate("", xy=(-1050, 3060), xytext=(-1050, 3395), arrowprops=dict(arrowstyle="<->", lw=0.8))
ax.text(-1070, 3230, "0.34", ha="right", va="center", fontsize=7)
ax.text(-1000, 2720, "System A: eave beam IPE 200 at the column line, panel overhangs to the outer face.\nSystem C: primary IPE 330 at y 35.2 / 35.7, rafters IPE 270 run to the outer face.\nIn both, the gutter hangs OUTSIDE the outer face on a continuous fascia rail.",
        fontsize=7.5, va="bottom", ha="left", bbox=dict(fc="white", ec="#9fb4c8"))
ax.set_xlim(-1100, 1000); ax.set_ylim(2650, 3700); ax.set_aspect("equal")
ax.set_xlabel("mm from north outer face (north / outside ->)"); ax.set_ylabel("mm above existing slab")
ax.set_title("(b) Eave detail: external box gutter 150x100 on brackets @ 600, fascia rail, outlet, overflow", fontsize=9.5)
ax.grid(True, color="#d0d6dc", lw=0.4, alpha=0.6)
fig.suptitle("North eave section - indicative, valid for System A and System C (existing height ~4.0 m assumed)", fontsize=11)
fig.tight_layout()
fig.savefig(f"{OUT}/gutter_section.png")
plt.close(fig)
print("figures + json written")
