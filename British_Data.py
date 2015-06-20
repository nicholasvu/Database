import numpy as np
import pandas as pd
from StringIO import StringIO
from scipy import stats

datastring = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.52, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

data = datastring.splitlines()
data = [i.split(', ') for i in data]

column_names = data[0]
data_rows = data[1::]
df = pd.DataFrame(data_rows, columns=column_names)
df.head()

df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)


alc_mean = df['Alcohol'].mean()
alc_med = df['Alcohol'].median()
tob_mean = df['Tobacco'].mean()
tob_med = df['Tobacco'].median()
stats.mode(df['Tobacco'])
stats.mode(df['Alcohol'])

alc_std = df['Alcohol'].std()
alc_var = df['Alcohol'].var()
max(df['Tobacco']) - min(df['Tobacco'])
tob_std = df['Tobacco'].std()
tob_var = df['Tobacco'].var()

alc_range = max(df['Alcohol']) - min(df['Alcohol'])
tob_range = max(df['Tobacco']) - min(df['Tobacco'])
tob_mode = stats.mode(df['Tobacco'])
alc_mode = stats.mode(df['Alcohol'])


msg = " {:.3f} for Alcohol and {:.3f} for Tobacco \n"

print "The ranges for the Alcohol and Tobacco dataset are" + msg.format(alc_range, tob_range)
print "The modes for the Alcohol and Tobacco dataset are " + msg.format(alc_mode[0][0], tob_mode[0][0])
print "The means for the Alcohol and Tobacco dataset are " + msg.format(alc_mean, tob_mean)
print "The medians for the Alcohol and Tobacco dataset are " + msg.format(alc_med, tob_med)
print "The standard deviation for the Alcohol and Tobacco dataset are " + msg.format(alc_std, tob_std)
print "The variance for the Alcohol and Tobacco dataset are " + msg.format(alc_var, tob_var)
