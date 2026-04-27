"""Data preparation: build a clean panel of European sovereign CDS spreads,
S&P and Moody's rating events for the 2010-2017 study window.

The pipeline produces three files in data/processed/:
- cds_panel.parquet: long-format daily CDS spreads with cleaning flags
- events.parquet: rating + outlook events with comprehensive credit rating (CCR)
- event_panel.parquet: merged event observations with surrounding spread changes

The numerical CCR follows Gande and Parsley (2005). The 21-point rating scale
runs from AAA = 21 down to D = 1; each notch is one unit. Outlook adjustments
add +0.5 for positive, -0.5 for negative, 0 for stable. The full credit rating
state is the sum of the rating notch and the outlook adjustment.
"""

from __future__ import annotations

from pathlib import Path
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
try:
    warnings.filterwarnings("ignore", category=pd.errors.Pandas4Warning)  # type: ignore[attr-defined]
except AttributeError:
    pass
pd.options.mode.chained_assignment = None

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

START = pd.Timestamp("2010-01-01")
END = pd.Timestamp("2017-12-31")

# A 21-notch alphanumeric rating scale (AAA=21 ... D=1).
SP_RATING_MAP = {
    "AAA": 21, "AA+": 20, "AA": 19, "AA-": 18,
    "A+": 17, "A": 16, "A-": 15,
    "BBB+": 14, "BBB": 13, "BBB-": 12,
    "BB+": 11, "BB": 10, "BB-": 9,
    "B+": 8, "B": 7, "B-": 6,
    "CCC+": 5, "CCC": 4, "CCC-": 3,
    "CC": 2, "C": 1, "D": 0, "SD": 0,
}
MOODY_RATING_MAP = {
    "Aaa": 21, "Aa1": 20, "Aa2": 19, "Aa3": 18,
    "A1": 17, "A2": 16, "A3": 15,
    "Baa1": 14, "Baa2": 13, "Baa3": 12,
    "Ba1": 11, "Ba2": 10, "Ba3": 9,
    "B1": 8, "B2": 7, "B3": 6,
    "Caa1": 5, "Caa2": 4, "Caa3": 3,
    "Ca": 2, "C": 1, "WR": np.nan,
    # historical pre-1982 terminology
    "Aa": 19,
}
OUTLOOK_MAP = {
    "Stable": 0.0, "stable": 0.0,
    "Positive": 0.5, "positive": 0.5, "POS": 0.5,
    "Negative": -0.5, "negative": -0.5, "NEG": -0.5,
}
# Outlook strings to treat as "no clean signal" - any sovereign-day with one of
# these labels is dropped from the outlook timeline.
OUTLOOK_DISCARD = {
    "Watch Pos", "Watch Neg", "Watch Dev", "Developing", "NR", "--",
    "Ratings Under Review", "Positive (multiple)", "Stable (multiple)",
    "Ratings Withdrawn", "No Outlook", "RUR",
}

# 25 European sovereigns with both rating coverage and a 5Y senior CDS
UNIVERSE = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech",
    "Denmark", "Estonia", "France", "Germany", "Greece", "Hungary",
    "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Poland",
    "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden",
    "United Kingdom",
]


