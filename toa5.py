import numpy as np
import pandas as pd
from pandas.tseries import converter

from tqdm import tqdm
from datetime import datetime
from calendar import monthrange

import matplotlib.pyplot as plt
import seaborn as sns

import swifter

from time import time


class toa5:
    def __init__(self, fileinput):
        self.fileinput = fileinput

    #     # fix hour format 24:00:00
    # def fixHours(self, str_datetime):
    #     if '24:' in str_datetime:
    #         str_datetime = str_datetime.replace(
    #             ':00', '', 1).replace('24:', '00:')
    #         return pd.to_datetime(str_datetime, format='%d/%m/%Y %H:%M')
    #     else:
    #         return pd.to_datetime(str_datetime, format='%d/%m/%Y %H:%M')

    def loading(self):

        head = ['date', 'record', 'tempAr', 'umidRel', 'radSolar', 'radSolarAcu', 'velVento10m',
                'dirVento', 'dp_dirVento', 'velVentoMax', 'dirVento_smm', 'lWmV', 'seco_tot',
                'contam_Tot', 'molhado_Tot', 'RS_Kohms_Hst', 'Chuva_Tot', 'ETz', 'Rso']

        def dateparse(x): return pd.datetime.strptime(x, '%d/%m/%Y %H:%M')

        # df = pd.read_csv(self.fileinput, skiprows=4)

        # df = pd.read_csv(self.fileinput,
        #                  skiprows=[0, 2, 3],
        #                  header=1,
        #                  na_values='NAN',
        #                  parse_dates=True,
        #                  date_parser=dateparse)
        df = pd.read_csv(self.fileinput,
                         skiprows=5, sep=",",
                         na_values='NAN',
                         names=head,
                         parse_dates=True,
                         date_parser=dateparse)

        # df = pd.read_csv(self.fileinput,
        #                  #  header=0,
        #                  skiprows=lambda x: x in [0, 2, 3])

        print(len(head))

        return df

    # def loading2(self):

    #     start_time = time()

    #     head = ['date', 'record', 'tempAr', 'umidRel', 'radSolar', 'radSolarAcu', 'velVento10m',
    #             'dirVento', 'dp_dirVento', 'velVentoMax', 'dirVento_smm', 'lWmV', 'seco_tot',
    #             'contam_Tot', 'molhado_Tot', 'RS_Kohms_Hst', 'Chuva_Tot', 'ETz', 'Rso']

    #     df = pd.read_csv(self.fileinput,
    #                      skiprows=5, sep=",",
    #                      na_values='NAN',
    #                      names=head)

    #     final_time = time()

    #     print(final_time - start_time)
    #     return df


data = toa5('SOBRADINHO-TOA5_2019_2020.csv')
df = data.loading()
print(df.head())


# data.loading2()
