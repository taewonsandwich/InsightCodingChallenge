#!/usr/bin/env python3

# Given an input file itcont.txt,
# This file creates two output files:
# 1. medianvals_by_zip.txt: contains a calculated running median, total dollar amount and total number of contributions
# by recipient and zip code
# 2. medianvals_by_date.txt: has the calculated median, total dollar amount and total number of contributions by
# recipient and date.


import sys
import os
import re
import pandas as pd
import numpy as np
from datetime import datetime


def get_df(file):
    columns = ['CMTE_ID', 'ZIPCODE', 'TRN_DATE', 'TRN_AMNT', 'COUNT_ZIP', 'COUNT_DATE', 'MED_ZIP', 'MED_DATE',
               'TOTAL_ZIP', 'TOTAL_DATE']
    df = pd.DataFrame(columns=columns)
    p = re.compile(
        r'^(?P<CMTE_ID>[^\|]+?)(\|[^\|]*?){9}\|(?P<ZC>[^\|]*?)(\|[^\|]*?){2}\|(?P<TD>[^\|]*?)\|(?P<TA>\d+?)\|\|'
    )
    # Empty CMTE_ID, empty transaction amount, or non-empty OTHER_ID will be skipped by above regular expression
    for line in file:
        meta = p.match(line)
        if meta:
            cmte = meta['CMTE_ID']

            if meta['ZC'].isnumeric() and len(meta['ZC']) > 5:
                zip = meta['ZC'][0:5]
            else:
                zip = np.nan
            try:
                date = datetime.strptime(meta['TD'], '%m%d%Y')
                date = date.strftime('%Y%m%d')
            except ValueError:
                date = np.nan
            money = int(meta['TA'])
            # Adding information by each pair of (recipient, zipcode)
            by_z = df[(df['CMTE_ID'] == cmte) & (df['ZIPCODE'] == zip)]
            count_z = by_z.shape[0] + 1
            if count_z == 1:
                tot_by_z = money
            else:
                tot_by_z = by_z.iat[-1, -1] + money
            med_by_z = int(round(np.median(by_z['TRN_AMNT'].tolist() + [money])))

            # Adding information by each pair of (recipient, date)
            by_d = df[(df['CMTE_ID'] == cmte) & (df['TRN_DATE'] == date)]
            count_d = by_d.shape[0] + 1
            if count_d == 1:
                tot_by_d = money
            else:
                tot_by_d = by_d.iat[-1, -1] + money
            med_by_d = int(round(np.median(by_d['TRN_AMNT'].tolist() + [money])))

            # New row of the data frame is appended.
            dat = pd.DataFrame(
                [[cmte, zip, date, money, count_z, count_d, med_by_z, med_by_d, tot_by_z, tot_by_d]],
                columns=columns)
            df = pd.concat([df, dat], ignore_index=True)
        else:
            pass
    return df


def by_zip(df):
    df_zip = df[['CMTE_ID', 'ZIPCODE', 'MED_ZIP', 'COUNT_ZIP', 'TOTAL_ZIP']]
    df_zip = df_zip.dropna(subset=['ZIPCODE'])
    return df_zip


def by_date(df):
    df_date = df[['CMTE_ID', 'TRN_DATE', 'MED_DATE', 'COUNT_DATE', 'TOTAL_DATE']]
    df_date = df_date.dropna(subset=['TRN_DATE'])
    df_date = df_date.sort_values('COUNT_DATE', ascending=False).drop_duplicates(['CMTE_ID', 'TRN_DATE'])
    df_date = df_date.sort_values(['CMTE_ID', 'TRN_DATE'])
    df_date['TRN_DATE'] = df_date['TRN_DATE'].apply(lambda x: datetime.strptime(x, '%Y%m%d').strftime('%m%d%Y'))
    return df_date


def main():
    try:
        file = open(sys.argv[1], 'r')
    except IndexError:
        print('Error: file name input required')
    except IOError:
        print('Error: cannot find or read the file')
    else:
        df = get_df(file)
        df_zip = by_zip(df)
        df_date = by_date(df)

        path = os.path.abspath(os.path.join(os.getcwd(), r'output'))
        df_zip.to_csv(os.path.join(path, r'medianvals_by_zip.txt'), header=None, index=None, mode='a', sep='|')
        df_date.to_csv(os.path.join(path, r'medianvals_by_date.txt'), header=None, index=None, mode='a', sep='|')


main()



