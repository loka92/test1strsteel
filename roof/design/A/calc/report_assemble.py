"""Assembles design_report_A.md from report_text.md (narrative with {{TABLE:name}} markers) and report_tables.md."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..')
tables = {}
cur = None
for line in open(os.path.join(HERE, 'report_tables.md')).read().splitlines():
    if line.startswith('## '):
        cur = line[3:].strip(); tables[cur] = []
    elif cur is not None:
        tables[cur].append(line)
text = open(os.path.join(HERE, 'report_text.md')).read()


def sub(m):
    return '\n'.join(tables[m.group(1)]).strip()


out = re.sub(r'\{\{TABLE:([^}]+)\}\}', sub, text)
open(os.path.join(OUT, 'design_report_A.md'), 'w').write(out)
words = len(re.sub(r'\|.*\|', '', out).split())
print('design_report_A.md written, approx. %d words outside tables' % words)
