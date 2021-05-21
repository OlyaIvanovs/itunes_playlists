import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform, pdist, cdist

width, height = 640, 480

fig = plt.figure()
ax = plt.axes(xlim=(0, width), ylim=(0, height))

n = 5

pos = [width/2.0, height/2.0] + 200*np.random.rand(2*n).reshape(n, 2)
angles = 2*math.pi*np.random.rand(n)
vel = np.array(list(zip(np.sin(angles), np.cos(angles))))
print('pos')
print(pos)
print('vel')
print(vel)
# vec = 10*vel/2 + pos

dist_matrix = squareform(pdist(pos))
print('dist_matrix')
print(dist_matrix)

D = dist_matrix < 100
print(D)
vel = D.sum(axis=1).reshape(n, 1)
print(vel)
vel = D.sum(axis=1).reshape(n, 1)*pos
print(vel)
vel2 = D.dot(pos)
vel3 = D.dot(pos)/D.sum(axis=1).reshape(n, 1) - pos
print("vel2", vel2)
print("vel3", vel3)


# print(vec)

pts = ax.plot(pos.reshape(2*n)[::2], pos.reshape(2*n)[1::2], markersize=10,
              c='k', marker='o', ls="None")
# beak = ax.plot(vec.reshape(2*n)[::2], vec.reshape(2*n)
#                [1::2], markersize=4, c='r', marker='o', ls="None")

plt.show()
