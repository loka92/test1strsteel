"""Load take-down: roof cells -> purlins (simple spans) -> N-S rafters -> E-W primaries -> columns.
Every beam is a chain of simple spans (pinned fin plates / cap plates). Load types tracked separately:
G (0.37 + steel), Gmin (0.17 + steel), Q, W_N, W_S, W_E, W_W (net uplift, cpi +0.2), W_D (downward, cpi -0.3)."""
import numpy as np, math
from model import *
from loads import *
from statics import simple_span, cantilever, continuous_beam
from model import SCHEME
from sections import sec, E as ES

TYPES = ['G', 'Gmin', 'Q', 'W_N', 'W_S', 'W_E', 'W_W', 'W_D']
COMBOS = {  # factors per load type
 'ULS1': dict(G=1.35, Q=1.5),
 'G':    dict(G=1.0),               # concurrent gravity moment for the seismic combination (psi_2 = 0 for roof imposed load)
 'ULS2': dict(G=1.35, W_D=1.5),
 'SLS':  dict(G=1.0, Q=1.0),
 'SLSW': dict(G=1.0, W_D=1.0),   # Rev 6: flat-roof pressure case (0.5 q_p > Q) for the L/200 check
 'ULS3N': dict(Gmin=1.0, W_N=1.5), 'ULS3S': dict(Gmin=1.0, W_S=1.5),
 'ULS3E': dict(Gmin=1.0, W_E=1.5), 'ULS3W': dict(Gmin=1.0, W_W=1.5),
}
def combine(vals, combo):
    return sum(f*vals.get(t, 0.0) for t, f in COMBOS[combo].items())

