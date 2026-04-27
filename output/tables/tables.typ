// Auto-generated. Do not edit by hand.

#let table_descriptive() = [
#figure(
  caption: [Summary statistics of daily CDS spreads and one-day percent changes by sovereign, 2010-2017.],
  table(
    columns: 7,
    align: (left, right, right, right, right, right, right),
    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },
    table.header[*Sovereign*][*EMU*][*N*][*Mean*][*Std. dev.*][*Min*][*Max*],
    [Austria], [Yes], [1,936], [36.7], [33.9], [7.3], [159.2],
    [Belgium], [Yes], [2,074], [66.9], [64.0], [9.5], [342.0],
    [Cyprus], [Yes], [1,978], [529.4], [402.0], [91.1], [1,674.2],
    [Estonia], [Yes], [1,732], [75.1], [27.6], [42.9], [201.0],
    [France], [Yes], [1,819], [49.4], [34.4], [7.7], [171.6],
    [Germany], [Yes], [1,715], [22.8], [15.6], [5.1], [79.3],
    [Greece], [Yes], [736], [1,836.7], [2,523.9], [229.2], [14,911.7],
    [Ireland], [Yes], [2,059], [205.8], [237.1], [15.1], [1,191.2],
    [Italy], [Yes], [2,086], [161.2], [99.7], [57.8], [498.7],
    [Latvia], [Yes], [1,855], [154.3], [112.0], [45.5], [573.0],
    [Lithuania], [Yes], [1,855], [139.5], [84.3], [47.6], [349.0],
    [Portugal], [Yes], [2,044], [356.6], [303.6], [50.0], [1,521.5],
    [Slovakia], [Yes], [1,826], [85.1], [65.0], [35.8], [285.1],
    [Slovenia], [Yes], [1,674], [170.8], [105.7], [52.0], [448.7],
    [Spain], [Yes], [2,086], [147.5], [105.9], [24.1], [492.1],
    [Bulgaria], [No], [1,820], [174.5], [74.6], [82.0], [400.0],
    [Croatia], [No], [2,039], [273.1], [84.8], [102.7], [559.7],
    [Czech], [No], [1,927], [64.5], [30.5], [34.9], [177.9],
    [Denmark], [No], [1,581], [34.9], [34.7], [7.4], [147.1],
    [Hungary], [No], [1,949], [237.6], [120.5], [82.4], [661.2],
    [Iceland], [No], [1,836], [204.0], [100.9], [82.3], [663.4],
    [Poland], [No], [1,899], [101.6], [52.5], [44.5], [300.9],
    [Romania], [No], [1,798], [202.1], [96.8], [85.6], [438.4],
    [Sweden], [No], [1,516], [23.4], [15.2], [6.9], [75.7],
    [United Kingdom], [No], [2,041], [39.6], [20.6], [12.3], [95.0],
  )
) <tab:descriptive>
]

