"""Rev 2. Horizontal load to the roof diaphragm (wind incl. the horizontal component of the roof suction, seismic check)
and its distribution to the X-braced bays: rigid-diaphragm stiffness share (3 DOF) AND flexible tributary share per
bracing line (bays on one line share by stiffness); the envelope is used. Roof-plane trusses with M24 rods and their
deflection by virtual work.  kN, m."""
import numpy as np, math
from functools import lru_cache
from model import FACES, POSTS, BAYS, bay_geom, wall_h, ENV, NOTCH, L_col, COLS, roofed
from loads import QP, G_ROOF, G_WALL, SLOPE_SIN, roof_grid, wind_fields
from sections import E, FY, FU, GM0, GM2

C_GLOBAL = 1.3            # cpe,D - cpe,E = 0.8 + 0.5 (no friction term, basis Rev 2)
DIAG = dict(name='L 70x7', A=940.0)                      # one angle per diagonal, tension only
BOLT = dict(d=20, d0=22, As=245.0, Fv=94.0, Ft=141.0)
ROD = dict(name='M24 rod 8.8', As=353.0, FtRd=0.9*800*353/1.25/1e3, kg=3.55)   # 203 kN

@lru_cache(None)
def roof_suction_component():
    """Horizontal (northward, +y) component of the net roof suction for wind from S, E, W (char., kN):
    total, centroid x, y, and the distribution along x (strip loads) for the tributary method."""
    X, Y, R, dx = roof_grid(0.1); W = wind_fields(X, Y, R)
    out = {}
    for d in 'SEW':
        f = -W[d]*dx*dx*SLOPE_SIN                # kN per cell, positive northward
        F = f.sum(); xc = (f*X).sum()/F; yc = (f*Y).sum()/F
        strips = list(zip(X[:, 0], f.sum(axis=1)))
        out[d] = (float(F), float(xc), float(yc), strips)
    return out

def face_roof_force(d):
    """Wind from d: characteristic force at roof level (kN) on each windward-projected face, resultant position,
    and its distribution along the face (for the tributary method). Returns list of dicts."""
    normal = {'N':'y+', 'S':'y-', 'E':'x+', 'W':'x-'}[d]
    out = []
    for f in FACES:
        if f['normal'] != normal: continue
        t = np.linspace(f['a'], f['b'], 201)
        if normal[0] == 'y': ys = np.full_like(t, f['c']); xs = t
        else: ys = t; xs = np.full_like(t, f['c'])
        q = C_GLOBAL*QP*wall_h(ys)/2.0            # half of the wall to the roof (pinned columns)
        F = np.trapezoid(q, t); xr = np.trapezoid(q*xs, t)/F; yr = np.trapezoid(q*ys, t)/F
        strips = list(zip(t, q*(f['b']-f['a'])/200))
        out.append(dict(F=float(F), x=float(xr), y=float(yr), id=f['id'], along='x' if normal[0]=='y' else 'y', strips=strips))
    if d in 'SEW':
        F, xc, yc, strips = roof_suction_component()[d]
        out.append(dict(F=F, x=xc, y=yc, id='roof-suction-h', along='x', strips=strips, dirn='y'))
    return out

def bay_stiffness():
    return {b['id']: E*DIAG['A']/1e3*(bay_geom(b)[0]/bay_geom(b)[2])**2/bay_geom(b)[2] for b in BAYS}   # kN/m

