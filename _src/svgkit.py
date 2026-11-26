# Small SVG chart kit. Colours come from CSS custom properties defined in style.css,
# so the same SVG works in light mode, dark mode and print.
import html, itertools
_uid = itertools.count(1)
E = html.escape
FONT = 'font-family="system-ui,-apple-system,Segoe UI,Roboto,sans-serif"'

def fmt(v):
    if isinstance(v, str): return v
    if abs(v - round(v)) < 1e-9: return f"{int(round(v)):,}"
    return f"{v:,.2f}".rstrip('0').rstrip('.')

def hatch_def(pid, color):
    return (f'<pattern id="{pid}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="7" height="7" fill="{color}" opacity=".22"/><line x1="0" y1="0" x2="0" y2="7" stroke="{color}" stroke-width="3"/></pattern>')

def svg(w, h, body, label):
    return (f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{E(label)}" {FONT} '
            f'xmlns="http://www.w3.org/2000/svg">{body}</svg>')

def text(x, y, s, cls='t', anchor='start', size=15, weight=None, extra=''):
    w = f' font-weight="{weight}"' if weight else ''
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}" font-size="{size}"{w} {extra}>{E(s)}</text>'

def ticks_x(x0, x1, vmax, ticks, y_top, y_bot, fmtf=fmt, vmin=0):
    out = []
    for t in ticks:
        x = x0 + (t - vmin) / (vmax - vmin) * (x1 - x0)
        out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y_top}" y2="{y_bot}" class="grid"/>')
        out.append(text(x, y_bot + 18, fmtf(t), 'm', 'middle', 13))
    return ''.join(out)

def hbar(rows, vmax, ticks, label, unit_note=None, lab_w=190, w=520, row_h=46, bar_h=22, fmtf=fmt, value_suffix=''):
    """rows: dict(label, value, color var, hatched bool, vlabel optional, sub optional)"""
    pid = f'h{next(_uid)}'
    x0, x1 = lab_w, w - 70
    top = 10
    h = top + row_h * len(rows) + 34
    defs, body = [], []
    colors = {r['color'] for r in rows if r.get('hatched')}
    pmap = {}
    for i, c in enumerate(sorted(colors)):
        pmap[c] = f'{pid}{i}'; defs.append(hatch_def(pmap[c], f'var({c})'))
    body.append(ticks_x(x0, x1, vmax, ticks, top, top + row_h * len(rows), fmtf))
    for i, r in enumerate(rows):
        y = top + i * row_h + (row_h - bar_h) / 2
        bw = max(2, r['value'] / vmax * (x1 - x0)) if r['value'] is not None else 0
        lines = r['label'].split('\n')
        ly = y + bar_h / 2 + 5 - (len(lines) - 1) * 8
        for j, ln in enumerate(lines):
            body.append(text(x0 - 10, ly + j * 16, ln, 't', 'end', 14))
        if r['value'] is None:
            body.append(f'<rect x="{x0}" y="{y}" width="{(x1-x0)*0.35:.1f}" height="{bar_h}" rx="3" fill="none" stroke="var(--muted)" stroke-dasharray="4 3"/>')
            body.append(text(x0 + (x1 - x0) * 0.35 + 8, y + bar_h / 2 + 5, r.get('vlabel', 'not yet estimated'), 'm', 'start', 13))
            continue
        fill = f'url(#{pmap[r["color"]]})' if r.get('hatched') else f'var({r["color"]})'
        stroke = f' stroke="var({r["color"]})" stroke-width="1.5"' if r.get('hatched') else ''
        body.append(f'<rect x="{x0}" y="{y}" width="{bw:.1f}" height="{bar_h}" rx="3" fill="{fill}"{stroke}><title>{E(r["label"].replace(chr(10)," "))}: {E(r.get("vlabel", fmt(r["value"])+value_suffix))}</title></rect>')
        body.append(text(x0 + bw + 7, y + bar_h / 2 + 5, r.get('vlabel', fmt(r['value']) + value_suffix), 't', 'start', 14, 600))
    return svg(w, h, f'<defs>{"".join(defs)}</defs>' + ''.join(body), label)