#let table_short_run() = [
#figure(
  caption: [Mean and median two-day adjusted CDS spread changes around rating events. Adjusted spread change is the country's two-day spread change minus the equivalent change of a leave-one-out cross-sectional benchmark. p-values are from the one-sample t-test (mean) and Wilcoxon signed-rank test (median); asterisks denote significance at the 10, 5 and 1 percent levels (one, two, three asterisks).],
  table(
    columns: 9,
    align: (left, left, left, right, right, right, right, right, right),
    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },
    table.header[*Agency*][*Sign*][*Split*][*N*][*Mean (bps)*][*Median (bps)*][*p (mean)*][*p (median)*][*BCa 95% CI*],
    [S&P], [Negative], [All], [53], [11.96\*\*], [0.98], [0.033], [0.259], [[3.7, 27.1]],
    [S&P], [Negative], [EMU], [38], [13.72\*], [-0.94], [0.069], [0.405], [[3.4, 34.8]],
    [S&P], [Negative], [Non-EMU], [15], [7.49], [2.53], [0.182], [0.151], [[0.9, 26.2]],
    [S&P], [Negative], [PreDraghi], [31], [14.00\*], [3.49], [0.068], [0.239], [[3.2, 33.3]],
    [S&P], [Negative], [PostDraghi], [22], [9.08], [0.60], [0.279], [0.656], [[0.0, 42.1]],
    [S&P], [Positive], [All], [67], [-5.05\*\*\*], [-3.05\*\*\*], [0.001], [0.001], [[-8.1, -2.7]],
    [S&P], [Positive], [EMU], [47], [-5.03\*\*\*], [-1.54\*\*], [0.009], [0.018], [[-9.5, -2.0]],
    [S&P], [Positive], [Non-EMU], [20], [-5.11\*\*\*], [-3.09\*\*], [0.009], [0.014], [[-8.8, -2.2]],
    [S&P], [Positive], [PreDraghi], [13], [-11.20\*\*\*], [-9.71\*\*\*], [0.003], [0.002], [[-18.0, -6.2]],
    [S&P], [Positive], [PostDraghi], [54], [-3.57\*\*], [-0.58\*], [0.021], [0.069], [[-7.3, -1.1]],
    [Moody], [Negative], [All], [55], [20.11\*\*\*], [3.95\*\*\*], [0.006], [0.008], [[9.1, 37.7]],
    [Moody], [Negative], [EMU], [42], [25.06\*\*\*], [5.03\*\*\*], [0.009], [0.009], [[11.5, 48.5]],
    [Moody], [Negative], [Non-EMU], [13], [4.09], [1.02], [0.329], [0.414], [[-2.1, 13.4]],
    [Moody], [Negative], [PreDraghi], [41], [25.89\*\*\*], [5.74\*\*\*], [0.008], [0.008], [[11.9, 50.3]],
    [Moody], [Negative], [PostDraghi], [14], [3.18], [1.10], [0.357], [0.426], [[-0.9, 13.5]],
    [Moody], [Positive], [All], [41], [-1.80], [-0.83], [0.300], [0.124], [[-5.4, 1.1]],
    [Moody], [Positive], [EMU], [29], [-1.96], [-1.18], [0.421], [0.198], [[-7.1, 2.2]],
    [Moody], [Positive], [Non-EMU], [12], [-1.40], [0.13], [0.179], [0.622], [[-3.7, 0.1]],
    [Moody], [Positive], [PreDraghi], [4], [--], [--], [--], [--], [[--, --]],
    [Moody], [Positive], [PostDraghi], [37], [-1.09], [-0.73], [0.545], [0.281], [[-5.1, 2.0]],
    [All], [Negative], [All], [108], [16.11\*\*\*], [2.09\*\*\*], [0.001], [0.009], [[8.6, 26.6]],
    [All], [Negative], [EMU], [80], [19.68\*\*\*], [2.51\*\*], [0.001], [0.024], [[10.2, 34.1]],
    [All], [Negative], [Non-EMU], [28], [5.91\*], [2.07\*], [0.091], [0.099], [[1.0, 14.9]],
    [All], [Negative], [PreDraghi], [72], [20.77\*\*\*], [5.03\*\*\*], [0.001], [0.009], [[10.4, 35.8]],
    [All], [Negative], [PostDraghi], [36], [6.78], [1.00], [0.195], [0.379], [[0.8, 27.0]],
    [All], [Positive], [All], [108], [-3.82\*\*\*], [-1.37\*\*\*], [0.001], [0.000], [[-6.2, -1.9]],
    [All], [Positive], [EMU], [76], [-3.86\*\*], [-1.37\*\*\*], [0.010], [0.009], [[-7.2, -1.4]],
    [All], [Positive], [Non-EMU], [32], [-3.72\*\*\*], [-1.24\*\*], [0.004], [0.014], [[-6.5, -1.7]],
    [All], [Positive], [PreDraghi], [17], [-10.51\*\*\*], [-9.67\*\*\*], [0.001], [0.001], [[-16.1, -6.1]],
    [All], [Positive], [PostDraghi], [91], [-2.57\*\*], [-0.66\*\*], [0.029], [0.038], [[-5.2, -0.5]],
  )
) <tab:short_run>
]

