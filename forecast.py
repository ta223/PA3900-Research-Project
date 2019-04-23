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
file_pointer = open("cut off periods.txt","w")

figure_counter = 0

def new_figure(fig_cntr):
    plt.figure(fig_cntr+1)
    return fig_cntr+1
    

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

    #Run simulation-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    mu = drift
    sigma = volatility
    s  = [initial_price]*N #list of states
    t = [0.0]*N  #list of time variable
    accuracy = [0.0]*N

    cut_off_period = 0    #after how many days accuracy drops below 98% - do not allow more than 2% accuracy

    for i in range(1,N):
        w = np.random.normal(0.0,np.sqrt(dt))
        delta = s[i-1]*(  mu*dt+sigma* w)
        s[i] = s[i-1] + delta
        t[i] = t[i-1]+dt
        accuracy[i] = calculate_accuracy(data[i],s[i])
        if accuracy[i] < 0.98 and cut_off_period == 0:
            cut_off_period = i+1

    #calculate MAPE
    MAPE = 0.0
    cut_off_period_MAPE = 0 #after how many days MAPE goes beyond 10%
    MAPE_data = [0.0]*N

    for i in range(0,N):
        MAPE = MAPE + (data[i]+s[i])/data[i]
        MAPE_data[i] = MAPE/(i+1)
        if MAPE/(i+1) > 0.01 and cut_off_period_MAPE == 0:
            cut_off_period_MAPE = i+1

    MAPE = MAPE/N
    str1 = str(cut_off_period)
    str2 = str(cut_off_period_MAPE)
    msg = asset_names[file_num] + ": cut off period = " + str1 + ",  cut off period(MAPE):" + str2
    file_pointer.write(msg+"\n")

    #plot results
    os.chdir(r"C:\Users\Tanveer\Desktop\The Brownian motion and the financial markets\Geometric Brownian Motion\Python scripts\historical data\plots")
    #main plot
    figure_counter = new_figure(figure_counter)
    plt.plot(t,s,color="blue",label="simulated")
    plt.plot(t,data,color="red",label="actual")
    plt.legend()
    plt.title(asset_names[file_num])
    plt.xlabel("t (years)")
    plt.ylabel("price value")
    figname = asset_names[file_num] + "_main_plot.png"
    plt.savefig(figname)

    #accuracy plot
    figure_counter = new_figure(figure_counter)
    plt.plot(t,accuracy)
    plt.title(asset_names[file_num])
    plt.xlabel("t (years)")
    plt.ylabel("accuracy")
    figname = asset_names[file_num] + "_accuracy.png"
    plt.savefig(figname)

    #MAPE plot
    figure_counter = new_figure(figure_counter)
    plt.plot(t,MAPE_data)
    plt.title(asset_names[file_num])
    plt.xlabel("t (years)")
    plt.ylabel("MAPE")
    figname = asset_names[file_num] + "_MAPE.png"
    plt.savefig(figname)
    
    plt.close('all')


file_pointer.close()
