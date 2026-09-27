"""Horizontal load to the roof diaphragm (wind, seismic check) and its distribution to the 7 X-braced bays.
Rigid-diaphragm stiffness share (3 DOF) AND simple tributary share; the envelope is used.  kN, m."""
import numpy as np, math
from model import FACES, POSTS, BAYS, bay_geom, wall_h, ENV, NOTCH, L_col, COLS
from loads import QP, G_ROOF, G_WALL
from sections import E, FY, FU, GM0, GM2

C_GLOBAL = 1.3            # (cpe,D - cpe,E + friction) per the load basis
DIAG = dict(name='L 70x7', A=940.0, e_bolt=19.7)   # mm2 ; one angle per diagonal, tension only
BOLT = dict(d=20, d0=22, As=245.0, Fv=94.0, Ft=141.0)  # M20 8.8 per basis

def face_roof_force(d):
    """Wind from d: characteristic force at roof level (kN) on each windward-projected face, with resultant position.
    Returns list of (F, x_res, y_res)."""
    normal = {'N':'y+', 'S':'y-', 'E':'x+', 'W':'x-'}[d]
    out = []
    for f in FACES:
        if f['normal'] != normal: continue
        n = 200; t = np.linspace(f['a'], f['b'], n+1)
        if normal[0] == 'y': ys = np.full_like(t, f['c']); xs = t
        else: ys = t; xs = np.full_like(t, f['c'])
        q = C_GLOBAL*QP*wall_h(ys)/2.0        # half of the wall to the roof (pinned columns)
        F = np.trapezoid(q, t); xr = np.trapezoid(q*xs, t)/F; yr = np.trapezoid(q*ys, t)/F
        out.append((F, xr, yr, f['id']))
    return out

def bay_stiffness():
    """k (kN/m) of one tension diagonal per bay: E A cos^2(alpha) / L_d."""
    ks = {}
    for b in BAYS:
        w, h, Ld, xm, ym = bay_geom(b)
        ks[b['id']] = E*DIAG['A']/1e3*(w/Ld)**2/(Ld)   # kN/m  (E MPa * mm2 = N -> /1e3 kN)
    return ks

def distribute(d):
    """Return {bay: H (kN, characteristic, roof level)} for wind from d: max of rigid-diaphragm and tributary."""
    forces = face_roof_force(d)
    Ftot = sum(F for F, *_ in forces)
    dirn = 'y' if d in 'NS' else 'x'
    ks = bay_stiffness()
    # rigid diaphragm
    kx = {b['id']: ks[b['id']] for b in BAYS if b['dir']=='x'}; ky = {b['id']: ks[b['id']] for b in BAYS if b['dir']=='y'}
    pos = {b['id']: bay_geom(b)[3:5] for b in BAYS}
    xr = sum(ky[i]*pos[i][0] for i in ky)/sum(ky.values()); yr = sum(kx[i]*pos[i][1] for i in kx)/sum(kx.values())
    J = sum(kx[i]*(pos[i][1]-yr)**2 for i in kx) + sum(ky[i]*(pos[i][0]-xr)**2 for i in ky)
    H = {i: 0.0 for i in ks}
    for F, xf, yf, _ in forces:
        if dirn == 'y':
            T = F*(xf - xr)                 # torque (Fy at xf about centre of rigidity)
            for i in ky: H[i] += F*ky[i]/sum(ky.values()) + T*ky[i]*(pos[i][0]-xr)/J
            for i in kx: H[i] += -T*kx[i]*(pos[i][1]-yr)/J
        else:
            T = -F*(yf - yr)
            for i in kx: H[i] += F*kx[i]/sum(kx.values()) - T*kx[i]*(pos[i][1]-yr)/J
            for i in ky: H[i] += T*ky[i]*(pos[i][0]-xr)/J
    Hrig = {i: abs(v) for i, v in H.items()}
    # tributary (perimeter truss spans between adjacent bracing lines; each face load split by tributary width)
    Htrib = {i: 0.0 for i in ks}
    lines = sorted([(pos[b['id']][0 if dirn=='y' else 1], b['id']) for b in BAYS if b['dir']==dirn])
    for F, xf, yf, fid in forces:
        # spread the face load along its length and assign each strip to the two adjacent bracing lines
        f = next(ff for ff in FACES if ff['id']==fid)
        t = np.linspace(f['a'], f['b'], 201); q = C_GLOBAL*QP*wall_h(np.full_like(t, f['c']) if f['normal'][0]=='y' else t)/2
        for ti, qi in zip(t, q):
            dF = qi*(f['b']-f['a'])/200
            left = [l for l in lines if l[0] <= ti]; right = [l for l in lines if l[0] > ti]
            if left and right:
                (a, ia), (b, ib) = left[-1], right[0]
                Htrib[ib] += dF*(ti-a)/(b-a); Htrib[ia] += dF*(b-ti)/(b-a)
            elif left: Htrib[left[-1][1]] += dF
            else: Htrib[right[0][1]] += dF
    return {i: max(Hrig[i], Htrib[i]) for i in ks}, Ftot, Hrig, Htrib