def load_cds() -> pd.DataFrame:
    """Read the Datastream CDS export and return long-format daily spreads."""
    raw = pd.read_excel(RAW / "cds" / "CDS_download_raw.xlsx", sheet_name=0)
    # Row 0 = Datastream codes, row 1 = currency (E for EUR), rows 2+ are dates.
    code_row = raw.iloc[0, 1:].to_dict()
    body = raw.iloc[2:].copy()
    body.columns = ["Date"] + list(raw.columns[1:])
    body["Date"] = pd.to_datetime(body["Date"], errors="coerce")
    body = body.dropna(subset=["Date"]).set_index("Date")

    long = body.stack(future_stack=True).rename("Spread").reset_index()
    long.columns = ["Date", "Sovereign_label", "Spread"]
    long["Spread"] = pd.to_numeric(long["Spread"], errors="coerce")

    # Sovereign labels in the file are the long Datastream descriptions; keep a
    # short Sovereign name parallel to UNIVERSE.
    name_map = {
        "REPUBLIC OF AUSTRIA SNR CR 5Y E - CDS PREM. MID": "Austria",
        "KINGDOM OF BELGIUM SNR CR 5Y E - CDS PREM. MID": "Belgium",
        "REPUBLIC OF BULGARIA SNR CR14 5Y E - CDS PREM. MID": "Bulgaria",
        "REPUBLIC OF CROATIA SNR CR14 5Y E - CDS PREM. MID": "Croatia",
        "REPUBLIC OF CYPRUS SNR CR 5Y E - CDS PREM. MID": "Cyprus",
        "CZECH REPUBLIC SNR CR14 5Y E - CDS PREM. MID": "Czech",
        "KINGDOM OF DENMARK SNR CR 5Y E - CDS PREM. MID": "Denmark",
        "REPUBLIC OF ESTONIA SNR CR14 5Y E - CDS PREM. MID": "Estonia",
        "FRANCE (GOVERNMENT) SNR CR 5Y E - CDS PREM. MID": "France",
        "FEDERAL REP GERMANY SNR CR 5Y E - CDS PREM. MID": "Germany",
        "HELLENIC REPUBLIC SNR CR 5Y E - CDS PREM. MID": "Greece",
        "HUNGARY SNR CR14 5Y E - CDS PREM. MID": "Hungary",
        "REPUBLIC OF ICELAND SNR CR 5Y E - CDS PREM. MID": "Iceland",
        "IRELAND SNR CR 5Y E - CDS PREM. MID": "Ireland",
        "REPUBLIC OF ITALY SNR CR 5Y E - CDS PREM. MID": "Italy",
        "REPUBLIC OF LATVIA SNR CR14 5Y E - CDS PREM. MID": "Latvia",
        "REP OF LITHUANIA SNR CR14 5Y E - CDS PREM. MID": "Lithuania",
        "REPUBLIC OF POLAND SNR CR14 5Y E - CDS PREM. MID": "Poland",
        "REPUBLIC OF PORTUGAL SNR CR 5Y E - CDS PREM. MID": "Portugal",
        "ROMANIA SNR CR14 5Y E - CDS PREM. MID": "Romania",
        "SLOVAK REPUBLIC SNR CR14 5Y E - CDS PREM. MID": "Slovakia",
        "REPUBLIC OF SLOVENIA SNR CR14 5Y E - CDS PREM. MID": "Slovenia",
        "KINGDOM OF SPAIN SNR CR 5Y E - CDS PREM. MID": "Spain",
        "KINGDOM OF SWEDEN SNR CR 5Y E - CDS PREM. MID": "Sweden",
        "UK AND NI SNR CR 5Y E - CDS PREM. MID": "United Kingdom",
    }
    long["Sovereign"] = long["Sovereign_label"].map(name_map)
    long = long.dropna(subset=["Sovereign"]).drop(columns=["Sovereign_label"])
    long = long[(long["Date"] >= START) & (long["Date"] <= END)]
    long = long.sort_values(["Sovereign", "Date"]).reset_index(drop=True)

    # Block-stale flag: a quote is "stale" if it sits inside a block of at
    # least 5 consecutive identical values. Greece 2012-2017 (frozen at
    # 14,909.36) is the canonical example. Every row in such a block is set
    # to NaN rather than dropped. Earlier versions of this filter only marked
    # the tail of the run; the implementation below labels the whole block.
    def stale_block_mask(s: pd.Series, run: int = 5) -> pd.Series:
        block = (s != s.shift()).cumsum()
        sizes = s.groupby(block).transform("size")
        return sizes >= run

    long["stale"] = (
        long.groupby("Sovereign")["Spread"]
        .transform(lambda s: stale_block_mask(s.astype(float), run=5))
        .fillna(False)
    )
    long["Spread_clean"] = np.where(long["stale"], np.nan, long["Spread"])
    return long


