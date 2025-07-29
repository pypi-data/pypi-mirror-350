import numpy as np

def num_grad(func, X, h):
    df = np.zeros(len(X))
    
    for i in range(len(X)):
        x1 = X.copy()
        x2 = X.copy()
        x1[i] = X[i] - h
        x2[i] = X[i] + h
        
        y1 = func(x1)
        y2 = func(x2)
        
        df[i] = (y2 - y1) / (2 * h)
    
    return df