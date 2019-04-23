import numpy as np
import matplotlib.pyplot as plt
import random

#investigate accuracy of parameter measurements with data size

def calculate_accuracy(actual, measured):
    if measured < actual:
        return measured/actual
    else:
        return actual/measured

#returns the accuracy of the mu and sigma estimation after 1 simulation
def run_sim(mu, sigma, N):     #N = size of data

    #maxT = 1.0 #years
    dt = 1/252  #252 trading days in a year
    maxT = float(N)*dt
    s  = [100]*N #list of states
    t = [0.0]*N  #list of time variable

    for i in range(1,N):
        w = np.random.normal(0.0,np.sqrt(dt))
        delta = s[i-1]*(  mu*dt+sigma* w)
        s[i] = s[i-1] + delta
        t[i] = t[i-1]+dt

    #calculate mu
    R = [0.0]*(N-1)
    drift = 0.0
    for i in range(1,N):
        R[i-1] = (s[i]-s[i-1])/s[i-1]
        drift = drift + R[i-1]

    drift = drift/len(R)
    drift = drift/dt    #annualized drift

    #volatility
    ds = [100.0]*N
    var = [0.0]*(N)
    for i in range(1,N):
        ds[i] = s[i]-s[i-1]
        var[i] = ds[i]*ds[i]/(s[i]*s[i]*dt)

    volatility = np.sqrt(np.mean(var))  #estimated volatility

    results = [0.0]*2   #index 0 = accuracy of sigma, index 1 = accuracy of volatility
    results[0] = calculate_accuracy(sigma, volatility)
    results[1] = calculate_accuracy(abs(mu), drift)
    return results


N = 1000
accuracy_sigma = [0.0]*N
accuracy_mu = [0.0]*N

for i in range(2,N+2):
    results = run_sim(0.01,0.1, i)
    sigma = results[0]
    mu = results[1]
    accuracy_sigma[i-2] = sigma
    accuracy_mu[i-2] = mu

N = range(1,N+1)
plt.plot(N,accuracy_sigma)
plt.title(r"accuracy of $\sigma$")
plt.xlabel("N")
plt.ylabel("accuracy")
plt.show()

plt.plot(N,accuracy_mu)
plt.title(r"accuracy of $\mu$")
plt.xlabel("N")
plt.ylabel("accuracy")
plt.show()
