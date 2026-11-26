from svgkit import *
F = {}
F['p-uk'] = ('This study fills that gap', figure('fig-uk',
 "In the UK, Asian women health workers passed FFP3 fit tests less often than White men",
 "FFP3 fit-test pass rate (%). UK data is the best available proxy: India has no published fit-test pass rates.",
 rangeplot([
  dict(label='Asian women', lo=60.3, hi=60.3, color='--s2', vlabel='60.3%'),
  dict(label='White men', lo=74.3, hi=74.3, color='--s1', vlabel='74.3%'),
 ], 50, 80, [50,60,70,80], 'Fit test pass rates', fmtf=lambda t: f'{t}%'),
 'Caggiari et al., 2023: 9,592 fit tests in 47 NHS trusts.',
 note='The axis starts at 50% to make the gap readable; it is not a zero baseline.'), 'before')

F['p-phases'] = ('## 5. Setting and sampling', figure('fig-phases',
 "The study runs in three phases over two years, with an optional third year for mask design",
 "Study phases, by month.",
 gantt([
  dict(label='0. Pilot (n = 150)', start=1, end=6),
  dict(label='1. Main survey\n(n ≈ 3,000)', start=6, end=20, color='--s1'),
  dict(label='2. Analysis and panel', start=15, end=24),
  dict(label='3. Co-design\n(optional)', start=24, end=36, hatched=True),
 ], 36, [0,6,12,18,24,30,36], 'Study phases'),
 'Section 4 design table.', note='Hatched = optional extension.'), 'before')

def funnel():
    b=[]; W=520; x0=10; full=500
    rows=[('Recruited (allowing 10% loss)',3300,'--muted','≈3,300'),
          ('Measured: callipers + phone 3D scan',3000,'--ink','≈3,000 (500 per zone)'),
          ('Quantitative fit test, 6–8 masks (40%)',1200,'--s1','1,200'),
          ('Reference 3D scan (20%)',600,'--s2','600')]
    for i,(l,v,c,vl) in enumerate(rows):
        y=10+i*58
        b.append(text(x0, y+14, l, 't','start',14))
        bw=v/3300*full
        b.append(f'<rect x="{x0}" y="{y+22}" width="{bw:.1f}" height="22" rx="3" fill="var({c})"><title>{E(l)}: {vl}</title></rect>')
        b.append(text(x0+bw+8 if bw<380 else x0+bw-8, y+38, vl, 't' if bw<380 else 'inv', 'start' if bw<380 else 'end', 14, 600))
    return svg(W, 10+58*4, ''.join(b), 'Participants at each stage')
F['p-flow'] = ('## 6. Sample size reasoning', figure('fig-flow',
 "Everyone is measured; a subset is fit-tested and a smaller subset gets a reference scan",
 "Planned number of participants at each step, all six zones combined.",
 funnel(), 'Sections 4, 5.3 and 6.', note='Each zone recruits 500: 250 women and 250 men, split across three age bands.'), 'before')

F['p-size'] = ('1. **Percentiles per zone (O1/O3).**', figure('fig-size',
 "A sample of about 3,000 matches what other countries used to build their national fit panels",
 "Participants measured in each national anthropometric survey.",
 hbar([
  dict(label='NIOSH (US, 2003)', value=3997, color='--ink'),
  dict(label='Malaysia', value=3324, color='--ink'),
  dict(label='China', value=3000, color='--ink'),
  dict(label='India (this study, planned)', value=3000, color='--s1', hatched=True, vlabel='≈3,000'),
 ], 4500, [0,1000,2000,3000,4000], 'Survey sample sizes', lab_w=200),
 'Section 6.', note='Hatched = planned, not yet collected.'), 'before')

F['p-gap'] = ('3. **3D scans for shape analysis (O4).**', figure('fig-gap',
 "We expect about 15% of Indian health workers to fall outside the US-based fit grid",
 "Share of people whose face size falls outside the NIOSH bivariate panel (%). Bars for India show the 95% confidence interval the planned sample would give.",
 rangeplot([
  dict(label='Malaysia (measured)', lo=10.8, hi=10.8, color='--ink', vlabel='10.8%'),
  dict(label='Taiwan (measured)', lo=30, hi=30, color='--ink', vlabel='≈30%'),
  dict(label='India, one zone × sex\n(assumed, n = 250)', lo=10.6, hi=19.4, color='--s1', hatched=True, vlabel='15% ± 4.4'),
  dict(label='India, national\n(assumed, n = 3,000)', lo=13.7, hi=16.3, color='--s1', hatched=True, vlabel='15% ± 1.3'),
 ], 0, 40, [0,10,20,30,40], 'Coverage gap', lab_w=200, fmtf=lambda t: f'{t}%'),
 'Section 6, item 2.', note='India values are a planning assumption (15%), not a result. Hatched = assumed.'), 'before')

