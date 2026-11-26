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
# Parenthetical citations made only of links -> numbered margin references.
A = r'<a href="https?://[^"]+" rel="noopener">(?:(?!</a>).)+?</a>'
notes = []
def cite(m):
    inner = m.group(1)
    notes.append(inner)
    n = len(notes)
    return f'<sup id="fnref:{n}" role="doc-noteref"><a href="#fn:{n}" class="footnote" rel="footnote">{n}</a></sup>'
t = re.sub(r'\s?\((' + A + r'(?:\s*[;,]\s*' + A + r')*)\)', cite, t, flags=re.S)
items = ''.join(f'<li id="fn:{i}" role="doc-endnote"><p>{x} <a href="#fnref:{i}" class="reversefootnote" role="doc-backlink">&#8617;</a></p></li>' for i, x in enumerate(notes, 1))
t = t.replace('REFLIST', f'<div class="footnotes" role="doc-endnotes"><h2 class="refs-h">References</h2><ol>{items}</ol></div>' if notes else '')
print(p_name := p, 'refs:', len(notes))
import glob, os
for f in ['style.css'] + ['assets/' + os.path.basename(x) for x in glob.glob('/home/claude/site/assets/*')]:
    v = hashlib.md5(open('/home/claude/site/' + f, 'rb').read()).hexdigest()[:8]
    t = t.replace(f'"/{f}"', f'"/{f}?v={v}"')
open(p, 'w').write(t)
