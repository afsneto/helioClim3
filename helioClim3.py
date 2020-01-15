import numpy as np
import pandas as pd
from pandas.tseries import converter

from tqdm import tqdm
from datetime import datetime
from calendar import monthrange

import matplotlib.pyplot as plt
import seaborn as sns

import swifter


class helioclim3:
    def __init__(self, fileinput):
        self.fileinput = fileinput

        # fix hour format 24:00:00
    def fixHours(self, str_datetime):
        if '24:' in str_datetime:
            str_datetime = str_datetime.replace(
                ':00', '', 1).replace('24:', '00:')
            return pd.to_datetime(str_datetime, format='%d/%m/%Y %H:%M')
        else:
            return pd.to_datetime(str_datetime, format='%d/%m/%Y %H:%M')

    def loading(self):
        df = pd.read_csv(self.fileinput, skiprows=31, sep=";",
                         parse_dates=[['# Date', 'Time']])

        df.rename(columns={"# Date_Time": "Date"}, inplace=True)
        df["Temperature"] = [(i - 273.15)
                             for i in df["Temperature"]]  # Temperature °F to °C
        return df

    def processing(self, datafix=True):
        df = self.loading()
        if datafix:
            df.replace(to_replace=-999, value=0, inplace=True)
        else:
            pass

        tqdm.pandas()
        # df.loc[:, "Date"] = df.Date.progress_apply(self.fixHours)
        df.loc[:, "Date"] = df.Date.swifter.apply(self.fixHours)
        # Assign "Date" column to index
        df.set_index("Date", inplace=True)
        return df

    def plot(self, date1: str, date2: str, data='Global Horiz'):
        df = self.processing(datafix=True)
        converter.register()

        d1 = datetime.strptime(date1, '%Y-%m-%d')
        d2 = datetime.strptime(date2, '%Y-%m-%d')

        df2plot = df.loc[d1:d2]
        sns.set(style="darkgrid")
        f, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x=df2plot.index, y=df2plot[data])

        # Removing top and right borders
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Finalize the plot
        sns.despine(bottom=True)
        plt.setp(f.axes, xticks=[],
                 xlabel='Interval\nfrom: {0}\nto: {1}'.format(date1, date2),
                 ylabel='Solar Irradiation (W/m²)')
        plt.tight_layout(h_pad=2)

        plt.savefig("output.png")
        print('Image saved.')

    def analysis(self):
        df = self.processing(datafix=False)
        noIrrad = df[df['Global Horiz'] == -999]
        noIrradDays = noIrrad.index.date
        noDataIrrad = len(noIrradDays)
        totalIrrad = len(df['Global Horiz'])
        percDataIrrad = (noDataIrrad/totalIrrad) * 100

        print('Número de linhas sem dados de irradiação: {0}'.format(
            noDataIrrad))
        print('Número total de linhas: {0}'.format(totalIrrad))
        print('Porcentagem de linhas sem dados de irradiação: {0:2.4f} %'.format(
            percDataIrrad))

        print('\nDias do ano sem registro de irradiação:')
        for i in sorted(set(noIrradDays)):
            print(i.strftime('%d/%m/%Y'))

        code = [0, 1, 2, 5, 6]
        numberbyCode = {i: len(df[df["Code"] == i]) for i in code}
        idbyCode = {0: 'no data', 1: 'sun below horizon',
                    2: 'satellite assessment', 5: 'interpolation in time', 6: 'forecast'}

        for i in numberbyCode.keys():
            print("{0}: {1} - {2:2.1f}%".format(
                idbyCode[i], numberbyCode[i], (numberbyCode[i] / totalIrrad)*100))

    def averSolarIrrad(self, freq='H'):
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#anchored-offsets

        df = self.processing()

        # Calculo da media para cada mes
        Wh_m2_mes = df.groupby(df.index.month).mean()['Global Horiz']
        kWh_m2_dia = df.groupby(df.index.month).mean()[
            'Global Horiz'] * 24/1000
        Months = Wh_m2_mes.index.to_list()

        result = {'kWh/m²_Diário': kWh_m2_dia,
                  'kWh/m²_Mensal': Wh_m2_mes, 'Month': Months}
        dfIrrad = pd.DataFrame(result)
        print(dfIrrad)
        print('Média diária Irradiação Solar: {0:.2f} kWh/m²/dia'.format(
            dfIrrad.loc[:, 'kWh/m²_Diário'].mean()))

        # kWh_Day = []
        # daysinMonth = []
        # kWh_Month = []
        # Month = []

        # # dfDay = dfHour.resample('D').mean()*24/1000
        # # kWh_Day.append(dfDay[dfDay.index.month == i].mean())

        # for i in sorted(set(dfMonth.index.month)):
        #     Month.append(int(i))
        #     # kWh_Day: media mensal considerando todos os anos
        #     kWh_Day.append(dfMonth[dfMonth.index.month == i].mean())
        #     # daysinMonth: numero de dias para cada mês
        #     daysinMonth.append(monthrange(dfMonth.index.year.max(), i)[1])

        #     kWh_Month.append(dfMonth[dfMonth.index.month == i].mean(
        #     ) * monthrange(dfMonth.index.year.max(), i)[1])

        # result = {'kWh/m²_Diário': kWh_Day,
        #           'kWh/m²_Mensal': kWh_Month, 'Month': Month}

        # dfIrrad = pd.DataFrame(result)

        # print(dfIrrad.head(12))
        # print('Média diária Irradiação Solar: {0:.2f} kWh/m²/dia'.format(
        #     dfIrrad.loc[:, 'kWh/m²_Diário'].mean()))
