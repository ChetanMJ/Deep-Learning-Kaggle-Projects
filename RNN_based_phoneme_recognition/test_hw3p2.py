# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 21:39:43 2019

@author: cheth
"""


import numpy as np

path = "C:\\Users\\cheth\\OneDrive\\Documents\\DeepLearning\\HW3\\part2\\homework-3-part-2-11-785-fall-2019\\HW3P2_Data"
x = np.load(path+"\\wsj0_dev.npy", allow_pickle = True, encoding='bytes')
print(x.shape)
print(x[3].shape)
print(x[3][0,:])


y = np.load(path+"\\wsj0_dev_merged_labels.npy", allow_pickle = True)
print(y.shape)
print(y[3].shape)
print(y[3])


test = np.load(path+"\\wsj0_test.npy", allow_pickle = True, encoding='bytes')
print(test.shape)
print(test[3].shape)
print(test[3])