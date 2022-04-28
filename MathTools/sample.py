# -*- coding:UTF-8 -*-

from scipy.stats import norm
import numpy as np


def normal(_, mean, cv):

    return norm.ppf(_)* cv * mean + mean


def uniform(_, mean, cv):

    return mean * (1 - cv) + _ * mean * cv * 2


def LHS(N, mean, cv, dis):

    dic = {'Normal': normal,
           'Uniform': uniform}

    result = np.empty([N])
    d = 1.0 / N
    for j in range(N):
        result[j] = np.random.uniform(low=j * d, high=(j + 1) * d, size=1)[0]
    np.random.shuffle(result)

    result = dic[dis](result, mean, cv)
    return result


def EZrandom(N, mean, cv, dis):
    if dis == 'Uniform':
        return np.random.uniform(low=mean*(1-cv),high=mean*(1+cv),size=N)
    elif dis == 'Normal':
        return np.random.normal(loc=mean, scale=mean*cv, size=N) 


def sample(N, mean, cv, dis, sample_way):
    sampledic = {True: LHS,
                 False: EZrandom}
    return sampledic[sample_way](N, mean, cv, dis)



if __name__ == '__main__':
    tuple = ((10, 20, 30, 0.1), (40, 50, 60, 0.2))
    Plastic_arr = np.zeros([2, 3, 100])
    for num, i in enumerate(tuple):
        for j in range(3):
            Plastic_arr[:][num][j] = sample(100, i[j], i[-1], 'Normal', False)
    Plastic_arr = np.reshape(Plastic_arr, (6,100))
    np.savetxt('test.csv', Plastic_arr.T, delimiter=',')
