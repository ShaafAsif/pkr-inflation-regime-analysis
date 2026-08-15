# Does the Rupee Really Drive Inflation? What the Data Actually Showed

## The starting question

Pakistan's economy leans heavily on remittances and is no stranger to currency pressure. The obvious hypothesis: when the rupee weakens, imported goods cost more, and inflation follows. Workers' remittances, as a major source of forex, seemed like they should be part of that story too — more dollars coming in should ease pressure on the currency.

I wanted to test this properly instead of assuming it, using ten years of monthly data from the State Bank of Pakistan: CPI inflation, the PKR/USD exchange rate, and workers' remittances (July 2016–July 2026).

## What I actually did

- Tested each series for stationarity (Augmented Dickey-Fuller test) before running any causal analysis — all three needed differencing or log-differencing first
- Ran Granger causality tests across 1–6 month lags, in both directions, for every pair of variables
- Built a VAR(2) model treating CPI, PKR/USD, and remittances as a joint system, and generated impulse response functions to trace how a shock to one variable moves through the others over 12 months
- Stress-tested the headline finding by re-running it excluding the 2022–2023 devaluation period, then split the sample into pre-2022 and post-2022 regimes

## What I expected vs. what I found

Remittances, despite being central to the "obvious" story, showed **no statistically significant effect** on either the exchange rate or CPI, at any lag tested. That surprised me — but the data was consistent on this across every method I tried (Granger, VAR, impulse response).

PKR/USD, on the other hand, showed a strong, consistent Granger-causal relationship with CPI (significant at every lag, p<0.005) — the exchange rate genuinely does predict inflation. A single-variable regression put this at R²=0.116 across the full sample.

## The part that made me actually stress-test the result

Before treating that R²=0.116 as the finding, I re-ran it excluding the 2022–2023 devaluation window — the period when Pakistan moved from a managed/pegged exchange rate to a market-determined one. The relationship nearly vanished: R² dropped to 0.005, p-value jumped to 0.50.

Splitting the sample confirmed exactly what that suggested:
- **Pre-2022 (managed regime):** R²=0.002, no significant relationship
- **Post-2022 (market regime):** R²=0.221, strong and highly significant (p<0.001)

## The real finding

Exchange rate pass-through to inflation in Pakistan isn't a constant, textbook relationship — it's regime-dependent. Under a managed exchange rate, PKR movements were largely disconnected from real market pressure and didn't transmit meaningfully to prices. Once the rate was allowed to float in 2022, that transmission became immediate and substantial.

This is a narrower claim than where I started, but a more honest and useful one — it says something specific about how Pakistan's monetary regime shapes inflation dynamics, rather than asserting a general law that the data didn't actually support.

## What I'd want to add next

Controlling for global oil and commodity prices would help isolate how much of the post-2022 effect is PKR-specific versus a shared response to global inflation shocks during the same window. I'd also want to test whether informal remittance channels (unobserved in this data) change the remittance findings at all.

Full code, data sourcing, and charts: https://github.com/ShaafAsif/pkr-inflation-regime-analysis
