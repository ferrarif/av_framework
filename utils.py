'''
Created on 14 Feb 2019

@author: francescoferrari
'''

import requests
import config
import pandas as pd
from time import sleep

def __get_request(function_,symbol_=None,outputsize_=None,interval_=None,
                  datatype_=None,from_currency_=None,to_currency_=None,
                  from_symbol_=None,to_symbol_=None,market_=None,
                  keywords_=None):
    fun_params=[function_,
                symbol_,
                outputsize_,
                interval_,
                datatype_,
                from_currency_,
                to_currency_,
                from_symbol_,
                to_symbol_,
                market_,
                keywords_]
    api_params=['function={}',
                '&symbol={}',
                '&outputsize={}',
                '&interval={}',
                '&datatype={}',
                '&from_currency={}',
                '&to_currency={}',
                '&from_symbol={}',
                '&to_symbol={}',
                '&market{}',
                '&keywords={}']
    query=[api_params[i].format(fun_params[i])
           if fun_params[i] is not None else ''
           for i in range(len(fun_params))]
    query.append('&apikey={}'.format(config.apiKey))
    response=requests.get(config.apiUrl.format(''.join(query)))
    return response
pass

def __get_eq_df_from_json(function_,ticker_,outputsize_,interval_,dictkey_,
                          store_=False):
    json_string=__get_request(function_=function_,
                              symbol_=ticker_,
                              interval_=interval_,
                              datatype_='json',
                              outputsize_=outputsize_).json()
    df=pd.DataFrame.from_dict(json_string[dictkey_],orient='index')
    df.columns=[col_name.split(' ')[1] for col_name in df.columns.values]
    if store_:
        df.to_csv('db//{}.csv'.format(ticker_))
    return df
pass

def __get_search_df_from_json(function_,keywords_,dictkey_):
    json_string=__get_request(function_=function_,
                              keywords_=keywords_,
                              datatype_='json').json()
    df=pd.DataFrame.from_dict(json_string[dictkey_])
    df.columns=[col_name.split(' ')[1] for col_name in df.columns.values]
    return df
pass

def __get_df_daily(ticker_,outputsize_,store_=False):
    function='TIME_SERIES_DAILY'
    dictkey='Time Series (Daily)'
    return __get_eq_df_from_json(function,ticker_,outputsize_,None,dictkey,
                                 store_)
pass

def __get_df_daily_adj(ticker_,outputsize_,store_=False):
    function='TIME_SERIES_DAILY_ADJUSTED'
    dictkey='Time Series (Daily)'
    return __get_eq_df_from_json(function,ticker_,outputsize_,None,dictkey,
                                 store_)
pass

def __get_df_intraday(ticker_,outputsize_,interval_):
    function='TIME_SERIES_INTRADAY'
    dictkey='Time Series ({})'.format(interval_)
    return __get_eq_df_from_json(function,ticker_,outputsize_,interval_,dictkey)
pass

def __get_df_weekly(ticker_,outputsize_):
    function='TIME_SERIES_WEEKLY'
    dictkey='Weekly Time Series'
    return __get_eq_df_from_json(function,ticker_,outputsize_,None,dictkey)
pass

def __get_df_weekly_adj(ticker_,outputsize_):
    function='TIME_SERIES_WEEKLY_ADJUSTED'
    dictkey='Weekly Adjusted Time Series'
    return __get_eq_df_from_json(function,ticker_,outputsize_,None,dictkey)
pass

def __get_df_monthly(ticker_,outputsize_):
    function='TIME_SERIES_MONTHLY'
    dictkey='Monthly Time Series'
    return __get_eq_df_from_json(function,ticker_,outputsize_,None,dictkey)
pass

def __get_df_monthly_adj(ticker_,outputsize_):
    function='TIME_SERIES_MONTHLY_ADJUSTED'
    dictkey='Monthly Adjusted Time Series'
    return __get_eq_df_from_json(function,ticker_,outputsize_,None,dictkey)
pass

def __get_search_results(keywords_):
    function='SYMBOL_SEARCH'
    dictkey='bestMatches'
    return __get_search_df_from_json(function,keywords_,dictkey)
pass

print(__get_df_daily('AAPL','full',store_=True))
sleep(12)
print(__get_df_daily_adj('AAPL','full'))
sleep(12)
print(__get_df_intraday('AAPL','full','5min'))
sleep(12)
print(__get_df_weekly('AAPL','full'))
sleep(12)
print(__get_df_weekly_adj('AAPL','full'))
sleep(12)
print(__get_df_monthly('AAPL','full'))
sleep(12)
print(__get_df_monthly_adj('AAPL','full'))
sleep(12)
print(__get_search_results('Apple'))
    