def _rigid(forces):
    """forces: list of (Fx, Fy, x, y). Returns {bay: H} (signed along its direction)."""
    ks = bay_stiffness(); pos = {b['id']: bay_geom(b)[3:5] for b in BAYS}
    kx = {b['id']: ks[b['id']] for b in BAYS if b['dir']=='x'}; ky = {b['id']: ks[b['id']] for b in BAYS if b['dir']=='y'}
    xr = sum(ky[i]*pos[i][0] for i in ky)/sum(ky.values()); yr = sum(kx[i]*pos[i][1] for i in kx)/sum(kx.values())
    J = sum(kx[i]*(pos[i][1]-yr)**2 for i in kx) + sum(ky[i]*(pos[i][0]-xr)**2 for i in ky)
    H = {i: 0.0 for i in ks}
    for Fx, Fy, xf, yf in forces:
        T = Fy*(xf - xr) - Fx*(yf - yr)          # torque about the centre of rigidity (z up)
        for i in ky: H[i] += Fy*ky[i]/sum(ky.values()) + T*ky[i]*(pos[i][0]-xr)/J
        for i in kx: H[i] += Fx*kx[i]/sum(kx.values()) - T*kx[i]*(pos[i][1]-yr)/J
    return H, (xr, yr)

def _tributary(items, dirn):
    """items: list of dicts with 'strips' [(coordinate along the perpendicular axis, dF)] for a load in direction dirn.
    Each strip goes to the two adjacent bracing lines (perpendicular coordinate), then to the bays on that line by k."""
    ks = bay_stiffness(); pos = {b['id']: bay_geom(b)[3:5] for b in BAYS}
    lines = {}
    for b in BAYS:
        if b['dir'] != dirn: continue
        key = round(pos[b['id']][0 if dirn=='y' else 1], 1); lines.setdefault(key, []).append(b['id'])
    lc = sorted(lines)
    Hl = {c: 0.0 for c in lc}
    for it in items:
        for t, dF in it['strips']:
            left = [c for c in lc if c <= t]; right = [c for c in lc if c > t]
            if left and right:
                a, b = left[-1], right[0]; Hl[b] += dF*(t-a)/(b-a); Hl[a] += dF*(b-t)/(b-a)
            elif left: Hl[left[-1]] += dF
            else: Hl[right[0]] += dF
    H = {b['id']: 0.0 for b in BAYS}
    for c, bays in lines.items():
        kt = sum(ks[i] for i in bays)
        for i in bays: H[i] = Hl[c]*ks[i]/kt
    return H

def distribute(d):
    """Wind from d. Returns ({bay: H char. (magnitude)}, F_total, H_rigid, H_trib)."""
    forces = face_roof_force(d)
    rig = []
    for f in forces:
        dirn = f.get('dirn', 'y' if d in 'NS' else 'x')
        sgn = {'N': -1, 'S': +1, 'E': -1, 'W': +1}[d] if f['id'] != 'roof-suction-h' else +1
        rig.append((sgn*f['F'] if dirn == 'x' else 0.0, sgn*f['F'] if dirn == 'y' else 0.0, f['x'], f['y']))
    Hr, _ = _rigid(rig)
    wall = [f for f in forces if f['id'] != 'roof-suction-h']; roof = [f for f in forces if f['id'] == 'roof-suction-h']
    Ht = _tributary(wall, 'y' if d in 'NS' else 'x')
    if roof:
        Hy = _tributary(roof, 'y')
        for i in Hy: Ht[i] += Hy[i] if d != 'N' else 0.0
    Ftot = sum(f['F'] for f in forces)
    return {i: max(abs(Hr[i]), abs(Ht[i])) for i in Hr}, Ftot, {i: abs(v) for i, v in Hr.items()}, Ht

def distribute_point(F, xc, yc, dirn):
    """A single horizontal force (seismic) at (xc, yc) in direction dirn, with 5 % accidental eccentricity: envelope of
    rigid share (both eccentricity signs) and tributary by roof area."""
    Lperp = (ENV['x1']-ENV['x0']) if dirn == 'y' else (ENV['y1']-ENV['y0'])
    Hs = []
    for e in (-0.05*Lperp, 0.05*Lperp):
        x, y = (xc + e, yc) if dirn == 'y' else (xc, yc + e)
        H, _ = _rigid([(F if dirn=='x' else 0.0, F if dirn=='y' else 0.0, x, y)]); Hs.append({i: abs(v) for i, v in H.items()})
    X, Y, R, dx = roof_grid(0.2); A = R.sum()
    ax = 0 if dirn == 'y' else 1
    coord = X[:, 0] if dirn == 'y' else Y[0, :]
    strips = list(zip(coord, F*R.sum(axis=1-ax)/A))
    Ht = _tributary([dict(strips=strips)], dirn)
    return {i: max(Hs[0][i], Hs[1][i], Ht[i]) for i in Ht}

