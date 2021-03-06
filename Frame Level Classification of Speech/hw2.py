# -*- coding: utf-8 -*-
"""Untitled.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sC3-NlhCc7vllnsoRdxgVkIB4n3wvC2G
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

from google.colab import drive
drive.mount('/content/drive')

"""**================New code Starts ======================================**"""

from google.colab import drive
drive.mount('/content/drive')

path = '/content/drive/My Drive/Colab Notebooks/data/'


input_file = "train.npy"
input_labels = "train_labels.npy"

#input_file = "dev.npy"
#input_labels = "dev_labels.npy"


train_inputs = np.load(path+input_file, allow_pickle = True)
train_labels = np.load(path+input_labels,allow_pickle = True )

train_utterance_lengths = np.zeros(1, dtype=int)

total_utterance_length = 0

for i in range(len(train_inputs)):
      total_utterance_length = total_utterance_length + train_inputs[i].shape[0]
      train_utterance_lengths = np.append(train_utterance_lengths, total_utterance_length)

      
train_utterance_lengths= train_utterance_lengths[1:] - 1
print(train_inputs.shape)
print(train_labels.shape)
print(train_utterance_lengths.shape)
print(train_utterance_lengths[0])
print(train_utterance_lengths[1])
print(train_inputs[1].shape)

input_file = "test.npy"



test_inputs = np.load(path+input_file, allow_pickle = True)

test_utterance_lengths = np.zeros(1, dtype=int)

total_utterance_length = 0

for i in range(len(test_inputs)):
      total_utterance_length = total_utterance_length + test_inputs[i].shape[0]
      test_utterance_lengths = np.append(test_utterance_lengths, total_utterance_length)

      
test_utterance_lengths= test_utterance_lengths[1:] - 1

class MyDataset(data.Dataset):
    def __init__(self, X, Y, Z, K):
        self.X = X 
        self.Y = Y
        self.Z = Z
        self.K = K
        
        #print(self.X.shape)
        #print(self.Y.shape)

    def __len__(self):
        return (np.max(self.Z) + 1)

    def __getitem__(self,index):
      
        utterance = np.digitize(index,self.Z,right=True)
        #print("index=",index, "Utterance=",utterance)
        
        if utterance > 0:
          previous_utterance_end_value = self.Z[utterance - 1]
          frame_index = (index - previous_utterance_end_value) - 1
        else:
          frame_index = index
        
        
        zero_padding = np.zeros((self.K,40), dtype = float)
        input_tmp = np.append(zero_padding,self.X[utterance], axis = 0 )
        input = np.append(input_tmp,zero_padding, axis = 0 )
      
        X = torch.tensor(input[frame_index:((2*self.K)+1 + frame_index)]).float().reshape(-1) #flatten the input
        Y = torch.tensor(self.Y[utterance][frame_index]).long().reshape(-1)
        
        #print(X.size())
        #print(Y)
        
        return X,Y

class MyDataset_test(data.Dataset):
    def __init__(self, X, Z, K):
        self.X = X 
        self.Z = Z
        self.K = K

    def __len__(self):
        return (np.max(self.Z) + 1)

    def __getitem__(self,index):
      
        utterance = np.digitize(index,self.Z,right=True)
        #print("index=",index, "Utterance=",utterance)
        
        if utterance > 0:
          previous_utterance_end_value = self.Z[utterance - 1]
          frame_index = (index - previous_utterance_end_value) - 1
        else:
          frame_index = index
        
        
        zero_padding = np.zeros((self.K,40), dtype = float)
        input_tmp = np.append(zero_padding,self.X[utterance], axis = 0 )
        input = np.append(input_tmp,zero_padding, axis = 0 )
      
        X = torch.tensor(input[frame_index:((2*self.K)+1 + frame_index)]).float().reshape(-1) #flatten the input
        
        #print(X.size())
        
        return X

num_workers = 0 if sys.platform == 'win32' else 2
    
# Training

#train_inputs_torch = torch.tensor(train_inputs, dtype=torch.float) 
#train_labels_torch = torch.tensor(train_labels, dtype=torch.float) 

train_inputs

train_dataset = MyDataset(train_inputs, train_labels, train_utterance_lengths, 13)

train_loader_args = dict(shuffle=True, batch_size=256, num_workers=num_workers, pin_memory=True) if cuda\
                    else dict(shuffle=True, batch_size=64)
train_loader = data.DataLoader(train_dataset, **train_loader_args)

# SIMPLE MODEL DEFINITION
class Simple_MLP(nn.Module):
    def __init__(self, size_list):
        super(Simple_MLP, self).__init__()
        layers = []
        self.size_list = size_list
        for i in range(len(size_list) - 2):
            if (i == 0):
              layers.append(nn.BatchNorm1d(size_list[i]))
              
            layers.append(nn.Linear(size_list[i],size_list[i+1]))
            layers.append(nn.ReLU())
            layers.append(nn.BatchNorm1d(size_list[i+1]))
            layers.append(nn.Dropout(p=0.1))


            
        layers.append(nn.Linear(size_list[-2], size_list[-1]))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)

def init_randn(m):
    if type(m) == nn.Linear:
        m.weight.data.normal_(0,1)

model = Simple_MLP([1080,1200,1200,1200,1200,1000, 900, 900, 138])
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())
#scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=4, gamma=0.1)
device = torch.device("cuda" if cuda else "cpu")
print(model)

def train_epoch(model, train_loader, criterion, optimizer, lr):
    model.train()
    model.to(device)

    running_loss = 0.0
    
    start_time = time.time()
    for batch_idx, (data, target) in enumerate(train_loader):   
        optimizer.zero_grad() # .backward() accumulates gradients
        optimizer.learning_rate = lr
        data = data.to(device)
        target = target.to(device) # all data & model on same device

        outputs = model(data)
        
        #print("outputs")
        #print(outputs.size())
        #print("Target")
        target = target.reshape(-1)
        #print(target.size())
        
        loss = criterion(outputs, target)
        running_loss += loss.item()

        loss.backward()
        optimizer.step()
    
    end_time = time.time()
    
    running_loss /= len(train_loader)
    print('Training Loss: ', running_loss, 'Time: ',end_time - start_time, 's')
    return running_loss

def test_model2(model, test_loader, criterion):
    with torch.no_grad():
        model.eval()
        model.to(device)

        with open("final_output.txt", 'a+') as outfile:
          i = 0
          
          z = np.zeros((1,1,2))
          
          for batch_idx, (data) in enumerate(test_loader):   
              data = data.to(device)

              outputs = model(data)

              _, predicted = torch.max(outputs.data, 1)
              x = np.ndarray.flatten(predicted.data.cpu().numpy())
            
              y = np.append(i,x)
            
              z = np.append(z,y.reshape(1,1,2),axis=0)
            
              i = i + 1
              
    return z

test_dataset = MyDataset_test(test_inputs, test_utterance_lengths, 13)

test_loader_args = dict(shuffle=False, batch_size=1)

test_loader = data.DataLoader(test_dataset, **test_loader_args)

cd '/content/drive/My Drive/Colab Notebooks/data/'

import math
def step_decay(epoch):
    initial_lrate = 0.1
    drop = 0.5
    epochs_drop = 10.0
    lrate = initial_lrate * math.pow(drop,  
           math.floor((1+epoch)/epochs_drop))
    return lrate

step_decay(10)

pathx = '/content/drive/My Drive/Colab Notebooks/data/'

def step_decay(epoch):
    initial_lrate = 0.1
    drop = 0.5
    epochs_drop = 10.0
    lrate = initial_lrate * math.pow(drop,  
           math.floor((1+epoch)/epochs_drop))
    return lrate



n_epochs = 17

Train_loss = []

for i in range(n_epochs):
    train_loss = train_epoch(model, train_loader, criterion, optimizer,step_decay(i))
    #test_loss, test_acc = test_model(model, test_loader, criterion)
    Train_loss.append(train_loss)
    '''
    print("saving")
    torch.save({
         'epoch': i,
         'model_sate_dict':model.state_dict(),
         'optimizer_state_dict':optimizer.state_dict(),
         'loss': loss},pathx+"model_params" + str(i) +".tar")
    print("saved")
    '''
    #Test_loss.append(test_loss)
    #Test_acc.append(test_acc)
    print('='*20)
    
    

output_z = test_model2(model, test_loader, criterion)


with open("final_output_923_1.csv", 'a+') as outfile:
  
  for i in range(1,len(output_z)):
    np.savetxt(outfile,output_z[i].reshape(1,2), delimiter=',')

test_dataset = MyDataset_test(test_inputs, test_utterance_lengths, 5)

#test_loader_args = dict(shuffle=False, batch_size=1, num_workers=num_workers, pin_memory=True) if cuda\
#                    else dict(shuffle=False, batch_size=1)

test_loader_args = dict(shuffle=False, batch_size=1)

test_loader = data.DataLoader(test_dataset, **test_loader_args)

cd '/content/drive/My Drive/Colab Notebooks/data/'

z = np.zeros((1,1,2))
print(z)

ls

output_z = test_model2(model, test_loader, criterion)

print(output_z.shape)

with open("final_output_923_1.csv", 'a+') as outfile:
  
  for i in range(1,len(output_z)):
    np.savetxt(outfile,output_z[i].reshape(1,2), delimiter=',')

plt.title('Training Loss')
plt.xlabel('Epoch Number')
plt.ylabel('Loss')
plt.plot(Train_loss)

plt.title('Test Loss')
plt.xlabel('Epoch Number')
plt.ylabel('Loss')
plt.plot(Test_loss)

plt.title('Test Accuracy')
plt.xlabel('Epoch Number')
plt.ylabel('Accuracy (%)')
plt.plot(Test_acc)