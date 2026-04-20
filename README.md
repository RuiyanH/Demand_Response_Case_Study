# Demand Response Event Analysis

Event-level performance and financial analysis for a 5-site commercial demand response (DR) portfolio during the June 14, 2022 Midwest heat wave. The analysis compares two industry-standard baseline methodologies, quantifies curtailment performance per site, and computes event-level settlement under real-time locational marginal pricing (LMP).

## Summary of findings

- 4 of 5 sites significantly curtailed load during the 2–6 PM event window; site 2 curtailed over 90% of its normal load (~4,700 kW → ~320 kW).
- Baseline methodology meaningfully changed measured performance: 10of10 produced a higher baseline than FSL for some sites, and vice versa for others, directly affecting settlement payouts.
- Total event profit was ~$30.8K across 5 sites, with sites 1, 2, and 5 driving ~95% of the total. A single hour at site 2 (16:00 EDT) generated ~$13K gross revenue due to a $3,000/MWh LMP spike.

## Methodology

**Event.** Emergency DR dispatch during a Midwest heat wave, 2:00–6:00 PM EDT on June 14, 2022. Conditions: high demand combined with low wind output.

**Data.** 5 commercial customer sites, 15-minute interval kWh readings across May–June 2022, resampled to hourly kW and normalized to EDT.

**Baselines compared:**
- **10of10** — average load across the 10 most recent comparable weekdays (or weekends) at the same hour. Site-specific and responsive to recent operations.
- **Firm Service Level (FSL)** — fixed system benchmark per site, based on MISO system peak conditions, independent of recent load.

**Performance.** Computed as `baseline − actual`, averaged over event hours. Negative performance (load above baseline) floored at zero per hour for settlement.

**Financials.** Gross revenue computed hourly using real-time LMP; profit split between customer payment and aggregator margin.

## Sample results

Site 2 was the strongest performer, with event load dropping from a ~4,700 kW baseline to ~320 kW — over 90% curtailment. Hourly settlement:

| Hour  | Load (kW) | 10of10 Baseline (kW) | Performance (kW) | LMP ($/MWh) | Gross Rev |
|-------|-----------|----------------------|------------------|-------------|-----------|
| 14:00 | 328       | 4,744                | 4,417            | 1,500       | $6,625    |
| 15:00 | 320       | 4,676                | 4,356            | 1,800       | $7,841    |
| 16:00 | 331       | 4,652                | 4,320            | 3,000       | $12,961   |
| 17:00 | 320       | 4,606                | 4,286            | 780         | $3,343    |

Site load profiles, event-day curtailment plots, and cross-site performance comparisons are in `outputs/`.

## Project structure

```
.
├── analysis.ipynb          # Main analysis: baselines, EDA, financial results
├── src/
│   ├── config.py           # Event constants and parameters (no hard-coded values in analysis)
│   ├── data_loader.py      # CSV ingest, timezone normalization, unit conversion, hourly resampling
│   └── baseline_model.py   # 10of10 and FSL baselines + hourly per-site performance
├── data/
│   ├── raw/                # 15-min interval kWh readings, May–Jun 2022
│   └── ref/gt.csv          # Ground-truth performance values for validation
└── outputs/                # Generated tables and plots
```

## Running the analysis

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook analysis.ipynb
```

## Design choices

- **Parameter-driven config** — event window, baseline lookback, LMP values set in `config.py`, no hard-coded values in analysis code.
- **Linear scalability** — modular per-site computation scales approximately linearly with portfolio size; site-level work is parallelizable for larger datasets.
- **Separation of concerns** — data loading, baseline computation, and settlement logic are decoupled so each can be tested or swapped independently.

## Known limitations / future work

- Weekday baselines do not currently exclude holidays; integrating a holiday calendar would improve accuracy for events near federal holidays.
- Missing-value and outlier handling is minimal; a production version would add more robust QA checks.
- Current implementation assumes a single continuous event window; multi-day or discontinuous dispatch events would need extensions to the baseline model.

---

*Built as a case study. Methodology follows standard ISO/RTO demand response settlement protocols.*