def _add_spread_changes(panel: pd.DataFrame, leave_one_out: bool) -> pd.DataFrame:
    """Compute event-window changes around each row.

    Windows are defined in **trading-day** terms by re-indexing to a per-country
    business-day calendar before shifting. This avoids the calendar/row-count
    mismatch that arises when stale weekends are included in a row-based shift.
    """
    panel = panel.sort_values(["Sovereign", "Date"]).reset_index(drop=True)

    # Daily benchmark: cross-sectional mean spread on each date.
    pivot = (
        panel.pivot(index="Date", columns="Sovereign", values="Spread_clean")
        .sort_index()
    )

    if leave_one_out:
        # market[i, t] = mean over all sovereigns except i (NaN-aware)
        denom = pivot.notna().sum(axis=1)
        total = pivot.sum(axis=1, min_count=1)
        market = pd.DataFrame(index=pivot.index, columns=pivot.columns, dtype=float)
        for c in pivot.columns:
            n = denom - pivot[c].notna().astype(int)
            s = total - pivot[c].fillna(0)
            market[c] = s / n.replace(0, np.nan)
    else:
        market = pivot.mean(axis=1).to_frame().reindex(columns=pivot.columns).ffill(axis=1)
        # broadcast scalar series to each column
        m = pivot.mean(axis=1)
        market = pd.DataFrame({c: m for c in pivot.columns})

    def n_day_change(p: pd.DataFrame, lower: int, upper: int) -> pd.DataFrame:
        """p[t+upper] - p[t+lower]; NaN if either endpoint missing."""
        return p.shift(-upper) - p.shift(-lower)

    def n_day_pct(p: pd.DataFrame, lower: int, upper: int) -> pd.DataFrame:
        return p.shift(-upper) / p.shift(-lower) - 1.0

    windows = {
        "_-1_1": (-1, 1),
        "_-1_0": (-1, 0),
        "_0_1": (0, 1),
        "_-30_-1": (-30, -1),
        "_-60_-31": (-60, -31),
        "_-90_-61": (-90, -61),
    }

    pieces = []
    for c in pivot.columns:
        sub = pd.DataFrame({"Spread_clean": pivot[c], "Market_clean": market[c]})
        sub.index.name = "Date"
        sub["Sovereign"] = c
        for tag, (lo, hi) in windows.items():
            sub[f"abs_chg{tag}"] = n_day_change(pivot[c], lo, hi)
            sub[f"pct_chg{tag}"] = n_day_pct(pivot[c], lo, hi)
            sub[f"market_abs_chg{tag}"] = n_day_change(market[c], lo, hi)
            sub[f"market_pct_chg{tag}"] = n_day_pct(market[c], lo, hi)
            sub[f"adj_abs_chg{tag}"] = sub[f"abs_chg{tag}"] - sub[f"market_abs_chg{tag}"]
            sub[f"adj_pct_chg{tag}"] = sub[f"pct_chg{tag}"] - sub[f"market_pct_chg{tag}"]
        pieces.append(sub.reset_index())

    out = pd.concat(pieces, ignore_index=True)
    return out


def build_cds_panel() -> pd.DataFrame:
    raw = load_cds()
    panel = _add_spread_changes(raw[["Date", "Sovereign", "Spread", "Spread_clean"]], leave_one_out=True)
    emu = pd.read_excel(RAW / "mappings" / "EMU_member.xlsx")
    emu["EMU"] = emu["EMU"].map({"EMU": 1, "Non-EMU": 0})
    # The original mapping does not list Slovenia explicitly; Slovenia joined
    # the euro on 2007-01-01, so it is EMU for the entire study window.
    if "Slovenia" not in set(emu["Sovereign"]):
        emu = pd.concat([emu, pd.DataFrame({"Sovereign": ["Slovenia"], "EMU": [1]})], ignore_index=True)
    panel = panel.merge(emu, on="Sovereign", how="left")
    panel.to_parquet(OUT / "cds_panel.parquet", index=False)
    return panel


def build_sp_events() -> pd.DataFrame:
    df = pd.read_excel(RAW / "sp" / "S&P_rating.xlsx")
    df["Date"] = pd.to_datetime(df["Date"], format="%b. %d, %Y", errors="coerce")
    df = df.dropna(subset=["Date"])
    df["Sovereign"] = df["Sovereign"].replace({"Czech Republic": "Czech"})
    df = df[df["Sovereign"].isin(UNIVERSE)].sort_values(["Sovereign", "Date"]).copy()
    df["rating_num"] = df["Rating"].map(SP_RATING_MAP)
    df = df[~df["Outlook"].isin(OUTLOOK_DISCARD)]
    df["outlook_num"] = df["Outlook"].map(OUTLOOK_MAP)
    df = df.dropna(subset=["rating_num", "outlook_num"])
    df["CCR_state"] = df["rating_num"] + df["outlook_num"]
    df["CCR_prev"] = df.groupby("Sovereign")["CCR_state"].shift(1)
    df["rating_prev"] = df.groupby("Sovereign")["rating_num"].shift(1)
    df["outlook_prev"] = df.groupby("Sovereign")["outlook_num"].shift(1)
    df["dCCR"] = df["CCR_state"] - df["CCR_prev"]
    df["dRating"] = df["rating_num"] - df["rating_prev"]
    df["dOutlook"] = df["outlook_num"] - df["outlook_prev"]
    df["Agency"] = "S&P"
    df = df[df["dCCR"].abs() > 0]
    return df[
        ["Date", "Sovereign", "Agency", "Rating", "Outlook",
         "rating_num", "outlook_num", "rating_prev", "outlook_prev",
         "CCR_state", "CCR_prev", "dCCR", "dRating", "dOutlook"]
    ]


