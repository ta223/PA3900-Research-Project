import numpy as np
import random
import matplotlib.pyplot as plt
import os

def calculate_accuracy(actual, measured):
    if measured < actual:
        return measured/actual
    else:
        return actual/measured

os.chdir("historical data")
files = ["EUR-USD.txt","Airbus.txt","Apple.txt","AUDI.txt","BMW.txt","Deutsche Bank.txt","EUR-GBP.txt","Ford.txt","GBP-USD.txt","Gold.txt","IBM.txt","JPMorgan.txt","JPY-USD.txt","Microsoft.txt","Oil-Brent.txt"]
asset_names = ["EUR-USD","Airbus","Apple","AUDI","BMW","Deutsche Bank","EUR-GBP","Ford","GBP-USD","Gold","IBM","J.P. Morgan","JPY-USD","Microsoft","Oil Brent"]


Nfiles = len(files)
Nassets = len(asset_names)
if Nfiles != Nassets:
    print("len_err")
else:
    print("len_ok")

dt = 1/252

os.chdir(r"C:\Users\Tanveer\Desktop\The Brownian motion and the financial markets\Geometric Brownian Motion\Python scripts\historical data\plots")
#variance_data = open("MC_variance.txt","w")

figure_counter = 0

def new_figure(fig_cntr):
    plt.figure(fig_cntr+1)
    return fig_cntr+1

N_SIM = 100000  #how many simulations to run to get Monte Carlo average

for file_num in range(0,Nfiles):
    os.chdir(r"C:\Users\Tanveer\Desktop\The Brownian motion and the financial markets\Geometric Brownian Motion\Python scripts\historical data")
    #read and store data----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    fp = open(files[file_num],"r")
    data = [0.0]*1
    line = fp.readline()
    line.replace('\n','')
    data[0] = float(line)

    while line:
        line = fp.readline()
        line.replace('\n','')
        try:
            data.append(float(line))
        except ValueError:
            break

    fp.close()

    N = len(data)
    maxT = dt*N

    #calculate mu----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    R = [0.0]*(N-1)
    drift = 0.0
    for i in range(1,N):
        R[i-1] = (data[i]-data[i-1])/data[i-1]
        drift = drift + R[i-1]

    drift = drift/len(R)
    drift = drift/dt    #annualized drift

    #volatility---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    initial_price = data[0]
    ds = [initial_price]*N
    var = [0.0]*(N)
    for i in range(1,N):
        ds[i] = data[i]-data[i-1]
        var[i] = ds[i]*ds[i]/(data[i]*data[i]*dt)

    volatility = np.sqrt(np.mean(var))  #estimated volatility

    #Run simulations-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    for n in range(0,N_SIM):

        mu = drift
        sigma = volatility
        s  = [initial_price]*N #list of states
        t = [0.0]*N  #list of time variable
        mean_s = [0.0]*N    #monte carlo mean

        for i in range(1,N):

            w = np.random.normal(0.0,np.sqrt(dt))
            delta = s[i-1]*(  mu*dt+sigma* w)
            s[i] = s[i-1] + delta
            t[i] = t[i-1]+dt

            #calculaate mean iteratively
            m = n+1
            mean_s[i] = mean_s[i]*n/m
            mean_s[i] = mean_s[i] + s[i]/m

    #calculate Monte Carlo variance_data
    mc_variance = 0.0
    for i in range(0,N):
        mc_variance = mc_variance + (mean_s[i]-s[i])*(mean_s[i]-s[i])

    mc_variance = mc_variance/N
    mc_variance = np.sqrt(mc_variance)
    variance_str = str(mc_variance)
    #str_ = str(mc_variance)
    #variance_data.write(asset_names[file_num] + ": " + str_ + "\n" )


    #plot results
    os.chdir(r"C:\Users\Tanveer\Desktop\The Brownian motion and the financial markets\Geometric Brownian Motion\Python scripts\historical data\MC plots")
    #main plot
    figure_counter = new_figure(figure_counter)
    plt.plot(t,mean_s,color="blue",label="MC")
    plt.plot(t,data,color="red",label="actual")
    plt.legend()
    plt.title(asset_names[file_num] + ", MC variance = " +  variance_str) 
    plt.xlabel("t (years)")
    plt.ylabel("price value")
    figname = asset_names[file_num] + "_main_plot_MC.png"
    plt.savefig(figname)

    plt.close('all')


