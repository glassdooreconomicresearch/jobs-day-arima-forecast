# jobs-day-arima-forecast

<b>SIMPLE ARIMA FORECAST OF BLS NONFARM PAYROLLS.</b>

This script (and accompanying data file) produces auto-ARIMA forecasts of BLS NSA payrolls, as well as implied BLS seasonal adjustment factors. Combines into a 12-month-ahead forecast of monthly SA nonfarm payrolls.

## Running Instructions

1. Update the monthly start/end date. `start_f` should be the start of the forecast period (generally the current month). `end_f` must be 11 months after `start_f`.
2. Make sure the working directory is pointing at the right folder.
3. Update `data.csv` using the latest data from BLS. Make sure to extend the empty rows too.
Source (NSA Payrolls): https://data.bls.gov/timeseries/CEU0000000001
Source (SA Payrolls): https://data.bls.gov/timeseries/CES0000000001
4. Run from command line: `python arima_jobs_day.py`

## Installation Instructions

<b>Note:</b> First time use may require installation of pyramid.arima and statsmodels Python packages. Mac Terminal commands:

<code>pip install pyramid-arima</code>

<code>pip install -U statsmodels</code>

See `requirements.txt` for version requirements. Newer versions of statsmodels appear to be incompatible with `pyramid.arima`. Installing the exact versions required can be accomplished with the following code:

```pip install -r requirements.txt```


Author: Andrew Chamberlain, Ph.D.

Glassdoor Economic Research (glassdoor.com/research)

October 2018
