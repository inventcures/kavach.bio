import sys, importlib
sys.path.insert(0, '/home/claude/build')
src, modname, out = sys.argv[1:4]
F = importlib.import_module(modname).F
lines = open(src).read().split('\n')
for key, spec in F.items():
    anchor, html_ = spec[0], f'\n\nFIGSLOT{key}FIGSLOT\n\n'
    mode = spec[2] if len(spec) > 2 else 'after'
    idx = [i for i, l in enumerate(lines) if l.startswith(anchor)]
    assert len(idx) == 1, (key, anchor, idx)
    i = idx[0]
    if mode == 'before':
        lines.insert(i, html_)
    elif mode == 'after':
        lines.insert(i + 1, html_)
    elif mode == 'table-after':
        j = i
        while j < len(lines) and lines[j].strip(): j += 1
        lines.insert(j, html_)
    print('placed', key)
open(out, 'w').write('\n'.join(lines))
import json; json.dump({k: v[1] for k, v in F.items()}, open(out + '.figs.json', 'w'))
