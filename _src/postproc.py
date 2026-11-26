import sys, re, json, hashlib
p, md, cssfile = sys.argv[1:4]
t = open(p).read()
figs = json.load(open(md + '.figs.json'))
COLLAPSE = {'w-budget', 'w-timeline', 'p-phases', 'p-timeline', 'p-budget'}
t = re.sub(r'(<table.*?</table>)', r'<div class="table-wrap">\1</div>', t, flags=re.S)
def put(key, table=None):
    h = figs[key]
    if table:
        h = h.replace('</figure>', f'<details class="fig-table"><summary>Show the numbers as a table</summary>{table}</details>\n</figure>')
    return h
for key in [k for k in COLLAPSE if k in figs]:
    t, n = re.subn(r'(<div class="table-wrap">(?:(?!</div>).)*?</div>)\s*<p>FIGSLOT' + re.escape(key) + r'FIGSLOT</p>',
                   lambda m: put(key, m.group(1)), t, flags=re.S)
    assert n == 1, key
t = re.sub(r'<p>FIGSLOT(.+?)FIGSLOT</p>', lambda m: put(m.group(1)), t)
t = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" rel="noopener"', t)
v = hashlib.md5(open(cssfile, 'rb').read()).hexdigest()[:8]
t = t.replace('href="/style.css"', f'href="/style.css?v={v}"')
open(p, 'w').write(t)