def build_moody_events() -> pd.DataFrame:
    out_dir = RAW / "moody" / "Raw_data" / "Outlook"
    rat_dir = RAW / "moody" / "Raw_data" / "Rating"
    rating_frames = []
    for p in sorted(rat_dir.glob("*.xlsx")):
        sov = p.stem.replace("rating_", "")
        try:
            t = pd.read_excel(p, header=5)
        except Exception:
            continue
        t["Sovereign"] = sov
        rating_frames.append(t)
    rat = pd.concat(rating_frames, ignore_index=True)
    rat.columns = [str(c).strip() for c in rat.columns]
    cols = list(rat.columns)
    rat = rat.rename(columns={cols[0]: "Date", cols[1]: "Currency", cols[2]: "Rating", cols[3]: "Action"})
    rat["Date"] = pd.to_datetime(rat["Date"], errors="coerce")
    rat = rat.dropna(subset=["Date", "Rating"])
    rat["Rating"] = rat["Rating"].replace({"Aa": "Aa1"})
    rat["rating_num"] = rat["Rating"].map(MOODY_RATING_MAP)
    rat = rat.dropna(subset=["rating_num"])
    # Restrict to foreign-currency long-term ratings where currency is given.
    if "Currency" in rat.columns:
        rat = rat[rat["Currency"].astype(str).str.contains("Foreign", na=True)]
    rat = rat.sort_values(["Sovereign", "Date"]).copy()

    outlook_frames = []
    for p in sorted(out_dir.glob("*.xlsx")):
        sov = p.stem.replace("outlook_", "")
        try:
            t = pd.read_excel(p, header=5)
        except Exception:
            continue
        t["Sovereign"] = sov
        outlook_frames.append(t)
    otk = pd.concat(outlook_frames, ignore_index=True)
    otk.columns = [str(c).strip() for c in otk.columns]
    cols = list(otk.columns)
    otk = otk.rename(columns={cols[0]: "Date", cols[1]: "Outlook"})
    otk["Date"] = pd.to_datetime(otk["Date"], errors="coerce")
    otk = otk.dropna(subset=["Date", "Outlook"])
    otk = otk[~otk["Outlook"].isin(OUTLOOK_DISCARD)]
    otk["outlook_num"] = otk["Outlook"].map(OUTLOOK_MAP)
    otk = otk.dropna(subset=["outlook_num"])
    otk = otk.sort_values(["Sovereign", "Date"]).copy()

    # Carry-forward rating + outlook across the union of dates per sovereign.
    full = pd.merge(rat[["Date", "Sovereign", "Rating", "rating_num"]],
                    otk[["Date", "Sovereign", "Outlook", "outlook_num"]],
                    on=["Date", "Sovereign"], how="outer")
    full = full.sort_values(["Sovereign", "Date"]).copy()
    full["rating_num"] = full.groupby("Sovereign")["rating_num"].ffill()
    full["outlook_num"] = full.groupby("Sovereign")["outlook_num"].ffill()
    full = full.dropna(subset=["outlook_num"])
    full["Rating"] = full.groupby("Sovereign")["Rating"].ffill()
    full["Outlook"] = full.groupby("Sovereign")["Outlook"].ffill()
    full = full.dropna(subset=["rating_num"])
    full["CCR_state"] = full["rating_num"] + full["outlook_num"]
    full["CCR_prev"] = full.groupby("Sovereign")["CCR_state"].shift(1)
    full["rating_prev"] = full.groupby("Sovereign")["rating_num"].shift(1)
    full["outlook_prev"] = full.groupby("Sovereign")["outlook_num"].shift(1)
    full["dCCR"] = full["CCR_state"] - full["CCR_prev"]
    full["dRating"] = full["rating_num"] - full["rating_prev"]
    full["dOutlook"] = full["outlook_num"] - full["outlook_prev"]
    full["Agency"] = "Moody"
    full = full[full["dCCR"].abs() > 0]
    full["Sovereign"] = full["Sovereign"].replace({"Czech": "Czech"})
    full = full[full["Sovereign"].isin(UNIVERSE)]
    return full[
        ["Date", "Sovereign", "Agency", "Rating", "Outlook",
         "rating_num", "outlook_num", "rating_prev", "outlook_prev",
         "CCR_state", "CCR_prev", "dCCR", "dRating", "dOutlook"]
    ]


