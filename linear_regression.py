import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import statsmodels.api as sm

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
#Remove any empty cells in the data set

loansData.dropna(inplace=True)

#Create a new set of interest rates, removing the % from the interest rate and converting it into a 4-digit decimal
cleanRate = loansData['Interest.Rate'].map(lambda x: round((float(x.rstrip('%')) / 100), 4))

#Create a new set of loan lengths with the word "months" removed
noMonths = loansData['Loan.Length'].map(lambda x: x.rstrip('months'))

#...FICO scores by picking the first value out of the range
cleanFICO = loansData['FICO.Range'].map(lambda x: int(x.split('-')[0]))

#replace Interest.Rate and Loan.Length with the cleaned versions, and add FICO.Score as a new column (NOTE:this way only works if you know tha the index values of the DataFrame are continuous. If you are dealing with non-continuous index values, see http://stackoverflow.com/questions/12555323/adding-new-column-to-existing-dataframe-in-python-pandas for the proper solution)
loansData['FICO.Score'] = cleanFICO
loansData['Interest.Rate'] = cleanRate
loansData['Loan.Length'] = noMonths

#Create the histogram

plt.figure()
p = loansData['FICO.Score'].hist()
plt.show()
plt.clf()

# Note - if we had wanted to rotate the x-axis labels, we could've used: plt.xticks(rotation='vertical')

# Create a scatterplot of the data to locate any trends / interrelationships between column data
scat = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
plt.show()

intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

#the dependent variable
y = np.matrix(intrate).transpose()
#The independent variables shaped as columns
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

x = np.column_stack([x1,x2])
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

plt.scatter(x1, y)
plt.ylabel('Interest Rate')
plt.xlabel('FICO Scores')
plt.show()

f.summary()
print(f.summary())
