"""Rev 5a (review Z1-Z6): strut / chord line forces through the fin plates, the actual strip end-shear split (Z4),
EN 1998-1 4.4.3.2 drift (Z3). Units kN, m, mm."""
import numpy as np
from loads import roof_grid
from model import TOS
from connections import BOLT, bearing, FY, FU, GM0, GM2

def line_split(F_y, H_bays):
    """Tributary N-S inertia per block (roof grid, x-extent) -> strip end shears, scaled per line so that the line totals
    equal the enveloped bay forces (rigid / tributary / 5 % eccentricity)."""
    X, Y, R, dx = roof_grid(0.2); A = R.sum()
    x = X[:, 0]; col = R.sum(axis=1)*dx*dx                  # roofed area per x-strip
    w = F_y*col/A                                           # kN per x-strip
    def blk(x0, x1): m = (x >= x0) & (x < x1); return w[m], x[m]
    out = {}
    wW, xW = blk(67.99, 77.80); wJ, xJ = blk(77.80, 81.85); wE, xE = blk(81.85, 95.60)
    # simple-beam split within each block between its two supporting lines
    out['NW_to_x68'] = float((wW*(77.80 - xW)/(77.80 - 67.99)).sum()); out['NW_to_x778'] = float((wW*(xW - 67.99)/(77.80 - 67.99)).sum())
    out['JOG_to_x778'] = float(wJ.sum())
    out['NE_to_x778'] = float((wE*(95.55 - xE)/(95.55 - 81.85)).sum()); out['NE_to_x955'] = float((wE*(xE - 81.85)/(95.55 - 81.85)).sum())
    trib = {'x68': out['NW_to_x68'], 'x778': out['NW_to_x778'] + out['JOG_to_x778'] + out['NE_to_x778'], 'x955': out['NE_to_x955']}
    env = {'x68': H_bays['B5'], 'x778': H_bays['B7'], 'x955': H_bays['B6'] + H_bays['B9']}
    scale = {k: env[k]/trib[k] for k in trib}
    act = dict(RT_N_W=(out['NW_to_x68']*scale['x68'], out['NW_to_x778']*scale['x778']),
               RT_JOG=out['JOG_to_x778']*scale['x778'],
               RT_N_E=(out['NE_to_x778']*scale['x778'], out['NE_to_x955']*scale['x955']))
    return dict(trib=trib, env=env, scale=scale, actual=act, R82=act['RT_N_E'][0], R78=env['x778'], R68=env['x68'], R95=env['x955'])

def fin_axial(N, V, n, tw, tp=10, e=50, p1=70, e1=40, e2=40):
    """Fin plate with n M20 in one vertical row under axial N (along the rafter) and shear V; bolt-line eccentricity e.
    Bearing on the rafter web (tw) and on the plate for the resultant bolt force; bolt shear; plate net section; weld."""
    hp = 2*e1 + (n - 1)*p1
    r = [(i - (n - 1)/2)*p1 for i in range(n)]; sr2 = sum(ri**2 for ri in r) or 1.0
    Fh_M = V*e*max(abs(ri) for ri in r)/sr2 if n > 1 else 0.0
    Fh = N/n + Fh_M; Fv = V/n; Fb = (Fh**2 + Fv**2)**0.5
    FbRd_w = min(bearing(tw, e1, p1, e2), bearing(tw, e2, None, e1))     # vertical / horizontal force directions
    FbRd_p = min(bearing(tp, e1, p1, e2), bearing(tp, e2, None, e1))
    u = dict(bearing_web=Fb/FbRd_w, bearing_plate=Fb/FbRd_p, bolt_shear=Fb/BOLT['FvRd'],
             plate_net=N/((hp - n*22)*tp*FU/GM2/1e3) + V/((hp - n*22)*tp*FY/3**0.5/GM0/1e3),
             weld=((N*1e3/(2*6*hp))**2 + 3*((V*1e3/(2*6*hp))**2 + (V*e*1e3/(2*6*hp**2/6))**2))**0.5/(FU/(3**0.5*0.85*GM2)))
    return dict(N=N, V=V, n=n, hp=hp, Fb=Fb, FbRd_web=FbRd_w, u=u, umax=max(u.values()), gov=max(u, key=u.get))

