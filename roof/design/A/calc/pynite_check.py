"""Independent cross-check of the in-house 2D solver (frame2d.py) with PyNiteFEA on frame F2, combination
1.35 G + 1.5 Q (no EHF). Same nodes, members, section properties and loads; compares the peak rafter moment,
the column-top moments and the base reactions.  Run: python3 pynite_check.py
"""
import numpy as np
from Pynite import FEModel3D
import frames_model as fm

f = fm.build_frame('F2')
for case, fac in (('G', 1.35), ('Q', 1.5)):
    fm.apply_case(f, case, fac)
f.solve(10)

m = FEModel3D()
m.add_material('S275', 210e6, 81e6, 0.3, 78.5)      # kN/m2, kN/m3
for n, (x, z) in f.nodes.items():
    m.add_node(n, x, z, 0.0)
for mem in f.members:
    m.add_section('S_' + mem['name'], mem['A'], mem['I'], mem['I'], 1e-6)
    m.add_member(mem['name'], mem['i'], mem['j'], 'S275', 'S_' + mem['name'])
for n in f.nodes:
    if n in f.supports:
        m.def_support(n, True, True, True, True, True, False)         # pinned in plane
    else:
        m.def_support(n, False, False, True, True, True, False)       # out-of-plane restrained
for (mi, wx, wz) in f.mloads:
    mem = f.members[mi]
    if wz: m.add_member_dist_load(mem['name'], 'FY', wz, wz, case='C')
    if wx: m.add_member_dist_load(mem['name'], 'FX', wx, wx, case='C')
for n, (Fx, Fz, M) in f.nloads.items():
    if Fx: m.add_node_load(n, 'FX', Fx, case='C')
    if Fz: m.add_node_load(n, 'FY', Fz, case='C')
m.add_load_combo('C', {'C': 1.0})
m.analyze(check_statics=False)

# peak rafter moment
own = max(np.abs(r['M']).max() for r, mem in zip(f.results, f.members) if mem['tag'][0] == 'raf')
pyn = max(max(abs(m.members[mem['name']].max_moment('Mz', 'C')), abs(m.members[mem['name']].min_moment('Mz', 'C')))
          for mem in f.members if mem['tag'][0] == 'raf')
print('F2 ULS-1 peak rafter |M|:  frame2d %.2f kNm   PyNite %.2f kNm   diff %.2f %%' % (own, pyn, 100 * (pyn - own) / own))
for k, y in f.meta['cols']:
    Ro = f.reactions['%s_0' % k]
    nd = m.nodes['%s_0' % k]
    print('  %s reactions  frame2d Rx %7.2f Rz %7.2f   PyNite Rx %7.2f Rz %7.2f' % (k, Ro[0], Ro[1], nd.RxnFX['C'], nd.RxnFY['C']))
    r_own = [r for r, mem in zip(f.results, f.members) if mem['tag'] == ('col', k, 3)][0]
    Mo = r_own['M'][-1]
    mp = m.members['%s_3' % k]
    Mp = max(abs(mp.max_moment('Mz', 'C')), abs(mp.min_moment('Mz', 'C')))
    print('     column-top |M|  frame2d %.2f  PyNite %.2f' % (abs(Mo), Mp))
# eaves sway under the same loads
n_top = 'r%d' % min(range(len(f.meta['ys'])), key=lambda i: abs(f.meta['ys'][i] - 35.27))
print('  K5 top horizontal displacement: frame2d %.2f mm  PyNite %.2f mm' % (f.displacement(n_top)[0] * 1e3, m.nodes[n_top].DX['C'] * 1e3))
