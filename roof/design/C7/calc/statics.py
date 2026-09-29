"""Simple-span beam statics by numerical integration (reviewer-checkable)."""
import numpy as np

def simple_span(L, w_fun=None, points=(), n=400, EI=None):
    """Simply supported span of length L. w_fun(s) distributed load kN/m (positive downward),
    points = [(a, P)] point loads. Returns dict with reactions RA, RB, Mmax (sagging +), Mmin, Vmax, and
    deflection dmax (m, positive downward) if EI (kNm2) given."""
    s = np.linspace(0, L, n+1)
    w = np.array([w_fun(si) for si in s]) if w_fun else np.zeros_like(s)
    ds = L/n
    Wtot = np.trapezoid(w, s); xw = np.trapezoid(w*s, s)/Wtot if abs(Wtot) > 1e-9 else 0
    RB = (Wtot*xw + sum(P*a for a, P in points))/L
    RA = Wtot + sum(P for a, P in points) - RB
    # shear V(s) = RA - int w - sum P(a<s)
    cumw = np.concatenate([[0], np.cumsum(0.5*(w[1:]+w[:-1])*ds)])
    V = RA - cumw - np.array([sum(P for a, P in points if a < si) for si in s])
    M = np.concatenate([[0], np.cumsum(0.5*(V[1:]+V[:-1])*ds)])
    out = dict(RA=RA, RB=RB, Mmax=M.max(), Mmin=M.min(), Vmax=np.abs(V).max(), s=s, M=M, V=V)
    if EI:
        th = np.concatenate([[0], np.cumsum(0.5*(M[1:]+M[:-1])*ds)])/EI
        d = np.concatenate([[0], np.cumsum(0.5*(th[1:]+th[:-1])*ds)])
        d = d - s/L*d[-1]                 # enforce d(L)=0
        out['dmax'] = float(np.abs(d).max()); out['d'] = d
    return out

def cantilever(L, w_fun=None, points=(), n=100, EI=None):
    s = np.linspace(0, L, n+1)     # s = 0 at the support
    w = np.array([w_fun(si) for si in s]) if w_fun else np.zeros_like(s)
    Wt = np.trapezoid(w, s) + sum(P for a, P in points)
    M = np.trapezoid(w*s, s) + sum(P*a for a, P in points)
    out = dict(R=Wt, M=M, V=Wt)
    if EI:
        out['dmax'] = abs(np.trapezoid(w*s**2*(3*L-s), s)/(6*EI)) + sum(abs(P)*a**2*(3*L-a)/(6*EI) for a, P in points)
    return out


def continuous_beam(L, supports, w_fun=None, points=(), EI=1.0, n=400):
    """Continuous beam of length L on pinned supports at `supports` (positions from the left end, cantilevers beyond the
    end supports allowed). w_fun(s) kN/m positive downward, points [(a, P)] downward. Euler-Bernoulli stiffness method
    with 2 DOF per node. Returns s, M (sagging +), V, d (m, downward +), R {support position: reaction kN}."""
    grid = set(np.linspace(0, L, n + 1).round(6)) | {round(p, 6) for p in supports} | {round(a, 6) for a, P in points}
    s = np.array(sorted(grid)); N = len(s); ndof = 2*N
    K = np.zeros((ndof, ndof)); F = np.zeros(ndof)
    w = np.array([w_fun(si) for si in s]) if w_fun else np.zeros_like(s)
    for e in range(N - 1):
        le = s[e + 1] - s[e]
        if le <= 0: continue
        k = EI/le**3*np.array([[12, 6*le, -12, 6*le], [6*le, 4*le**2, -6*le, 2*le**2], [-12, -6*le, 12, -6*le], [6*le, 2*le**2, -6*le, 4*le**2]])
        idx = [2*e, 2*e + 1, 2*e + 2, 2*e + 3]
        K[np.ix_(idx, idx)] += k
        we = 0.5*(w[e] + w[e + 1])              # downward load -> nodal loads in the -v sense (v positive up in the element formulation)
        F[idx] += np.array([-we*le/2, -we*le**2/12, -we*le/2, we*le**2/12])
    for a, P in points:
        i = int(np.argmin(np.abs(s - a))); F[2*i] -= P
    fixed = [2*int(np.argmin(np.abs(s - p))) for p in supports]
    free = [i for i in range(ndof) if i not in fixed]
    u = np.zeros(ndof)
    u[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    Rv = K @ u - F                              # reactions at the fixed DOFs (upward positive)
    R = {float(p): float(Rv[2*int(np.argmin(np.abs(s - p)))]) for p in supports}
    d = -u[0::2]                                # downward positive
    # shear and moment from equilibrium (same convention as simple_span)
    cumw = np.concatenate([[0], np.cumsum(0.5*(w[1:] + w[:-1])*np.diff(s))])
    V = np.array([sum(r for p, r in R.items() if p <= si + 1e-9) for si in s]) - cumw - np.array([sum(P for a, P in points if a <= si + 1e-9) for si in s])
    M = np.concatenate([[0], np.cumsum(0.5*(V[1:] + V[:-1])*np.diff(s))])
    return dict(s=s, M=M, V=V, d=d, R=R, Mmax=M.max(), Mmin=M.min(), dmax=float(np.abs(d).max()))
