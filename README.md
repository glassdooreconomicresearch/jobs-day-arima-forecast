# jobs-day-arima-forecast

<b>SIMPLE ARIMA FORECAST OF BLS NONFARM PAYROLLS.</b>

This script (and accompanying data file) produces auto-ARIMA forecasts of BLS NSA payrolls, as well as implied BLS seasonal adjustment factors. Combines into a 12-month-ahead forecast of monthly SA nonfarm payrolls.

Source (NSA Payrolls): https://data.bls.gov/timeseries/CEU0000000001
Source (SA Payrolls): https://data.bls.gov/timeseries/CES0000000001

<b>Note:</b> First time use may require installation of pyramid.arima and statsmodels Python packages. Mac Terminal commands:

<code>pip install pyramid-arima</code>

<code>pip install -U statsmodels</code>

Author: Andrew Chamberlain, Ph.D.

Glassdoor Economic Research (glassdoor.com/research)

October 2018 