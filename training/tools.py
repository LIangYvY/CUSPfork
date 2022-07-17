import numpy as np
import torch

def getGaussianKernel(ksize,sigma=None):
    if sigma is None:
        sigma =  0.3*(ksize/2 - 1) + 0.8
    v = np.exp(-((np.arange(ksize)-(ksize-1)/2)**2)/(2*(sigma)**2))
    return (v / v.sum())[:,None]

def identity_f(x):
    return x

def batch_blur_quick(ims,ksize):
    k = torch.tensor(getGaussianKernel(ksize, None)).type_as(ims)
    b,c,w,h = ims.shape
    blur = torch.nn.functional.conv2d(ims.reshape(b*c,1,w,h),k[None,None,:],padding=((ksize-1)//2,0))
    blur = torch.nn.functional.conv2d(blur,k.T[None,None,:],padding=(0,(ksize-1)//2)).reshape(*ims.shape)
    return blur