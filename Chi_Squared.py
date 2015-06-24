from scipy import stats
import collections
import pandas as pd
import matplotlib.pyplot as plt


#Load the reduced version of the Lending Club Dataset
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dropna(inplace=True)

freq = collections.Counter(loansData['Open.CREDIT.Lines'])
plt.figure()
plt.bar(freq.keys(), freq.values(), width=1)
plt.show()

chi, p = stats.chisquare(freq.values())
print 'The result of the chi-squared test on the Open.CREDIT.Lines data is {}, with a p-value of {}'.format(chi,p)
