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

import numpy_financial as npf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import math as m
import numpy as np
import copy
from pandasql import sqldf

class Cashflow:
    def __init__(self,  rate: float = None):
        
        self.__cfd = {}
        self.__rate = rate
        self.__cfd_plot = None

        return
    
    def __add__(self, cf2: 'Cashflow', rate = None):
        maxindex1 = max(list(self.__cfd.keys()))
        maxindex2 = max(list(cf2.__cfd.keys()))

        if maxindex1 > maxindex2:
            maxindex = maxindex1
        else:
            maxindex = maxindex2

        cf_dict = {}

        for i in range(0, maxindex + 1):
            if i in self.__cfd.keys():
                augend = self.__cfd[i]
            else:
                augend = 0.0
            
            if i in cf2.__cfd.keys():
                addend = cf2.__cfd[i]
            else:
                addend = 0.0

            cf_dict[i] = augend + addend

        cf = Cashflow(rate)
        cf.__cfd = cf_dict

        return cf

    def __sub__(self, cf2: 'Cashflow', rate = None):
        maxindex1 = max(list(self.__cfd.keys()))
        maxindex2 = max(list(cf2.__cfd.keys()))

        if maxindex1 > maxindex2:
            maxindex = maxindex1
        else:
            maxindex = maxindex2

        cf_dict = {}

        for i in range(0, maxindex + 1):
            if i in self.__cfd.keys():
                minuend = self.__cfd[i]
            else:
                minuend = 0.0
            
            if i in cf2.__cfd.keys():
                subtrahend = cf2.__cfd[i]
            else:
                subtrahend = 0.0

            cf_dict[i] = minuend - subtrahend

        cf = Cashflow(rate)
        cf.__cfd = cf_dict

        return cf
    
    def __mul__(self, factor: float):
        cf_mult = Cashflow.from_list([value * factor for value in self.to_list()])
        cf_mult.set_rate(self.get_rate())

        return cf_mult
    
    __rmul__ = __mul__
    
    def __truediv__(self, divisor: float):
        cf_mult = Cashflow.from_list([value / divisor for value in self.to_list()])
        cf_mult.set_rate(self.get_rate())

        return cf_mult

    def __neg__(self):

        cf_dict = {}

        for key in self.__cfd.keys():
            cf_dict[key] = -self.__cfd[key]

        cf = Cashflow(self.__rate)
        cf.__cfd = cf_dict

        return cf

    def get_rate(self):
        return self.__rate
    
    def set_rate(self, rate: float):
        self.__rate = rate
        return

    def get_period(self, period: int):
        if period in self.__cfd.keys():
            return self.__cfd[period]
        else:
            return None

    def set_period(self, period: int, amount: float = 0.0):
        self.__cfd[period] = amount
        if max(self.__cfd.keys()) > (len(self.__cfd) - 1):
            cfd_hold = {}
            for i in range(0, max(self.__cfd.keys())):
                if i in self.__cfd.keys():
                    cfd_hold[i] = float(self.__cfd[i])
                else:
                    cfd_hold[i] = 0.0

            self.__cfd = cfd_hold

        return
            

    def from_list(cflist: list, rate: float = None):
        cf = Cashflow(rate)
        cf.__cfd = dict(zip(list(range(0,len(cflist)+1)),cflist))
                
        return cf
    
    def to_list(self):
        return list(self.__cfd.values())
    
    def from_dict(cfdict: dict, rate: float = None):
        cfdict_out = {}
        for i in range(0, max(cfdict.keys()) + 1):
            if i in cfdict.keys():
                cfdict_out[i] = cfdict[i]
            else:
                cfdict_out[i] = 0.0
        
        cf = Cashflow(rate)
        cf.__cfd = cfdict_out

        return cf
    
    def expansion_from_dict(cfdict: dict, rate: float = None):
        entries = list(cfdict.keys())
        last_period = max(entries)

        full_cfd = {}
        current_value = 0.0

        for i in range(0, last_period + 1):
            if i in cfdict.keys():
                current_value = float(cfdict[i])
            
            full_cfd[i] = current_value

        cf = Cashflow(rate)
        cf.__cfd = full_cfd
        return cf
    
    def from_annuity(start_period: int, end_period: int, amount: float, rate: float = None):
        cfd = {}

        for i in range(0, end_period + 1):
            if i < start_period:
                cfd[i] = 0.0
            else:
                cfd[i] = float(amount)
        
        cf = Cashflow(rate = rate)
        cf.__cfd = cfd

        return cf
    
    def from_arith(start_period: int, end_period: int, amount: float, rate: float = None):
        cfd = {}
        arith_index = 0

        for i in range(0, end_period + 1):
            if i < start_period:
                cfd[i] = 0.0
            else:
                cfd[i] = float(amount) * arith_index
                arith_index += 1

        cf = Cashflow(rate = rate)
        cf.__cfd = cfd

        return cf
    
    def from_geom(start_period: int, end_period: int, amount: float, pct_change: float, rate = None):
        cfd = {}
        factor = float(1) + pct_change
        geom_index = 0

        for i in range(0, end_period + 1):
            if i < start_period:
                cfd[i] = 0.0
            else:
                cfd[i] = amount * (factor ** geom_index)
                geom_index += 1

        cf = Cashflow(rate = rate)
        cf.__cfd = cfd

        return cf
    
    def fetch_entries(file: str, entry_names: list = None, merge_into: dict = {}):
        with open(file, 'r') as readfile:
            for entryline in readfile:
                [entry_name, a, b, c] = entryline.split('|')
                if (entry_names is None) or (entry_name in entry_names):
                    merge_into = merge_into | Cashflow.parse_entry_text(entryline)

        return merge_into
    
    def fetch_entry_names(file: str):
        entry_names = []
        with open(file, 'r') as readfile:
            for entryline in readfile:
                [entry_name, a, b, c] = entryline.split('|')
                entry_names.append(entry_name)

        return entry_names
    
    def write_entry(self, file: str, entry_name: str):
        with open(file, 'a') as appendfile:
            appendfile.write(self.make_entry_text(entry_name) + "\n")

        return
    
    def write_all_entries(file: str, cf_named_dict: dict):
        with open(file, 'a') as appendfile:
            for entry_name in cf_named_dict.keys():
                appendfile.write(cf_named_dict[entry_name].make_entry_text(entry_name) + "\n")

        return

    def parse_entry_text(entry: str):
        [entry_name, method, rate, definition] = entry.split('|')
        if rate is None or rate.strip() == '':
            rate = None

        result = {}

        if method == 'list':
            result[entry_name] = Cashflow.from_list([float(cash) for cash in definition.split(',')], rate = rate)            
        elif method in ['dict', 'expand']:
            cf_dict = {}
            entries = definition.split(',')
            for entry in entries:
                [period, value] = entry.split(':')
                cf_dict[int(period)] = float(value)
            if method == 'dict':
                result[entry_name] = Cashflow.from_dict(cf_dict, rate = rate)
            elif method == 'expand':
                result[entry_name] = Cashflow.expansion_from_dict(cf_dict, rate = rate)
        elif method == 'arith':
            [start_period, end_period, amount] = definition.split(',')
            result[entry_name] = Cashflow.from_arith(int(start_period), int(end_period), float(amount), rate = rate)
        elif method == 'geom':
            [start_period, end_period, amount, pct_change] = definition.split(',')
            result[entry_name] = Cashflow.from_geom(int(start_period), int(end_period), float(amount), float(pct_change), rate = rate)

        return result
    
    def make_entry_text(self, entry_name: str):
        if self.get_rate() is None:
            rate = ''
        else:
            rate = str(self.get_rate())

        definition = str(self.to_dict())[1:-1].replace(' ','')

        return f"{entry_name}|dict|{rate}|{definition}"

    def to_dict(self):
        return self.__cfd

    def nper(self):
        return len(self.__cfd) - 1
    
    def irr(self):
        return npf.irr(self.to_list()) 
    
    def mirr(self, reinvest_rate: float):
        return npf.mirr(self.to_list(), self.get_rate(), invest_rate=reinvest_rate)

    def npv(self):
        return npf.npv(values = self.to_list(), rate = self.get_rate())
    
    def nfv(self):
        npv = npf.npv(values = self.to_list(), rate = self.get_rate())
        return npv * ((1.0 + self.get_rate())**(self.nper())) 

    def nus(self):
        return -npf.pmt(rate = self.get_rate(), nper = self.nper(), pv = self.npv())      
    
    def same_horizon(self, cfd: 'Cashflow'): 
        cfd1 = self.__cfd
        cfd2 = cfd.__cfd  
        cfd1_min = min(cfd1.keys())
        cfd1_max = max(cfd1.keys())
        cfd1_len = len(cfd1)
        cfd2_min = min(cfd2.keys())
        cfd2_max = max(cfd2.keys())
        cfd2_len = len(cfd2)
        if (cfd1_min == cfd2_min) and (cfd1_max == cfd2_max) and (cfd1_len == cfd2_len):
            return True
        else:
            return False

    def payback(self):
        net = 0
        index = 0
        for value in self.__cfd.values():
            net += value
            if net >= 0:
                return float(index) - (net/value)
            index += 1

        return m.inf
    
    def payback_disc(self):
        net = 0
        index = 0

        disc_cf = [self.__cfd[key]/((1.0 + self.get_rate()) ** key) for key in self.__cfd.keys()]

        for value in disc_cf:
            net += value
            if net >= 0:
                return float(index) - (net/value)
            index += 1

        return m.inf

    def replicate(self, times: int = 2):
        
        cfd = copy.deepcopy(self.__cfd)
       
        master_index = 0
        
        full_cfd = {}
        for repl in range(0, times):
            for i in self.__cfd.keys():
                if master_index == 0:
                    full_cfd[0] = cfd[0]
                    master_index += 1
                elif i == 0:
                    full_cfd[master_index - 1] += cfd[i]
                else:
                    full_cfd[master_index] = cfd[i]
                    master_index += 1


        cf = Cashflow(self.__rate)
        cf.__cfd = full_cfd

        return cf

    def separate_bc(self):
        benefit = []
        cost = []
        for value in list(self.__cfd.values()):
            if value > 0.0:
                benefit.append(value)
                cost.append(0.0)
            elif value < 0.0:
                benefit.append(0.0)
                cost.append(value)
            else:
                benefit.append(0.0)
                cost.append(0.0)

        cf_benefit = Cashflow.from_list(benefit, self.__rate)
        cf_cost = Cashflow.from_list(cost, self.__rate)

        return cf_benefit, cf_cost

    def plot_cfd(self, subject: str = None, scale: int = 1, savefile: str = None, showplot: bool = False, poscolor: str = '#005643', negcolor: str = '#FF4F00', barfontsize: int = 12):

        def currency_formatter(x, pos):
            if x < 0:
                return '(${:,.0f})'.format(abs(x))  # Parentheses for negative currency
            else:
                return '${:,.0f}'.format(x)   # Regular currency format

        def color_selection(x):
            if x > 0:
                return poscolor
            elif x < 0:
                return negcolor
            else:
                return '#777777'

        sns.set_theme(rc={"figure.figsize":(self.nper()+3, 6)}) #width=8, height=4

        data = {
            'period': list(self.__cfd.keys()),
            'cash': [float(x)/float(scale) for x in self.__cfd.values()],
            'colors': [color_selection(x) for x in self.__cfd.values()]
        }

        df_data = pd.DataFrame(data)

        title_str = 'Cash Flow Diagram'
        if subject is not None:
            title_str += f" for {subject}"

        sns.set_context('talk', rc={"axes.labelsize": barfontsize})
        ax = sns.barplot(data = df_data, x = 'period', y = 'cash', legend = False) 
        plt.title(title_str)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(currency_formatter))
        ax.bar_label(ax.containers[0], 
                     labels = [currency_formatter(i, None) for i in df_data['cash']],
                     fontsize = 16)

        scale_ylabel = 'Cash'

        if scale > 1:
            scale_ylabel += f"/{scale:,}"

        ax.set(ylabel = scale_ylabel, xlabel = 'Compounding Period')

        for bar, color in zip(ax.patches, list(df_data['colors'])):
            bar.set_color(color)


        if showplot == True:
            plt.show()

        if savefile is not None:
            try:
                ax.get_figure().savefig(savefile, bbox_inches='tight')
            except:
                pass

        del ax
        plt.close()
        
        return 