#let table_event_class() = [
#figure(
  caption: [Mean and median two-day adjusted spread changes by event sub-type. Rating-only events are pure rating-notch changes; outlook-only events are pure outlook revisions; combined events are days when both occur.],
  table(
    columns: 6,
    align: (left, left, left, right, right, right),
    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },
    table.header[*Agency*][*Sign*][*Sub-type*][*N*][*Mean (bps)*][*Median (bps)*],
    [S&P], [Negative], [Rating], [22], [32.60\*\*], [14.96],
    [S&P], [Negative], [Outlook], [16], [-1.07], [-1.60],
    [S&P], [Negative], [Rating+Outlook], [15], [-4.41\*], [-2.09],
    [S&P], [Positive], [Rating], [14], [-4.31], [-0.48],
    [S&P], [Positive], [Outlook], [38], [-5.55\*\*\*], [-3.09],
    [S&P], [Positive], [Rating+Outlook], [15], [-4.49], [-3.16],
    [Moody], [Negative], [Rating], [26], [19.20\*\*], [4.85],
    [Moody], [Negative], [Outlook], [13], [-0.40], [-1.11],
    [Moody], [Negative], [Rating+Outlook], [16], [38.24\*], [7.14],
    [Moody], [Positive], [Rating], [8], [-2.26], [0.03],
    [Moody], [Positive], [Outlook], [24], [-1.44], [-0.36],
    [Moody], [Positive], [Rating+Outlook], [9], [-2.34], [-1.77],
  )
) <tab:by_class>
]

#let table_panel_reg() = [
#figure(
  caption: [Country fixed-effects panel regressions of the two-day adjusted spread change on the change in comprehensive credit rating (CCR). Standard errors are two-way clustered by sovereign and trading day.],
  table(
    columns: 7,
    align: (left, left, right, right, right, right, right),
    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },
    table.header[*Agency*][*Sign*][*N*][*Coef. on dCCR*][*Cluster SE*][*p-value*][*R²*],
    [S&P], [Negative], [53], [-15.51\*], [8.93], [0.082], [0.373],
    [S&P], [Positive], [67], [-2.60], [3.37], [0.441], [0.205],
    [Moody], [Negative], [55], [-12.08], [16.50], [0.464], [0.247],
    [Moody], [Positive], [41], [-0.62], [4.83], [0.898], [0.479],
    [All], [Negative], [108], [-12.92], [8.70], [0.138], [0.258],
    [All], [Positive], [108], [-0.88], [1.60], [0.580], [0.093],
  )
) <tab:panel_reg>
]

#let table_anticipation() = [
#figure(
  caption: [Mean and median adjusted spread changes in the months prior to a rating event. Each row reports the cross-event mean of the within-window adjusted spread change.],
  table(
    columns: 7,
    align: (left, left, left, right, right, right, right),
    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },
    table.header[*Window*][*Agency*][*Sign*][*N*][*Mean (bps)*][*Median (bps)*][*p (mean)*],
    [[-30,-1]], [S&P], [Negative], [51], [1.98], [-4.22], [0.907],
    [[-30,-1]], [S&P], [Positive], [59], [-2.46], [-5.08], [0.674],
    [[-30,-1]], [Moody], [Negative], [55], [12.87], [9.90], [0.425],
    [[-30,-1]], [Moody], [Positive], [38], [-9.21], [0.37], [0.229],
    [[-30,-1]], [All], [Negative], [106], [7.63], [9.21], [0.512],
    [[-30,-1]], [All], [Positive], [97], [-5.11], [-2.35], [0.270],
    [[-60,-31]], [S&P], [Negative], [51], [9.28], [-13.07], [0.586],
    [[-60,-31]], [S&P], [Positive], [60], [-5.21], [0.36], [0.524],
    [[-60,-31]], [Moody], [Negative], [56], [-33.68], [-1.33], [0.391],
    [[-60,-31]], [Moody], [Positive], [40], [-18.22\*\*], [-2.08], [0.025],
    [[-60,-31]], [All], [Negative], [107], [-13.20], [-6.78], [0.548],
    [[-60,-31]], [All], [Positive], [100], [-10.42\*], [-0.74], [0.076],
    [[-90,-61]], [S&P], [Negative], [48], [-18.18], [-5.88], [0.240],
    [[-90,-61]], [S&P], [Positive], [63], [-1.55], [1.27], [0.818],
    [[-90,-61]], [Moody], [Negative], [53], [83.65], [3.65], [0.326],
    [[-90,-61]], [Moody], [Positive], [38], [-1.89], [-0.83], [0.577],
    [[-90,-61]], [All], [Negative], [101], [35.25], [-1.58], [0.435],
    [[-90,-61]], [All], [Positive], [101], [-1.68], [1.09], [0.700],
  )
) <tab:anticipation>
]

