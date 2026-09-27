"""Minimal 2D beam-element stiffness solver (plane frame, 3 dof/node).

Units: kN, m, kNm.  Axes: x horizontal (along the frame), z vertical up.
Positive sign conventions for results (engineering):
  N > 0 tension, V = shear, M = bending moment (sagging positive for a
  horizontal beam loaded downwards -> M plotted on the tension side).
Also provides a linear buckling eigenvalue (alpha_cr) with the consistent
geometric stiffness matrix, and a step-wise internal force recovery.
"""
import numpy as np
from scipy.linalg import eigh

E_STEEL = 210e6  # kN/m2


class Frame2D:
    def __init__(self):
        self.nodes = {}      # name -> (x, z)
        self.members = []    # dict(name, i, j, EA, EI, w=[...loads])
        self.supports = {}   # node -> (ux, uz, rot) bools
        self.springs = {}    # node -> (kx, kz, krot)
        self.nloads = {}     # node -> [Fx, Fz, M]
        self.mloads = []     # (member index, wx, wz) uniform loads in global axes per m of member length

    # ---- model building -------------------------------------------------
    def add_node(self, name, x, z):
        self.nodes[name] = (float(x), float(z))

    def add_member(self, name, i, j, A, I, E=E_STEEL, tag=None):
        self.members.append(dict(name=name, i=i, j=j, EA=E * A, EI=E * I, A=A, I=I, tag=tag))
        return len(self.members) - 1

    def support(self, node, ux=True, uz=True, rot=False):
        self.supports[node] = (ux, uz, rot)

    def spring(self, node, kx=0.0, kz=0.0, krot=0.0):
        self.springs[node] = (kx, kz, krot)

    def node_load(self, node, Fx=0.0, Fz=0.0, M=0.0):
        f = self.nloads.setdefault(node, [0.0, 0.0, 0.0])
        f[0] += Fx; f[1] += Fz; f[2] += M

    def member_load(self, midx, wx=0.0, wz=0.0):
        """Uniform load per m of member length in GLOBAL directions."""
        self.mloads.append((midx, wx, wz))

    def clear_loads(self):
        self.nloads = {}
        self.mloads = []

    # ---- element matrices ------------------------------------------------
    def _geom(self, m):
        xi, zi = self.nodes[m['i']]; xj, zj = self.nodes[m['j']]
        L = np.hypot(xj - xi, zj - zi)
        c, s = (xj - xi) / L, (zj - zi) / L
        T = np.array([[c, s, 0, 0, 0, 0], [-s, c, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                      [0, 0, 0, c, s, 0], [0, 0, 0, -s, c, 0], [0, 0, 0, 0, 0, 1]])
        return L, c, s, T

    def _ke(self, m, L):
        EA, EI = m['EA'], m['EI']
        k = np.zeros((6, 6))
        k[0, 0] = k[3, 3] = EA / L; k[0, 3] = k[3, 0] = -EA / L
        a, b, cc = 12 * EI / L**3, 6 * EI / L**2, 4 * EI / L
        d = 2 * EI / L
        k[1, 1] = k[4, 4] = a; k[1, 4] = k[4, 1] = -a
        k[1, 2] = k[2, 1] = b; k[1, 5] = k[5, 1] = b
        k[2, 4] = k[4, 2] = -b; k[4, 5] = k[5, 4] = -b
        k[2, 2] = k[5, 5] = cc; k[2, 5] = k[5, 2] = d
        return k

    @staticmethod
    def _kg(N, L):
        """Consistent geometric stiffness, N = axial force (tension positive)."""
        kg = np.zeros((6, 6))
        kg[1, 1] = kg[4, 4] = 6 / 5; kg[1, 4] = kg[4, 1] = -6 / 5
        kg[1, 2] = kg[2, 1] = kg[1, 5] = kg[5, 1] = L / 10
        kg[2, 4] = kg[4, 2] = kg[4, 5] = kg[5, 4] = -L / 10
        kg[2, 2] = kg[5, 5] = 2 * L**2 / 15; kg[2, 5] = kg[5, 2] = -L**2 / 30
        return kg * N / L

    def _dofs(self):
        return {n: 3 * k for k, n in enumerate(self.nodes)}

    def _assemble(self):
        dof = self._dofs(); n = 3 * len(self.nodes)
        K = np.zeros((n, n)); F = np.zeros(n)
        fixed_end = []
        for m in self.members:
            L, c, s, T = self._geom(m)
            k = T.T @ self._ke(m, L) @ T
            idx = [dof[m['i']], dof[m['i']] + 1, dof[m['i']] + 2, dof[m['j']], dof[m['j']] + 1, dof[m['j']] + 2]
            K[np.ix_(idx, idx)] += k
            fixed_end.append(np.zeros(6))
        for (mi, wx, wz) in self.mloads:
            m = self.members[mi]; L, c, s, T = self._geom(m)
            # local components: axial q (along member) and transverse p (local y)
            q = wx * c + wz * s
            p = -wx * s + wz * c
            fe = np.array([q * L / 2, p * L / 2, p * L**2 / 12, q * L / 2, p * L / 2, -p * L**2 / 12])
            fixed_end[mi] += fe
            fg = T.T @ fe
            idx = [self._dofs()[m['i']] + k for k in range(3)] + [self._dofs()[m['j']] + k for k in range(3)]
            F[idx] += fg
        for n_, f in self.nloads.items():
            F[dof[n_]:dof[n_] + 3] += f
        for n_, (kx, kz, kr) in self.springs.items():
            K[dof[n_], dof[n_]] += kx; K[dof[n_] + 1, dof[n_] + 1] += kz; K[dof[n_] + 2, dof[n_] + 2] += kr
        return K, F, fixed_end, dof

    def _free(self, dof):
        n = 3 * len(self.nodes); fixed = np.zeros(n, bool)
        for n_, (ux, uz, r) in self.supports.items():
            fixed[dof[n_]] = ux; fixed[dof[n_] + 1] = uz; fixed[dof[n_] + 2] = r
        return ~fixed, fixed

    # ---- solve -----------------------------------------------------------
    def solve(self, nsteps=20):
        K, F, fe, dof = self._assemble()
        free, fixed = self._free(dof)
        U = np.zeros(len(F))
        U[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
        R = K @ U - F
        self.U = U; self.dof = dof
        self.reactions = {n_: R[dof[n_]:dof[n_] + 3].copy() for n_ in self.supports}
        for n_, (kx, kz, kr) in self.springs.items():   # spring reactions
            u = U[dof[n_]:dof[n_] + 3]
            self.reactions[n_] = self.reactions.get(n_, np.zeros(3)) + np.array([kx * u[0], kz * u[1], kr * u[2]])
        self.results = []
        for mi, m in enumerate(self.members):
            L, c, s, T = self._geom(m)
            idx = [dof[m['i']] + k for k in range(3)] + [dof[m['j']] + k for k in range(3)]
            ul = T @ U[idx]
            f = self._ke(m, L) @ ul - fe[mi]            # local end forces (Fx_i, Fy_i, M_i, Fx_j, Fy_j, M_j)
            wx = sum(l[1] for l in self.mloads if l[0] == mi); wz = sum(l[2] for l in self.mloads if l[0] == mi)
            q = wx * c + wz * s; p = -wx * s + wz * c
            xs = np.linspace(0, L, nsteps + 1)
            N = -f[0] - q * xs
            V = f[1] + p * xs
            M = -f[2] + f[1] * xs + p * xs**2 / 2
            # deflection transverse (local) via Hermite shape functions + load term
            xi = xs / L
            N1 = 1 - 3 * xi**2 + 2 * xi**3; N2 = L * (xi - 2 * xi**2 + xi**3)
            N3 = 3 * xi**2 - 2 * xi**3; N4 = L * (-xi**2 + xi**3)
            v = N1 * ul[1] + N2 * ul[2] + N3 * ul[4] + N4 * ul[5] + p * xs**2 * (L - xs)**2 / (24 * m['EI'])
            self.results.append(dict(name=m['name'], tag=m['tag'], L=L, x=xs, N=N, V=V, M=M, v=v,
                                     ux=(N1 * 0 + (1 - xi) * ul[0] + xi * ul[3])))
        return self

    def displacement(self, node):
        return self.U[self.dof[node]:self.dof[node] + 3]

    def alpha_cr(self):
        """Linear buckling eigenvalue for the current load state (call after solve)."""
        K, F, fe, dof = self._assemble()
        free, _ = self._free(dof)
        KG = np.zeros_like(K)
        for mi, m in enumerate(self.members):
            L, c, s, T = self._geom(m)
            Nmean = float(np.mean(self.results[mi]['N']))
            kg = T.T @ self._kg(Nmean, L) @ T
            idx = [dof[m['i']] + k for k in range(3)] + [dof[m['j']] + k for k in range(3)]
            KG[np.ix_(idx, idx)] += kg
        Kf = K[np.ix_(free, free)]; KGf = -KG[np.ix_(free, free)]  # compression (N<0) destabilises
        # KGf phi = mu * K phi ; alpha_cr = 1/mu_max  (K is positive definite, KGf may be indefinite)
        Kf = 0.5 * (Kf + Kf.T); KGf = 0.5 * (KGf + KGf.T)
        D = np.diag(1 / np.sqrt(np.diag(Kf)))          # Jacobi scaling for conditioning
        mu = eigh(D @ KGf @ D, D @ Kf @ D, eigvals_only=True)
        mu = mu[mu > 1e-9]
        return float(1.0 / mu.max()) if len(mu) else np.inf


if __name__ == '__main__':
    # sanity check: simply supported beam 10 m, w = 10 kN/m, EI from IPE300
    f = Frame2D(); f.add_node('a', 0, 0); f.add_node('b', 10, 0)
    mi = f.add_member('b1', 'a', 'b', 53.8e-4, 8356e-8)
    f.support('a', True, True, False); f.support('b', False, True, False)
    f.member_load(mi, 0, -10); f.solve(40)
    r = f.results[0]
    print('Mmax  %.2f (theory 125)' % r['M'].max(), 'V_end %.2f (50)' % r['V'][0],
          'delta %.4f m (theory %.4f)' % (-r['v'].min(), 5 * 10 * 10**4 / (384 * 210e6 * 8356e-8)))
    # Euler column check: pinned-pinned 4 m, HEA200 strong axis
    g = Frame2D(); g.add_node('a', 0, 0); g.add_node('m', 0, 2); g.add_node('b', 0, 4)
    g.add_member('c1', 'a', 'm', 53.8e-4, 3692e-8); g.add_member('c2', 'm', 'b', 53.8e-4, 3692e-8)
    g.support('a', True, True, False); g.support('b', True, False, False)
    g.node_load('b', Fz=-100); g.solve(4)
    print('alpha_cr %.2f  (Euler: %.2f)' % (g.alpha_cr(), np.pi**2 * 210e6 * 3692e-8 / 16 / 100))