def build_event_panel() -> pd.DataFrame:
    sp = build_sp_events()
    md = build_moody_events()
    events = pd.concat([sp, md], ignore_index=True)
    events = events[(events["Date"] >= START) & (events["Date"] <= END)]
    events["Type"] = np.where(events["dCCR"] > 0, "Positive", "Negative")
    events["EventClass"] = np.select(
        [
            (events["dRating"].abs() > 0) & (events["dOutlook"].abs() > 0),
            events["dRating"].abs() > 0,
            events["dOutlook"].abs() > 0,
        ],
        ["Rating+Outlook", "Rating", "Outlook"],
        default="Other",
    )
    events.to_parquet(OUT / "events.parquet", index=False)

    cds = build_cds_panel()
    keep = [c for c in cds.columns if c.startswith(("adj_", "abs_", "pct_", "market_", "Spread"))] + ["EMU"]
    merged = events.merge(
        cds[["Date", "Sovereign"] + keep],
        on=["Date", "Sovereign"], how="left",
    )

    # If an event lands on a non-trading day, snap forward to the next
    # available CDS quote (within 5 calendar days). This avoids losing events
    # to weekend/holiday timing.
    miss = merged["Spread_clean"].isna()
    if miss.any():
        cds_idx = cds.set_index(["Sovereign", "Date"]).sort_index()
        for i in merged.index[miss]:
            sov = merged.at[i, "Sovereign"]
            d = merged.at[i, "Date"]
            for off in range(1, 6):
                d2 = d + pd.Timedelta(days=off)
                if (sov, d2) in cds_idx.index:
                    row = cds_idx.loc[(sov, d2)]
                    for c in keep:
                        merged.at[i, c] = row.get(c, np.nan)
                    merged.at[i, "Date"] = d2
                    break

    # Investment-grade dummies on the *prior* state (avoid look-ahead bias).
    merged["InvGrade_prior"] = (merged["rating_prev"] >= 12).astype(int)

    # Confounded-event flag: any other rating event by either agency on the
    # same country within +/- 1 *trading* day. Calendar-day adjacency would
    # miss Friday/Monday pairs.
    trading_days = (
        cds.sort_values(["Sovereign", "Date"])
        .groupby("Sovereign")["Date"]
        .apply(lambda s: pd.DatetimeIndex(sorted(s.unique())))
        .to_dict()
    )

    def _trading_pos(sov: str, d: pd.Timestamp) -> int | None:
        idx = trading_days.get(sov)
        if idx is None or len(idx) == 0:
            return None
        pos = idx.get_indexer([d], method="bfill")[0]
        return int(pos) if pos != -1 else None

    e2 = events.copy()
    e2["td_pos"] = [_trading_pos(s, d) for s, d in zip(e2["Sovereign"], e2["Date"])]
    merged["td_pos"] = [_trading_pos(s, d) for s, d in zip(merged["Sovereign"], merged["Date"])]
    by_sov_pos: dict[tuple[str, int], int] = {}
    for sov, pos in zip(e2["Sovereign"], e2["td_pos"]):
        if pos is None:
            continue
        by_sov_pos[(sov, pos)] = by_sov_pos.get((sov, pos), 0) + 1
    confound = []
    for sov, pos in zip(merged["Sovereign"], merged["td_pos"]):
        if pos is None:
            confound.append(False)
            continue
        n = (
            by_sov_pos.get((sov, pos - 1), 0)
            + by_sov_pos.get((sov, pos), 0)
            + by_sov_pos.get((sov, pos + 1), 0)
        )
        confound.append(n > 1)
    merged["Confounded_self"] = confound
    merged = merged.drop(columns=["td_pos"])

    # Crisis / post-Draghi regime split: 2012-07-26 = "whatever it takes".
    merged["PostDraghi"] = (merged["Date"] >= pd.Timestamp("2012-07-26")).astype(int)

    merged.to_parquet(OUT / "event_panel.parquet", index=False)
    return merged


if __name__ == "__main__":
    panel = build_event_panel()
    print(f"CDS panel rows: {pd.read_parquet(OUT/'cds_panel.parquet').shape[0]:,}")
    print(f"Events: {pd.read_parquet(OUT/'events.parquet').shape[0]:,}")
    print(f"Event panel rows: {panel.shape[0]:,}")
    print(panel[["Type", "Agency"]].value_counts().to_string())
