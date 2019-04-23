import numpy as np
import matplotlib.pyplot as plt

dt = 1/252
maxT = dt*5166
N = (int )(maxT/dt)

fp = open("EUR-USD.txt","r")

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

#fourier transform
ft = [0.0]*len(data)
ft = np.fft.fft(data)

ft = np.abs(ft)/N

freq = [0.0]*len(data)
freq = np.fft.fftfreq(N, dt)

#sort data
sorted_indices = [1]*N
sorted_indices = sorted(range(len(freq)),key=freq.__getitem__)

temp_freq  = [0.0]*N
temp = [0.0]*N

for i in range(0,N):
    temp_freq[i] = freq[i]
    temp[i] = ft[i]

for i in range(0,N):
    ft[i] = temp[sorted_indices[i]]
    freq[i] = temp_freq[sorted_indices[i]]

#output the data
fp = open("fft.txt","w")
for i in range(0,len(data)):
    fp.write(str(data[i]) + '\t'+str(ft[i])+'\t'
    + str(freq[i])+'\n')

fp.close()

#Find peaks

peaks = []
freq_peaks = []
dft = [0.0]*N
dfreq = freq[2]-freq[1]

#Method 1 - brute force

#for i in range(1,N-1):
    #if ft[i] > ft[i+1] and ft[i] > ft[i-1]:
        #peaks.append(ft[i])
        #freq_peaks.append(freq[i])

#Method 2 - derivative methods
for i in range(1,N-1):
    dft[i] = (ft[i+1]-ft[i-1])/(2*dfreq)
    if dft[i] == 0.0:
        if ft[i] > ft[i+1] and ft[i] > ft[i-1]:
            peaks.append(ft[i])
            freq_peaks.append(freq[i])

fp = open("peaks.txt","w")
for i in range(0,len(peaks)):
    fp.write(str(peaks[i])+'\t'+str(freq_peaks[i])+'\n')
fp.close()