class IncrementalIRR:
    def __init__(self, marr: float = None, outputfile: str = None):

        self.__marr = marr
        self.__outputfile = outputfile
        self.__df_alternatives = pd.DataFrame()
        self.__alternatives = {}
        self.__results = pd.DataFrame()

        return

    def set_marr(self, marr: float):
        self.__marr = marr
        return

    def get_marr(self):
        return self.__marr

    def set_outputfile(self, outputfile):
        self.__outputfile = outputfile
        return 

    def get_outputfile(self):
        return self.__outputfile

    def add_alternative(self, altname: str, cfd: 'Cashflow'):
        self.__alternatives[altname] = cfd.to_dict()
        return

    def del_alternative(self, altname: str, fail_silent: bool = False):
        if altname in self.__alternatives.keys():
            del self.__alternatives[altname]
        elif fail_silent == False:
            raise Exception(f"Alternative {altname} does not exist.")
        return
    
    def ingest_file(self, file: str):
        entries = {}
        partial_benefits = {}
        partial_costs = {}
        entries = Cashflow.fetch_entries(file)

        for entry in entries.keys():
            if entry[-3] == '$B$' or entry[-3] == '$C$':
                basename = entry[0:-3]
                hold_cf = entries[entry]
                if hold_cf.npv() <= 0:
                    partial_costs[basename] = hold_cf
                else:  
                    partial_benefits[basename] = hold_cf
            else:
                self.add_alternative(entry, entries[entry])

            names_costs = partial_costs.keys()
            names_benefits = partial_benefits.keys()

            names_common = list(set(names_costs) & set(names_benefits))

            for name in names_common:
                self.add_alternative(name, partial_benefits[name] + partial_costs[name])

        return

    def fetch_alternatives(self):
        return self.__df_alternatives
    
    def fetch_pairwise(self):
        return self.__results
    
    def list_alternatives(self):
        return list(self.__alternatives.keys())

    def __compare_pair(self, challenger_name: str, challenger_cf: 'Cashflow', defender_name: str, defender_cf: 'Cashflow'):

        if challenger_cf.same_horizon(defender_cf):
            defender_cf_norm = defender_cf
            challenger_cf_norm = challenger_cf
        else:
            lcm = m.lcm(defender_cf.nper() + 1,challenger_cf.nper() + 1)

            factor_def = int(lcm/(defender_cf.nper() + 1))
            factor_chal = int(lcm/(challenger_cf.nper() + 1))

            defender_cf_norm = defender_cf.replicate(factor_def)
            challenger_cf_norm = challenger_cf.replicate(factor_chal)

        cfd_diff = challenger_cf_norm - defender_cf_norm
        delta_irr = cfd_diff.irr()
        
        if delta_irr > self.__marr:
            winner = challenger_name
        else:
            winner = defender_name

        return winner, delta_irr

    def prep_bcr(self):
        bcr = IncrementalBCR(marr = self.__marr)

        for cf_key in self.__alternatives.keys():
            cf_alt = Cashflow.from_dict(self.__alternatives[cf_key])
            [cf_benefit, cf_cost] = cf_alt.separate_bc()
            bcr.add_alternative(altname = cf_key, cf_benefit=cf_benefit, cf_cost=cf_cost)

        return bcr

    def generate(self):

        self.__df_alternatives = pd.DataFrame()
        self.__results = pd.DataFrame()

        entries_list = []
        for alt in self.__alternatives.keys():
            entries_list.append(len(self.__alternatives[alt])-1)

        fieldlist = ['alternative', 'periods', 'IRR', 'NPV', 'EUAW', 'CBR', 'payback period', 'discounted payback period']
        sortfields = []
        sortorder = []
        do_nothing = []

        maxfields = -1

        for alt in self.__alternatives.keys():
            numcols = len(self.__alternatives[alt])
            if numcols > maxfields:
                maxfields = numcols

        for i in range(0, maxfields):
            sortfields.append('cf_' + str(i).strip())  
            sortorder.append(False)
            do_nothing.append(0)         


        fieldlist.extend(sortfields)

        sqlfieldlist = ['[' + field + ']' for field in fieldlist]
        sqlfieldlist.extend(sortfields)

        sqlfieldlist_str = ", ".join(sqlfieldlist)

        self.__df_alternatives = pd.DataFrame(columns = fieldlist)

        for alt in self.__alternatives.keys():
            alt_irr_list = [element for element in self.__alternatives[alt].values() if ((element is not None) and (np.isnan(element) == False))]
            row_cf = Cashflow.from_list(alt_irr_list, self.get_marr())
            alt_periods = row_cf.nper()
            alt_irr = row_cf.irr()
            alt_npv = row_cf.npv()
            alt_euaw = row_cf.nus()
            alt_payback = row_cf.payback()
            alt_payback_disc = row_cf.payback_disc()
            alt_benefit, alt_cost = row_cf.separate_bc()
            alt_benefit.set_rate(self.get_marr())
            alt_cost.set_rate(self.get_marr())
            alt_cbr = abs(float(alt_benefit.npv())/float(alt_cost.npv()))
            insert_row = [alt, alt_periods, alt_irr, alt_npv, alt_euaw, alt_cbr, alt_payback, alt_payback_disc]
            
            alt_cf = Cashflow.from_list(list(self.__alternatives[alt].values()))
            insert_row.extend(alt_cf.to_list())
            rec_dict = dict(zip(fieldlist, insert_row))
            self.__df_alternatives.loc[len(self.__df_alternatives)] = rec_dict

        self.__df_alternatives = self.__df_alternatives.sort_values(by = sortfields, ascending = sortorder)
        dfq = self.__df_alternatives

        working_df = sqldf(f"select {sqlfieldlist_str} from dfq;")

        defender_name = 'NOTHING'

        results = {}
        comparison_count = 1

        for index, row in working_df.iterrows():
            challenger = row.to_list()[len(insert_row):]
            if defender_name == 'NOTHING':
                defender_cf = Cashflow.from_list([0 for element in challenger if ((element is not None) and (np.isnan(element) == False))])
            challenger_name = row['alternative']
            challenger_cf = Cashflow.from_list([element for element in challenger if ((element is not None) and (np.isnan(element) == False))])

            [winner, delta_irr] = self.__compare_pair(challenger_name, challenger_cf, defender_name, defender_cf)

            results[comparison_count] = {'comparison': comparison_count,
                                            'defender': defender_name,
                                            'challenger': challenger_name,
                                            'winner': winner,
                                            'Delta IRR': delta_irr,
                                            'MARR': self.__marr}
            
            comparison_count += 1

            if winner == challenger_name:
                defender_name = challenger_name
                defender_cf = challenger_cf

            
        df_results = pd.DataFrame(columns = ['comparison', 'defender', 'challenger', 'winner', 'Delta IRR', 'MARR'])
        for result in results.keys():
            df_results.loc[len(df_results)] = results[result]

        self.__results = df_results

        if self.__outputfile is not None:
            with pd.ExcelWriter(self.__outputfile) as writer:
                self.__df_alternatives.to_excel(writer, sheet_name = 'alternatives listing', index = False)
                df_results.to_excel(writer, sheet_name = 'pairwise comparisons', index = False)

        return
    
