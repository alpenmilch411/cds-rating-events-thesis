"""Render tables as Typst snippets for the thesis to import.

Produces output/tables/tables.typ which exposes named functions returning
ready-to-place Typst content (#table(...) blocks). The thesis.typ then does
e.g. `#tab.table_short_run()`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
OUT = ROOT / "output" / "tables"
OUT.mkdir(parents=True, exist_ok=True)


def stars(p: float) -> str:
    """Significance stars escaped for Typst content blocks."""
    if pd.isna(p):
        return ""
    if p < 0.01:
        return r"\*\*\*"
    if p < 0.05:
        return r"\*\*"
    if p < 0.10:
        return r"\*"
    return ""


def fmt(x: float, dp: int = 2) -> str:
    if pd.isna(x):
        return "--"
    return f"{x:,.{dp}f}"


def render_descriptive(rows: list[dict]) -> str:
    """Table 1: descriptive statistics."""
    df = pd.DataFrame(rows).sort_values(["EMU", "Sovereign"], ascending=[False, True])
    lines = ["#figure(", "  caption: [Summary statistics of daily CDS spreads and one-day percent changes by sovereign, 2010-2017.],",
             "  table(",
             "    columns: 7,",
             "    align: (left, right, right, right, right, right, right),",
             "    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },",
             "    table.header[*Sovereign*][*EMU*][*N*][*Mean*][*Std. dev.*][*Min*][*Max*],"]
    for _, r in df.iterrows():
        emu = "Yes" if r["EMU"] == 1 else "No"
        lines.append(f"    [{r['Sovereign']}], [{emu}], [{int(r['count']):,}], [{fmt(r['mean'],1)}], [{fmt(r['std'],1)}], [{fmt(r['min'],1)}], [{fmt(r['max'],1)}],")
    lines += ["  )", ") <tab:descriptive>"]
    return "\n".join(lines)


def render_short_run(rows: list[dict]) -> str:
    df = pd.DataFrame(rows)
    lines = ["#figure(",
             "  caption: [Mean and median two-day adjusted CDS spread changes around rating events. Adjusted spread change is the country's two-day spread change minus the equivalent change of a leave-one-out cross-sectional benchmark. p-values are from the one-sample t-test (mean) and Wilcoxon signed-rank test (median); asterisks denote significance at the 10, 5 and 1 percent levels (one, two, three asterisks).],",
             "  table(",
             "    columns: 9,",
             "    align: (left, left, left, right, right, right, right, right, right),",
             "    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },",
             "    table.header[*Agency*][*Sign*][*Split*][*N*][*Mean (bps)*][*Median (bps)*][*p (mean)*][*p (median)*][*BCa 95% CI*],"]
    order = [("S&P","Negative"),("S&P","Positive"),("Moody","Negative"),("Moody","Positive"),("All","Negative"),("All","Positive")]
    splits = ["All", "EMU", "Non-EMU", "PreDraghi", "PostDraghi"]
    for ag, sign in order:
        for sp in splits:
            sub = df[(df["agency"] == ag) & (df["sign"] == sign) & (df["split"] == sp)]
            if sub.empty:
                continue
            r = sub.iloc[0]
            ci = "[" + fmt(r["ci_lo"], 1) + ", " + fmt(r["ci_hi"], 1) + "]"
            lines.append(f"    [{ag}], [{sign}], [{sp}], [{int(r['n'])}], [{fmt(r['mean'],2)}{stars(r['p_t'])}], [{fmt(r['median'],2)}{stars(r['p_w'])}], [{fmt(r['p_t'],3)}], [{fmt(r['p_w'],3)}], [{ci}],")
    lines += ["  )", ") <tab:short_run>"]
    return "\n".join(lines)


def render_event_class(rows: list[dict]) -> str:
    df = pd.DataFrame(rows)
    lines = ["#figure(",
             "  caption: [Mean and median two-day adjusted spread changes by event sub-type. Rating-only events are pure rating-notch changes; outlook-only events are pure outlook revisions; combined events are days when both occur.],",
             "  table(",
             "    columns: 6,",
             "    align: (left, left, left, right, right, right),",
             "    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },",
             "    table.header[*Agency*][*Sign*][*Sub-type*][*N*][*Mean (bps)*][*Median (bps)*],"]
    for ag in ["S&P", "Moody"]:
        for sign in ["Negative", "Positive"]:
            for cls in ["Rating", "Outlook", "Rating+Outlook"]:
                sub = df[(df["agency"] == ag) & (df["sign"] == sign) & (df["class"] == cls)]
                if sub.empty:
                    continue
                r = sub.iloc[0]
                lines.append(f"    [{ag}], [{sign}], [{cls}], [{int(r['n'])}], [{fmt(r.get('mean',float('nan')),2)}{stars(r.get('p_t', float('nan')))}], [{fmt(r.get('median',float('nan')),2)}],")
    lines += ["  )", ") <tab:by_class>"]
    return "\n".join(lines)


def render_panel(rows: list[dict]) -> str:
    df = pd.DataFrame(rows)
    df = df[df["window"] == "adj_abs_chg_-1_1"]
    lines = ["#figure(",
             "  caption: [Country fixed-effects panel regressions of the two-day adjusted spread change on the change in comprehensive credit rating (CCR). Standard errors are two-way clustered by sovereign and trading day.],",
             "  table(",
             "    columns: 7,",
             "    align: (left, left, right, right, right, right, right),",
             "    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },",
             "    table.header[*Agency*][*Sign*][*N*][*Coef. on dCCR*][*Cluster SE*][*p-value*][*R²*],"]
    order = [("S&P","neg"),("S&P","pos"),("Moody","neg"),("Moody","pos"),("All","neg"),("All","pos")]
    for ag, sign in order:
        sub = df[(df["agency"] == ag) & (df["sign"] == sign)]
        if sub.empty:
            continue
        r = sub.iloc[0]
        sign_word = "Negative" if sign == "neg" else "Positive"
        lines.append(f"    [{ag}], [{sign_word}], [{int(r['n'])}], [{fmt(r['coef'],2)}{stars(r['p'])}], [{fmt(r['se'],2)}], [{fmt(r['p'],3)}], [{fmt(r['r2'],3)}],")
    lines += ["  )", ") <tab:panel_reg>"]
    return "\n".join(lines)


def render_anticipation(rows: list[dict]) -> str:
    df = pd.DataFrame(rows)
    lines = ["#figure(",
             "  caption: [Mean and median adjusted spread changes in the months prior to a rating event. Each row reports the cross-event mean of the within-window adjusted spread change.],",
             "  table(",
             "    columns: 7,",
             "    align: (left, left, left, right, right, right, right),",
             "    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },",
             "    table.header[*Window*][*Agency*][*Sign*][*N*][*Mean (bps)*][*Median (bps)*][*p (mean)*],"]
    for win in ["[-30,-1]", "[-60,-31]", "[-90,-61]"]:
        for ag in ["S&P", "Moody", "All"]:
            for sign in ["Negative", "Positive"]:
                sub = df[(df["window"] == win) & (df["agency"] == ag) & (df["sign"] == sign)]
                if sub.empty:
                    continue
                r = sub.iloc[0]
                lines.append(f"    [{win}], [{ag}], [{sign}], [{int(r['n'])}], [{fmt(r['mean'],2)}{stars(r['p_t'])}], [{fmt(r['median'],2)}], [{fmt(r['p_t'],3)}],")
    lines += ["  )", ") <tab:anticipation>"]
    return "\n".join(lines)


def render_logit(d: dict) -> str:
    lines = ["#figure(",
             "  caption: [Logistic regression: probability that a sovereign-month contains a rating event of the given sign as a function of past leave-one-out adjusted spread changes. Pseudo-R² is the McFadden value.],",
             "  table(",
             "    columns: 8,",
             "    align: (left, left, right, right, right, right, right, right),",
             "    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },",
             "    table.header[*Sign*][*Model*][*N*][*Events*][*Const.*][*$beta_(\"[-60,-31]\")$*][*$beta_(\"[-90,-61]\")$*][*Pseudo R²*],"]
    for sign in ["positive", "negative"]:
        for m in ["M1", "M2", "M3"]:
            r = d.get(sign, {}).get(m, {})
            if not r or "params" not in r:
                continue
            params = r["params"]
            const = params.get("const", {}).get("coef", float("nan"))
            constp = params.get("const", {}).get("p", float("nan"))
            w1 = params.get("w1", {}).get("coef", float("nan"))
            w1p = params.get("w1", {}).get("p", float("nan"))
            w2 = params.get("w2", {}).get("coef", float("nan"))
            w2p = params.get("w2", {}).get("p", float("nan"))
            lines.append(
                f"    [{sign.title()}], [{m}], [{int(r['n'])}], [{int(r['events'])}], "
                f"[{fmt(const,3)}{stars(constp)}], "
                f"[{fmt(w1,5) if w1==w1 else '--'}{stars(w1p)}], "
                f"[{fmt(w2,5) if w2==w2 else '--'}{stars(w2p)}], "
                f"[{fmt(r['pseudo_r2'],4)}],"
            )
    lines += ["  )", ") <tab:logit>"]
    return "\n".join(lines)


def render_spillover(d: dict) -> str:
    lines = ["#figure(",
             "  caption: [Pooled OLS regressions of two-day percentage CDS spread changes for non-event countries on the absolute aggregate CCR change of event countries. Each column adds further controls; standard errors are two-way clustered by event country and event date. Sovereigns with a t-1 spread below 25 bps are excluded to avoid the small-denominator bias.],",
             "  table(",
             "    columns: 9,",
             "    align: (left, right, right, right, right, right, right, right, right),",
             "    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },",
             "    table.header[*Variable*][*Pos M1*][*Pos M2*][*Pos M3*][*Pos M4*][*Neg M1*][*Neg M2*][*Neg M3*][*Neg M4*],"]
    rows_out = []
    var_order = ["CCR_event", "PriorEvent", "InvBoth", "CCR_x_InvBoth", "EmuBoth", "CCR_x_EmuBoth"]
    var_labels = {"CCR_event": "Event ΔCCR", "PriorEvent": "Prior-month event mass",
                  "InvBoth": "Both inv-grade", "CCR_x_InvBoth": "ΔCCR × InvBoth",
                  "EmuBoth": "Both EMU", "CCR_x_EmuBoth": "ΔCCR × EmuBoth"}
    pos = d.get("pos", {}); neg = d.get("neg", {})
    for v in var_order:
        cells = [f"[{var_labels[v]}]"]
        for sign_grp in [pos, neg]:
            for m in ["m1", "m2", "m3", "m4"]:
                r = sign_grp.get(m, {}).get(v)
                if r is None:
                    cells.append("[--]")
                else:
                    cells.append(f"[{fmt(r['coef'],4)}{stars(r['p'])}]")
        rows_out.append(", ".join(cells) + ",")
    lines += ["    " + r for r in rows_out]
    # N row
    n_cells = ["[N]"]
    for sign_grp in [pos, neg]:
        for m in ["m1","m2","m3","m4"]:
            n_cells.append(f"[{int(sign_grp.get(m, {}).get('n', 0))}]")
    lines.append("    " + ", ".join(n_cells) + ",")
    # R2 row
    r_cells = ["[R²]"]
    for sign_grp in [pos, neg]:
        for m in ["m1","m2","m3","m4"]:
            r_cells.append(f"[{fmt(sign_grp.get(m, {}).get('r2', float('nan')), 3)}]")
    lines.append("    " + ", ".join(r_cells) + ",")

    lines += ["  )", ") <tab:spillover>"]
    return "\n".join(lines)


def main():
    res = json.load(open(PROC / "results.json"))
    chunks = [
        "// Auto-generated. Do not edit by hand.",
        "",
        "#let table_descriptive() = [",
        render_descriptive(res["table1_descriptive"]),
        "]",
        "",
        "#let table_short_run() = [",
        render_short_run(res["table_short_run"]),
        "]",
        "",
        "#let table_event_class() = [",
        render_event_class(res["table_by_class"]),
        "]",
        "",
        "#let table_panel_reg() = [",
        render_panel(res["table_panel_reg"]),
        "]",
        "",
        "#let table_anticipation() = [",
        render_anticipation(res["table_anticipation"]),
        "]",
        "",
        "#let table_logit() = [",
        render_logit(res["table_logit"]),
        "]",
        "",
        "#let table_spillover() = [",
        render_spillover(res["table_spillover"]),
        "]",
        "",
    ]
    out_path = OUT / "tables.typ"
    out_path.write_text("\n".join(chunks))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
