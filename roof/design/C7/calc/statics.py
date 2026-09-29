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
