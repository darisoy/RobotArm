#!/usr/bin/env python
# coding: utf-8

# In[4]:


import ikpy
import numpy as np
from ikpy import plot_utils


# In[5]:


my_chain = ikpy.chain.Chain.from_urdf_file("./niryo_one.urdf")


# In[6]:


target_vector = [ 0.1, -0.2, 0.1]
target_frame = np.eye(4)
target_frame[:3, 3] = target_vector


# In[7]:

angles = my_chain.inverse_kinematics(target_frame)
print("The angles of each joints are :")
for i in range(len(angles)):
    print(angles[i])
