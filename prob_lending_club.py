import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dropna(inplace=True)

loansData.boxplot(column='Amount.Requested')
plt.title('Box Plot Amount Requested')
plt.show()

loansData.hist(column='Amount.Requested')
plt.title('Histogram Amount Requested')
plt.show()

plt.figure()
graph = stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt)
plt.title('QQ Plot Amount Requested')
plt.show()
