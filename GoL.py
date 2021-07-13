# -*- coding: utf-8 -*-
"""
Created on Sun May 23 01:50:41 2021

@author: Shreyansh
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

A = np.zeros(10000).reshape(100,100)

# # Diehard
# A[48,51] = 1
# A[49,45] = 1
# A[49,46] = 1
# A[50,46] = 1
# A[50,50] = 1
# A[50,51] = 1
# A[50,52] = 1

# # Glider
# A[48,51] = 1
# A[49,52] = 1
# A[50,50] = 1
# A[50,51] = 1
# A[50,52] = 1

# Random Initialization
for t in range(5000):
    i = np.random.randint(100)
    j = np.random.randint(100)
    A[i,j] = 1
  

# # Blinker Line  
# A[47,49] = 1
# A[48,49] = 1
# A[49,49] = 1


neighbour_kernel = np.ones(9).reshape(3,3)
neighbour_kernel[1,1] = 0

image = plt.imshow(A, cmap='gray')
plt.pause(0.05)


while True:
    neighbour_count = np.round(fftconvolve(A,neighbour_kernel,mode='same'))
    
    # R1 = (A==1) & (neighbour_count<2)
    R2 = (A==1) & ((neighbour_count>1) & (neighbour_count<4))
    # R3 = (A==1) & (neighbour_count>3)
    R4 = (A==0) & (neighbour_count==3)
    
    A = np.zeros(10000).reshape(100,100)
    A[R2|R4] = 1
    image.set_data(A)
    plt.pause(0.05)

