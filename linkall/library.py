import csv
import numpy as np

def renew(datas, betas, alpha):
    betas = list(betas)
    tempSum = [0, 0, 0]
    for data in datas:
        for i in range(len(betas)):
            tempSum[i] += predict(data, betas) * data[i]
    for i in range(len(betas)):
        betas[i] -= alpha * tempSum[i] / len(datas)
    return betas

def predict():
    alpha = 0.085
    iteration = 100
    with open('~/data/1.csv') as f:
        data = parse(csv.reader(f))
        pass

def ana(datas):
    u = sum(datas) / len(datas)
    s = 0
    for data in datas:
        s += (data - u) ** 2
    s = s / len(datas)
    s = s ** 0.5
    return (s, u)

def parse(data):
    data = list(data)

    times = []
    weights = []
    for row in data:
        times.append(int(row[0]))
        weights.append(int(row[1]))
    
    times_std = np.std(times, ddof=1)
    times_mean = np.mean(times)
    weights_std = np.std(weights, ddof=1)
    weights_mean = np.mean(weights)

    parsedData = []
    for row in data:
        nvRow = [1]
        for i in range(len(row)-1):
            nvRow.append((float(row[i])-u[i])/s[i])
        nvRow.append(float(row[-1]))
        parsedData.append(nvRow)

    return parsedData