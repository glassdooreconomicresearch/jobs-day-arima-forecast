# SIMPLE ARIMA FORECAST OF BLS NONFARM PAYROLLS. 
# Note: Produces ARIMA forecasts of BLS NSA payrolls, as well as implied 
# BLS seasonal adjustment factors. Combines into a 12-month-ahead forecast
# of monthly SA nonfarm payrolls.
#
# Andrew Chamberlain, Ph.D.
# Glassdoor Economic Research 
# Web: glassdoor.com/research
# ORIGINAL: July 2018
# LAST UPDATE: May 23, 2019

import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from pyramid.arima import auto_arima
import os

# Set working directory (CHANGE THIS FOR YOUR ENVIRONMENT)
os.chdir('/Users/andrew.chamberlain/GitHub/jobs-day-arima-forecast')

# UPDATE MONTHLY: Choose starting and ending dates for ARIMA model.
start = '2010-01-01'
end = '2019-04-01'

# UPDATE MONTHLY: Choose starting and ending dates for forecast ahead period.
start_f = '2019-05-01'
end_f = '2020-04-01'

# Load BLS payrolls data (NSA, SA, and implied SA factors).
# Source: https://data.bls.gov/timeseries/CEU0000000001
df = pd.read_csv('data.csv', index_col=0)

# Cast date time, name columns.
df.index = pd.to_datetime(df.index)
df.columns = ['payrolls_nsa','payrolls_sa','implied_sa_factors']

# Perform seasonal and trend decomposition for NSA payrolls.
decomp = seasonal_decompose(df.loc[start:end,'payrolls_nsa'], model='additive', freq=12, extrapolate_trend=12)
fig = decomp.plot()
fig.savefig('decomp.png')

# Examine components of the NSA payrolls time series decomposition. 
trend = decomp.trend
seasonal = decomp.seasonal
resid = decomp.resid

##########################################################################
# Run auto ARIMA proceedure for NSA payrolls and implied BLS SA factors.
##########################################################################

# Auto ARIMA for NSA payrolls.
model_nsa = auto_arima(df.loc[start:end,'payrolls_nsa'], exogenous=None, start_p=1, start_q=1,
                           max_p=6, max_q=6, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
model_nsa.summary()

# Auto ARIMA for implied BLS SA factors.
model_sa_factors = auto_arima(df.loc[start:end,'implied_sa_factors'], exogenous=None, start_p=1, start_q=1,
                           max_p=6, max_q=6, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
model_sa_factors.summary()


#################################################
# Create 12-month ahead forecast of NSA payrolls. 
#################################################

# Create training and forecast data frames.
train = df.loc[start:end,'payrolls_nsa']
test = df.loc[start_f:end_f, 'payrolls_nsa']

# Fit arima model on NSA payrolls time series. 
model_nsa.fit(train)

# Forecast 12 months ahead. 
forecast_nsa = model_nsa.predict(n_periods = 12)

# Create forecast dataframe.
forecast_nsa_df = pd.DataFrame(forecast_nsa, index=test.index, columns=['prediction_nsa'])


###########################################################
# Create 12-month ahead forecast of BLS implied SA factors. 
###########################################################

# Create training and forecast data frames.
train_sa_factors = df.loc[start:end,'implied_sa_factors']
test_sa_factors = df.loc[start_f:end_f, 'implied_sa_factors']

# Fit arima model on BLS implied SA factors time series.
model_sa_factors.fit(train_sa_factors)

# Forecast 12 months ahead. 
forecast_sa_factors = model_sa_factors.predict(n_periods = 12)

# Create forecast dataframe.
forecast_sa_factors_df = pd.DataFrame(forecast_sa_factors, index=test.index, columns=['prediction_sa_factors'])


###########################################
# Merge full forecast data together.
###########################################

# Merge together forecasts of NSA payrolls and implied BLS SA factors. 
df_forecast = pd.concat([df,forecast_nsa_df,forecast_sa_factors_df],axis=1)

# Generate new column for 12-month ahead forecast of SA payrolls (NSA forecast minus forecasted SA factors). 
df_forecast['forecast_sa'] = df_forecast['prediction_nsa'] - df_forecast['prediction_sa_factors']

# Push out 12-month SA nonfarm payrolls forecast to CSV.
df_forecast.to_csv('forecast.csv')

### end ###