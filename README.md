# The Impact of Credit Ratings on CDS Spreads — Empirical Evidence from European Sovereign States

**A methodologically revised reconstruction of my 2019 master's thesis.**

This repository is a personal redo of the empirical study I wrote in 2019 as my master's thesis. The original was a competent first empirical study but had several methodological choices I would not make today: an equally-weighted market benchmark that contained the event country, naively-iid panel standard errors, no regime split for the European debt crisis, and a spillover specification that was contaminated by very tight-spread sovereigns in the post-2014 sub-period. This repo re-runs the analysis on the same data with corrected methods and re-renders the thesis from scratch.

The output document, [`output/thesis.pdf`](output/thesis.pdf), is the result. It is not graded by, submitted to, or otherwise endorsed by any university — it is a personal exercise in reproducing my own earlier work to the standard I would hold myself to today.

## What the thesis investigates

Three questions about how 5Y senior sovereign CDS spreads of 25 European sovereigns moved between January 2010 and December 2017 in response to rating actions by S&P and Moody's:

1. **Short-run reaction.** Do CDS spreads react to rating events in the two-day event window?
2. **Predictability.** Do past CDS spread changes carry information about future rating events?
3. **Spillovers.** Do rating events for one European sovereign move the CDS spreads of other European sovereigns?

The dataset is 263 rating events (147 S&P, 116 Moody's; 137 positive, 126 negative) and ~52k daily CDS observations. The 25-sovereign panel splits 15 EMU members against 10 non-EMU members.

## Headline findings

- **Negative events move CDS spreads more than positive events**, by roughly a factor of five in mean magnitude. Average two-day adjusted spread reaction to a negative event is +13.7 bps (median +2.1 bps), versus −2.6 bps (median −0.9 bps) for positive events.
- **The asymmetric reaction is concentrated in two sub-samples** that the original thesis did not separate:
  - **EMU sovereigns** react roughly three times more strongly to negative events than non-EMU sovereigns (+16.9 bps vs +5.6 bps).
  - **Pre-Draghi** (before 2012-07-26) the negative-event reaction is +17.6 bps; **post-Draghi** it falls to +6.3 bps and is no longer statistically distinguishable from zero. Most of the asymmetric reaction is a feature of the European debt crisis, not a structural feature of European CDS markets.
- **Once standard errors are two-way clustered by sovereign and trading day**, the pooled negative-event panel coefficient is no longer statistically significant (−9.1 bps, p = 0.21). Only the S&P negative-event coefficient retains marginal significance (p = 0.06). The original naive-iid version of this regression delivered comfortably significant pooled results.
- **CDS premiums do not predict negative rating events**; they predict positive events only marginally and only at the two-month horizon. The McFadden pseudo-R² of the best logistic specification is below 1%.
- **Spillover effects exist for negative rating events between EMU sovereigns of investment-grade quality**, and not otherwise. The "positive spillover from positive events" finding from the original thesis was an artifact of percentage-change scaling on very tight-spread sovereigns; once observations with prior-day spreads below 25 bps are dropped, the effect disappears.

## Methodology corrections relative to the 2019 version

| Original (2019) | This redo |
|---|---|
| Equally-weighted benchmark including the event country | Leave-one-out cross-sectional benchmark |
| iid standard errors in panel regressions | Two-way clustered (sovereign × trading day), Cameron-Gelbach-Miller (2011) |
| Per-row stale-quote drop | Block-stale flag (≥5 consecutive identical quotes) |
| No filter for events confounded by simultaneous events | Confounded-event flag dropped from event-window regressions |
| No regime split | Pre-/post-Draghi (2012-07-26) sub-sample comparison |
| No multiple-testing adjustment | Benjamini-Hochberg adjustment in appendix tests |
| Spillover regression on percentage changes incl. low-spread obs | Spillover regression drops obs with prior-day spread < 25 bps |
| In-sample logit pseudo-R² only | Same, but properly non-overlapping sovereign-month grid |

## Repository layout

```
analysis/        Python pipeline (pandas, statsmodels, scipy, matplotlib)
  data_prep.py    Build cleaned CDS panel + event panel
  analysis.py     Statistical tests, panel regressions, spillover, logit
  figures.py      Generate publication-quality figures
  build_tables.py Render Typst tables from results.json
data/
  raw/            Source data: CDS quotes, S&P + Moody's ratings, mappings
  processed/      Cleaned outputs (parquet) + results.json
thesis/
  thesis.typ      Typesetting source for the thesis PDF
output/
  thesis.pdf      Compiled thesis (~36 pages)
  figures/        All figures as 300 dpi PNG + PDF
  tables/         Auto-generated Typst tables
SOURCES.md        Reference list with DOIs and what was taken from each
```

## How to reproduce

The full pipeline is reproducible from the raw data:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python analysis/data_prep.py
.venv/bin/python analysis/analysis.py
.venv/bin/python analysis/figures.py
.venv/bin/python analysis/build_tables.py
.venv/bin/python -c "import typst; typst.compile('thesis/thesis.typ', output='output/thesis.pdf', root='.')"
```

Pinned versions and dependencies are listed in [`requirements.txt`](requirements.txt). The pipeline runs end-to-end in approximately three minutes on a 2020-vintage MacBook.

## Data sources

Daily 5Y senior sovereign CDS spreads are taken from Thomson Reuters Datastream. Sovereign credit ratings are from S&P's Sovereign Rating and Country Transfer and Convertibility Assessment Histories and Moody's academic data access. The full reference list with DOIs is in [`SOURCES.md`](SOURCES.md).

## License

The code in `analysis/` is released under the MIT license. Data and rating histories belong to their respective providers; this repository contains snapshots of public-domain or academically-licensed data only. The text of the thesis is © the author, 2019 / revised 2026.
