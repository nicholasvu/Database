import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt

plt.figure()
test_data = np.random.normal(size=1000)   
graph1 = stats.probplot(test_data, dist="norm", plot=plt)
plt.show() #this will generate the first graph