def fitflow():
    b=[]; W=520
    steps=['Put on\nthe mask','User seal\ncheck','Quantitative\nfit test','Comfort and\nspeech rating']
    for i,s in enumerate(steps):
        x=10+i*128; y=20
        b.append(f'<rect x="{x}" y="{y}" width="112" height="56" rx="8" fill="var(--card)" stroke="var(--ink)" stroke-width="2"/>')
        ls=s.split('\n')
        for j,ln in enumerate(ls): b.append(text(x+56, y+33-(len(ls)-1)*8+j*16, ln,'t','middle',13))
        if i<3: b.append(f'<path d="M{x+113} {y+28} l13 0" stroke="var(--muted)" stroke-width="2" marker-end="url(#a5)"/>')
    b.append(text(10+64, 96, 'participant judges', 'm','middle',12)); b.append(text(10+64, 111, 'the seal: recorded', 'm','middle',12))
    x=266+56
    b.append(f'<path d="M{x} 77 L{x} 128" stroke="var(--muted)" stroke-width="2" marker-end="url(#a5)"/>')
    b.append(f'<rect x="{x-150}" y="130" width="140" height="48" rx="8" fill="var(--card)" stroke="var(--s1)" stroke-width="2"/>')
    b.append(text(x-80, 151, 'Pass', 't','middle',14,700)); b.append(text(x-80, 168, 'fit factor ≥ 100', 'm','middle',12))
    b.append(f'<rect x="{x+10}" y="130" width="180" height="48" rx="8" fill="var(--card)" stroke="var(--s2)" stroke-width="2"/>')
    b.append(text(x+100, 151, 'Fail', 't','middle',14,700)); b.append(text(x+100, 168, 'record leak: nose, cheek, chin', 'm','middle',12))
    b.append(text(260, 206, 'Repeated for each of 6–8 masks, in random order (about 45–60 minutes)', 'm','middle',13))
    defs='<defs><marker id="a5" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--muted)"/></marker></defs>'
    return svg(W, 216, defs+''.join(b), 'Fit test steps for each mask')
F['p-fit'] = ('### 7.4 Quality control', figure('fig-fitflow',
 "Each mask goes through the same four steps, so the seal check can be compared with the fit test",
 "What happens for each mask in the fit-test subsample (n = 1,200).",
 fitflow(), 'Section 7.3. TSI PortaCount 8048, OSHA modified ambient-aerosol CNC protocol (2019).'), 'before')

def grid():
    b=[]; W=520; H=330
    x0,x1,y0,y1=70,500,20,280
    # axis ranges: width 110-170 on x, length 90-150 on y
    sx=lambda v: x0+(v-110)/(170-110)*(x1-x0)
    sy=lambda v: y1-(v-90)/(150-90)*(y1-y0)
    for t in [120,140,160]:
        b.append(f'<line x1="{sx(t):.1f}" x2="{sx(t):.1f}" y1="{y0}" y2="{y1}" class="grid"/>'); b.append(text(sx(t), y1+18, f'{t}', 'm','middle',13))
    for t in [100,120,140]:
        b.append(f'<line x1="{x0}" x2="{x1}" y1="{sy(t):.1f}" y2="{sy(t):.1f}" class="grid"/>'); b.append(text(x0-8, sy(t)+4, f'{t}', 'm','end',13))
    b.append(text((x0+x1)/2, y1+40, 'Face width (mm)', 'm','middle',13))
    b.append(text(16, (y0+y1)/2, 'Face length (mm)', 'm','middle',13, extra=f'transform="rotate(-90 16 {(y0+y1)/2})"'))
    # NIOSH grid: width 120.5-158.5, length 98.5-138.5
    b.append(f'<rect x="{sx(120.5):.1f}" y="{sy(138.5):.1f}" width="{sx(158.5)-sx(120.5):.1f}" height="{sy(98.5)-sy(138.5):.1f}" fill="var(--s1)" fill-opacity=".1" stroke="var(--s1)" stroke-width="2.5"/>')
    b.append(text(sx(139.5), sy(138.5)-8, 'NIOSH bivariate panel (10 cells inside)', 't','middle',13,600))
    import random; random.seed(4)
    for _ in range(90):
        wv=random.gauss(136,8); lv=random.gauss(114,9)
        if not (112<wv<168 and 92<lv<148): continue
        inside = 120.5<=wv<=158.5 and 98.5<=lv<=138.5
        b.append(f'<circle cx="{sx(wv):.1f}" cy="{sy(lv):.1f}" r="3.5" fill="{"var(--ink)" if inside else "var(--s2)"}" opacity=".75"/>')
    
    return svg(W, H, ''.join(b), 'Schematic of the NIOSH bivariate grid')
F['p-grid'] = ('4. **Indian panels (O3).**', figure('fig-grid',
 "How the coverage gap is measured: plot every participant on the existing fit grid and count who falls outside",
 "Explanatory sketch. The box is the NIOSH/ISO bivariate panel (face width 120.5–158.5 mm, face length 98.5–138.5 mm). Grey dots inside the box are covered; orange dots outside it are the coverage gap. <strong>The dots are made up for illustration; they are not data.</strong>",
 grid(), 'Section 8.3 (panel limits).'), 'before')