class IncrementalBCR():

    def __init__(self, outputfile: str = None, marr: float = None):

        self.__outputfile = outputfile
        self.__df_alternatives = pd.DataFrame()
        self.__alternatives = {}
        self.__results = pd.DataFrame()
        self.__marr = marr

    def add_alternative(self, altname: str, cf_benefit: 'Cashflow', cf_cost: 'Cashflow'):
        if cf_benefit.same_horizon(cf_cost) == False:
            raise Exception(f"The cost and benefit cashflows for alternative {altname} do not have the same horizon.")
        self.__alternatives[altname] = [cf_benefit, cf_cost]
        return

    def del_alternative(self, altname: str, fail_silent: bool = False):
        if altname in self.__alternatives.keys():
            del self.__alternatives[altname]
        elif fail_silent == False:
            raise Exception(f"Alternative {altname} does not exist.")
        return
    
    def ingest_file(self, file: str):
        partial_benefits = {}
        partial_costs = {}
        entries = Cashflow.fetch_entries(file)

        for entry in entries.keys():
            if entry[-3] == '$B$' or entry[-3] == '$C$':
                basename = entry[0:-3]
                hold_cf = entries[entry]
                if hold_cf.npv() <= 0:
                    partial_costs[basename] = hold_cf
                else:  
                    partial_benefits[basename] = hold_cf


            names_costs = partial_costs.keys()
            names_benefits = partial_benefits.keys()

            names_common = list(set(names_costs) & set(names_benefits))

            for name in names_common:
                self.add_alternative(name, partial_benefits[name], partial_costs[name])

        return


    def list_alternatives(self):
        return list(self.__alternatives.keys())
    
    def fetch_alternatives(self):
        return self.__df_alternatives
    
    def fetch_pairwise(self):
        return self.__results

    
    def get_marr(self):
        return self.__marr
    
    def set_marr(self, marr: float):
        self.__marr = marr
        return
    
    def get_outputfile(self):
        return self.__outputfile
    
    def set_outputfile(self, outputfile: str):
        self.__outputfile = outputfile
        return
    
    def prep_irr(self):
        irr = IncrementalIRR(marr = self.__marr)
        for alt in self.__alternatives.keys():
            [cf_benefit, cf_cost] = self.__alternatives[alt]
            irr.add_alternative(altname = alt, cfd = cf_benefit + cf_cost)
        return irr       
    
    def generate(self):
        marr = self.__marr
        self.__df_alternatives = pd.DataFrame()
        self.__results = pd.DataFrame()

        fields_df = ['alternative', 'MARR',
                     'PW(benefit)', 'PW(cost)', 'NPW', 
                     'EUAB', 'EUAC', 'EUAW', 'CBR',
                     'IRR', 'payback period', 'discounted payback period']

        self.__df_alternatives = pd.DataFrame(columns = fields_df)

        for alt in self.__alternatives.keys():
            f_marr = self.__marr
            [cf_benefit, cf_cost] = self.__alternatives[alt]
            cf_benefit.set_rate(f_marr)
            cf_cost.set_rate(f_marr)
            cf_net = cf_benefit + cf_cost
            cf_net.set_rate(f_marr)
            f_pw_benefit = cf_benefit.npv()
            f_pw_cost = cf_cost.npv()
            f_npw = cf_net.npv()
            f_euab = cf_benefit.nus()
            f_euac = cf_cost.nus()
            f_euaw = cf_net.nus()
            f_cbr = abs(f_euab/f_euac)
            f_irr = cf_net.irr()
            f_payback = cf_net.payback()
            f_payback_disc = cf_net.payback_disc()   
            new_record = [alt, f_marr, 
                          f_pw_benefit, f_pw_cost, f_npw,
                          f_euab, f_euac, f_euaw, f_cbr,
                          f_irr, f_payback, f_payback_disc]
            df_entry = pd.Series(dict(zip(fields_df,new_record))).to_frame().transpose()
            self.__df_alternatives = pd.concat([self.__df_alternatives, df_entry], ignore_index=True)

        self.__df_alternatives.sort_values(by='EUAC', inplace=True, ascending = False)

        comparison_fields = ['comparison', 'defender', 'challenger', 'winner', 'incremental BCR', 'MARR']
        f_defender = {'alternative': 'NOTHING', 'EUAB': 0, 'EUAC': 0}
        f_comparison = 0
        df_alternatives = self.__df_alternatives

        for challenger in df_alternatives['alternative'].to_list(): 
            f_comparison += 1
            f_challenger = sqldf(f"select alternative, EUAB, EUAC from df_alternatives where alternative = '{challenger}';").transpose().to_dict()[0]
            f_defender_name = f_defender['alternative']
            f_challenger_name = f_challenger['alternative']
            f_incremental_bcr = abs((f_challenger['EUAB'] - f_defender['EUAB'])/(f_challenger['EUAC'] - f_defender['EUAC']))
            if f_incremental_bcr > 1.0:
                f_winner_name = f_challenger_name
                f_defender = copy.deepcopy(f_challenger)
            else:
                f_winner_name = f_defender_name
            new_record = [f_comparison, f_defender_name, f_challenger_name, f_winner_name, f_incremental_bcr, self.__marr]

            df_result = pd.Series(dict(zip(comparison_fields, new_record))).to_frame().transpose()
            self.__results = pd.concat([self.__results, df_result], ignore_index=True)

        if self.__outputfile is not None:
            with pd.ExcelWriter(self.__outputfile) as writer:
                self.__df_alternatives.to_excel(writer, sheet_name = 'alternatives listing', index = False)
                self.__results.to_excel(writer, sheet_name = 'pairwise comparisons', index = False)

        

    