def strut_table(H_bays, trusses, seg_V, split):
    """Members carrying diaphragm axial force through fin plates. N = E_y + 0.3 E_x or E_x + 0.3 E_y envelope of the
    strut (N-S line) and chord (E-W strip) forces; V = gravity end shear (G + Q, the seismic combination has psi_2 = 0)."""
    ch = {t['id']: t['chord'] for t in trusses}
    rows = []
    def add(m, where, Nstrut, Nchord, V, n, tw=6.6, note=''):
        N = max(Nstrut + 0.3*Nchord, Nchord + 0.3*Nstrut)
        f = fin_axial(N, V, n, tw)
        rows.append(dict(member=m, where=where, N_strut=Nstrut, N_chord=Nchord, N=N, V=V, n=n, u_bearing=f['u']['bearing_web'], u_bolt=f['u']['bolt_shear'], u_net=f['u']['plate_net'], u_weld=f['u']['weld'], umax=f['umax'], note=note))
    add('R68', 'K8, K15, K19, K25 (x 68 line)', split['R68'], ch['RT-W'], seg_V['R68'], 3, note='strut into B5 + RT-W chord')
    add('R72', 'K9, ST2, K26 (RT-W chord)', 8.2, ch['RT-W'], seg_V['R72'], 3, note='RT-W chord + rafter N-S strut')
    add('R78', 'K10, K16, K20 (x 77.8 line)', split['R78'], 0.0, seg_V['R78'], 2, note='strut into B7: whole line force')
    add('R82', 'K11, K17 (RT-N-E west post)', split['R82'], 0.0, seg_V['R82'], 2, note='RT-N-E west end shear (actual split)')
    add('R90', 'K13, K22 (RT-E chord)', 8.2, ch['RT-E'], seg_V['R90'], 3, note='RT-E chord + rafter N-S strut')
    add('R95', 'K4, K14, K18, K23 (x 95.5 line)', split['R95'], ch['RT-E'], seg_V['R95'], 3, note='strut into B6 + B9 + RT-E chord')
    add('R70/R75/R85/R87/R92', 'y 29.3 primary (N-S struts)', 8.2, 0.0, max(seg_V.values()), 2, note='south-band inertia to the y 29.3 chord')
    return rows

def drift_check(trusses, bays, q=1.5, nu=0.5):
    """EN 1998-1 4.4.3.2: d_r = q x d_e (d_e from the design forces, q 1.5), nu 0.5, limit 0.005 h (brittle cladding).
    d_e = roof-truss deflection at the wall mid-length (ULS design force) + bay sway. h = TOS at the location."""
    t = {x['id']: x for x in trusses}
    EA = 210000*4590/1e3                                     # IPE 270, kN
    out = {}
    out['west wall (RT-W + B4/B2)'] = dict(de=t['RT-W']['delta'] + max(bays['B4']['sway'], bays['B2']['sway']), h=TOS(25.6))
    out['east wall (RT-E + B3/B1)'] = dict(de=t['RT-E']['delta'] + max(bays['B3']['sway'], bays['B1']['sway']), h=TOS(28.0))
    out['x 77.8 line (jog + R78 + B7)'] = dict(de=t['RT-JOG']['delta'] + t['RT-JOG']['V']*13.4/EA*1000 + bays['B7']['sway'], h=TOS(24.5))
    out['x 68 line (RT-N-W + R68 + B5)'] = dict(de=t['RT-N-W']['delta'] + t['RT-N-W']['V']*3.0/EA*1000 + bays['B5']['sway'], h=TOS(26.4))
    for k, v in out.items():
        v['dr_nu'] = q*v['de']*nu; v['lim'] = 0.005*v['h']*1000; v['u'] = v['dr_nu']/v['lim']
    return out
