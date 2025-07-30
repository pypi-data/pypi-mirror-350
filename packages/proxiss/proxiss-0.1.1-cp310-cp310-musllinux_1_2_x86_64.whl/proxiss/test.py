from ProxiCluster import ProxiCluster as pxc
import numpy as np

a = np.random.random((1000, 10))
b = np.random.randint((1000,)).astype(np.object_)

idx = pxc(3, 1, 20, "l1")
idx.index_data(a, b)