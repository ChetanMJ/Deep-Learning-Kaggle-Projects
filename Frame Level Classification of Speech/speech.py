# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 18:45:49 2019

@author: cheth
"""

import numpy as np
import torch
import sys
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch.utils import data
from torchvision import transforms
from torchvision.datasets import MNIST

import matplotlib.pyplot as plt
import time

cuda = torch.cuda.is_available()
cuda



import numpy as np


path = "C:\\Users\\cheth\\OneDrive\\Documents\\DeepLearning\\HW1\\Part2\\11-785hw1p2-f19.tar\\11-785hw1p2-f19\\11-785hw1p2-f19"

x = np.load(path+"\\dev.npy", allow_pickle = True)
y = np.load(path+"\\dev_labels.npy",allow_pickle = True )

print(y.shape)
print(y[0].shape)
print(y[0][0])

'''
k= 1
feature_length = 40

#final_input = np.zeros((1,(((2*k) + 1) * feature_length)), dtype = float)

f = open('dev_input.txt', 'w')
f.close()

total_length = 0

with open('dev_input.txt', 'a+') as outfile:
    for i in range(len(x)):
        #print(i)
        utterance_length = x[i].shape[0]
        total_length = total_length + utterance_length        
        zero_padding = np.zeros((k,40), dtype = float)
        input_tmp = np.append(zero_padding,x[i], axis = 0 )
        input = np.append(input_tmp,zero_padding, axis = 0 )
        flat_utterance = input.flatten()
    
        for j in range(utterance_length):
            tmp1 = flat_utterance[(j*feature_length) : ((((2*k) + 1) * feature_length) + (j*feature_length))]
            tmp2 = tmp1.reshape(1,(((2*k) + 1) * feature_length))
            np.savetxt(outfile,tmp2)
            

with open('dev_labels.txt', 'a+') as outfile:
    for i in range(len(y)):
        print(i)
        utterance_length = y[i].shape[0]
    
        for j in range(utterance_length):
            np.savetxt(outfile,np.array([y[i][j]]))     

  '''

#final_input =   final_input[1:, :]
#z = np.load('dev_input.txt', allow_pickle = True)
dev_data = np.loadtxt('dev_input.txt', delimiter=' ')
print(dev_data.shape)

dev_labels = np.loadtxt('dev_labels.txt', delimiter=' ')
print(dev_labels.shape)

