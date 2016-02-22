#!/usr/bin/env python
import argparse
import os
import sys
import datetime
import csv
import decimal
from yahoo_finance import Share
import xlsxwriter

TIME_FMT = '%Y-%m-%d'

def check_date_format(s):
    try:
        d = datetime.datetime.strptime(s, TIME_FMT)
    except:
        return False
    else:
        return True

def check_args(start_date, end_date):
    exit = False
    if not check_date_format(start_date):
        print " [-] Invalid start date format! Use: %s"%TIME_FMT
        exit = True
    if not check_date_format(end_date):
        print " [-] Invalid end date format! Use: %s"%TIME_FMT
        exit = True
    if not exit:
        s_d =  datetime.datetime.strptime(start_date, TIME_FMT)
        e_d =  datetime.datetime.strptime(end_date, TIME_FMT)
        if s_d >= e_d:
            print ' [-] Start date must come before end date'
            exit = True
    return exit

def download_data(s, s_date, e_date):
    ticker = Share(s)
    return ticker.get_historical(s_date, e_date)

def main(ticker, start_date, end_date):
    if check_args(start_date, end_date):
        return []
    
    rows = download_data(ticker, start_date, end_date)
    for row in rows:
        del row['Symbol']
    return rows
