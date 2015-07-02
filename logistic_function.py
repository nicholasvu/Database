#This script will prompt the user for an interest rate, their FICO score, and a loan amount, and print the probability that Lending Club will offer them a loan with the provided information. It also prints the logarithmic optimization results.

#Import required libraries
import pandas as pd
import statsmodels.api as sm
import numpy as np

#Import the cleaned lending club data
loansData = pd.read_csv('loansData_clean.csv')
#Get the maximum interest rate from the user. Converts the interest rate to a decimal if the user provides an interest rate >1.

maxInterest = int(raw_input('What is the highest interest rate you can afford?'))
if maxInterest > 1:
    maxInterst = maxInterest / 100.00

# Create a column in the dataframe to hold a binary variable - whether or not the interest rate is below the user-specified interest rate. 0 indicates the value is less than or equal to the user-specified interest rate, 1 indicates the value is more.
def less_max(i):
    if i<= maxInterest:
        return 0
    else:
        return 1
#Create the column of data
ir_tf = loansData['Interest.Rate'].map(lambda x: less_max(x))

#Add the data to the dataframe
loansData['IR_TF'] = ir_tf

#Create an intercept column
loansData['Intercept'] = 1

#Create a list of column names of all independent variables
ind_vars = ['Amount.Funded.By.Investors', 'FICO.Score', 'Intercept']

#Define the logistic regression model
logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])

#Fit the model
result = logit.fit()

#Get the fitted coefficients from the results
coeff = result.params
print coeff

#This function will return p (the probability that you'll get a loan with an interest rate under 12% given your FICO score and the loan amount you're requesting). We're going to access the coefficients produced by the logit.fit() above, which outputs a series where 0, 1, and 2 are the indices for the coefficients of Loan.Amount, FICO.Score, and Intercept respectively.
loan_amt_c = coeff[0]
fico_c = coeff[1]
intercept_c = coeff[2]

def logistic_function(fico, loan_amt):
    return (1 / (1 + np.exp(intercept_c + (fico_c * fico) + (loan_amt_c * loan_amt))))

#Get the FICO Score and Loan Amount from the user
ficoScore = int(raw_input('What is your FICO score?'))
loanAmount = int(raw_input('How much money do you want to borrow?'))

#Calculate the probability that the user will get the loan using logistic_function()
p = logistic_function(ficoScore, loanAmount)
#Print the result
print "There is a {}% chance that Lending Club will offer you a ${} loan at an interest rate of {}% or less with a FICO score of {}.".format(p*100, loanAmount, maxInterest*100, ficoScore)