def build(sec_prim=SEC_PRIM, sec_raft=SEC_RAFT, sec_col=SEC_COL, dx=0.1):
    SP, SR, SC = sec(sec_prim), sec(sec_raft), sec(sec_col)
    X, Y, R, dx = roof_grid(dx)
    fields = dict(G=np.where(R, G_ROOF, 0.0), Gmin=np.where(R, G_MIN, 0.0), Q=np.where(R, Q_ROOF, 0.0),
                  W_D=down_field(X, Y, R))                 # Rev 3: flat-roof pressure case, zone I only
    for d, f in wind_fields(X, Y, R).items(): fields['W_'+d] = f
    # gutter and fascia on the north eave (Rev 2, review F6): line loads spread over the northmost cell row
    # gutter G-W at y 35.37 (x < 81.79) and G-E at y 35.87: the northmost roofed cell of each column of cells (Rev 3, C1)
    for i in range(X.shape[0]):
        js = np.where(R[i, :])[0]
        if len(js) == 0: continue
        jn = js.max()
        fields['G'][i, jn] += GUTTER_G/dx; fields['Gmin'][i, jn] += GUTTER_GMIN/dx
        for d in 'NSEW': fields['W_'+d][i, jn] += GUTTER_W/dx
    # --- purlin tributary: each cell to the adjacent N-S beams left/right (purlins = simple spans)
    ybins = {r['id']: np.arange(r['y0'], r['y1']+1e-9, dx) for r in RAFTERS}
    line = {r['id']: {t: np.zeros(len(ybins[r['id']])-1) for t in TYPES} for r in RAFTERS}
    nx, ny = X.shape
    for j in range(ny):
        y = Y[0, j]
        act = [r for r in RAFTERS if r['y0'] - 1e-9 <= y <= r['y1'] + 1e-9]
        xs = np.array([r['x'] for r in act]); ids = [r['id'] for r in act]
        for i in range(nx):
            if not R[i, j]: continue
            x = X[i, j]
            l = np.where(xs <= x)[0]; rr = np.where(xs > x)[0]
            if len(l) and len(rr):
                a, b = l[-1], rr[0]; fb = (x - xs[a])/(xs[b]-xs[a]); share = [(ids[a], 1-fb), (ids[b], fb)]
            elif len(l): share = [(ids[l[-1]], 1.0)]
            else: share = [(ids[rr[0]], 1.0)]
            for rid, fr in share:
                k = int((y - next(r for r in RAFTERS if r['id']==rid)['y0'])/dx)
                for t in TYPES: line[rid][t][k] += fields[t][i, j]*fr*dx   # kN/m per dx bin -> summed over x
    # results containers
    res = dict(spans=[], reactions={}, colloads={c: {t: 0.0 for t in TYPES} for c in COLS}, sections=dict(prim=SP, raft=SR, col=SC))
    ptloads = {}   # target id -> list of (pos, {type: P})
    def add_pt(target, pos, vals):
        ptloads.setdefault(target, []).append((pos, vals))
    def add_react(sid, vals, src):
        if sid.startswith('K'):
            for t in TYPES: res['colloads'][sid][t] += vals.get(t, 0.0)
        res['reactions'].setdefault(sid, []).append((src, vals))

    def analyse_beam(bid, S, coord0, coord1, sups, wline_fun, extra_pts, kind, axis):
        """Beam along an axis with supports; simple spans + end cantilevers (nested scheme), or one continuous beam over all
        supports incl. cantilevers (rafters in the 'ontop' scheme). wline_fun(t, s) -> kN/m of type t at s."""
        sw = S['w']
        sup = sorted(sups)
        reacts = {sid: {t: 0.0 for t in TYPES} for _, sid in sup}
        if SCHEME == 'ontop' and kind == 'raft' and len(sup) >= 2:
            Lb = coord1 - coord0; pos = [sc - coord0 for sc, _ in sup]; EI = ES*1e3*S['Iy']*1e-8
            per_type = {}
            for t in TYPES:
                f = (lambda s, t=t: wline_fun(t, coord0 + s) + (sw if t in ('G', 'Gmin') else 0))
                pts = [(p - coord0, v.get(t, 0)) for p, v in extra_pts]
                per_type[t] = continuous_beam(Lb, pos, f, pts, EI=EI, n=300)
                for (sc, sid) in sup: reacts[sid][t] += per_type[t]['R'][float(round(sc - coord0, 6))] if float(round(sc - coord0, 6)) in per_type[t]['R'] else per_type[t]['R'][min(per_type[t]['R'], key=lambda p: abs(p - (sc - coord0)))]
            sg = per_type['G']['s']
            for (a, sa), (b, sb) in zip(sup[:-1], sup[1:]):
                L = b - a; m = (sg >= a - coord0 - 1e-9) & (sg <= b - coord0 + 1e-9)
                span = dict(id=bid, section=S['name'], L=L, a=a, b=b, sa=sa, sb=sb, kind=kind, axis=axis, M={}, V={}, RA={}, RB={}, d={}, continuous=True)
                for c in COMBOS:
                    M = sum(COMBOS[c].get(t, 0)*per_type[t]['M'] for t in TYPES); V = sum(COMBOS[c].get(t, 0)*per_type[t]['V'] for t in TYPES)
                    span['M'][c] = (float(M[m].max()), float(M[m].min())); span['V'][c] = float(np.abs(V[m]).max())
                    span.setdefault('Marr', {})[c] = M[m]; span['s'] = sg[m] - (a - coord0)
                    span['RA'][c] = combine({t: reacts[sa][t] for t in TYPES}, c); span['RB'][c] = combine({t: reacts[sb][t] for t in TYPES}, c)
                    if c in ('SLS', 'SLSW'):
                        dsum = sum(COMBOS[c][t]*per_type[t]['d'] for t in COMBOS[c]); span['d'][c] = float(np.abs(dsum[m]).max())*1000
                span['w_G'] = float(np.mean([wline_fun('G', a + x) for x in np.linspace(0, L, 21)]) + sw)
                span['w_Q'] = float(np.mean([wline_fun('Q', a + x) for x in np.linspace(0, L, 21)]))
                span['w_Wmin'] = float(min(np.mean([wline_fun(t, a + x) for x in np.linspace(0, L, 21)]) for t in ('W_N','W_S','W_E','W_W')))
                res['spans'].append(span)
            for sid, vals in reacts.items(): add_react(sid, vals, bid)
            return reacts
        # cantilevers
        for end, (sc, sid), L in ((0, sup[0], sup[0][0]-coord0), (1, sup[-1], coord1-sup[-1][0])):
            if L > 0.02:
                for t in TYPES:
                    f = (lambda s, t=t, sc=sc, end=end: wline_fun(t, sc - s if end == 0 else sc + s) + (sw if t in ('G', 'Gmin') else 0))
                    pts = [(abs(p - sc), v.get(t, 0)) for p, v in extra_pts if (p < sc if end == 0 else p > sc)]
                    c = cantilever(L, f, pts)
                    reacts[sid][t] += c['R']
        for (a, sa), (b, sb) in zip(sup[:-1], sup[1:]):
            L = b - a
            span = dict(id=bid, section=S['name'], L=L, a=a, b=b, sa=sa, sb=sb, kind=kind, axis=axis, M={}, V={}, RA={}, RB={}, d={})
            per_type = {}
            for t in TYPES:
                f = (lambda s, t=t: wline_fun(t, a + s) + (sw if t in ('G', 'Gmin') else 0))
                pts = [(p - a, v.get(t, 0)) for p, v in extra_pts if a < p < b]
                per_type[t] = simple_span(L, f, pts, n=200, EI=ES*1e3*S['Iy']*1e-8)   # EI kNm2 (E kN/m2 x Iy m4)
                reacts[sa][t] += per_type[t]['RA']; reacts[sb][t] += per_type[t]['RB']
            for c in COMBOS:
                M = sum(COMBOS[c].get(t, 0)*per_type[t]['M'] for t in TYPES)
                V = sum(COMBOS[c].get(t, 0)*per_type[t]['V'] for t in TYPES)
                span['M'][c] = (float(M.max()), float(M.min())); span['V'][c] = float(np.abs(V).max())
                span.setdefault('Marr', {})[c] = M; span['s'] = per_type['G']['s']
                span['RA'][c] = combine({t: per_type[t]['RA'] for t in TYPES}, c); span['RB'][c] = combine({t: per_type[t]['RB'] for t in TYPES}, c)
                if c in ('SLS', 'SLSW'):
                    dsum = sum(COMBOS[c][t]*per_type[t]['d'] for t in COMBOS[c])
                    span['d'][c] = float(np.abs(dsum).max())*1000  # mm (d computed with EI passed above)
            span['w_G'] = float(np.mean([wline_fun('G', a + s) for s in np.linspace(0, L, 21)]) + sw)
            span['w_Q'] = float(np.mean([wline_fun('Q', a + s) for s in np.linspace(0, L, 21)]))
            span['w_Wmin'] = float(min(np.mean([wline_fun(t, a + s) for s in np.linspace(0, L, 21)]) for t in ('W_N','W_S','W_E','W_W')))
            res['spans'].append(span)
        for sid, vals in reacts.items(): add_react(sid, vals, bid)
        return reacts

    # 1) trimmers / eave beams with no roof load, loaded by upstand + self weight -> reactions onto rafters
    for p in PRIMARIES:
        if p['kind'] in ('trim',) or p['id'] == 'P_NOTCH':
            up = UPSTAND_ON.get(p['id'])
            wl = lambda t, s, up=up: (UPSTAND if (t in ('G', 'Gmin') and up and up[0] <= s <= up[1]) else 0.0)
            reacts = analyse_beam(p['id'], SR if p['kind'] == 'trim' else SP, p['x0'], p['x1'], [(x, i) for x, i in p['sup']], wl, [], p['kind'], 'x')
            for sid, vals in reacts.items():
                if sid.startswith('R'): add_pt(sid, p['y'], vals)
    # 2) rafters (N-S)
    for r in RAFTERS:
        yb = ybins[r['id']]; ln = line[r['id']]
        def wl(t, s, yb=yb, ln=ln, rid=r['id']):
            k = min(max(int((s - yb[0])/dx), 0), len(ln[t])-1)
            v = ln[t][k]
            if t in ('G', 'Gmin'):
                for (u0, u1) in UPSTAND_ON_R.get(rid, []):
                    if u0 <= s <= u1: v += UPSTAND
            return v
        reacts = analyse_beam(r['id'], SR, r['y0'], r['y1'], [(y, i) for y, i in r['sup']], wl, ptloads.get(r['id'], []), 'raft', 'y')
        for sid, vals in reacts.items():
            if sid.startswith('P_'): add_pt(sid, r['x'], vals)
    # 3) primaries (E-W)
    for p in PRIMARIES:
        if p['kind'] == 'trim' or p['id'] == 'P_NOTCH': continue
        up = UPSTAND_ON.get(p['id'])
        wl = lambda t, s, up=up: (UPSTAND if (t in ('G', 'Gmin') and up and up[0] <= s <= up[1]) else 0.0)
        from model import SPAN_SECTION
        analyse_beam(p['id'], sec(SPAN_SECTION[p['id']]) if p['id'] in SPAN_SECTION else SP, p['x0'], p['x1'], [(x, i) for x, i in p['sup']], wl, ptloads.get(p['id'], []), p['kind'], 'x')   # Rev 6a: P13 IPE 330
    # 4) columns: add wall weight and self weight (G and Gmin)
    ft = face_tribs()
    res['wall_trib'] = ft
    for cid in COLS:
        y = COLS[cid][1]
        # Rev 3 / brief Rev 5: no wall self-weight in G or G_min (G_WALL = 0); column self-weight only
        wall = sum(G_WALL*wall_h(y)*L for _, L, _ in ft.get(cid, []))
        res['colloads'][cid]['G'] += wall + SC['w']*L_col(y, cid)
        res['colloads'][cid]['Gmin'] += wall + SC['w']*L_col(y, cid)
    res['roof_area'] = float(R.sum()*dx*dx)
    res['line'] = line; res['ybins'] = ybins; res['fields'] = fields; res['grid'] = (X, Y, R, dx)
    return res

if __name__ == '__main__':
    res = build()
    print('roofed area %.1f m2' % res['roof_area'])
    tot = {t: sum(v[t] for v in res['colloads'].values()) for t in TYPES}
    print('sum of column loads', {t: round(v, 1) for t, v in tot.items()})
    for s in res['spans']:
        print('%-10s %-8s L=%5.2f  M_ULS1=%6.1f  Mmin_ULS3=%6.1f  V=%5.1f  d_SLS=%5.1f mm (L/%d)  wG=%.2f' % (
            s['id'], s['section'], s['L'], s['M']['ULS1'][0], min(s['M'][c][1] for c in ('ULS3N','ULS3S','ULS3E','ULS3W')),
            s['V']['ULS1'], s['d']['SLS'], s['L']*1000/max(s['d']['SLS'], 0.01), s['w_G']))
    for c in COLS:
        v = res['colloads'][c]
        print(c, 'G=%.1f Q=%.1f Wmin=%.1f' % (v['G'], v['Q'], min(v['W_N'], v['W_S'], v['W_E'], v['W_W'])))
