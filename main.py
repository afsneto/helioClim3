from helioClim3 import helioclim3


file1 = 'SOBRADINHO-BA_HC3-METEOhour_lat-9.619_lon-40.910_2004-02-01_2019-11-28_hz1.csv'
file2 = 'NORTE-MINAS_HC3-METEOhour_lat-15.576_lon-43.591_2004-02-01_2019-11-28_hz1.csv'

data = helioclim3(file1)

d1 = '2005-02-01'
d2 = '2006-02-02'
# data.plot(d1, d2)
# data.analysis()
data.averSolarIrrad()