def seismic_check(roof_area, steel_kN):
    """EN 1998-1 lateral force method, a_g = 0.10 g, soil B S = 1.2, plateau 2.5/q, q = 1.5, lambda = 1 (roof mass only;
    floor amplification through the existing building is an open item, review F9)."""
    m = G_ROOF*roof_area + steel_kN + 0.5*sum(G_WALL*(f['b']-f['a'])*wall_h(0.5*(f['a']+f['b']) if f['normal'][0]=='x' else f['c']) for f in FACES)
    Sd = 0.10*1.2*2.5/1.5
    return dict(W=m, Sd=Sd, Fb=Sd*m)

def check_diagonal(T_Ed):
    """Single angle L70x7 S275 connected by one leg with 2 M20 (p1 = 5 d0): EN 1993-1-8 3.10.3 beta2 = 0.7.
    Gusset bolts: 2 M20 single shear; bearing on the 10 mm gusset and the 7 mm angle leg with e1 = 40, p1 = 110,
    e2 = 30 (standard 40 mm gauge on the 70 leg, review F14)."""
    A = DIAG['A']; Anet = A - BOLT['d0']*7
    Npl = A*FY/GM0/1e3; Nu = 0.7*Anet*FU/GM2/1e3; NtRd = min(Npl, Nu)
    ab = min(40/(3*22), 110/(3*22)-0.25, 800/430, 1.0); k1 = min(2.8*30/22-1.7, 2.5)
    FbRd_g = k1*ab*FU*20*10/GM2/1e3; FbRd_a = k1*ab*FU*20*7/GM2/1e3
    FvRd = 2*BOLT['Fv']
    return dict(NtRd=NtRd, Npl=Npl, Nu=Nu, util=T_Ed/NtRd, FvRd=FvRd, FbRd=2*FbRd_a, util_bolt=T_Ed/min(FvRd, 2*FbRd_g, 2*FbRd_a))

def bay_forces(H):
    out = {}
    for b in BAYS:
        w, h, Ld, xm, ym = bay_geom(b); Hi = H[b['id']]
        out[b['id']] = dict(H=Hi, T=Hi*Ld/w, N=Hi*h/w, w=w, h=h, Ld=Ld, sway=Hi/bay_stiffness()[b['id']]*1000)
    return out

