set -e
S=/home/claude/site; mkdir -p $S/white-paper $S/fit-panel-protocol
cp style.css favicon.svg $S/
WP=/mnt/project-files/bioprevail-research/india-respirator-stockpile-white-paper-v0.1.md
FP=/mnt/project-files/bioprevail-research/indian-fit-panel/02-draft-study-protocol.md
sed '1{/^<!--/d}' $WP | sed '0,/^# /{/^# /d}' > wp.md
sed 's/\[`01-research-report.md`\](01-research-report.md)/`01-research-report.md` (not yet published)/' $FP | sed '0,/^# /{/^# /d}' > fp.md
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
for f in $S/white-paper/index.html $S/fit-panel-protocol/index.html; do
  python3 -c "import sys,re;p=sys.argv[1];t=open(p).read();t=re.sub(r'(<table.*?</table>)',r'<div class=\"table-wrap\">\1</div>',t,flags=re.S);t=re.sub(r'<a href=\"(https?://[^\"]+)\"',r'<a href=\"\1\" rel=\"noopener\"',t);open(p,'w').write(t)" $f
done
echo built