items=[('Field staff',59,84),('Fit-test equipment',57,76),('Travel and logistics',25,40),('Project manager',24,36),('Participant compensation',15,30),
('Data / shape analyst',18,27),('Reference scanners',10,26),('Disposable respirators',7,23),('Site coordinators',17,17),('Elastomerics',5,15),
('Data engineer / security',9,14),('Ethics, insurance, legal',5,10),('Data infrastructure',5,10),('Headforms, co-design',5,10),('Manufacturer engagement',5,10),
('Fit-test accessories',5,8),('Phones',4,8),('Callipers',4,8),('Training and QC',5,8),('Software',2,5),('Dissemination, BIS',3,5)]
F['p-budget'] = ('**Cheaper variants:**', figure('fig-fpbudget',
 "People and fit-test equipment are the biggest costs",
 "Indicative budget for Phases 0–2 by item, ₹ lakh (1 lakh = 100,000), low to high estimate. Subtotal ₹289–470 lakh before 10–15% overhead.",
 rangeplot([dict(label=l, lo=lo, hi=hi, color='--s1', hatched=True, vlabel=f'{lo}–{hi}' if lo!=hi else f'{lo}') for l,lo,hi in items], 0, 90, [0,30,60,90], 'Budget items', lab_w=200, row_h=30, right_labels=True),
 'Section 12 budget table. Assumes ₹88 per US$ and about 30% added to US list prices for import duty, GST and shipping.',
 note='All estimates (hatched); no quotes yet.'), 'before')

F['p-variants'] = ('**Likely funders:**', figure('fig-variants',
 "A one-site pilot costs about a tenth of the full study",
 "Three ways to run it, ₹ lakh (100 lakh = 1 crore), low to high estimate.",
 rangeplot([
  dict(label='Pilot alone\n(1 site, n = 150)', lo=25, hi=40, color='--s1', hatched=True, vlabel='25–40'),
  dict(label='Lean main study\n(n = 1,800)', lo=200, hi=250, color='--s1', hatched=True, vlabel='200–250'),
  dict(label='Full study, Phases 0–2\n(n ≈ 3,000)', lo=320, hi=540, color='--s1', hatched=True, vlabel='320–540'),
 ], 0, 600, [0,200,400,600], 'Budget variants', lab_w=200),
 'Section 12.', note='All estimates (hatched).'), 'before')

F['p-timeline'] = ('## 12. Budget', figure('fig-fptime',
 "First results at month 12; panels, headforms and the BIS dossier by month 24",
 "Study timeline, by month.",
 gantt([
  dict(label='Agreements, ethics,\nequipment, hiring', start=1, end=3),
  dict(label='Training and pilot', start=3, end=6),
  dict(label='Community engagement\n(NE, Adivasi zones)', start=6, end=8),
  dict(label='Main fieldwork', start=7, end=20, color='--s1'),
  dict(label='Interim analysis', start=12, end=12, color='--s2'),
  dict(label='Panels, headforms,\nfit models', start=15, end=22),
  dict(label='BIS dossier, papers,\nopen data', start=20, end=24),
  dict(label='Optional Phase 3', start=24, end=36, hatched=True),
 ], 36, [0,6,12,18,24,30,36], 'Study timeline'),
 'Section 11 timeline table.', note='Diamond = interim analysis (first publishable result). Hatched = optional.'), 'before')

def outputs():
    b=[]; W=520
    b.append(f'<rect x="10" y="40" width="150" height="110" rx="8" fill="var(--card)" stroke="var(--ink)" stroke-width="2"/>')
    for j,l in enumerate(['~3,000 Indian','health workers','in 6 zones,','50% women']): b.append(text(85, 72+j*18, l, 't','middle',13))
    b.append(text(85, 30, 'Measure', 'm','middle',13,700))
    b.append(text(335, 30, 'Three things the study produces', 'm','middle',13,700))
    outs=[('An Indian fit panel','which faces masks must fit','--s1'),('Indian headforms','open 3D files for makers','--s1'),('Which masks fit','pass rates by model and size','--s2')]
    for i,(a,c,col) in enumerate(outs):
        y=40+i*42
        b.append(f'<path d="M162 95 C200 95 200 {y+16} 236 {y+16}" fill="none" stroke="var(--muted)" stroke-width="2" marker-end="url(#a7)"/>')
        b.append(f'<rect x="240" y="{y-2}" width="270" height="36" rx="6" fill="var(--card)" stroke="var({col})" stroke-width="2"/>')
        b.append(text(252, y+13, a, 't','start',13,700)); b.append(text(252, y+28, c, 'm','start',12))
    b.append(text(260, 182, 'Inputs for a national respirator stockpile and a BIS standard amendment', 'm','middle',12.5))
    defs='<defs><marker id="a7" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--muted)"/></marker></defs>'
    return svg(W, 192, defs+''.join(b), 'Study inputs and outputs')
F['p-out'] = ('## 3. Aims and objectives', figure('fig-out',
 "The study in one picture",
 "Measure Indian health workers' faces and test the masks India buys, to produce three things a stockpile needs.",
 outputs(), 'This protocol, sections 2 and 13.'), 'before')
