from runner import  Runner
import numpy as np
np1=tuple([2,3,4])
np2=tuple([2,3,6])
V={np1:1,np2:2}
new_V={key:0 for key in V}
for key in new_V:
    print(key)
    print(new_V[key])