# ---------------- roof-plane bracing: X of M24 rods in the cells listed (one rafter bay x one rafter span), except the
# east and west edge trusses whose diagonals span TWO rafter bays (R90-R95 and R68-R72, passing the intermediate rafter
# through a slotted web clip) so that the truss depth is 5.65 / 4.10 m (review F10).
ROOF_TRUSSES = [
 dict(id='RT-N-W', dirs='NS', span=(67.99, 77.78), D=5.90, face='N1',  a=[2.05, 2.05, 2.81, 2.88],
      panels=[(67.99,70.04,29.32,35.22),(70.04,72.09,29.32,35.22),(72.09,74.90,29.27,35.22),(74.90,77.78,29.27,35.17)]),
 dict(id='RT-N-E', dirs='NS', span=(81.85, 95.55), D=6.40, face='N2',  a=[2.65, 2.69, 2.71, 2.58, 3.07],
      panels=[(81.85,84.50,29.27,35.67),(84.50,87.19,29.27,35.72),(87.19,89.90,29.27,35.77),(89.90,92.48,29.27,35.77),(92.48,95.55,29.27,35.67)]),
 dict(id='RT-S-E', dirs='NS', span=(81.85, 95.55), D=9.20, face='S2', a=[2.65, 2.69, 2.71, 2.58, 3.07],
      panels=[(81.85,84.50,20.07,29.27),(84.50,87.19,20.07,29.27),(87.19,89.90,20.07,29.27),(89.90,92.48,20.07,29.27),(92.48,95.55,20.07,29.27)]),
 dict(id='RT-S-W', dirs='NS', span=(67.99, 77.78), D=5.89, face='S1', a=[2.05, 2.05, 2.81, 2.88],
      panels=[(67.99,70.04,15.87,21.76),(70.04,72.09,15.87,21.76),(72.09,74.90,15.92,21.76),(74.90,77.78,15.92,21.76)]),
 dict(id='RT-W',   dirs='EW', span=(15.87, 35.22), D=4.10, face='W',  a=[5.89, 7.56, 5.90],
      panels=[(67.99,72.09,15.87,21.76),(67.99,72.09,21.76,29.32),(67.99,72.09,29.32,35.22)]),
 dict(id='RT-E',   dirs='EW', span=(20.07, 35.72), D=5.65, face='E',  a=[9.20, 6.45],
      panels=[(89.90,95.55,20.07,29.27),(89.90,95.55,29.27,35.72)]),
 dict(id='RT-JOG', dirs='NS', span=(77.78, 81.85), D=4.81, face='N2', a=[4.07], panels=[(77.78,81.85,24.46,29.27)]),   # single panel: carries the west-end reaction of RT-N-E into B8 (K10-K16)
]
def truss_analysis(t, w, V_end=None):
    """Simply supported horizontal truss, uniform load w (kN/m) over the span, panels a_i, depth D, X diagonals
    tension-only (one active per panel). Returns max diagonal T, chord force, and the deflection at the panel points by
    virtual work over the diagonals (chords and posts rigid), for rods of area ROD['As']."""
    a = np.array(t['a']); L = a.sum(); D = t['D']
    xs = np.concatenate([[0], np.cumsum(a)]); xm = 0.5*(xs[:-1] + xs[1:])
    V = w*L/2 - w*xm                                   # shear at panel mid-points
    if V_end is not None: V = V*(V_end/(w*L/2))        # scale to the bay force actually collected at the ends
    Ld = np.sqrt(a**2 + D**2); T = np.abs(V)*Ld/D
    M = w*L/2*xm - w*xm**2/2; chord = M.max()/D
    # deflection at each interior panel point p: unit load at p -> shear n_i = (1 - xp/L) for x < xp, -xp/L beyond
    dmax = 0.0
    for p in xs[1:-1]:
        n = np.where(xm < p, 1 - p/L, -p/L)*Ld/D
        dmax = max(dmax, float(abs((T*np.sign(V)*n*Ld).sum())/(E*ROD['As']/1e3)))  # m
    return dict(T=float(T.max()), chord=float(chord), V=float(np.abs(V).max()), Ld=float(Ld.max()), delta=dmax*1000, L=float(L))

def roof_truss_forces(H_bays_uls):
    out = []
    for t in ROOF_TRUSSES:
        f = next(ff for ff in FACES if ff['id'] == t['face'])
        c = 0.5*(f['a']+f['b']); yy = f['c'] if f['normal'][0]=='y' else c
        w = 1.5*C_GLOBAL*QP*wall_h(yy)/2.0
        if t['id'] in ('RT-N-E', 'RT-S-E', 'RT-N-W', 'RT-S-W'):    # add the roof-suction component share (N-S trusses)
            F, xc, yc, strips = roof_suction_component()['S']
            w += 1.5*F/(ENV['x1']-ENV['x0'])*0.5
        r = truss_analysis(t, w)
        if t['id'] == 'RT-E': r = truss_analysis(t, w, V_end=max(H_bays_uls.get('B3', 0), H_bays_uls.get('B1', 0)))
        if t['id'] == 'RT-W': r = truss_analysis(t, w, V_end=max(H_bays_uls.get('B2', 0), H_bays_uls.get('B4', 0)))
        if t['id'] == 'RT-JOG':      # one panel: end shear = west-end reaction of RT-N-E, T = V L_d/D, chord = V a/D
            Vj = next(x for x in out if x['id'] == 'RT-N-E')['w']*13.7/2
            Ld = (4.07**2 + 4.81**2)**0.5
            r = dict(T=Vj*Ld/4.81, chord=Vj*4.07/4.81, V=Vj, Ld=Ld, delta=Vj*Ld/4.81*Ld/(E*ROD['As']/1e3)*(Ld/4.81)*1000, L=4.07)
        r.update(id=t['id'], D=t['D'], w=w, util=r['T']/ROD['FtRd'], npanels=len(t['panels']), post=r['V'])
        out.append(r)
    return out

