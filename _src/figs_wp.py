from svgkit import *
F = {}
EST = 'Hatched = our estimate (inferred), not a reported figure.'

# W1 output vs need
F['w-output'] = ('Domestic N95 capacity went from', figure('fig-output',
 "Even at its 2020 peak, India's N95 output was about a third of what health workers alone would use each day",
 "N95 respirators per day, in lakh (1 lakh = 100,000). Daily use assumes one N95 per worker per day.",
 hbar([
  dict(label='Output, mid-May 2020', value=2.5, color='--ink', vlabel='2.5 lakh'),
  dict(label='Capacity, Dec 2020', value=32, color='--ink', vlabel='32 lakh'),
  dict(label='Use: 1 crore\nhealth workers', value=100, color='--s2', hatched=True, vlabel='≈100 lakh'),
  dict(label='Use: 3 crore health\n+ frontline workers', value=300, color='--s2', hatched=True, vlabel='≈300 lakh'),
 ], 340, [0,100,200,300], 'Bar chart of N95 output versus daily need'),
 'PIB, Ministry of Textiles, Dec 2020 (output and capacity); BOOM, Dec 2020 (worker counts).',
 note=EST, legend=[('Reported output','--ink',False),('Estimated daily use (inferred)','--s2',True)]))

# W2 fit failure UK
F['w-fit'] = ('**Fit depends on who is wearing the mask.**', figure('fig-fit',
 "In UK hospitals, minority-ethnic staff failed FFP3 fit tests more often, and the mask model mattered even more",
 "Share of FFP3 fit tests failed, early in COVID-19 (%).",
 rangeplot([
  dict(label='Black, Asian and\nminority ethnic staff', lo=25.7, hi=25.7, color='--s2', vlabel='25.7%'),
  dict(label='Other staff', lo=16.8, hi=16.8, color='--s1', vlabel='16.8%'),
  dict(label='Range across\nmask models', lo=2, hi=67, color='--ink', vlabel='2% to 67%'),
 ], 0, 100, [0,25,50,75,100], 'Fit test failure rates', fmtf=lambda t: f'{t}%'),
 'Green et al., Journal of Hospital Infection, 2021.'))

# W3 static vs rotating diagram (before ## 7)
def cycle_diagram():
    b = []
    W=520
    b.append(text(10, 24, 'Bought once, left to expire', 't', 'start', 16, 700))
    steps = ['Bulk purchase','Held in a warehouse','Expires (~5 years)','No budget to replace','Crisis: shelves empty']
    y=40
    for i,s in enumerate(steps):
        x = 10 + i*102
        col = '--s2' if i>=2 else '--ink'
        b.append(f'<rect x="{x}" y="{y}" width="92" height="54" rx="8" fill="var(--card)" stroke="var({col})" stroke-width="2"/>')
        words = s.split(' ')
        lines=[]; cur=''
        for wd in words:
            if len(cur+' '+wd)>12 and cur: lines.append(cur); cur=wd
            else: cur=(cur+' '+wd).strip()
        lines.append(cur)
        for j,ln in enumerate(lines):
            b.append(text(x+46, y+27-(len(lines)-1)*8+j*16, ln, 't', 'middle', 13))
        if i<4: b.append(f'<path d="M{x+93} {y+27} l8 0" stroke="var(--muted)" stroke-width="2" marker-end="url(#arr)"/>')
    ex = ['California: all 21 million remaining N95s expired by 2020',
          'UK: of 3.8 million masks, only ~34% expected usable by April 2020',
          'Canada: ~2 million expired N95s sent to landfill in 2019']
    for j,e in enumerate(ex): b.append(text(14, 120+j*20, '• '+e, 'm', 'start', 13))
    y2=200
    b.append(f'<line x1="10" x2="{W-10}" y1="{y2-12}" y2="{y2-12}" class="grid"/>')
    b.append(text(10, y2+14, 'Rotated through routine use', 't', 'start', 16, 700))
    cx, cy, R = 260, y2+150, 92
    import math
    labels = ['Buy a fixed share\nof the target each year','Hold in monitored\nstorage','Hospitals use the\noldest stock first','Replace what\nwas used']
    pos = [(cx, cy-R),(cx+R+70, cy),(cx, cy+R),(cx-R-70, cy)]
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="var(--s1)" stroke-width="2.5" stroke-dasharray="10 6"/>')
    for a in [45,135,225,315]:
        ang=math.radians(a); px=cx+R*math.cos(ang); py=cy+R*math.sin(ang)
        # small arrowhead tangent (clockwise)
        tx, ty = -math.sin(ang), math.cos(ang)
        b.append(f'<path d="M{px-6*tx-5*math.cos(ang):.1f} {py-6*ty-5*math.sin(ang):.1f} L{px+6*tx:.1f} {py+6*ty:.1f} L{px-6*tx+5*math.cos(ang):.1f} {py-6*ty+5*math.sin(ang):.1f}" fill="none" stroke="var(--s1)" stroke-width="2.5"/>')
    for (x,y),l in zip(pos,labels):
        b.append(f'<rect x="{x-80}" y="{y-24}" width="160" height="48" rx="8" fill="var(--card)" stroke="var(--s1)" stroke-width="2"/>')
        ls=l.split('\n')
        for j,ln in enumerate(ls): b.append(text(x, y+5-(len(ls)-1)*8+j*16, ln, 't','middle',13))
    b.append(text(cx, cy-4, 'Stock never', 'm','middle',13)); b.append(text(cx, cy+13, 'sits long enough', 'm','middle',13)); b.append(text(cx, cy+30, 'to expire', 'm','middle',13))
    b.append(text(14, y2+300, '• CDC team proposal: buy 20% of the target every year for a 5-year shelf life', 'm','start',13))
    b.append(text(14, y2+320, '• UK now calls this "dynamic stockpiling" (DHSC, 2026)', 'm','start',13))
    defs='<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--muted)"/></marker></defs>'
    return svg(W, y2+332, defs+''.join(b), 'Diagram comparing a static stockpile with a rotating one')
