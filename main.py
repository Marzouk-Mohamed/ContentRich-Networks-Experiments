import numpy as np
import scipy.io as sio
from AANE_fun import AANE
import time


'''################# Load data  #################'''
mat_contents = sio.loadmat('BlogCatalog.mat')
lambd = 10**-0.6  # the regularization parameter
rho = 5  # the penalty parameter

# mat_contents = sio.loadmat('Flickr.mat')
# lambd = 0.0425  # the regularization parameter
# rho = 4  # the penalty parameter

'''################# Experimental Settings #################'''
d = 100  # the dimension of the embedding representation
G = mat_contents["Network"]
A = mat_contents["Attributes"]
Label = mat_contents["Label"]
del mat_contents
n = G.shape[0]
Indices = np.random.randint(25, size=n)+1 

Group1 = []
Group2 = []
[Group1.append(x) for x in range(0, n) if Indices[x] <= 20]  
[Group2.append(x) for x in range(0, n) if Indices[x] >= 21]  
n1 = len(Group1)  
n2 = len(Group2)  
CombG = G[Group1+Group2, :][:, Group1+Group2]
CombA = A[Group1+Group2, :]

'''################# Accelerated Attributed Network Embedding #################'''
print("Accelerated Attributed Network Embedding (AANE), 5-fold with 100% of training is used:")
start_time = time.time()
H_AANE = AANE(CombG, CombA, d, lambd, rho).function()
print("time elapsed: {:.2f}s".format(time.time() - start_time))


print("AANE for a pure network:")
start_time = time.time()
H_Net = AANE(CombG, CombG, d, lambd, rho).function()
print("time elapsed: {:.2f}s".format(time.time() - start_time))
sio.savemat('Embedding.mat', {"H_AANE": H_AANE, "H_Net": H_Net})