def roof_bracing_length():
    tot = 0.0; n = 0
    for t in ROOF_TRUSSES:
        for (x0, x1, y0, y1) in t['panels']:
            tot += 2*((x1-x0)**2 + (y1-y0)**2)**0.5; n += 1
    return tot, n

if __name__ == '__main__':
    for d in 'NSEW':
        H, Ftot, Hr, Ht = distribute(d)
        print(d, 'F=%.1f' % Ftot, 'env', {k: round(v, 1) for k, v in H.items()})
        print('   rigid', {k: round(v, 1) for k, v in Hr.items()}); print('   trib ', {k: round(v, 1) for k, v in Ht.items()})
    print('roof comp', {d: (round(v[0], 1), round(v[1], 1), round(v[2], 1)) for d, v in roof_suction_component().items()})
    for t in roof_truss_forces({k: 1.5*v for k, v in distribute('E')[0].items()}): print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in t.items()})

# ---------------- thermal restraint (Rev 3, C4) -------------------------------------------------------------------
ALPHA_T = 12e-6
def thermal_check(dT_service=20.0, dT_erection=30.0):
    """Locked-in E-W force between the two north E-W bays B2 (K5-K7, y 35.2) and B1 (K1-K2, y 35.8). Path: B2 -
    RT-N-W rods - y 29.3 primary chord (P_K10K11, tie plates) - RT-N-E rods - B1. Elastic upper bound, no bolt-slip
    credit. The south pair B4-B3 is linked only through the weak-axis bending of R78 (k ~ 0.3 kN/mm) and the N-S lines
    through three fin-plated rafter spans each (2 mm hole clearance per joint): both are released and not checked."""
    ks = bay_stiffness()
    def k_truss(tid):
        t = next(x for x in ROOF_TRUSSES if x['id'] == tid); k = 0.0
        for a in t['a']:
            Ld = (a**2 + t['D']**2)**0.5; cos2 = (a/Ld)**2
            k += E*ROD['As']/(Ld*1e3)*cos2/1e3      # one tension rod per panel, kN/mm
        return k
    kB2, kB1 = ks['B2']/1e3, ks['B1']/1e3            # kN/mm
    kW, kE = k_truss('RT-N-W'), k_truss('RT-N-E')
    Lch = 4.07; kch = E*62.6e2/(Lch*1e3)/1e3        # IPE 330 chord between the trusses, kN/mm
    keff = 1/(1/kB2 + 1/kW + 1/kch + 1/kE + 1/kB1)
    Lbay = 0.5*(87.19 + 92.48) - 0.5*(72.09 + 77.78)  # bay centres, m
    dL_s = ALPHA_T*dT_service*Lbay*1e3; dL_e = ALPHA_T*dT_erection*Lbay*1e3
    return dict(kB1=kB1, kB2=kB2, kW=kW, kE=kE, kch=kch, keff=keff, Lbay=Lbay, dL_s=dL_s, dL_e=dL_e,
                F_s=keff*dL_s, F_e=keff*dL_e, F_uls_wind=1.5*0.6*keff*dL_s, F_uls_erect=1.5*keff*dL_e)
