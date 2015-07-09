import pandas as pd
#key problem was to change it from pyplot to plt
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import seaborn as sns

df=pd.read_csv('LoanStats3c.csv', skiprows=1, low_memory = False)
df.dropna(inplace=True)
df.head()
#x = df['int_rate'].values means that you're converting it to an array which means map and lambda won't work
df['int_rate']
#mapping the function df['int_rate'] is needed to read strings
df['int_rate'] = df['int_rate'].map(lambda x: float(x.rstrip('%')))
print df['int_rate']
#df['int_rate'].hist() problem causes:
#/Users/nicholasvu/anaconda/lib/python2.7/site-packages/matplotlib/tight_layout.py:225: UserWarning: tight_layout : falling back to Agg renderer
 #warnings.warn("tight_layout : falling back to Agg renderer")"""

plt.hist(df['int_rate'].tolist(), normed = True)
plt.show()
#plt.hist(df['int_rate'], bin = 10, normed = True)

df.plot('annual_inc', 'int_rate', kind='scatter')
sns.jointplot('annual_inc', 'int_rate', data=df)
df['home_ownership'].unique()
#df['home_ownership'] = pd.Categorical(loansData.home_ownership).codes
sns.barplot(x='home_ownership', y='int_rate', data=df)
sns.lmplot('annual_inc', 'int_rate', data=df, hue='home_ownership')
model_l=sm.OLS.from_formula('int_rate ~ annual_inc', data=df)
results=model_l.fit()
results.summary()

model_2=sm.OLS.from_formula('int_rate ~ annual_inc + home_ownership', data=df)
results=model_2.fit()
results.summary()

model_3=sm.OLS.from_formula('int_rate ~ annual_inc * home_ownership', data=df)
results=model_3.fit()
results.summary()

results.resid.hist(bins=30)