def seismic_check(roof_area, steel_kN):
    """EN 1998-1 lateral force method, a_g = 0.10 g, soil B (S=1.2, TB..TC plateau), q = 1.5."""
    m = G_ROOF*roof_area + steel_kN + 0.5*sum(G_WALL*(f['b']-f['a'])*wall_h(0.5*(f['a']+f['b']) if f['normal'][0]=='x' else f['c']) for f in FACES)
    Sd = 0.10*1.2*2.5/1.5      # g
    return dict(W=m, Sd=Sd, Fb=Sd*m)

def check_diagonal(T_Ed):
    """Single angle L70x7 S275 connected by one leg with 2 M20 bolts (p1 = 5 d0): EN 1993-1-8 3.10.3 beta2 = 0.7."""
    A = DIAG['A']; Anet = A - BOLT['d0']*7
    Npl = A*FY/GM0/1e3; Nu = 0.7*Anet*FU/GM2/1e3
    NtRd = min(Npl, Nu)
    # gusset bolts: 2 M20 single shear; bearing on 10 mm gusset (e1 = 40, p1 = 110 -> alpha_b = min(40/66, 110/66-0.25, 800/430, 1) = 0.61)
    ab = min(40/(3*22), 110/(3*22)-0.25, 800/430, 1.0); k1 = min(2.8*40/22-1.7, 2.5)
    FbRd = k1*ab*FU*20*10/GM2/1e3
    FvRd = 2*BOLT['Fv']; FbRd2 = 2*FbRd
    return dict(NtRd=NtRd, Npl=Npl, Nu=Nu, util=T_Ed/NtRd, FvRd=FvRd, FbRd=FbRd2, util_bolt=T_Ed/min(FvRd, FbRd2))

def bay_forces(H):
    """Given bay shear H (kN), return diagonal tension T, column axial +/-N, base shear."""
    out = {}
    for b in BAYS:
        w, h, Ld, xm, ym = bay_geom(b)
        Hi = H[b['id']]
        out[b['id']] = dict(H=Hi, T=Hi*Ld/w, N=Hi*h/w, w=w, h=h, Ld=Ld, sway=Hi/bay_stiffness()[b['id']]*1000)  # sway mm at H
    return out

if __name__ == '__main__':
    for d in 'NSEW':
        H, Ftot, Hr, Ht = distribute(d)
        print(d, 'F_roof=%.1f' % Ftot, {k: round(v,1) for k, v in H.items()})
    print(bay_stiffness())

