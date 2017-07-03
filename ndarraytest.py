import numpy as np
x=np.array([[1,2,3],[9,8,7],[6,5,4]])
print(x.T)

#print(x.flags)
print(x.flat[:])

x = np.sqrt([2+3j, 5+0j])
print(x)
print(x.imag)
print(x.real)

x = np.arange(16)
print(x)
x1 = x.reshape(2,8)
# x1 = x.reshape(2,2,4)
print(x1)
# print(x1.size)
# print(x1.ndim) #3
# print(x1.shape) #(2,2,4)
print(x1.swapaxes(0,1))
print(x1.transpose())

# y = x1.reshape(8,2)
# print(y)
# print(y.base)
# print(y.any())