F['w-cycle'] = ('## 7. A proposed design for India', figure('fig-cycle',
 "Stockpiles fail through replenishment, not purchase",
 "Every high-income country we looked at bought stock and then let it expire. A rotating reserve keeps stock moving through hospitals so it is used before it expires.",
 cycle_diagram(),
 'Reveal/LA Times 2020; COVID Inquiry Module 5, 2026; Auditor General of Canada 2021; Health Security 2017; DHSC 2026. See section 4.'), 'before')

# W4 procurement
F['w-sa'] = ("WHO's guidance supports reusable elastomeric", figure('fig-procure',
 "Emergency buying is where the biggest losses happened",
 "South Africa's investigators examined R14.3 billion of COVID-19 contracts (rand, billions). Brazil's 2020 mask order from China (millions of masks).",
 hbar([
  dict(label='SA: contracts examined', value=14.3, color='--ink', vlabel='R14.3 bn'),
  dict(label='SA: found irregular', value=7.87, color='--s2', vlabel='R7.87 bn'),
  dict(label='SA: recovered', value=0.0343, color='--s1', vlabel='R0.03 bn (R34.3 m)'),
 ], 16, [0,5,10,15], 'South Africa COVID contract irregularities') +
 hbar([
  dict(label='Brazil: masks ordered', value=200, color='--ink', vlabel='200 m'),
  dict(label='Brazil: expected to arrive', value=10, color='--s2', vlabel='10 m'),
 ], 220, [0,100,200], 'Brazil mask order'),
 'Special Investigating Unit report, Dec 2021; Jornal do Brasil, Apr 2020.'), 'before')

# W5 square rule
def square():
    b=[]; W=520
    rows=[('Respirators (protection factor 30)', '1 in 30 out', '1 in 30 in', '1 in 900', '--s1'),
          ('Basic masks (protection factor 2)', '1 in 2 out', '1 in 2 in', '1 in 4', '--s2')]
    for i,(lab,o,n,res,c) in enumerate(rows):
        y=30+i*140
        b.append(text(10, y, lab, 't','start',15,700))
        # person A
        for k,(x,t1,t2) in enumerate([(10,'Infected','person'),(330,'Healthy','person')]):
            b.append(f'<circle cx="{x+40}" cy="{y+45}" r="16" fill="none" stroke="var(--ink)" stroke-width="2"/>')
            b.append(f'<path d="M{x+16} {y+95} q24 -38 48 0" fill="none" stroke="var(--ink)" stroke-width="2"/>')
            b.append(text(x+40, y+112 if False else y+110, f'{t1} {t2}', 'm','middle',12))
            mx = x+58 if k==0 else x+22
            b.append(f'<rect x="{mx-5}" y="{y+36}" width="10" height="20" rx="3" fill="var({c})"/>')
        b.append(f'<path d="M95 {y+46} L320 {y+46}" stroke="var(--muted)" stroke-width="2" stroke-dasharray="3 4" marker-end="url(#arr2)"/>')
        b.append(text(150, y+36, o, 't','middle',13))
        b.append(text(270, y+36, n, 't','middle',13))
        b.append(text(210, y+68, '×', 'm','middle',16))
        b.append(f'<rect x="420" y="{y+24}" width="94" height="44" rx="8" fill="var({c})" opacity=".15"/>')
        b.append(text(467, y+44, res, 't','middle',16,700))
        b.append(text(467, y+61, 'gets through', 'm','middle',12))
    defs='<defs><marker id="arr2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--muted)"/></marker></defs>'
    return svg(W, 300, defs+''.join(b), 'Diagram of the square rule for two-way respirator protection')