# ---------------- roof-plane bracing (horizontal trusses in the roof plane, X diagonals tension-only) ----------
ROD = dict(name='M20 rod 8.8', As=245.0, FtRd=141.0, kg=2.47)
# Trusses: id, wind dir served, chord lines, depth D, span L between bracing lines, panel list (x0,x1,y0,y1)
ROOF_TRUSSES = [
 dict(id='RT-N-W', dirs='NS', span=(67.99, 77.78), D=5.90, face='N',  panels=[(67.99,70.04,29.32,35.22),(70.04,72.09,29.32,35.22),(72.09,74.90,29.27,35.22),(74.90,77.78,29.27,35.17)]),
 dict(id='RT-N-E', dirs='NS', span=(81.85, 95.55), D=6.40, face='N',  panels=[(81.85,84.50,29.27,35.67),(84.50,87.19,29.27,35.72),(87.19,89.90,29.27,35.77),(89.90,92.48,29.27,35.77),(92.48,95.55,29.27,35.67)]),
 dict(id='RT-S-E', dirs='NS', span=(81.85, 95.55), D=9.20, face='S2', panels=[(81.85,84.50,20.07,29.27),(84.50,87.19,20.07,29.27),(87.19,89.90,20.07,29.27),(89.90,92.48,20.07,29.27),(92.48,95.55,20.07,29.27)]),
 dict(id='RT-S-W', dirs='NS', span=(67.99, 77.78), D=5.89, face='S1', panels=[(67.99,70.04,15.87,21.76),(70.04,72.09,15.87,21.76),(72.09,74.90,15.92,21.76),(74.90,77.78,15.92,21.76)]),
 dict(id='RT-W',   dirs='EW', span=(15.87, 35.22), D=4.10, face='W',  panels=[(67.99,72.09,21.76,29.32)]),   # + shares the N-W and S-W panels
 dict(id='RT-E',   dirs='EW', span=(20.07, 35.72), D=5.65, face='E',  panels=[]),                             # uses the two east panels of RT-N-E / RT-S-E
 dict(id='RT-JOG', dirs='NS', span=(77.78, 81.85), D=4.81, face='N',  panels=[(77.78,81.85,24.46,29.27)]),   # shear transfer past the stair well
]
def roof_truss_forces(H_bays_uls):
    """Simple statics per truss: line load w = wind at roof level on the served face (ULS), truss simply supported
    between its two bracing lines: V = wL/2 (>= the larger adjacent bay force is NOT required: each bay's H comes
    from the diaphragm shear next to it), chord = wL^2/8/D, diagonal T = V/sin(theta), post = V."""
    out = []
    for t in ROOF_TRUSSES:
        f = next(ff for ff in FACES if ff['id'] == t['face'])
        L = t['span'][1] - t['span'][0]
        c = 0.5*(f['a']+f['b']); yy = f['c'] if f['normal'][0]=='y' else c
        w = 1.5*C_GLOBAL*QP*wall_h(yy)/2.0            # ULS kN/m along the eave
        if t['id'] == 'RT-JOG':                          # carries the shear of RT-N-E's west end past the stair well
            V = H_bays_uls['B8'] if 'B8' in H_bays_uls else w*L/2
        elif t['id'] == 'RT-E': V = max(H_bays_uls.get('B3', 0), H_bays_uls.get('B1', 0))
        elif t['id'] == 'RT-W': V = max(H_bays_uls.get('B2', 0), H_bays_uls.get('B4', 0))
        else: V = w*L/2
        # panel aspect: use the shallowest angle of the truss panels (worst for the diagonal)
        if t['id'] == 'RT-E': a = 9.20; D = t['D']
        elif t['id'] == 'RT-W': a = 7.56; D = t['D']
        else:
            a = max(p[1]-p[0] for p in t['panels']) if t['panels'] else 3.0; D = t['D']
        Ld = (a**2 + D**2)**0.5; sin = D/Ld
        T = V/sin; chord = w*L**2/8/D if t['id'] not in ('RT-E', 'RT-W', 'RT-JOG') else V*L/4/D
        out.append(dict(id=t['id'], L=L, D=D, w=w, V=V, T=T, chord=chord, post=V, Ld=Ld, util=T/ROD['FtRd'], npanels=len(t['panels'])))
    return out

def roof_bracing_length():
    tot = 0.0; n = 0
    for t in ROOF_TRUSSES:
        for (x0, x1, y0, y1) in t['panels']:
            tot += 2*((x1-x0)**2 + (y1-y0)**2)**0.5; n += 1
    return tot, n
