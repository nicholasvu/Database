import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt

plt.figure()
test_data2 = np.random.uniform(size=1000)   
graph2 = stats.probplot(test_data2, dist="norm", plot=plt)
plt.show() #this will generate the second graph
plt.figure()

