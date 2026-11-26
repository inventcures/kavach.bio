# kavach.bio

Source for [kavach.bio](https://kavach.bio/): a small effort to help prepare India for the next epidemic.

- `/white-paper/`: A Respiratory Protection Stockpile for India (working draft v0.1), web page + PDF
- `/fit-panel-protocol/`: Draft study protocol, India Respirator Fit Panel (v0.1), web page + PDF
- Planner: https://planner.kavach.bio (repo `india-stockpile-planner`)
- Mask drill: https://drill.kavach.bio (repo `kavach-mask-drill`)

Pages are static HTML generated from the markdown drafts with pandoc (`_src/build.sh`); PDFs are printed from the same pages with headless Chromium (`_src/render.js`). The white paper's master copy is a Google Doc; regenerate after edits there.