def rangeplot(rows, vmin, vmax, ticks, label, lab_w=180, w=520, row_h=50, fmtf=fmt, right_labels=False):
    """rows: label, lo, hi, color, hatched, vlabel, ext (dashed extension to value)"""
    pid = f'r{next(_uid)}'
    x0, x1 = lab_w, w - 30
    top = 10
    h = top + row_h * len(rows) + 34
    sx = lambda v: x0 + (v - vmin) / (vmax - vmin) * (x1 - x0)
    body = [ticks_x(x0, x1, vmax, ticks, top, top + row_h * len(rows), fmtf, vmin)]
    defs = []
    for i, r in enumerate(rows):
        yc = top + i * row_h + row_h / 2 + (0 if right_labels else 4)
        lines = r['label'].split('\n')
        for j, ln in enumerate(lines):
            body.append(text(x0 - 10, yc + 5 - (len(lines) - 1) * 8 + j * 16, ln, 't', 'end', 14))
        c = f'var({r["color"]})'
        if r.get('ext'):
            body.append(f'<line x1="{sx(r["hi"]):.1f}" x2="{sx(r["ext"]):.1f}" y1="{yc}" y2="{yc}" stroke="{c}" stroke-width="3" stroke-dasharray="4 4"/>')
        if r['lo'] == r['hi']:
            body.append(f'<circle cx="{sx(r["lo"]):.1f}" cy="{yc}" r="7" fill="{c}" stroke="var(--bg)" stroke-width="2"><title>{E(r["label"])}: {E(r.get("vlabel",""))}</title></circle>')
            if right_labels: body.append(text(sx(r['lo']) + 11, yc + 5, r.get('vlabel', fmt(r['lo'])), 't', 'start', 13, 600))
            else: body.append(text(sx(r['lo']), yc - 13, r.get('vlabel', fmt(r['lo'])), 't', 'middle', 13, 600))
        else:
            fill = c
            if r.get('hatched'):
                p = f'{pid}{i}'; defs.append(hatch_def(p, c)); fill = f'url(#{p})'
            body.append(f'<rect x="{sx(r["lo"]):.1f}" y="{yc-9}" width="{sx(r["hi"])-sx(r["lo"]):.1f}" height="18" rx="9" fill="{fill}" stroke="{c}" stroke-width="1.5"><title>{E(r["label"].replace(chr(10)," "))}: {E(r.get("vlabel",""))}</title></rect>')
            vl = r.get('vlabel', f'{fmt(r["lo"])}–{fmt(r["hi"])}')
            if right_labels: body.append(text(sx(r['hi']) + 7, yc + 5, vl, 't', 'start', 13, 600))
            else: body.append(text((sx(r['lo']) + sx(r['hi'])) / 2, yc - 15, vl, 't', 'middle', 13, 600))
    return svg(w, h, f'<defs>{"".join(defs)}</defs>' + ''.join(body), label)

def gantt(rows, vmax, ticks, label, lab_w=170, w=520, row_h=40, axis_label='Month'):
    pid = f'g{next(_uid)}'
    x0, x1 = lab_w, w - 20
    top = 10
    h = top + row_h * len(rows) + 50
    sx = lambda v: x0 + v / vmax * (x1 - x0)
    body = [ticks_x(x0, x1, vmax, ticks, top, top + row_h * len(rows))]
    body.append(text((x0 + x1) / 2, top + row_h * len(rows) + 40, axis_label, 'm', 'middle', 13))
    defs = []
    for i, r in enumerate(rows):
        y = top + i * row_h + 9
        lines = r['label'].split('\n')
        for j, ln in enumerate(lines):
            body.append(text(x0 - 10, y + 16 - (len(lines) - 1) * 8 + j * 16, ln, 't', 'end', 14))
        c = f'var({r.get("color","--s1")})'
        fill = c
        if r.get('hatched'):
            p = f'{pid}{i}'; defs.append(hatch_def(p, c)); fill = f'url(#{p})'
        if r['start'] == r['end']:
            body.append(f'<path d="M{sx(r["start"]):.1f} {y+2} l9 9 l-9 9 l-9 -9z" fill="{c}"><title>{E(r["label"])}: month {r["start"]}</title></path>')
        else:
            body.append(f'<rect x="{sx(r["start"]):.1f}" y="{y}" width="{sx(r["end"])-sx(r["start"]):.1f}" height="22" rx="4" fill="{fill}" stroke="{c}" stroke-width="1.5"><title>{E(r["label"].replace(chr(10)," "))}: months {r["start"]}–{r["end"]}</title></rect>')
    return svg(w, h, f'<defs>{"".join(defs)}</defs>' + ''.join(body), label)

def figure(fid, title, sub, svg_html, source, note=None, legend=None):
    leg = ''
    if legend:
        leg = '<div class="fig-legend">' + ''.join(
            f'<span><i class="sw{" hatch" if h else ""}" style="--c:var({c})"></i>{E(t)}</span>' for t, c, h in legend) + '</div>'
    n = f'<p class="fig-note">{note}</p>' if note else ''
    return (f'\n\n<figure class="fig" id="{fid}">\n<p class="fig-title">{E(title)}</p>\n<p class="fig-sub">{sub}</p>\n{leg}'
            f'<div class="fig-body">{svg_html}</div>\n<figcaption>{n}<p class="fig-src">Source: {source}</p></figcaption>\n</figure>\n\n')
