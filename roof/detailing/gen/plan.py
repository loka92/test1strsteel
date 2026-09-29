"""Shared plan drawing for S01 (1:1) and the enlarged partial plans on S01a (2x). Coordinates: true (x, y) -> sheet-local via L()."""
import math
from common import *
from geom import *
def clip_seg(x0, y0, x1, y1, R):
    """Clip a segment to rect R = (xa, ya, xb, yb); None if outside (Liang-Barsky)."""
    if R is None: return (x0, y0, x1, y1)
    xa, ya, xb, yb = R; dx, dy = x1-x0, y1-y0; t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0-xa), (dx, xb-x0), (-dy, y0-ya), (dy, yb-y0)):
        if p == 0:
            if q < 0: return None
        else:
            t = q/p
            if p < 0: t0 = max(t0, t)
            else: t1 = min(t1, t)
            if t0 > t1: return None
    return (x0+dx*t0, y0+dy*t0, x0+dx*t1, y0+dy*t1)
def inside(x, y, R): return R is None or (R[0] <= x <= R[2] and R[1] <= y <= R[3])
class Plan:
    """Draws the framing at scale s about origin (x0, y0) true -> local (lx0, ly0); region R clips."""
    def __init__(self, sh, x0, y0, lx0, ly0, s=1.0, R=None):
        self.sh, self.x0, self.y0, self.lx0, self.ly0, self.s, self.R = sh, x0, y0, lx0, ly0, s, R
    def L(self, x, y): return (self.lx0 + (x - self.x0)*self.s, self.ly0 + (y - self.y0)*self.s)
    def line(self, x0, y0, x1, y1, layer, owner=None, **kw):
        c = clip_seg(x0, y0, x1, y1, self.R)
        if c is None: return None
        return self.sh.line(*self.L(c[0], c[1]), *self.L(c[2], c[3]), layer, owner, **kw)
    def rect(self, x0, y0, x1, y1, layer, owner=None, **kw):
        if self.R and (x1 < self.R[0] or x0 > self.R[2] or y1 < self.R[1] or y0 > self.R[3]): return None
        xa, ya, xb, yb = (max(x0, self.R[0]), max(y0, self.R[1]), min(x1, self.R[2]), min(y1, self.R[3])) if self.R else (x0, y0, x1, y1)
        return self.sh.rect(*self.L(xa, ya), *self.L(xb, yb), layer, owner, **kw)
    def label(self, s, x, y, **kw):
        if not inside(x, y, self.R): return None
        return self.sh.label(s, *self.L(x, y), **kw)
    # ---- content
    def existing(self):
        o = 'exist'; sh = self.sh
        pts = [(67.89,15.57), (77.89,15.57), (77.89,19.97), (95.69,19.97), (95.69,35.87), (81.79,35.87), (81.79,35.37), (67.89,35.37)]
        for a, b in zip(pts, pts[1:] + pts[:1]): self.line(a[0], a[1], b[0], b[1], 'S-EXIST', owner=o)
        for k, c in COLS.items():
            x, y, bx, by = c['cx'], c['cy'], c['bx'], c['by']
            if not inside(x, y, self.R): continue
            r = self.rect(x-bx/2, y-by/2, x+bx/2, y+by/2, 'S-EXIST', owner=o)
            sh.hatch([self.L(x-bx/2, y-by/2), self.L(x+bx/2, y-by/2), self.L(x+bx/2, y+by/2), self.L(x-bx/2, y+by/2)], 'S-EXIST', 'ANSI31', 0.06*self.s, 8)
    def openings(self, label=True):
        sh = self.sh
        for name, op in OPEN.items():
            pts = [(op['x0'],op['y0']), (op['x1'],op['y0']), (op['x1'],op['y1']), (op['x0'],op['y1'])]
            if self.R and (op['x1'] < self.R[0] or op['x0'] > self.R[2] or op['y1'] < self.R[1] or op['y0'] > self.R[3]): continue
            self.rect(op['x0'], op['y0'], op['x1'], op['y1'], 'S-OPEN', owner='open' + name, lineweight=25)
            xa, ya, xb, yb = (max(op['x0'], self.R[0]), max(op['y0'], self.R[1]), min(op['x1'], self.R[2]), min(op['y1'], self.R[3])) if self.R else (op['x0'], op['y0'], op['x1'], op['y1'])
            sh.hatch([self.L(xa, ya), self.L(xb, ya), self.L(xb, yb), self.L(xa, yb)], 'S-OPEN', 'ANSI31', 0.3*self.s, 8, 45)
            if label:
                cx, cy = 0.5*(xa+xb), 0.5*(ya+yb)
                sh.text(*self.L(cx, cy+0.35), name + ' WELL', TH_MARK, 'S-TEXT-NOTE', 'CENTER', allowed=('open' + name,), owner='open' + name)
                sh.text(*self.L(cx, cy-0.15), 'NOT ROOFED', TH_DIM, 'S-TEXT-NOTE', 'CENTER', allowed=('open' + name,), owner='open' + name)
                if name == 'STAIR': sh.text(*self.L(cx, cy-0.55), 'open to the north face', TH_DIM, 'S-TEXT-NOTE', 'CENTER', allowed=('open' + name,), owner='open' + name)
    def purlins(self):
        for y, a, b in purlin_segments(): self.line(a, y, b, y, 'S-PURL', owner='purl')
        self.line(67.89, 35.32, 77.89, 35.32, 'S-PURL', owner='rail', lineweight=25); self.line(81.79, 35.82, 95.69, 35.82, 'S-PURL', owner='rail', lineweight=25)
        self.line(77.89, 35.37, 81.79, 35.37, 'S-PURL', owner='header', lineweight=50)
        self.line(81.79, 35.37, 81.79, 35.87, 'S-DETAIL', owner='return', lineweight=50)
    def members(self):
        for p in PRIMARIES:
            self.line(p['x0'], p['y'], p['x1'], p['y'], 'S-PRIM', owner=p['mark'], lineweight=50 if p['kind'] != 'trim' else 35)
        for s in POSTS: self.line(s['x0'], s['y'], s['x1'], s['y'], 'S-RAFT', owner=s['id'], lineweight=35)
        for r in RAFTERS: self.line(r['x'], r['y0'], r['x'], r['y1'], 'S-RAFT', owner=r['mark'], lineweight=35)
    def columns(self, base_plates=True):
        sh = self.sh; S = self.s
        for k, c in COLS.items():
            x, y = c['cx'], c['cy']
            if not inside(x, y, self.R): continue
            ew = c['bx'] > c['by']; b, h = 0.14, 0.133; o = 'C' + k[1:]
            if ew:
                self.line(x-b/2, y-h/2, x+b/2, y-h/2, 'S-COL', owner=o, lineweight=50); self.line(x-b/2, y+h/2, x+b/2, y+h/2, 'S-COL', owner=o, lineweight=50); self.line(x, y-h/2, x, y+h/2, 'S-COL', owner=o, lineweight=50)
            else:
                self.line(x-h/2, y-b/2, x-h/2, y+b/2, 'S-COL', owner=o, lineweight=50); self.line(x+h/2, y-b/2, x+h/2, y+b/2, 'S-COL', owner=o, lineweight=50); self.line(x-h/2, y, x+h/2, y, 'S-COL', owner=o, lineweight=50)
            if base_plates: self.rect(x-0.2, y-0.15, x+0.2, y+0.15, 'S-COL', owner=o) if ew else self.rect(x-0.15, y-0.2, x+0.15, y+0.2, 'S-COL', owner=o)
        if inside(WP1[0], WP1[1], self.R): self.rect(WP1[0]-0.07, WP1[1]-0.07, WP1[0]+0.07, WP1[1]+0.07, 'S-COL', owner='WP1', lineweight=50)
    def bracing(self):
        for tid, panels in ROOF_TRUSSES:
            for (x0, x1, y0, y1) in panels:
                self.line(x0, y0, x1, y1, 'S-BRACE', owner=tid); self.line(x0, y1, x1, y0, 'S-BRACE', owner=tid)
        for b, d, (a, c) in BAYS:
            (x1, y1), (x2, y2) = KXY[a], KXY[c]
            self.line(x1, y1, x2, y2, 'S-BRACE', owner=b, lineweight=70)
            xm, ym = 0.5*(x1+x2), 0.5*(y1+y2); w = 0.5 if self.s < 1.5 else 0.35
            if d == 'x': self.line(xm-w, ym-0.7*w, xm+w, ym+0.7*w, 'S-BRACE', owner=b, lineweight=50); self.line(xm-w, ym+0.7*w, xm+w, ym-0.7*w, 'S-BRACE', owner=b, lineweight=50)
            else: self.line(xm-0.7*w, ym-w, xm+0.7*w, ym+w, 'S-BRACE', owner=b, lineweight=50); self.line(xm-0.7*w, ym+w, xm+0.7*w, ym-w, 'S-BRACE', owner=b, lineweight=50)
    def gutters(self):
        for g in GUTTERS:
            y = g['y']; self.line(g['x0'], y+0.05, g['x1'], y+0.05, 'S-DRAIN', owner=g['id']); self.line(g['x0'], y+0.20, g['x1'], y+0.20, 'S-DRAIN', owner=g['id'])
            for xe in (g['x0'], g['x1']): self.line(xe, y+0.05, xe, y+0.20, 'S-DRAIN', owner=g['id'], lineweight=35)
            self.line(g['hp'], y+0.02, g['hp'], y+0.23, 'S-DRAIN', owner=g['id'])
        for dp, x in DOWNPIPES:
            y = north_edge(x); self.rect(x-0.08, y+0.045, x+0.08, y+0.205, 'S-DRAIN', owner=dp)
        self.line(79.84, 29.37, 79.84, 27.37, 'S-DRAIN', owner='cricket'); self.line(79.84, 27.37, 77.89, 29.37, 'S-DRAIN', owner='cricket'); self.line(79.84, 27.37, 81.79, 29.37, 'S-DRAIN', owner='cricket')
    def grids(self, ext=(1.5, 1.5), bubbles_at=('top', 'left')):
        sh = self.sh; R = self.R or (ENV['x0'], ENV['y0'], ENV['x1'], ENV['y1'])
        for g, x in XGRID:
            if not (R[0]-0.3 <= x <= R[2]+0.3): continue
            self.sh.line(*self.L(x, R[1]-ext[0]*0.6), *self.L(x, R[3]+ext[0]), 'S-GRID', owner='grid')
            sh.bubble(*self.L(x, R[3]+ext[0]+0.5/self.s*1.0), g, r=0.45)
        for g, y in YGRID:
            if not (R[1]-0.3 <= y <= R[3]+0.3): continue
            self.sh.line(*self.L(R[0]-ext[1], y), *self.L(R[2]+ext[1]*0.6, y), 'S-GRID', owner='grid')
            sh.bubble(*self.L(R[0]-ext[1]-0.5/self.s, y), g, r=0.45)
    # ---- marks
    def mark_members(self, with_sections=False, columns=True):
        for p in PRIMARIES:
            xm = 0.5*(p['x0']+p['x1']); s = p['mark'] + (' ' + prim_sec(p) if with_sections else '')
            self.label(s, xm, p['y'], cands=[(0, 0.12, 'CENTER'), (0, -0.37, 'CENTER'), (-0.8, 0.12, 'CENTER'), (0.8, 0.12, 'CENTER'), (-0.8, -0.37, 'CENTER'), (0.8, -0.37, 'CENTER'), (0, 0.6, 'CENTER'), (0, -0.85, 'CENTER'), (1.5, 0.6, 'CENTER'), (-1.5, 0.6, 'CENTER'), (1.5, -0.85, 'CENTER'), (-1.5, -0.85, 'CENTER')], allowed=(p['mark'],))
        for st in POSTS:
            self.label(st['id'] + (' IPE 240' if with_sections else ''), 0.5*(st['x0']+st['x1']), st['y'], cands=[(0, 0.12, 'CENTER'), (0, -0.37, 'CENTER'), (-1, 0.12, 'CENTER'), (1, 0.12, 'CENTER'), (0, 0.6, 'CENTER'), (0, -0.85, 'CENTER')], allowed=(st['id'],))
        for r in RAFTERS:
            ys = [r['y0'] + 0.6 + 0.9*i for i in range(6)] + [r['y1'] - 0.8]
            s = r['mark'] + (' IPE 240' if with_sections else '')
            for y in ys:
                if not inside(r['x'], y, self.R): continue
                e = self.label(s, r['x'], y, rot=90, cands=[(0.12, 0, 'LEFT'), (-0.12, 0, 'RIGHT'), (0.12, 0.5, 'LEFT'), (-0.12, 0.5, 'RIGHT'), (0.12, -0.5, 'LEFT'), (-0.12, -0.5, 'RIGHT')], allowed=(r['mark'],), leader=False)
                if e is not None and not self.sh.reg.hits(self.sh.tbox(e), self.sh.reg.allowed[e.dxf.handle], 0.03): break
        if columns:
            for k, c in COLS.items():
                self.label('C%s/%s' % (k[1:], k), c['cx'], c['cy'], allowed=('C' + k[1:],))
            self.label('WP1', WP1[0], WP1[1], allowed=('WP1',))
    def mark_bracing(self, sections=False):
        for b, d, (a, c) in BAYS:
            (x1, y1), (x2, y2) = KXY[a], KXY[c]; xm, ym = 0.5*(x1+x2), 0.5*(y1+y2); s = b + (' 2 L70x7 X' if sections else '')
            out = 1 if (d == 'x' and ym > 30) else -1
            if d == 'x': cands = [(0, out*0.55 if out > 0 else -0.8, 'CENTER'), (0, -out*0.55 if out > 0 else 0.55, 'CENTER'), (1.5, 0.55, 'CENTER'), (-1.5, 0.55, 'CENTER')]
            else:
                side = 1 if xm > 90 else -1
                cands = [(side*0.45, 0, 'LEFT' if side > 0 else 'RIGHT'), (-side*0.45, 0, 'RIGHT' if side > 0 else 'LEFT'), (side*0.45, 1.0, 'LEFT' if side > 0 else 'RIGHT'), (side*0.45, -1.0, 'LEFT' if side > 0 else 'RIGHT')]
            self.label(s, xm, ym, cands=cands, allowed=(b,))
        for tid, panels in ROOF_TRUSSES:
            (x0, x1, y0, y1) = panels[0]
            if len(panels) > 1: (x0, x1, y0, y1) = panels[1] if tid != 'RT-E' else panels[1]
            self.label(tid + (' M24 rods' if sections else ''), x0 + 0.3, y1 - 0.5, cands=[(0, 0, 'LEFT'), (0, -0.5, 'LEFT'), (0.8, -1.0, 'LEFT'), (0, -1.5, 'LEFT'), (1.2, 0, 'LEFT'), (0.3, -2.2, 'LEFT'), (2.0, -1.4, 'LEFT'), (0, -3.0, 'LEFT'), (2.5, -3.0, 'LEFT')], allowed=(tid,))
