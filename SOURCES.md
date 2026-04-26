# Sources

This document lists the academic and policy sources that the thesis draws on, with DOIs or stable URLs and a one-line note on what was taken from each. The PDFs themselves are not included in this repository for copyright reasons; the references below should be sufficient to retrieve them.

## Methodological foundation

- **Ismailescu, I., & Kazemi, H. (2010).** The reaction of emerging market credit default swap spreads to sovereign credit rating changes. *Journal of Banking & Finance*, 34(12), 2861–2873. [doi:10.1016/j.jbankfin.2010.05.014](https://doi.org/10.1016/j.jbankfin.2010.05.014). The methodological template for the event study and the spillover regression. The redo applies their two-day window and adjusted-spread-change definition, but with the leave-one-out benchmark instead of the equally-weighted full-panel benchmark.
- **Afonso, A., Furceri, D., & Gomes, P. (2012).** Sovereign credit ratings and financial markets linkages: Application to European data. *Journal of International Money and Finance*, 31(3), 606–638. [doi:10.1016/j.jimonfin.2012.01.016](https://doi.org/10.1016/j.jimonfin.2012.01.016). The closest comparison study for European sovereigns. Their Lehman structural-break design motivates the pre-/post-Draghi split used in this redo.
- **Hull, J., Predescu, M., & White, A. (2004).** The relationship between credit default swap spreads, bond yields, and credit rating announcements. *Journal of Banking and Finance*, 28(11), 2789–2811. [doi:10.1016/j.jbankfin.2004.06.010](https://doi.org/10.1016/j.jbankfin.2004.06.010). The 5Y benchmark choice and the logistic prediction model are from this paper.
- **Norden, L., & Weber, M. (2004).** Informational efficiency of credit default swap and stock markets: The impact of credit rating announcements. *Journal of Banking & Finance*, 28(11), 2813–2843. [doi:10.1016/j.jbankfin.2004.06.011](https://doi.org/10.1016/j.jbankfin.2004.06.011). Used for the comparison of CDS vs. equity reactions and the rating-level dependence of event impact.
- **Norden, L. (2011).** Credit Derivatives, Corporate News, and Credit Ratings. *SSRN Electronic Journal*. [doi:10.2139/ssrn.1343012](https://doi.org/10.2139/ssrn.1343012). Used for the discussion of media coverage and private information channels.
- **Gande, A., & Parsley, D. C. (2005).** News spillovers in the sovereign debt market. *Journal of Financial Economics*, 75(3), 691–734. [doi:10.1016/j.jfineco.2003.11.003](https://doi.org/10.1016/j.jfineco.2003.11.003). Source of the comprehensive credit rating (CCR) construction and the sovereign-spillover specification.

## Statistical / econometric methods

- **Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2011).** Robust Inference With Multiway Clustering. *Journal of Business & Economic Statistics*, 29(2), 238–249. [doi:10.1198/jbes.2010.07136](https://doi.org/10.1198/jbes.2010.07136). The two-way clustered standard error correction used in every panel regression in this redo.
- **Efron, B., & Tibshirani, R. J. (1993).** *An Introduction to the Bootstrap.* Chapman & Hall, New York. The bias-corrected and accelerated (BCa) bootstrap construction used for the confidence intervals on the mean of the adjusted spread change.

## CDS market structure and regulation

- **Augustin, P., Subrahmanyam, M. G., Tang, D. Y., & Wang, S. Q. (2016).** Credit Default Swaps: Past, Present, and Future. *Annual Review of Financial Economics*, 8(1), 175–196. [doi:10.1146/annurev-financial-121415-032806](https://doi.org/10.1146/annurev-financial-121415-032806). Background on CDS market history and structure.
- **Linden, S. (2012).** The euro-area sovereign CDS market. *Quarterly Report on the Euro Area*, 11(1), 31–36. Background on euro-area sovereign CDS use cases (proxy hedging, naked CDS, etc.).
- **Stulz, R. M. (2009).** Credit Default Swaps and the Credit Crisis. *NBER Working Paper*, 15384. Used for the discussion of CDS contribution to the global financial crisis.
- **Culp, C. L., van der Merwe, A., & Stärkle, B. (2016).** Single-Name Credit Default Swaps: A Review of the Empirical Academic Literature. ISDA. Reference for physical vs. cash settlement.
- **Arakelyan, A., & Serrano, P. (2016).** Liquidity in Credit Default Swap Markets. *Journal of Multinational Financial Management*, 37–38, 139–157. [doi:10.1016/j.mulfin.2016.09.001](https://doi.org/10.1016/j.mulfin.2016.09.001). Justifies the choice of the 5Y senior tier as the most liquid benchmark.

## Rating agencies and sovereign debt

- **White, L. J. (2010).** Markets: The Credit Rating Agencies. *Journal of Economic Perspectives*, 24(2), 211–226. Overview of the rating-agency industry and its incentives.
- **White, L. J. (2013).** Credit Rating Agencies: An Overview. *Annual Review of Financial Economics*, 5(1), 93–122. Companion review article cited for the information-asymmetry framing.
- **Lane, P. R. (2012).** The European Sovereign Debt Crisis. *Journal of Economic Perspectives*, 26(3), 49–68. [doi:10.1257/jep.26.3.49](https://doi.org/10.1257/jep.26.3.49). Used in the introduction for the macro framing of the European debt crisis.
- **Candelon, B., Sy, A. N. R., & Arezki, R. (2011).** Sovereign Rating News and Financial Markets Spillovers: Evidence From the European Debt Crisis. *IMF Working Papers*, 11(68), 1. [doi:10.5089/9781455227112.001](https://doi.org/10.5089/9781455227112.001). Reference for transmission channels and ECAF / Basel framework discussion.
- **Claeys, P., & Vašíček, B. (2014).** Measuring bilateral spillover and testing contagion on sovereign bond markets in Europe. *Journal of Banking and Finance*, 46, 151–165. [doi:10.1016/j.jbankfin.2014.05.011](https://doi.org/10.1016/j.jbankfin.2014.05.011). Companion evidence on European sovereign-bond spillovers, motivating the H3 expectation.
- **Blundell-Wignall, A., & Slovik, P. (2010).** The EU Stress Test and Sovereign Debt Exposures. *OECD Working Papers on Finance, Insurance and Private Pensions*, 4. Reference for the bank cross-holdings of sovereign debt as a transmission channel.
- **Hornung, D., Robinson, M., Lemay, Y., et al. (2018).** *Rating Methodology: Sovereign Bond Ratings.* Moody's Investors Service. Used to describe the sovereign rating-methodology factor structure.
- **Reisen, H., & von Maltzan, J. (1999).** Boom and bust and sovereign ratings. *International Finance*, 2(2), 273–293. [doi:10.1111/1468-2362.00028](https://doi.org/10.1111/1468-2362.00028). Cited for S&P's earlier-and-more-frequent rating action pattern.

## Background and context

- **Soroka, S. N. (2006).** Good news and bad news: Asymmetric responses to economic information. *Journal of Politics*, 68(2), 372–385. The behavioural-economic frame for the asymmetric reaction to negative vs. positive events.
- **Hand, J. R. M., Holthausen, R. W., & Leftwich, R. W. (1992).** The Effect of Bond Rating Agency Announcements on Bond and Stock Prices. *The Journal of Finance*, 47(2), 733–752.
- **Hite, G., & Warga, A. (1997).** The Effect of Bond-Rating Changes on Bond Price Performance. *Financial Analysts Journal*, 53(3), 35–51.
- **Steiner, M., & Heinke, V. G. (2001).** Event study concerning international bond price effects of credit rating actions. *International Journal of Finance & Economics*, 6(2), 139–157. [doi:10.1002/ijfe.148](https://doi.org/10.1002/ijfe.148).
- **Dichev, I. D., & Piotroski, J. D. (2001).** The Long-Run Stock Returns Following Bond Ratings Changes. *The Journal of Finance*, 56(1), 173–203.
- **Vassalou, M., & Xing, Y. (2003).** Equity Returns Following Changes in Default Risk: New Insights into the Informational Content of Credit Ratings. *SSRN Electronic Journal*.
- **Acharya, V. V., Engle, R. F., Figlewski, S., Lynch, A. W., & Subrahmanyam, M. G. (2012).** Centralized Clearing for Credit Derivatives. In *Restoring Financial Stability* (pp. 251–268). John Wiley & Sons. [doi:10.1002/9781118258163.ch11](https://doi.org/10.1002/9781118258163.ch11).
- **Gonzalez, F., Haas, F., Johannes, R., et al. (2004).** Market dynamics associated with credit ratings: a literature review. *ECB Occasional Paper Series*, 16.
- **Neal, R. (1996).** Credit derivatives: New financial instruments for controlling credit risk. *Economic Review (Federal Reserve Bank of Kansas City)*, 81(2), 15–27.

## Policy and press

- **European Commission.** Regulating credit rating agencies. https://ec.europa.eu/info/business-economy-euro/banking-and-finance/financial-supervision-and-risk-management/managing-risks-banks-and-financial-institutions/regulating-credit-rating-agencies_en
- **European Parliament.** Parliament seals ban on sovereign debt speculation and short selling limitations. 15 November 2011.
- **Creswell, J., & Bowley, G. (2011).** Rating Firms Misread Signs of Greek Woes. *The New York Times*, 30 November 2011.
- **Fontevecchia, A. (2012, February 12).** ISDA Says Greece In Default, CDS Will Trigger. *Forbes.*
