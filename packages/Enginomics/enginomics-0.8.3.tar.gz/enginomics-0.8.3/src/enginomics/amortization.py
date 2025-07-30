# -*- coding: utf-8 -*-
""" 
Copyright 2025 Wayne Matthew Syvinski

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. 
"""
import pandas as pd
import numpy as np
import numpy_financial as npf
import math as m
from pandasql import sqldf

class Amortization:

    def __init__(self, principal: float, intrate: float, periods: int, description: str = None, period_type: str = 'month', extra_pmt: float = 0):
        self.__principal = principal
        self.__intrate = intrate
        self.__periods = periods
        self.__period_type = period_type
        self.__extra_pmt = extra_pmt
        self.__description = description

        self.__df_amortization = pd.DataFrame()

        self.__minimum_payment = float(0)
        self.__total_payments = float(0)
        self.__total_interest = float(0)
        self.__number_payments = int(0)

    def generate(self):
        self.__df_amortization = pd.DataFrame(columns = ['period', 'principal', 'payment', 'interest paid', 'principal paid', 'remaining_principal'])
        self.__df_amortization = self.__df_amortization.astype({'period': 'str', 'principal': 'float', 'payment': 'float', 'interest paid': 'float', 'principal paid': 'float', 'remaining_principal': 'float'})

        if self.__period_type == 'month':
            period_intrate = float(self.__intrate) / float(100 * 12)
        elif self.__period_type == 'quarter':
            period_intrate = float(self.__intrate) / float(100 * 4)
        elif self.__period_type == 'year':
            period_intrate = float(self.__intrate) / float(100)
        elif self.__period_type == 'period':
            period_intrate = float(self.__intrate) / float(100)
        elif self.__period_type == 'semiannual':
            period_intrate = float(self.__intrate) / float(100 * 2)
        

        principal = self.__principal
        self.__minimum_payment = abs(npf.pmt(rate = period_intrate, nper = self.__periods, pv = self.__principal))
        payment = self.__minimum_payment + self.__extra_pmt
        interest_paid = 0
        principal_paid = 0
        remaining_principal = self.__principal

        for period in range(1, self.__periods + 1):

            if remaining_principal > 0:
                principal = remaining_principal
                interest_paid = principal * period_intrate
                principal_paid = payment - interest_paid
                remaining_principal = principal - principal_paid
            else:
                principal = 0
                payment = 0
                interest_paid = 0
                principal_paid = 0

            if remaining_principal < 0:
                payment = payment + remaining_principal
                principal_paid = principal_paid + remaining_principal
                remaining_principal = 0

            self.__df_amortization.loc[period - 1] = [period, principal, payment, interest_paid, principal_paid, remaining_principal]

        df_amort = self.__df_amortization

        query = 'select sum(`interest paid`) as total_interest from df_amort;'
        dfresult = sqldf(query)
        self.__total_interest = dfresult.iloc[0]['total_interest']

        query = 'select sum(payment) as total_payments from df_amort;'
        dfresult = sqldf(query)
        self.__total_payments = dfresult.iloc[0]['total_payments']

        query = 'select count(*) as number_payments from df_amort where principal > 0;' 
        dfresult = sqldf(query)
        self.__number_payments = dfresult.iloc[0]['number_payments']

        return
        
    def get_minimum_payment(self):
        return self.__minimum_payment
    
    def get_total_interest(self):
        return self.__total_interest
    
    def get_total_payments(self):
        return self.__total_payments
    
    def get_number_payments(self):
        return self.__number_payments
    
    def export_to_excel(self, filepath: str):

        df_summary = pd.DataFrame()

        col_metric = pd.Series(['Description',
                       'Principal',
                       'Interest Rate',
                       'Loan Term',
                       'Compounding Period',
                       'Extra Payment per Term', 
                       'Required Minimum Payment', 
                       'Number of Payments Made',
                       'Total Payments Made', 
                       'Total Interest Paid'], name = 'metric')
        
        col_value = pd.Series([self.__description, 
                      '${:,.2f}'.format(self.__principal), 
                      str(self.__intrate).strip() + '%', 
                      str(self.__periods).strip(),
                      self.__period_type, 
                      '${:,.2f}'.format(self.__extra_pmt), 
                      '${:,.2f}'.format(self.__minimum_payment), 
                      str(self.__number_payments).strip(),
                      '${:,.2f}'.format(self.__total_payments), 
                      '${:,.2f}'.format(self.__total_interest)], name = 'value')

        df_summary = pd.concat([df_summary, col_metric, col_value], axis = 1)

        try:
            with pd.ExcelWriter(filepath) as writer:
                df_summary.to_excel(writer, sheet_name='Summary', index = False)
                self.__df_amortization.to_excel(writer,sheet_name = 'Amortization', float_format="%.2f", header = True, index = False)
                return True
        except:
            return False 
        
    def fetch_amortization(self):
        return self.__df_amortization

