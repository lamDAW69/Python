import numpy as np

def calculate(list):
    if len(list) != 9:
      raise ValueError("The list must contain exactly 9 elements.")

    arry3x3 = np.array(list).reshape(3,3)
    
    calculations = {
       'mean': [np.mean(arry3x3, axis=0).tolist(), np.mean(arry3x3, axis=1).tolist(), np.mean(arry3x3).tolist()],
        'variance': [np.var(arry3x3, axis=0).tolist(), np.var(arry3x3, axis=1).tolist(), np.var(arry3x3).tolist()],
        'standard deviation': [np.std(arry3x3, axis=0).tolist(), np.std(arry3x3, axis=1).tolist(), np.std(arry3x3).tolist()],
        'max': [np.max(arry3x3, axis=0).tolist(), np.max(arry3x3, axis=1).tolist(), np.max(arry3x3).tolist()],
        'min': [np.min(arry3x3, axis=0).tolist(), np.min(arry3x3, axis=1).tolist(), np.min(arry3x3).tolist()],
        'sum': [np.sum(arry3x3, axis=0).tolist(), np.sum(arry3x3, axis=1).tolist(), np.sum(arry3x3).tolist()]
        }
    return calculations





list = [3, 2,3,4,5,6,7,8,9]
print(calculate(list))