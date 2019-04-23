import numpy as np
import matplotlib.pyplot as plt
import random

#calculates average mu and sigma of N_sim simulations
def parameters_estimation(mu, sigma, N_sim):     #N_sim = number of simulations to make

    average_volatility = 0.0
    average_mu = 0.0

    mu_estimation_data = [0.0]*N_sim
    sigma_estimation_data = [0.0]*N_sim    #list that contains all sigma estimation data

    for n in range(0,N_sim):

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
        average_mu = average_mu + drift
        mu_estimation_data[n] = drift

        #volatility
        ds = [100.0]*N
        var = [0.0]*(N)
        for i in range(1,N):
            ds[i] = s[i]-s[i-1]
            var[i] = ds[i]*ds[i]/(s[i]*s[i]*dt)

        volatility = np.sqrt(np.mean(var))  #estimated volatility
        average_volatility = average_volatility + volatility
        sigma_estimation_data[n] = volatility

    average_volatility = average_volatility/N_sim
    average_mu = average_mu/N_sim

    results = [0.0]*2  #2D list

    results[0] = [0.0]*2    #index 0 = mean of volatility and mu
    results[1] = [0.0]*2    #index 1 = sd of volatility and mu

    results[0][0] = average_volatility
    results[0][1] = average_mu
    results[1][0] = np.std(sigma_estimation_data)
    results[1][1] = np.std(mu_estimation_data)

    return results



def calculate_accuracy(actual, measured):
    if measured < actual:
        return measured/actual
    else:
        return actual/measured


def parameters_estimation2(mu, sigma, N_sim):     #N_sim = number of simulations to make

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
    results[1] = calculate_accuracy(mu, drift)
    return result


#analyze accuracy in function of N_sim
N_sim = 1000
accuracy_sigma = [0.0]*N_sim
accuracy_mu = [0.0]*N_sim
mu_sd = [0.0]*N_sim #standard deviation values
sigma_sd = [0.0]*N_sim

for i in range(0,N_sim):
    results = parameters_estimation(0.01,0.1,i+1)
    sigma = results[0][0]
    mu = results[0][1]
    accuracy_sigma[i] =  calculate_accuracy(0.1,sigma)
    accuracy_mu[i] =  calculate_accuracy(0.01,mu)

plt.plot(n, accuracy_sigma)
plt.ylabel("accuracy")
plt.xlabel("n")
plt.title(r"accuracy of $\sigma$")
plt.show()

plt.plot(n, accuracy_mu)
plt.ylabel("accuracy")
plt.xlabel("n")
plt.title(r"accuracy of $\mu$")
plt.show()

s = input("exit:")

#plt.plot(t,s)
#plt.show()
