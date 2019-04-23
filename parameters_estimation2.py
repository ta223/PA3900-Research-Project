import numpy as np
import matplotlib.pyplot as plt
import random


def calculate_accuracy(actual, measured):
    if measured < actual:
        return measured/actual
    else:
        return actual/measured

#returns the accuracy of the mu and sigma estimation after 1 simulation
def parameters_estimation2(mu, sigma):     #N_sim = number of simulations to make

    maxT = 1.0 #years
    dt = 1/252  #252 trading days in a year
    N = int(maxT/dt)
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


N_sim = 1000
accuracy_sigma = [0.0]*N_sim
mean_accuracy_sigma = 0.0
mean_accuracy_mu = 0.0
accuracy_mu = [0.0]*N_sim

for i in range(0,N_sim):
    results = parameters_estimation2(0.01,0.1)
    sigma = results[0]
    mu = results[1]
    #fix this crap
    #accuracy_sigma[i] =  calculate_accuracy(0.1,sigma)
    #accuracy_mu[i] =  calculate_accuracy(0.01,mu)
    mean_accuracy_mu = mean_accuracy_mu + mu #accuracy_mu[i]
    mean_accuracy_sigma = mean_accuracy_sigma + accuracy_sigma[i]

mean_accuracy_mu = mean_accuracy_mu/N_sim
mean_accuracy_sigma = mean_accuracy_sigma/N_sim
print(mean_accuracy_mu)
print(mean_accuracy_sigma)
    
    
