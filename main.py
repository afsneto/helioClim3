from hc3 import helioclim3
from pathlib import PureWindowsPath
from pathlib import Path
from windtemp import windtemp
from energycalc import energycalc

import matplotlib.pyplot as plt


file1 = 'SOBRADINHO-BA_HC3-METEOhour_lat-9.619_lon-40.910_2004-02-01_2019-11-28_hz1.csv'
file2 = 'NORTE-MINAS_HC3-METEOhour_lat-15.576_lon-43.591_2004-02-01_2019-11-28_hz1.csv'

file3 = r'D:\Analise_Dados_Solares\UFV Rio do Peixe\Séries de longo prazo (Helio-Clim3)\SAO_JOAO_DO_RIO_DO_PEIXE_HC3-METEO_10min_lat-6.725_lon-38.454_2004-02-01_2019-01-30_hz1.csv'
file4 = r'D:\Analise_Dados_Solares\UFV Rio do Peixe\Séries de longo prazo (Helio-Clim3)\SAO_JOAO_DO_RIO_DO_PEIXE_HC3-METEO_hour_lat-6.725_lon-38.454_2004-02-01_2019-01-30_hz1.csv'

# localdirectory = Path.cwd()
# input_file = str(PureWindowsPath(localdirectory, file3))


data = helioclim3(file4)

# d1 = '2005-02-01'
# d2 = '2006-02-02'
# data.plot(d1, d2)

# data.analysis()
# data.averSolarIrrad()

# data.save_boxplot_monthly()
# data.boxplot_mean_month_yearly()
# data.save_barplot_yearly_sns()
# data.savecsv_mean_month_yearly()
# data.describe_ghi()


# clima = windtemp(data.dfloaded())
# x, y, z = clima.windvalues(2, 50, 50)
# clima.tempvalues()


df = energycalc(data.dfloaded()).irradcalc()
plt.hist(df['I(A)'], bins=20)
plt.show()