F['w-square'] = ('A worked example of that square rule', figure('fig-square',
 "When both people wear a respirator, the protection multiplies",
 "A respirator filters air going out and coming in, so the two protection factors multiply. That is why respirators on essential workers can cut transmission so sharply.",
 square(), 'Arnscheidt and Binder, Oct 2026 (the square rule and the 900-fold example).'))

# W6 tiers
F['w-tiers'] = ('The 2 to 13 crore (20 to 130 million) range', figure('fig-tiers',
 "Health and frontline workers come to about 3 crore people",
 "People in each proposed tier, in crore (1 crore = 10 million). Tier sizes are from India's COVID-19 vaccine priority list.",
 hbar([
  dict(label='Tier 1: health workers', value=1, color='--s1', vlabel='≈1 crore'),
  dict(label='Tier 2: frontline workers', value=2, color='--s1', vlabel='≈2 crore'),
  dict(label='Tier 3: other essential\nservices', value=None, vlabel='not yet estimated'),
 ], 2.4, [0,1,2], 'Workers per tier') +
 '<p class="fig-sub" style="margin-top:.8rem">Some of the groups inside Tier 1, in lakh (1 lakh = 100,000):</p>' +
 hbar([
  dict(label='Nursing personnel', value=42.9, color='--ink', vlabel='42.9 lakh'),
  dict(label='Registered doctors', value=13.9, color='--ink', vlabel='13.9 lakh'),
  dict(label='ASHAs', value=10.3, color='--ink', vlabel='over 10.3 lakh'),
 ], 50, [0,25,50], 'Selected groups within Tier 1'),
 'BOOM, Dec 2020 (tiers); Medical Dialogues, Mar 2026 and PIB, Jan 2025 (groups).',
 note='The tiers are our proposal (inferred). The three groups shown overlap with Tier 1 but do not add up to it.'), 'before')

# W7 protection
F['w-protect'] = ('Blueprint Biosecurity recommends government stockpiles', figure('fig-protect',
 "Reusable elastomeric respirators give more protection than disposable N95s",
 "Protection factor: how many times fewer particles reach the wearer. Higher is better.",
 '<p class="fig-panel">In real use, groups of wearers</p>' +
 rangeplot([
  dict(label='Disposable N95', lo=15, hi=40, color='--s2', vlabel='about 15–40'),
  dict(label='Elastomeric (EHMR)', lo=30, hi=70, ext=100, color='--s1', vlabel='about 30–70, possibly 100+'),
 ], 0, 110, [0,25,50,75,100], 'Group protection factor ranges') +
 '<p class="fig-panel">The worst-protected 1 in 20 wearers, without fit testing</p>' +
 rangeplot([
  dict(label='Disposable N95', lo=3.3, hi=3.3, color='--s2', vlabel='3.3'),
  dict(label='Elastomeric (EHMR)', lo=7.3, hi=7.3, color='--s1', vlabel='7.3'),
 ], 0, 110, [0,25,50,75,100], 'Fifth percentile protection factor'),
 'Arnscheidt and Binder, 2026 (group protection); Coffey et al., 2007 (5th percentile). Dashed line: "possibly over 100 with P100 filters".',
 note='Same scale in both panels. Elastomerics also take about 200 times less storage space than an equivalent N95 stock (Council on Strategic Risks, 2026).'), 'before')

