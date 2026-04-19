// Auto-generated. Do not edit by hand.

#let table_descriptive() = [
#figure(
  caption: [Summary statistics of daily CDS spreads and one-day percent changes by sovereign, 2010-2017.],
  table(
    columns: 7,
    align: (left, right, right, right, right, right, right),
    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else if y == 1 { (bottom: 0.3pt) } else { none },
    table.header[*Sovereign*][*EMU*][*N*][*Mean*][*Std. dev.*][*Min*][*Max*],
    [Austria], [Yes], [1,978], [36.9], [33.7], [7.3], [159.2],
    [Belgium], [Yes], [2,080], [66.8], [64.0], [9.5], [342.0],
    [Cyprus], [Yes], [2,014], [524.2], [400.3], [91.1], [1,674.2],
    [Estonia], [Yes], [1,879], [75.1], [27.3], [42.9], [201.0],
    [France], [Yes], [1,936], [47.9], [34.0], [7.7], [171.6],
    [Germany], [Yes], [1,871], [21.8], [15.4], [5.1], [79.3],
    [Greece], [Yes], [751], [1,887.6], [2,642.0], [229.2], [14,911.7],
    [Ireland], [Yes], [2,074], [204.7], [236.6], [15.1], [1,191.2],
    [Italy], [Yes], [2,086], [161.2], [99.7], [57.8], [498.7],
    [Latvia], [Yes], [1,942], [153.0], [111.0], [45.5], [573.0],
    [Lithuania], [Yes], [1,948], [138.3], [83.9], [47.6], [349.0],
    [Portugal], [Yes], [2,053], [358.3], [305.3], [50.0], [1,521.5],
    [Slovakia], [Yes], [1,934], [84.2], [63.4], [35.8], [285.1],
    [Slovenia], [Yes], [1,821], [164.9], [104.3], [48.0], [448.7],
    [Spain], [Yes], [2,086], [147.5], [105.9], [24.1], [492.1],
    [Bulgaria], [No], [1,916], [172.6], [74.3], [82.0], [400.0],
    [Croatia], [No], [2,057], [273.1], [84.6], [102.7], [559.7],
    [Czech], [No], [1,996], [64.4], [30.2], [34.9], [177.9],
    [Denmark], [No], [1,752], [33.0], [33.4], [7.4], [147.1],
    [Hungary], [No], [2,006], [235.4], [121.2], [82.4], [661.2],
    [Iceland], [No], [1,893], [200.8], [101.1], [82.3], [663.4],
    [Poland], [No], [1,986], [100.2], [51.8], [44.5], [300.9],
    [Romania], [No], [1,876], [198.3], [96.7], [85.6], [438.4],
    [Sweden], [No], [1,702], [22.1], [14.8], [6.9], [75.7],
    [United Kingdom], [No], [2,053], [39.4], [20.6], [11.7], [95.0],
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
    [S&P], [Negative], [All], [55], [10.88\*\*], [0.98], [0.039], [0.331], [[3.3, 24.7]],
    [S&P], [Negative], [EMU], [38], [13.01\*], [-1.37], [0.076], [0.518], [[2.9, 33.5]],
    [S&P], [Negative], [Non-EMU], [17], [6.11], [2.03], [0.237], [0.159], [[-0.5, 21.2]],
    [S&P], [Negative], [PreDraghi], [32], [12.76\*], [2.60], [0.074], [0.246], [[2.8, 32.9]],
    [S&P], [Negative], [PostDraghi], [23], [8.26], [0.21], [0.304], [0.800], [[-0.5, 39.3]],
    [S&P], [Positive], [All], [70], [-3.15\*\*\*], [-2.33\*\*\*], [0.004], [0.009], [[-5.5, -1.3]],
    [S&P], [Positive], [EMU], [49], [-2.86\*\*], [-1.37\*], [0.042], [0.080], [[-6.0, -0.6]],
    [S&P], [Positive], [Non-EMU], [21], [-3.83\*\*], [-3.05\*\*], [0.015], [0.024], [[-6.5, -1.2]],
    [S&P], [Positive], [PreDraghi], [15], [-7.18\*\*], [-6.08\*\*], [0.023], [0.012], [[-13.6, -2.5]],
    [S&P], [Positive], [PostDraghi], [55], [-2.05\*], [-0.78], [0.057], [0.150], [[-4.3, -0.2]],
    [Moody], [Negative], [All], [56], [16.53\*\*\*], [3.63\*\*\*], [0.009], [0.007], [[7.6, 33.4]],
    [Moody], [Negative], [EMU], [42], [20.36\*\*], [4.31\*\*], [0.015], [0.021], [[8.4, 40.6]],
    [Moody], [Negative], [Non-EMU], [14], [5.02], [3.11], [0.202], [0.135], [[-1.3, 12.8]],
    [Moody], [Negative], [PreDraghi], [41], [21.33\*\*], [5.74\*\*\*], [0.013], [0.009], [[9.2, 43.4]],
    [Moody], [Negative], [PostDraghi], [15], [3.40], [1.76], [0.283], [0.330], [[-0.3, 13.0]],
    [Moody], [Positive], [All], [43], [-1.74], [-0.18], [0.261], [0.491], [[-5.3, 0.6]],
    [Moody], [Positive], [EMU], [31], [-2.27], [-0.20], [0.277], [0.433], [[-7.5, 0.9]],
    [Moody], [Positive], [Non-EMU], [12], [-0.36], [0.14], [0.806], [0.970], [[-3.0, 2.4]],
    [Moody], [Positive], [PreDraghi], [4], [--], [--], [--], [--], [[--, --]],
    [Moody], [Positive], [PostDraghi], [39], [-1.23], [-0.02], [0.423], [0.725], [[-5.4, 1.0]],
    [All], [Negative], [All], [111], [13.73\*\*\*], [2.10\*\*], [0.001], [0.011], [[7.4, 23.6]],
    [All], [Negative], [EMU], [80], [16.87\*\*\*], [1.92\*\*], [0.002], [0.048], [[8.3, 30.4]],
    [All], [Negative], [Non-EMU], [31], [5.62\*], [2.53\*\*], [0.085], [0.037], [[0.8, 13.9]],
    [All], [Negative], [PreDraghi], [73], [17.57\*\*\*], [5.23\*\*], [0.002], [0.010], [[8.9, 31.6]],
    [All], [Negative], [PostDraghi], [38], [6.34], [1.05], [0.201], [0.396], [[0.7, 24.2]],
    [All], [Positive], [All], [113], [-2.61\*\*\*], [-0.92\*\*\*], [0.003], [0.009], [[-4.5, -1.2]],
    [All], [Positive], [EMU], [80], [-2.63\*\*], [-0.65\*], [0.024], [0.063], [[-5.2, -0.7]],
    [All], [Positive], [Non-EMU], [33], [-2.57\*\*], [-1.03\*\*], [0.024], [0.048], [[-4.7, -0.5]],
    [All], [Positive], [PreDraghi], [19], [-7.07\*\*], [-6.08\*\*], [0.014], [0.011], [[-12.6, -2.7]],
    [All], [Positive], [PostDraghi], [94], [-1.71\*], [-0.22], [0.055], [0.168], [[-3.8, -0.2]],
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
    [S&P], [Negative], [Rating], [24], [28.53\*\*], [10.50],
    [S&P], [Negative], [Outlook], [16], [-1.64], [-1.59],
    [S&P], [Negative], [Rating+Outlook], [15], [-4.02\*], [-3.38],
    [S&P], [Positive], [Rating], [17], [-3.29], [-2.68],
    [S&P], [Positive], [Outlook], [38], [-2.56\*], [-1.51],
    [S&P], [Positive], [Rating+Outlook], [15], [-4.49\*], [-3.16],
    [Moody], [Negative], [Rating], [26], [19.79\*\*], [5.90],
    [Moody], [Negative], [Outlook], [14], [-0.56], [-1.26],
    [Moody], [Negative], [Rating+Outlook], [16], [26.19], [6.12],
    [Moody], [Positive], [Rating], [8], [-4.18\*\*], [-2.58],
    [Moody], [Positive], [Outlook], [26], [-2.09], [0.09],
    [Moody], [Positive], [Rating+Outlook], [9], [1.46], [0.68],
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
    [S&P], [Negative], [55], [-15.17\*], [8.19], [0.064], [0.397],
    [S&P], [Positive], [70], [-4.79\*], [2.64], [0.070], [0.251],
    [Moody], [Negative], [56], [-4.59], [12.28], [0.709], [0.252],
    [Moody], [Positive], [43], [1.86], [4.76], [0.697], [0.266],
    [All], [Negative], [111], [-9.13], [7.29], [0.210], [0.256],
    [All], [Positive], [113], [-1.22], [1.57], [0.436], [0.134],
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
    [[-30,-1]], [S&P], [Negative], [56], [-0.30], [-3.67], [0.984],
    [[-30,-1]], [S&P], [Positive], [63], [-4.88], [-2.45], [0.379],
    [[-30,-1]], [Moody], [Negative], [56], [12.17], [7.72], [0.442],
    [[-30,-1]], [Moody], [Positive], [39], [-10.35], [-0.86], [0.170],
    [[-30,-1]], [All], [Negative], [112], [5.93], [6.40], [0.590],
    [[-30,-1]], [All], [Positive], [102], [-6.97], [-1.62], [0.117],
    [[-60,-31]], [S&P], [Negative], [56], [11.94], [-3.26], [0.437],
    [[-60,-31]], [S&P], [Positive], [64], [-5.12], [0.38], [0.505],
    [[-60,-31]], [Moody], [Negative], [58], [-32.12], [2.26], [0.397],
    [[-60,-31]], [Moody], [Positive], [42], [-17.95\*\*], [-4.75], [0.017],
    [[-60,-31]], [All], [Negative], [114], [-10.48], [-2.91], [0.612],
    [[-60,-31]], [All], [Positive], [106], [-10.20\*], [-1.46], [0.063],
    [[-90,-61]], [S&P], [Negative], [51], [-18.82], [-9.93], [0.194],
    [[-90,-61]], [S&P], [Positive], [68], [-4.96], [-1.97], [0.434],
    [[-90,-61]], [Moody], [Negative], [55], [92.86], [3.97], [0.261],
    [[-90,-61]], [Moody], [Positive], [40], [-5.48\*], [-0.59], [0.097],
    [[-90,-61]], [All], [Negative], [106], [39.12], [0.22], [0.367],
    [[-90,-61]], [All], [Positive], [108], [-5.15], [-1.68], [0.215],
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
    [Positive], [M1], [2151], [115], [-2.922\*\*\*], [0.00022\*\*\*], [--], [0.0073],
    [Positive], [M2], [2151], [115], [-2.907\*\*\*], [--], [0.00016\*\*], [0.0036],
    [Positive], [M3], [2151], [115], [-2.918\*\*\*], [0.00049\*\*\*], [-0.00031], [0.0102],
    [Negative], [M1], [2166], [91], [-3.133\*\*\*], [0.00004], [--], [0.0002],
    [Negative], [M2], [2166], [91], [-3.146\*\*\*], [--], [0.00010], [0.0012],
    [Negative], [M3], [2166], [91], [-3.152\*\*\*], [-0.00060\*], [0.00065\*\*], [0.0052],
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
    [Event ΔCCR], [0.0005], [0.0006], [0.0039\*], [0.0029], [0.0009], [-0.0001], [-0.0008], [-0.0034\*\*],
    [Prior-month event mass], [--], [-0.0005], [-0.0001], [0.0004], [--], [-0.0019], [-0.0023], [-0.0024],
    [Both inv-grade], [--], [--], [0.0143], [0.0148], [--], [--], [0.0034], [0.0035],
    [ΔCCR × InvBoth], [--], [--], [-0.0078], [-0.0084], [--], [--], [0.0024], [0.0027],
    [Both EMU], [--], [--], [--], [-0.0130], [--], [--], [--], [-0.0052],
    [ΔCCR × EmuBoth], [--], [--], [--], [0.0035], [--], [--], [--], [0.0045\*\*\*],
    [N], [2263], [2263], [2263], [2263], [2417], [2417], [2417], [2417],
    [R²], [0.054], [0.054], [0.061], [0.067], [0.053], [0.056], [0.058], [0.060],
  )
) <tab:spillover>
]
