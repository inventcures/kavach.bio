set -e
S=/home/claude/site; mkdir -p $S/white-paper $S/fit-panel-protocol
cp style.css favicon.svg $S/
WP=/mnt/project-files/bioprevail-research/india-respirator-stockpile-white-paper-v0.1.md
FP=/mnt/project-files/bioprevail-research/indian-fit-panel/02-draft-study-protocol.md
sed '1{/^<!--/d}' $WP | sed '0,/^# /{/^# /d}' > wp.md
python3 insert.py wp.md figs_wp wp.md
sed 's/\[`01-research-report.md`\](01-research-report.md)/`01-research-report.md` (not yet published)/' $FP | sed '0,/^# /{/^# /d}' > fp.md
python3 insert.py fp.md figs_fp fp.md
F="markdown-tex_math_dollars-implicit_figures"
pandoc wp.md -f $F -s --template template.html --toc --toc-depth=2 \
  -M pagetitle="A Respiratory Protection Stockpile for India" \
  -V description="Working draft v0.1: why India needs a respirator reserve, what other countries learned, and a pilot design for Kerala." \
  -V pdf="india-respirator-stockpile-white-paper-v0.1.pdf" \
  -V doctitle="A Respiratory Protection Stockpile for India" -o $S/white-paper/index.html
pandoc fp.md -f $F -s --template template.html --toc --toc-depth=2 \
  -M pagetitle="Draft study protocol: India Respirator Fit Panel" \
  -V description="Draft v0.1 study protocol for head-and-face anthropometry and respirator fit among Indian health workers." \
  -V pdf="india-respirator-fit-panel-protocol-v0.1.pdf" \
  -V doctitle="Draft study protocol: India Respirator Fit Panel (IRFP)" -o $S/fit-panel-protocol/index.html
for pair in "white-paper wp.md" "fit-panel-protocol fp.md"; do set -- $pair; f=$S/$1/index.html
  python3 postproc.py $f $2 style.css
done
echo built
V=$(md5sum style.css | cut -c1-8); sed -i -E "s#href=\"/style.css(\?v=[a-f0-9]+)?\"#href=\"/style.css?v=$V\"#" $S/index.html
