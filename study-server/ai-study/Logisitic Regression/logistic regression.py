"""
시그모이드 함수: sigmoid function
    - 0과 1의 결과를 같은 데이터 셋에서 사용하는 함수이다.
    - 0의 값 x1과 1의 값 x2 사이의 값을 어떻게 나타낼 것인가에 대한 함수이다.

공식: sigmoid(Wx + b) = 1 / (1 + e^-(Wx + b))
"""

import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_basic_example():
    x = np.arange(-5.0, 5.0, 0.1)
    y = sigmoid(x)

    plt.plot(x, y)
    plt.plot([0,0], [1.0, 0.0], ':') # 가운데 점선 추가
    plt.title('Sigmoid Function')
    plt.show()

# sigmoid_basic_example()

def slope_change_depend_on_Wvalue():
    x = np.arange(-5.0, 5.0, 0.1)
    y1 = sigmoid(0.5*x)
    y2 = sigmoid(x)
    y3 = sigmoid(2*x)

    plt.plot(x, y1, 'r', linestyle='--') # W값이 0.5일 때
    plt.plot(x, y2, 'g') # W값이 1일 때
    plt.plot(x, y3, 'b', linestyle='--') # W값이 2일 때
    plt.plot([0,0], [1.0, 0.0], ':') # 가운데 점선 추가
    plt.title('Sigmoid Function')
    plt.show()

# slope_change_depend_on_Wvalue()
    

def bias_change_depend_on_bvalue():
    x = np.arange(-5.0, 5.0, 0.1)
    y1 = sigmoid(x + 0.5)
    y2 = sigmoid(x + 1)
    y3 = sigmoid(x + 1.5)

    plt.plot(x, y1, 'r', linestyle='--') # b값이 0.5일 때
    plt.plot(x, y2, 'g') # b값이 1일 때
    plt.plot(x, y3, 'b', linestyle='--') # b값이 1.5일 때
    plt.plot([0,0], [1.0, 0.0], ':') # 가운데 점선 추가
    plt.title('Sigmoid Function')
    plt.show()

# bias_change_depend_on_bvalue()
    


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)

x_data = [[1, 2], [2, 3], [3, 1], [4, 3], [5, 3], [6, 2]]
y_data = [[0], [0], [0], [1], [1], [1]]
x_train = torch.FloatTensor(x_data)
y_train = torch.FloatTensor(y_data)

torch.Size([6, 2])
torch.Size([6, 1])

W = torch.zeros((2, 1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)

optimizer = optim.SGD([W, b], lr=1)


nb_epochs = 1000
for epoch in range(nb_epochs + 1):

    # Cost 계산
    hypothesis = torch.sigmoid(x_train.matmul(W) + b)


    # cost = -(y_train * torch.log(hypothesis) + (1 - y_train) * torch.log(1 - hypothesis)).mean()
    cost = F.binary_cross_entropy(hypothesis, y_train)

    # cost로 H(x) 개선
    optimizer.zero_grad()
    cost.backward()
    optimizer.step()
    # if epoch % 100 == 0:
    #     print('Epoch {:4d}/{} Cost: {:.6f}'.format(epoch, nb_epochs, cost.item()))

hpothesis = torch.sigmoid(x_train.matmul(W) + b)
prediction = hypothesis >= torch.FloatTensor([0.5])
print(prediction)
print(W)
print(b)
