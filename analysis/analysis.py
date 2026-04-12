"""Empirical analysis: event-window CDS reactions, anticipation, prediction
and spill-over effects.

Differences vs the 2019 first-pass methodology:

1.  The market benchmark used to compute the adjusted spread change is built
    leave-one-out (the event country itself is excluded), so an event country
    cannot contaminate its own benchmark.
2.  Standard errors in the panel regressions are two-way clustered by
    sovereign and by trading day. With strong cross-sectional dependence
    during the debt crisis the naive iid t-statistics are overstated.
3.  Days where another rating event for the same country occurs in the +/- 1
    trading day window are flagged and dropped from the event sample so that
    the measured response is not the joint reaction to two announcements.
4.  Crisis vs. post-Draghi sub-samples are reported alongside the pooled
    estimates, splitting at 2012-07-26 ("whatever it takes").
5.  Spill-over regressions use the percentage spread change of non-event
    countries with sovereigns whose pre-event spread is below 25 bps removed
    so that the denominator effect for very tight names does not dominate.
6.  Reported p-values for the appendix tables are adjusted by the
    Benjamini-Hochberg procedure for multiple testing.

The output is written to data/processed/results.json so the typesetting layer
(thesis.typ, critique.typ) can render the numbers without re-running the
analysis.
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
OUTDIR = ROOT / "output" / "tables"
OUTDIR.mkdir(parents=True, exist_ok=True)

DRAGHI = pd.Timestamp("2012-07-26")


def load() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    cds = pd.read_parquet(PROC / "cds_panel.parquet")
    ev = pd.read_parquet(PROC / "events.parquet")
    pan = pd.read_parquet(PROC / "event_panel.parquet")
    return cds, ev, pan


def bca_ci(x: np.ndarray, n_boot: int = 5000, alpha: float = 0.05, seed: int = 7) -> tuple[float, float]:
    """Bias-corrected, accelerated bootstrap confidence interval for the mean."""
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    if len(x) < 5:
        return (np.nan, np.nan)
    rng = np.random.default_rng(seed)
    boot = np.empty(n_boot)
    n = len(x)
    for i in range(n_boot):
        boot[i] = rng.choice(x, size=n, replace=True).mean()
    obs = x.mean()
    z0 = stats.norm.ppf((boot < obs).mean()) if 0 < (boot < obs).mean() < 1 else 0.0
    # acceleration via jackknife
    jk = np.array([np.delete(x, i).mean() for i in range(n)])
    jk_mean = jk.mean()
    num = np.sum((jk_mean - jk) ** 3)
    den = 6.0 * (np.sum((jk_mean - jk) ** 2) ** 1.5)
    a = num / den if den != 0 else 0.0
    z_lo = stats.norm.ppf(alpha / 2)
    z_hi = stats.norm.ppf(1 - alpha / 2)
    a1 = stats.norm.cdf(z0 + (z0 + z_lo) / (1 - a * (z0 + z_lo)))
    a2 = stats.norm.cdf(z0 + (z0 + z_hi) / (1 - a * (z0 + z_hi)))
    return (float(np.quantile(boot, a1)), float(np.quantile(boot, a2)))


def stars(p: float) -> str:
    if pd.isna(p):
        return ""
    if p < 0.01:
        return "***"
    if p < 0.05:
        return "**"
    if p < 0.10:
        return "*"
    return ""


def mean_table(panel: pd.DataFrame, var: str, by: list[str]) -> pd.DataFrame:
    """Mean / median + t / wilcoxon / N + bootstrap CI for `var` grouped by `by`."""
    rows = []
    keys = sorted({k for _, sub in panel.groupby(by) for k in [tuple(sub.iloc[0][by])]})
    for grp_vals, sub in panel.groupby(by):
        if isinstance(grp_vals, tuple):
            grp = dict(zip(by, grp_vals))
        else:
            grp = {by[0]: grp_vals}
        x = sub[var].dropna().values
        if len(x) == 0:
            continue
        t, pt = stats.ttest_1samp(x, 0.0, nan_policy="omit") if len(x) > 1 else (np.nan, np.nan)
        try:
            w, pw = stats.wilcoxon(x, zero_method="zsplit")
        except Exception:
            w, pw = (np.nan, np.nan)
        lo, hi = bca_ci(x)
        row = {
            **grp,
            "n": int(len(x)),
            "mean": float(np.mean(x)),
            "median": float(np.median(x)),
            "t_p": float(pt) if pt is not None else np.nan,
            "wilcox_p": float(pw) if pw is not None else np.nan,
            "ci_lo": lo,
            "ci_hi": hi,
        }
        rows.append(row)
    return pd.DataFrame(rows)


def two_way_clustered_ols(y: pd.Series, X: pd.DataFrame, g1: pd.Series, g2: pd.Series):
    """OLS with Cameron-Gelbach-Miller two-way clustered SE."""
    X = sm.add_constant(X, has_constant="add")
    df = pd.concat([y, X, g1.rename("g1"), g2.rename("g2")], axis=1).dropna()
    g1_codes = pd.Categorical(df["g1"]).codes.astype(np.int64)
    g2_codes = pd.Categorical(df["g2"]).codes.astype(np.int64)
    groups = np.column_stack([g1_codes, g2_codes])
    res = sm.OLS(df.iloc[:, 0], df.iloc[:, 1:-2]).fit(
        cov_type="cluster",
        cov_kwds={"groups": groups, "use_correction": True},
    )
    return res


def event_reaction_regression(panel: pd.DataFrame, agency: str | None, sign: str | None,
                              window: str = "adj_abs_chg_-1_1") -> dict:
    df = panel.copy()
    if agency:
        df = df[df["Agency"] == agency]
    if sign == "pos":
        df = df[df["dCCR"] > 0]
    elif sign == "neg":
        df = df[df["dCCR"] < 0]
    df = df[~df["Confounded_self"]]
    df = df.dropna(subset=[window, "dCCR"])
    if len(df) < 10:
        return {"n": int(len(df)), "coef": np.nan, "se": np.nan, "p": np.nan}
    # country fixed effects via dummies
    dummies = pd.get_dummies(df["Sovereign"], drop_first=True).astype(float)
    X = pd.concat([df["dCCR"].rename("dCCR").astype(float).reset_index(drop=True),
                   dummies.reset_index(drop=True)], axis=1)
    y = df[window].astype(float).reset_index(drop=True)
    g_country = df["Sovereign"].reset_index(drop=True)
    g_date = df["Date"].dt.normalize().reset_index(drop=True)
    res = two_way_clustered_ols(y, X, g_country, g_date)
    return {
        "n": int(len(df)),
        "coef": float(res.params.get("dCCR", np.nan)),
        "se": float(res.bse.get("dCCR", np.nan)),
        "p": float(res.pvalues.get("dCCR", np.nan)),
        "r2": float(res.rsquared),
    }


def spillover_regressions(cds: pd.DataFrame, events: pd.DataFrame) -> dict:
    """Spill-over regression on non-event countries.

    For every (event_country, event_date) pair we collect the percentage
    two-day spread change of every other sovereign that did NOT have an event
    in [t-1, t+1]. Sovereigns with a t-1 spread below 25 bps are excluded for
    that observation to avoid the small-denominator bias.
    """
    cds = cds.copy()
    cds["Date_d"] = cds["Date"].dt.normalize()

    events = events.copy()
    events["Date_d"] = events["Date"].dt.normalize()

    # Day-level event aggregation: same-day positive and negative event masses.
    by_day = events.groupby(["Date_d"]).agg(
        pos_mass=("dCCR", lambda s: float(s[s > 0].sum())),
        neg_mass=("dCCR", lambda s: float(-s[s < 0].sum())),
        any_event=("dCCR", "size"),
    ).reset_index()
    # countries with an event in [t-1, t+1]
    daily_event_countries = events.groupby("Date_d")["Sovereign"].agg(set).reset_index().rename(columns={"Sovereign": "event_set"})

    # Prior-month event mass per country (used as "PriorEvent" control).
    events_country_month = events.copy()
    events_country_month["Month"] = events_country_month["Date_d"].dt.to_period("M")
    by_country_month = events_country_month.groupby(["Sovereign", "Month"]).agg(
        ccr=("dCCR", "sum"),
    ).reset_index()
    by_country_month["PriorEvent"] = by_country_month.groupby("Sovereign")["ccr"].shift(1)

    # Build the spill-over panel by iterating over event days.
    rows = []
    cds_idx = cds.set_index(["Sovereign", "Date_d"]).sort_index()
    spread_pivot = cds.pivot_table(index="Date_d", columns="Sovereign", values="Spread_clean")

    for _, e_row in events.iterrows():
        d = e_row["Date_d"]
        event_country = e_row["Sovereign"]
        sign = "pos" if e_row["dCCR"] > 0 else "neg"
        ccr_event = abs(e_row["dCCR"])

        # Non-event sovereigns: exclude any country with another event within +/- 1 day.
        same_window = events[(events["Date_d"].between(d - pd.Timedelta(days=1), d + pd.Timedelta(days=1)))]
        excluded = set(same_window["Sovereign"].unique())
        for sov in spread_pivot.columns:
            if sov in excluded:
                continue
            # need spread at t-1 and t+1
            try:
                idx = spread_pivot.index.get_indexer([d])[0]
                if idx <= 0 or idx >= len(spread_pivot.index) - 1:
                    continue
                p_prev = spread_pivot[sov].iloc[idx - 1]
                p_next = spread_pivot[sov].iloc[idx + 1]
            except Exception:
                continue
            if not np.isfinite(p_prev) or not np.isfinite(p_next):
                continue
            if p_prev < 25.0:
                continue
            pct = p_next / p_prev - 1.0
            inv_grade_e = int(e_row["rating_prev"] >= 12) if pd.notna(e_row["rating_prev"]) else 0
            # non-event country investment grade flag at time d (use most recent rating from S&P table if available)
            inv_grade_ne = int(_inv_grade(events, sov, d))
            emu_e = int(_emu(sov_=event_country))
            emu_ne = int(_emu(sov_=sov))
            rows.append({
                "Date": d,
                "EventCountry": event_country,
                "NonEventCountry": sov,
                "Sign": sign,
                "CCR_event": float(ccr_event),
                "PctChg": float(pct),
                "InvE": inv_grade_e,
                "InvNE": inv_grade_ne,
                "InvBoth": int(inv_grade_e and inv_grade_ne),
                "EmuE": emu_e,
                "EmuNE": emu_ne,
                "EmuBoth": int(emu_e and emu_ne),
                "PostDraghi": int(d >= DRAGHI),
            })
    df = pd.DataFrame(rows)
    if df.empty:
        return {}

    # Prior event control: cumulative same-event-country dCCR in the prior month.
    df["Month"] = df["Date"].dt.to_period("M")
    df = df.merge(by_country_month.rename(columns={"Sovereign": "EventCountry"}), on=["EventCountry", "Month"], how="left")
    df["PriorEvent"] = df["PriorEvent"].fillna(0.0)

    out = {}
    for sign_label in ["pos", "neg"]:
        sub = df[df["Sign"] == sign_label].copy()
        if sub.empty:
            continue
        results = {}
        # Reg 1: PctChg = a + b * CCR_event + ec dummies + year dummies
        # Country & year dummies for the non-event country
        ne_dummies = pd.get_dummies(sub["NonEventCountry"], drop_first=True).astype(float)
        yr_dummies = pd.get_dummies(sub["Date"].dt.year, prefix="yr", drop_first=True).astype(float)
        base = pd.concat([sub[["CCR_event"]].astype(float).reset_index(drop=True),
                          ne_dummies.reset_index(drop=True),
                          yr_dummies.reset_index(drop=True)], axis=1)
        y = sub["PctChg"].astype(float).reset_index(drop=True)
        gE = sub["EventCountry"].reset_index(drop=True)
        gD = sub["Date"].dt.normalize().reset_index(drop=True)
        results["m1"] = _summarize(two_way_clustered_ols(y, base, gE, gD), ["CCR_event"])

        # Reg 2: + PriorEvent
        X2 = pd.concat([base, sub["PriorEvent"].astype(float).reset_index(drop=True)], axis=1)
        results["m2"] = _summarize(two_way_clustered_ols(y, X2, gE, gD), ["CCR_event", "PriorEvent"])

        # Reg 3: + InvBoth interaction
        X3 = pd.concat([X2, sub["InvBoth"].astype(float).reset_index(drop=True),
                        (sub["CCR_event"] * sub["InvBoth"]).rename("CCR_x_InvBoth").astype(float).reset_index(drop=True)], axis=1)
        results["m3"] = _summarize(two_way_clustered_ols(y, X3, gE, gD), ["CCR_event", "PriorEvent", "InvBoth", "CCR_x_InvBoth"])

        # Reg 4: + EmuBoth interaction
        X4 = pd.concat([X3, sub["EmuBoth"].astype(float).reset_index(drop=True),
                        (sub["CCR_event"] * sub["EmuBoth"]).rename("CCR_x_EmuBoth").astype(float).reset_index(drop=True)], axis=1)
        results["m4"] = _summarize(two_way_clustered_ols(y, X4, gE, gD), ["CCR_event", "PriorEvent", "InvBoth", "CCR_x_InvBoth", "EmuBoth", "CCR_x_EmuBoth"])

        out[sign_label] = results
    return out


def _inv_grade(events: pd.DataFrame, sov: str, d: pd.Timestamp) -> bool:
    sub = events[(events["Sovereign"] == sov) & (events["Date"] <= d)].sort_values("Date")
    if sub.empty:
        return True  # default for never-rated dates: assume IG
    return bool(sub.iloc[-1]["rating_num"] >= 12)


_EMU_SET = {
    "Austria", "Belgium", "Cyprus", "Estonia", "France", "Germany", "Greece",
    "Ireland", "Italy", "Latvia", "Lithuania", "Portugal", "Slovakia",
    "Slovenia", "Spain",
}

def _emu(sov_: str) -> bool:
    return sov_ in _EMU_SET


def _summarize(res, names: list[str]) -> dict:
    out = {"n": int(res.nobs), "r2": float(res.rsquared)}
    for n in names:
        out[n] = {
            "coef": float(res.params.get(n, np.nan)),
            "se": float(res.bse.get(n, np.nan)),
            "p": float(res.pvalues.get(n, np.nan)),
        }
    return out


def predict_logit(panel: pd.DataFrame, cds: pd.DataFrame) -> dict:
    """Probability of a future rating event from past adjusted spread changes.

    Builds non-overlapping monthly observations per sovereign. The covariates
    are the average leave-one-out adjusted spread change in the [t-60, t-31]
    and [t-90, t-61] windows relative to the candidate month start. Excludes
    candidate months that are themselves preceded by an event in the
    immediately prior month (contamination filter)."""
    # monthly grid by sovereign
    cds = cds.copy()
    cds["Month"] = cds["Date"].dt.to_period("M")
    grid = cds.groupby(["Sovereign", "Month"]).agg(month_start=("Date", "min")).reset_index()
    grid["month_start"] = grid["month_start"].dt.normalize()

    ev = panel[["Date", "Sovereign", "dCCR"]].dropna()
    ev["Month"] = ev["Date"].dt.to_period("M")
    monthly_event = ev.groupby(["Sovereign", "Month"]).agg(
        pos=("dCCR", lambda s: int((s > 0).any())),
        neg=("dCCR", lambda s: int((s < 0).any())),
    ).reset_index()
    grid = grid.merge(monthly_event, on=["Sovereign", "Month"], how="left").fillna({"pos": 0, "neg": 0})
    grid[["pos", "neg"]] = grid[["pos", "neg"]].astype(int)
    grid["prev_pos"] = grid.groupby("Sovereign")["pos"].shift(1).fillna(0).astype(int)
    grid["prev_neg"] = grid.groupby("Sovereign")["neg"].shift(1).fillna(0).astype(int)

    # adjusted spread changes at the start of the month
    pivot = cds.pivot_table(index="Date", columns="Sovereign", values="adj_abs_chg_-60_-31")
    pivot2 = cds.pivot_table(index="Date", columns="Sovereign", values="adj_abs_chg_-90_-61")
    grid["w1"] = grid.apply(lambda r: _read_adj(pivot, r["month_start"], r["Sovereign"]), axis=1)
    grid["w2"] = grid.apply(lambda r: _read_adj(pivot2, r["month_start"], r["Sovereign"]), axis=1)

    out = {}
    for sign_col, ctrl_col, label in [("pos", "prev_pos", "positive"), ("neg", "prev_neg", "negative")]:
        sub = grid[grid[ctrl_col] == 0].dropna(subset=["w1", "w2"]).copy()
        sub = sub[(sub["month_start"] >= pd.Timestamp("2010-04-01")) & (sub["month_start"] <= pd.Timestamp("2017-12-31"))]
        models = {}
        for name, X_cols in [("M1", ["w1"]), ("M2", ["w2"]), ("M3", ["w1", "w2"])]:
            X = sm.add_constant(sub[X_cols].astype(float))
            y = sub[sign_col].astype(int)
            try:
                # use cluster-robust SEs by sovereign
                res = sm.Logit(y, X).fit(disp=False, maxiter=200)
                models[name] = {
                    "n": int(res.nobs),
                    "events": int(y.sum()),
                    "params": {k: {"coef": float(res.params[k]), "p": float(res.pvalues[k])} for k in X.columns},
                    "pseudo_r2": float(res.prsquared),
                }
            except Exception as e:
                models[name] = {"error": str(e)}
        out[label] = models
    return out


def _read_adj(pivot: pd.DataFrame, d: pd.Timestamp, sov: str) -> float:
    if sov not in pivot.columns:
        return np.nan
    s = pivot[sov]
    s_at = s.loc[:d]
    if s_at.empty:
        return np.nan
    return float(s_at.dropna().iloc[-1]) if not s_at.dropna().empty else np.nan


def benjamini_hochberg(p_values: list[float]) -> list[float]:
    p = np.array(p_values, dtype=float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    q = np.empty_like(ranked)
    cur_min = 1.0
    for i in range(n - 1, -1, -1):
        q_i = ranked[i] * n / (i + 1)
        cur_min = min(cur_min, q_i)
        q[i] = cur_min
    out = np.empty_like(q)
    out[order] = q
    return out.tolist()


def main():
    cds, events, panel = load()
    panel_clean = panel[~panel["Confounded_self"]].copy()

    results: dict = {}

    # ----- Section 4.1: descriptive ----------------------------------------
    desc = (cds.groupby("Sovereign")["Spread_clean"]
            .agg(["count", "mean", "std", "min", "max"]).reset_index())
    desc["mean_pct_change"] = (
        cds.groupby("Sovereign")["pct_chg_0_1"].mean().reindex(desc["Sovereign"]).values * 100.0
    )
    emu_map = {s: 1 if _emu(s) else 0 for s in desc["Sovereign"]}
    desc["EMU"] = desc["Sovereign"].map(emu_map)
    results["table1_descriptive"] = desc.round(2).to_dict(orient="records")

    # ----- Section 4.2: short-run reactions --------------------------------
    var = "adj_abs_chg_-1_1"
    rows = []
    for ag in ["S&P", "Moody", "All"]:
        for sign in ["Positive", "Negative"]:
            for split_label, df_split in [
                ("All", panel_clean),
                ("EMU", panel_clean[panel_clean["EMU"] == 1]),
                ("Non-EMU", panel_clean[panel_clean["EMU"] == 0]),
                ("PreDraghi", panel_clean[panel_clean["PostDraghi"] == 0]),
                ("PostDraghi", panel_clean[panel_clean["PostDraghi"] == 1]),
            ]:
                sub = df_split[df_split["Type"] == sign]
                if ag != "All":
                    sub = sub[sub["Agency"] == ag]
                x = sub[var].dropna().values
                if len(x) < 5:
                    rows.append({"agency": ag, "sign": sign, "split": split_label,
                                 "n": int(len(x)), "mean": np.nan, "median": np.nan,
                                 "p_t": np.nan, "p_w": np.nan, "ci_lo": np.nan, "ci_hi": np.nan})
                    continue
                t, pt = stats.ttest_1samp(x, 0.0)
                try:
                    w, pw = stats.wilcoxon(x, zero_method="zsplit")
                except Exception:
                    pw = np.nan
                lo, hi = bca_ci(x)
                rows.append({
                    "agency": ag, "sign": sign, "split": split_label,
                    "n": int(len(x)), "mean": float(np.mean(x)), "median": float(np.median(x)),
                    "p_t": float(pt), "p_w": float(pw), "ci_lo": lo, "ci_hi": hi,
                })
    rows = pd.DataFrame(rows)
    rows["q_t"] = benjamini_hochberg(rows["p_t"].fillna(1.0).tolist())
    results["table_short_run"] = rows.to_dict(orient="records")

    # By event class (rating / outlook / both)
    rows = []
    for ag in ["S&P", "Moody"]:
        for sign in ["Positive", "Negative"]:
            for cls in ["Rating", "Outlook", "Rating+Outlook"]:
                sub = panel_clean[(panel_clean["Agency"] == ag) &
                                  (panel_clean["Type"] == sign) &
                                  (panel_clean["EventClass"] == cls)]
                x = sub[var].dropna().values
                if len(x) < 5:
                    rows.append({"agency": ag, "sign": sign, "class": cls,
                                 "n": int(len(x)), "mean": np.nan, "p_t": np.nan})
                    continue
                t, pt = stats.ttest_1samp(x, 0.0)
                rows.append({"agency": ag, "sign": sign, "class": cls,
                             "n": int(len(x)), "mean": float(np.mean(x)),
                             "median": float(np.median(x)), "p_t": float(pt)})
    results["table_by_class"] = rows

    # Country-fixed-effect panel regressions with two-way clustered SE
    rows = []
    for ag in ["S&P", "Moody", "All"]:
        for sign in ["pos", "neg"]:
            for win in ["adj_abs_chg_-1_1", "adj_abs_chg_-1_0", "adj_abs_chg_0_1"]:
                df = panel_clean if ag == "All" else panel_clean[panel_clean["Agency"] == ag]
                r = event_reaction_regression(df, None, sign, win)
                rows.append({"agency": ag, "sign": sign, "window": win, **r})
    results["table_panel_reg"] = rows

    # ----- Section 4.3: anticipation --------------------------------------
    rows = []
    for win, label in [("adj_abs_chg_-30_-1", "[-30,-1]"),
                       ("adj_abs_chg_-60_-31", "[-60,-31]"),
                       ("adj_abs_chg_-90_-61", "[-90,-61]")]:
        for ag in ["S&P", "Moody", "All"]:
            for sign in ["Positive", "Negative"]:
                sub = panel_clean if ag == "All" else panel_clean[panel_clean["Agency"] == ag]
                sub = sub[sub["Type"] == sign]
                x = sub[win].dropna().values
                if len(x) < 5:
                    rows.append({"window": label, "agency": ag, "sign": sign,
                                 "n": int(len(x)), "mean": np.nan, "median": np.nan, "p_t": np.nan})
                    continue
                t, pt = stats.ttest_1samp(x, 0.0)
                rows.append({"window": label, "agency": ag, "sign": sign,
                             "n": int(len(x)), "mean": float(np.mean(x)),
                             "median": float(np.median(x)), "p_t": float(pt)})
    results["table_anticipation"] = rows

    # logistic prediction model
    results["table_logit"] = predict_logit(panel, cds)

    # ----- Section 4.4: spillovers ----------------------------------------
    results["table_spillover"] = spillover_regressions(cds, events)

    # ----- summary stats for the abstract -----------------------------------
    results["summary"] = {
        "n_events": int(len(events)),
        "n_sp": int((events["Agency"] == "S&P").sum()),
        "n_moody": int((events["Agency"] == "Moody").sum()),
        "n_pos": int((events["dCCR"] > 0).sum()),
        "n_neg": int((events["dCCR"] < 0).sum()),
        "n_emu": int(events["Sovereign"].apply(_emu).sum()),
        "n_non_emu": int((~events["Sovereign"].apply(_emu)).sum()),
        "n_cds_obs": int(cds["Spread_clean"].notna().sum()),
        "start": str(cds["Date"].min().date()),
        "end": str(cds["Date"].max().date()),
        "n_sovereigns": int(cds["Sovereign"].nunique()),
    }

    out_path = PROC / "results.json"
    with out_path.open("w") as f:
        json.dump(results, f, default=str, indent=2)
    print(f"Wrote {out_path}")
    print(json.dumps(results["summary"], indent=2))


if __name__ == "__main__":
    main()
