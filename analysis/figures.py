"""Generate the figures used in the thesis.

All figures are saved into output/figures as 300 dpi PNGs and as PDF for the
typesetter. Style is consistent across figures: serif body font, muted color
palette, finding-stating titles where the figure itself answers a question."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
FIG = ROOT / "output" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# Color palette: muted academic. Approximate Okabe-Ito for color-blind safety.
PAL = {
    "blue": "#3554a5",
    "orange": "#d97706",
    "red": "#b91c1c",
    "green": "#15803d",
    "grey": "#6b7280",
    "lightgrey": "#cbd5e1",
    "ink": "#0f172a",
}


def style():
    plt.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif", "Liberation Serif", "serif"],
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#e5e7eb",
        "grid.linestyle": "-",
        "grid.linewidth": 0.6,
        "axes.axisbelow": True,
        "legend.frameon": False,
        "lines.linewidth": 1.6,
    })


def save(fig, name: str):
    fig.savefig(FIG / f"{name}.png", facecolor="white")
    fig.savefig(FIG / f"{name}.pdf", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 1 / 2 / 3: schematic CDS cashflow, physical settlement, cash settlement
# (vector schematics rendered programmatically for the theory chapter)
# ---------------------------------------------------------------------------

def fig_cashflow_diagrams():
    style()
    for tag, title, settlement_caption in [
        ("cashflow_premaurity", "CDS cashflows before maturity / default",
         "Buyer pays a fixed premium; protection seller assumes the credit risk."),
        ("settlement_physical", "Physical settlement upon credit event",
         "Defaulted bond is delivered to the seller against payment of the par amount."),
        ("settlement_cash", "Cash settlement upon credit event",
         "Seller pays par minus the auction-determined recovery to the buyer."),
    ]:
        fig, ax = plt.subplots(figsize=(7.0, 3.0))
        ax.set_axis_off()
        ax.set_xlim(0, 10); ax.set_ylim(0, 6)
        # Two boxes
        ax.add_patch(plt.Rectangle((0.4, 2.0), 2.6, 2.0, facecolor="#eef2ff", edgecolor=PAL["ink"], linewidth=1.2))
        ax.text(1.7, 3.0, "Protection\nbuyer", ha="center", va="center", fontsize=11, weight="bold")
        ax.add_patch(plt.Rectangle((7.0, 2.0), 2.6, 2.0, facecolor="#fef3c7", edgecolor=PAL["ink"], linewidth=1.2))
        ax.text(8.3, 3.0, "Protection\nseller", ha="center", va="center", fontsize=11, weight="bold")
        if tag == "cashflow_premaurity":
            ax.annotate("", xy=(7.0, 3.5), xytext=(3.0, 3.5),
                        arrowprops=dict(arrowstyle="->", color=PAL["blue"], lw=1.6))
            ax.text(5.0, 3.8, "Periodic premium (bps p.a.)", ha="center", color=PAL["blue"], fontsize=10)
            ax.annotate("", xy=(3.0, 2.5), xytext=(7.0, 2.5),
                        arrowprops=dict(arrowstyle="->", color=PAL["grey"], lw=1.0, linestyle="--"))
            ax.text(5.0, 2.3, "Contingent payoff if credit event", ha="center", color=PAL["grey"], fontsize=10)
        elif tag == "settlement_physical":
            ax.annotate("", xy=(7.0, 3.7), xytext=(3.0, 3.7),
                        arrowprops=dict(arrowstyle="->", color=PAL["red"], lw=1.6))
            ax.text(5.0, 4.0, "Defaulted bond", ha="center", color=PAL["red"], fontsize=10)
            ax.annotate("", xy=(3.0, 2.5), xytext=(7.0, 2.5),
                        arrowprops=dict(arrowstyle="->", color=PAL["green"], lw=1.6))
            ax.text(5.0, 2.2, "Notional amount", ha="center", color=PAL["green"], fontsize=10)
        else:  # cash
            ax.annotate("", xy=(3.0, 3.0), xytext=(7.0, 3.0),
                        arrowprops=dict(arrowstyle="->", color=PAL["green"], lw=1.6))
            ax.text(5.0, 3.3, "Notional - Auction recovery", ha="center", color=PAL["green"], fontsize=10)
        ax.set_title(title, loc="left")
        ax.text(0.0, 0.7, settlement_caption, fontsize=9, color=PAL["grey"])
        save(fig, tag)


# ---------------------------------------------------------------------------
# Figure 4: aggregate EU CDS spread time series
# ---------------------------------------------------------------------------

def fig_eu_cds_timeseries():
    style()
    cds = pd.read_parquet(PROC / "cds_panel.parquet")
    by_day = cds.groupby("Date")["Spread_clean"].mean().sort_index()

    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.plot(by_day.index, by_day.values, color=PAL["blue"], linewidth=1.4)
    ax.axvline(pd.Timestamp("2012-07-26"), color=PAL["red"], linestyle="--", linewidth=1.0)
    ax.text(pd.Timestamp("2012-07-26"), by_day.max() * 0.9,
            "Draghi 'whatever it takes'", color=PAL["red"], fontsize=8, rotation=90, va="top")
    ax.set_ylabel("CDS spread (bps)")
    ax.set_xlabel("")
    ax.set_title("European sovereign CDS premiums peak at the height of the debt crisis and decline sharply after the ECB's July 2012 commitment", loc="left", fontsize=10, wrap=True)
    ax.set_title("Cross-sectional mean of 5Y senior EUR CDS spreads across 25 European sovereigns",
                 loc="left", fontsize=8, color=PAL["grey"], pad=18, fontstyle="italic")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    save(fig, "f4_eu_cds_timeseries")


# ---------------------------------------------------------------------------
# Figure: per-sovereign CDS spreads (small multiples appendix)
# ---------------------------------------------------------------------------

def fig_per_sovereign():
    style()
    cds = pd.read_parquet(PROC / "cds_panel.parquet")
    sovs = sorted(cds["Sovereign"].unique())
    cols = 4; rows = int(np.ceil(len(sovs) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(11, 1.8 * rows), sharex=True)
    axes = axes.flatten()
    for i, sov in enumerate(sovs):
        ax = axes[i]
        sub = cds[cds["Sovereign"] == sov].set_index("Date")["Spread_clean"]
        ax.plot(sub.index, sub.values, color=PAL["blue"], linewidth=0.9)
        ax.set_title(sov, fontsize=9, loc="left")
        ax.tick_params(labelsize=7)
        ax.grid(True)
    for j in range(len(sovs), len(axes)):
        axes[j].set_axis_off()
    fig.suptitle("Daily 5Y senior CDS spreads for the 25 European sovereigns in the sample, 2010-2017",
                 fontsize=10, x=0.02, ha="left")
    fig.tight_layout()
    save(fig, "fA_per_sovereign")


# ---------------------------------------------------------------------------
# Figure: rating event distribution over time
# ---------------------------------------------------------------------------

def fig_event_distribution():
    style()
    ev = pd.read_parquet(PROC / "events.parquet")
    fig, axes = plt.subplots(2, 1, figsize=(7.5, 3.6), sharex=True)
    for ax, ag in zip(axes, ["S&P", "Moody"]):
        sub = ev[ev["Agency"] == ag].copy()
        pos = sub[sub["dCCR"] > 0]; neg = sub[sub["dCCR"] < 0]
        ax.scatter(pos["Date"], np.full(len(pos), 1), s=20, color=PAL["green"], alpha=0.6, label="Positive")
        ax.scatter(neg["Date"], np.full(len(neg), 0), s=20, color=PAL["red"], alpha=0.6, label="Negative")
        ax.set_yticks([0, 1]); ax.set_yticklabels(["Negative", "Positive"])
        ax.set_title(ag, loc="left", fontsize=10)
        ax.set_ylim(-0.5, 1.5)
        ax.axvline(pd.Timestamp("2012-07-26"), color=PAL["grey"], linestyle="--", linewidth=0.7)
    axes[0].legend(loc="upper right", ncol=2, fontsize=8)
    axes[1].xaxis.set_major_locator(mdates.YearLocator())
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.suptitle("Rating events cluster by sign and crisis phase: negative events dominate 2010-2012, positive events dominate 2013-2017",
                 fontsize=10, x=0.02, ha="left")
    fig.tight_layout()
    save(fig, "f5_event_distribution")


# ---------------------------------------------------------------------------
# Figure: short-run reactions across splits (forest-plot style)
# ---------------------------------------------------------------------------

def fig_short_run_forest():
    style()
    r = json.load(open(PROC / "results.json"))
    df = pd.DataFrame(r["table_short_run"])
    df = df[df["agency"] == "All"].copy()
    df["label"] = df["split"]
    rows = ["All", "EMU", "Non-EMU", "PreDraghi", "PostDraghi"]

    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.4), sharex=False)
    for ax, sign, color in zip(axes, ["Negative", "Positive"], [PAL["red"], PAL["green"]]):
        sub = df[df["sign"] == sign].set_index("split").reindex(rows).reset_index()
        y = np.arange(len(sub))[::-1]
        ax.errorbar(sub["mean"], y,
                    xerr=[sub["mean"] - sub["ci_lo"], sub["ci_hi"] - sub["mean"]],
                    fmt="o", color=color, ecolor=PAL["grey"], capsize=3)
        ax.axvline(0, color=PAL["ink"], linewidth=0.7)
        ax.set_yticks(y); ax.set_yticklabels(sub["split"])
        ax.set_title(f"{sign} events", loc="left")
        ax.set_xlabel("Two-day adjusted spread change (bps)")
        for yi, m, lo, hi, n in zip(y, sub["mean"], sub["ci_lo"], sub["ci_hi"], sub["n"]):
            ax.text(ax.get_xlim()[1] if ax.get_xlim()[1] > m else m,
                    yi, f"  n={n}", va="center", fontsize=8, color=PAL["grey"])
    fig.suptitle("EMU sovereigns react three times more strongly to negative events than non-EMU; the reaction is concentrated in the pre-Draghi crisis sub-period",
                 fontsize=10, x=0.02, ha="left", wrap=True)
    fig.tight_layout()
    save(fig, "f6_short_run_forest")


# ---------------------------------------------------------------------------
# Figure: panel regression coefficients
# ---------------------------------------------------------------------------

def fig_panel_regression():
    style()
    r = json.load(open(PROC / "results.json"))
    df = pd.DataFrame(r["table_panel_reg"])
    df = df[df["window"] == "adj_abs_chg_-1_1"]
    df["label"] = df["agency"] + " " + df["sign"].str.upper()

    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    y = np.arange(len(df))[::-1]
    colors = [PAL["red"] if s == "neg" else PAL["green"] for s in df["sign"]]
    ax.errorbar(df["coef"], y, xerr=1.96 * df["se"], fmt="o", ecolor=PAL["grey"], color=PAL["ink"], capsize=3)
    for yi, c, color in zip(y, df["coef"], colors):
        ax.scatter(c, yi, s=60, color=color, zorder=3)
    ax.axvline(0, color=PAL["ink"], linewidth=0.7)
    ax.set_yticks(y); ax.set_yticklabels(df["label"].values)
    ax.set_xlabel("Coefficient on dCCR (bps per notch)")
    ax.set_title("Once standard errors are two-way clustered by country and trading day, only the S&P negative-event coefficient retains marginal significance",
                 loc="left", fontsize=10, wrap=True)
    fig.tight_layout()
    save(fig, "f7_panel_regression")


# ---------------------------------------------------------------------------
# Figure: pre / post Draghi splitting demonstration
# ---------------------------------------------------------------------------

def fig_regime_split():
    style()
    panel = pd.read_parquet(PROC / "event_panel.parquet")
    panel = panel[~panel["Confounded_self"]]

    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    sns.stripplot(data=panel[(panel["Type"] == "Negative") & panel["adj_abs_chg_-1_1"].notna()],
                  x="PostDraghi", y="adj_abs_chg_-1_1",
                  jitter=0.25, alpha=0.45, color=PAL["red"], size=4, ax=ax)
    ax.axhline(0, color=PAL["ink"], linewidth=0.7)
    ax.set_xticklabels(["Pre-Draghi", "Post-Draghi"])
    ax.set_xlabel("")
    ax.set_ylabel("Two-day adjusted spread change (bps)")
    ax.set_ylim(-200, 400)

    pre_mean = panel[(panel["Type"] == "Negative") & (panel["PostDraghi"] == 0)]["adj_abs_chg_-1_1"].mean()
    post_mean = panel[(panel["Type"] == "Negative") & (panel["PostDraghi"] == 1)]["adj_abs_chg_-1_1"].mean()
    ax.scatter([0, 1], [pre_mean, post_mean], color=PAL["ink"], s=80, zorder=4, marker="D")
    ax.text(0, pre_mean + 18, f"{pre_mean:+.1f} bps", ha="center", fontsize=9, color=PAL["ink"], weight="bold")
    ax.text(1, post_mean + 18, f"{post_mean:+.1f} bps", ha="center", fontsize=9, color=PAL["ink"], weight="bold")
    ax.set_title("Negative-event reaction collapses from +20.8 bps to +6.8 bps after the ECB's July 2012 commitment",
                 loc="left", fontsize=10, wrap=True)
    fig.tight_layout()
    save(fig, "f8_regime_split")


def fig_anticipation_paths():
    style()
    panel = pd.read_parquet(PROC / "event_panel.parquet")
    panel = panel[~panel["Confounded_self"]]

    cols = [
        ("adj_abs_chg_-90_-61", "[-90,-61]"),
        ("adj_abs_chg_-60_-31", "[-60,-31]"),
        ("adj_abs_chg_-30_-1", "[-30,-1]"),
        ("adj_abs_chg_-1_1", "[-1,+1]"),
    ]
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    xs = list(range(len(cols)))
    for sign, color in [("Positive", PAL["green"]), ("Negative", PAL["red"])]:
        means = [panel[panel["Type"] == sign][c].mean() for c, _ in cols]
        cis = [1.96 * panel[panel["Type"] == sign][c].sem() for c, _ in cols]
        ax.errorbar(xs, means, yerr=cis, fmt="o-", color=color, label=sign, ecolor=color, alpha=0.85, capsize=3)
    ax.axhline(0, color=PAL["ink"], linewidth=0.7)
    ax.set_xticks(xs); ax.set_xticklabels([lab for _, lab in cols])
    ax.set_xlabel("Pre-event window (trading days)")
    ax.set_ylabel("Mean adjusted spread change (bps)")
    ax.legend()
    ax.set_title("Positive events show modest two-month-ahead anticipation; negative events show none",
                 loc="left", fontsize=10, wrap=True)
    fig.tight_layout()
    save(fig, "f9_anticipation")


def fig_emu_share():
    style()
    ev = pd.read_parquet(PROC / "events.parquet")
    cnt = ev.groupby([ev["Date"].dt.year, "Type"]).size().unstack(fill_value=0)
    cnt = cnt.reindex(columns=["Positive", "Negative"], fill_value=0)
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    cnt[["Positive", "Negative"]].plot(kind="bar", stacked=False, ax=ax,
                                       color=[PAL["green"], PAL["red"]])
    ax.set_xlabel("")
    ax.set_ylabel("Number of rating events")
    ax.set_title("Positive and negative rating events by year, 2010-2017",
                 loc="left", fontsize=10)
    ax.legend(title=None)
    fig.tight_layout()
    save(fig, "f10_event_year")


def fig_spread_distribution():
    style()
    cds = pd.read_parquet(PROC / "cds_panel.parquet")
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    avg = cds.groupby("Sovereign")["Spread_clean"].median().sort_values()
    colors = [PAL["red"] if c in {"Greece", "Cyprus", "Portugal", "Ireland"} else
              PAL["orange"] if c in {"Italy", "Spain"} else PAL["blue"] for c in avg.index]
    ax.barh(range(len(avg)), avg.values, color=colors)
    ax.set_yticks(range(len(avg)))
    ax.set_yticklabels(avg.index, fontsize=8)
    ax.set_xlabel("Median CDS spread (bps, log scale)")
    ax.set_xscale("log")
    ax.set_title("Greece, Cyprus and Portugal stand apart by an order of magnitude",
                 loc="left", fontsize=10, wrap=True)
    fig.tight_layout()
    save(fig, "f11_spread_levels")


def main():
    fig_cashflow_diagrams()
    fig_eu_cds_timeseries()
    fig_per_sovereign()
    fig_event_distribution()
    fig_short_run_forest()
    fig_panel_regression()
    fig_regime_split()
    fig_anticipation_paths()
    fig_emu_share()
    fig_spread_distribution()
    print("figures written to", FIG)


if __name__ == "__main__":
    main()