# W8 cost
F['w-cost'] = ('**Our recommended mix (inferred).**', figure('fig-cost',
 "On these estimates, an elastomeric-led reserve costs less up front and less each year",
 "Cost of covering Tier 1 (about 1 crore health workers) for a 150-day emergency, ₹ crore. <strong>All figures are our estimates from assumed prices and still need Indian quotes.</strong>",
 '<p class="fig-panel">Up-front cost (₹ crore)</p>' +
 rangeplot([
  dict(label='All disposable N95\n(150 crore masks)', lo=3750, hi=6000, color='--s2', hatched=True, vlabel='₹3,750–6,000'),
  dict(label='Elastomeric-led\n(1 crore EHMRs + filters)', lo=2600, hi=4200, color='--s1', hatched=True, vlabel='₹2,600–4,200'),
 ], 0, 6500, [0,2000,4000,6000], 'Up-front cost ranges', lab_w=200) +
 '<p class="fig-panel">Recurring cost (₹ crore per year)</p>' +
 rangeplot([
  dict(label='All disposable N95\n(replaced every 5 years)', lo=750, hi=1200, color='--s2', hatched=True, vlabel='₹750–1,200'),
  dict(label='Elastomeric-led\n(10-year facepiece life)', lo=300, hi=500, color='--s1', hatched=True, vlabel='₹300–500 + filters'),
 ], 0, 1400, [0,400,800,1200], 'Recurring cost ranges', lab_w=200),
 'Section 7.2 cost table. Assumes ₹88 per US$, one N95 per worker per day, N95 ₹25–40, EHMR ₹1,800–2,600, two filter sets per worker at ₹400–800.',
 note=EST + ' The all-disposable option also equals about 470 days of India\'s 2020 peak N95 output.'), 'before')

# W9 surge flow
def surge():
    b=[]; W=520
    def box(x,y,w,h,lines,col='--ink',bold=False,fill='var(--card)'):
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="var({col})" stroke-width="2"/>')
        for j,ln in enumerate(lines):
            b.append(text(x+w/2, y+h/2+5-(len(lines)-1)*8+j*16, ln, 't','middle',13, 700 if (bold and j==0) else None))
    def arrow(x1,y1,x2,y2): b.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="var(--muted)" stroke-width="2" marker-end="url(#arr3)"/>')
    box(110,10,300,58,['Peacetime','Small standing order from each','pre-qualified maker; feeds rotation'],bold=True)
    arrow(260,68,260,92)
    box(10,94,240,58,['Domestic trigger','Notified disaster','under the DM Act'],'--s2',True)
    box(270,94,240,58,['International trigger','WHO emergency','declaration'],'--s2',True)
    b.append(text(260,170,'whichever comes first','m','middle',13))
    arrow(130,152,240,186); arrow(390,152,280,186)
    box(60,188,400,58,['On trigger','Makers scale to a pre-agreed volume within set days;','government buys up to a ceiling at a pre-agreed price'],'--s1',True)
    arrow(260,246,260,270)
    box(60,272,400,44,['Emergency ends early?','Unused output goes into the rotating reserve, not to waste'],bold=True)
    defs='<defs><marker id="arr3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--muted)"/></marker></defs>'
    return svg(W, 326, defs+''.join(b), 'Flowchart of the proposed surge commitment')
F['w-surge'] = ('A full term sheet for this commitment', figure('fig-surge',
 "A surge commitment: makers keep lines warm, and a declaration switches them to full output",
 "Proposed model for India (inferred, for discussion). We found no existing PPE contract anywhere with a trigger written to a declaration.",
 surge(), 'Section 7.5. Blueprint Biosecurity, Jun 2024 (guaranteed purchase of surge output).'), 'before')

# W10 Nipah timeline
def nipah():
    b=[]; W=520; x0,x1=30,490; years=list(range(2018,2026)); out={2018,2019,2021,2023,2024,2025}
    sx=lambda y: x0+(y-2018)/7*(x1-x0)
    b.append(f'<line x1="{x0}" x2="{x1}" y1="60" y2="60" class="grid"/>')
    for y in years:
        if y in out:
            b.append(f'<circle cx="{sx(y):.1f}" cy="60" r="11" fill="var(--s2)"><title>Nipah outbreak in Kerala, {y}</title></circle>')
        else:
            b.append(f'<circle cx="{sx(y):.1f}" cy="60" r="8" fill="var(--bg)" stroke="var(--muted)" stroke-width="2"><title>No outbreak listed, {y}</title></circle>')
        b.append(text(sx(y), 92, str(y), 'm','middle',13))
    b.append(text(sx(2018), 30, '23 cases, 91% died', 't','start',13))
    b.append(text(sx(2023), 30, 'spread in hospital', 't','middle',13))
    return svg(W, 104, ''.join(b), 'Timeline of Nipah outbreaks in Kerala 2018 to 2025')