#let table_logit() = [
#figure(
  caption: [Logistic regression: probability that a sovereign-month contains a rating event of the given sign as a function of past leave-one-out adjusted spread changes. Pseudo-R² is the McFadden value.],
  table(
    columns: 8,
    align: (left, left, right, right, right, right, right, right),
    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },
    table.header[*Sign*][*Model*][*N*][*Events*][*Const.*][*$beta_("[-60,-31]")$*][*$beta_("[-90,-61]")$*][*Pseudo R²*],
    [Positive], [M1], [2149], [115], [-2.921\*\*\*], [0.00021\*\*\*], [--], [0.0073],
    [Positive], [M2], [2149], [115], [-2.907\*\*\*], [--], [0.00017\*\*], [0.0038],
    [Positive], [M3], [2149], [115], [-2.918\*\*\*], [0.00047\*\*], [-0.00028], [0.0095],
    [Negative], [M1], [2164], [91], [-3.133\*\*\*], [0.00004], [--], [0.0002],
    [Negative], [M2], [2164], [91], [-3.146\*\*\*], [--], [0.00011], [0.0013],
    [Negative], [M3], [2164], [91], [-3.151\*\*\*], [-0.00061\*], [0.00067\*\*], [0.0059],
  )
) <tab:logit>
]

#let table_spillover() = [
#figure(
  caption: [Pooled OLS regressions of two-day percentage CDS spread changes for non-event countries on the absolute aggregate CCR change of event countries. Each column adds further controls; standard errors are two-way clustered by event country and event date. Sovereigns with a t-1 spread below 25 bps are excluded to avoid the small-denominator bias.],
  table(
    columns: 9,
    align: (left, right, right, right, right, right, right, right, right),
    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },
    table.header[*Variable*][*Pos M1*][*Pos M2*][*Pos M3*][*Pos M4*][*Neg M1*][*Neg M2*][*Neg M3*][*Neg M4*],
    [Event ΔCCR], [-0.0019], [-0.0018], [0.0003], [0.0004], [0.0011], [0.0000], [-0.0010], [-0.0033\*\*],
    [Prior-month event mass], [--], [-0.0003], [-0.0000], [0.0005], [--], [-0.0022], [-0.0024], [-0.0025],
    [Both inv-grade], [--], [--], [0.0103], [0.0109], [--], [--], [0.0001], [0.0001],
    [ΔCCR × InvBoth], [--], [--], [-0.0041], [-0.0051], [--], [--], [0.0029], [0.0031],
    [Both EMU], [--], [--], [--], [-0.0133], [--], [--], [--], [-0.0032],
    [ΔCCR × EmuBoth], [--], [--], [--], [0.0017], [--], [--], [--], [0.0039\*\*],
    [N], [2200], [2200], [2200], [2200], [2396], [2396], [2396], [2396],
    [R²], [0.050], [0.050], [0.055], [0.063], [0.047], [0.051], [0.053], [0.054],
  )
) <tab:spillover>
]
