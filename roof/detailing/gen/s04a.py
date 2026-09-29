"""S04a connection details D9-D11 and the connection notes (continuation of S04)."""
from common import *
from s04 import d9, d10, d11, dnotes, prep
OX, OY = 410.0, 8.0
def draw(msp):
    sh = Sheet(msp, OX, OY, 'S04a', 'CONNECTION DETAILS D9 - D11, NOTES', 'Details drawn 4x or 5x in model space (scale in each frame); DIMENSION text = true mm (dimlfac 250 / 200)')
    for i, f in enumerate([d9, d10, d11, dnotes]): prep(f); f(sh, 0.3 + i*10.35, 16.4)
    sh.note_block(0.5, 15.2, 'DETAIL INDEX', ['D1 fin plates FP1 / FP2 (S04) - D2 cap plate - D3 chord tie - D4 bracing gusset - D5 roof rod gusset, RG-C combined gusset, R2 / R10 web clip - D6 well upstand (T2, R5 / R6, P8) - D7 eave and gutter - D8 purlin cleat and fly brace (S04); D9 girt cleat and wall panel - D10 wind post WP1 head and base - D11 wall sill / base rail (this sheet). Base details type E / P / WP1: S05.'], 0.16, 41.0)
    return sh