F['w-nipah'] = ('Nipah outbreaks need thousands of respirators', figure('fig-nipah',
 "Kerala has had a Nipah outbreak in six of the last eight years",
 "Years with a Nipah outbreak in Kerala, 2018–2025 (filled circles).",
 nipah(), 'WHO Disease Outbreak News DON577, Aug 2025.'), 'before')

# W11 pilot budget
items=[('EHMRs (5,000)',1.25,'--s1'),('Rotating N95 buffer (2 lakh)',0.60,'--s1'),('Staff and evaluation',0.60,'--ink'),('Filter sets (10,000)',0.50,'--s1'),
       ('Contingency (10%)',0.38,'--ink'),('Fit-test instruments (2)',0.30,'--ink'),('Cleaning, training, SOPs',0.30,'--ink'),('Storage, access, stock app',0.20,'--ink')]
F['w-budget'] = ('| 5,000 EHMRs at about ₹2,500', figure('fig-budget',
 "More than half of the ≈₹4.1 crore Kerala pilot budget is respirators and filters",
 "Indicative 12-month pilot budget for about 5,000 health workers, ₹ crore. <strong>Estimates; all prices still to be quoted.</strong>",
 hbar([dict(label=l, value=v, color=c, hatched=True, vlabel=f'₹{v:.2f}') for l,v,c in items], 1.4, [0,0.5,1.0], 'Pilot budget by item', lab_w=210),
 'Section 8 indicative budget table.', note=EST + ' The N95 buffer is largely recovered through routine hospital use.',
 legend=[('Respirators and filters','--s1',True),('Everything else','--ink',True)]), 'table-after')

F['w-timeline'] = ('| 0 to 2 | Agreement with the state health', figure('fig-pilot-time',
 "The pilot runs for 12 months, through one monsoon season",
 "Proposed Kerala pilot timeline, by month (inferred).",
 gantt([
  dict(label='Agreements, ethics,\nsupplier quotes', start=0, end=2),
  dict(label='Fit testing, model\nchoice, procurement', start=2, end=4),
  dict(label='Issue, train, set up\ncleaning and storage', start=4, end=6),
  dict(label='Use through monsoon;\nmid-point review', start=6, end=10, color='--s2'),
  dict(label='District drill;\nfinal evaluation', start=10, end=12),
 ], 12, [0,2,4,6,8,10,12], 'Pilot timeline'),
 'Section 8 timeline table.'), 'table-after')

def plan():
    b=[]; W=520
    cols=[('Who','--ink',['~1 crore','health workers,','then ~2 crore','frontline workers']),
          ('What','--s1',['Reusable','elastomerics','at the core, plus','an N95 buffer']),
          ('Kept fresh','--s1',['Rotated through','hospital use;','one owner,','own budget']),
          ('In a crisis','--s2',['Indian makers','surge on a','DM Act or WHO','declaration'])]
    for i,(h,c,ls) in enumerate(cols):
        x=10+i*127
        b.append(f'<rect x="{x}" y="10" width="117" height="128" rx="8" fill="var(--card)" stroke="var({c})" stroke-width="2"/>')
        b.append(f'<rect x="{x}" y="10" width="117" height="28" rx="8" fill="var({c})"/><rect x="{x}" y="30" width="117" height="8" fill="var({c})"/>')
        b.append(text(x+58.5, 29, h, 'inv','middle',12.5,700))
        for j,l in enumerate(ls): b.append(text(x+58.5, 60+j*18, l, 't','middle',12))
    b.append(f'<rect x="10" y="152" width="498" height="58" rx="8" fill="var(--s1)" fill-opacity=".1" stroke="var(--s1)" stroke-width="2" stroke-dasharray="6 4"/>')
    b.append(text(259, 175, 'Start small: a 12-month Kerala pilot', 't','middle',14,700))
    b.append(text(259, 195, '~5,000 health workers, ~₹4 crore (inferred), tests all four ideas', 'm','middle',12.5))
    return svg(W, 220, ''.join(b), 'The proposal in one picture')
F['w-plan'] = ('For scale (inferred):', figure('fig-plan',
 "The proposal in one picture",
 "Our recommendations, summarised. Each part is explained, with its evidence, in sections 7 and 8.",
 plan(), 'This paper, sections 1, 7 and 8.'), 'before')
