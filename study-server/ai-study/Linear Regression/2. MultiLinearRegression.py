import torch
import torch.optim as optim

torch.manual_seed(1) # 랜덤 시드 고정


# 훈련 데이터
x1_train = torch.FloatTensor([[73], [93], [89], [96], [73]])
x2_train = torch.FloatTensor([[80], [88], [91], [98], [66]])
x3_train = torch.FloatTensor([[75], [93], [90], [100], [70]])
y_train = torch.FloatTensor([[152], [185], [180], [196], [142]])


# 가중치 w와 편향 b 초기화
w1 = torch.zeros(1, requires_grad=True)
w2 = torch.zeros(1, requires_grad=True)
w3 = torch.zeros(1, requires_grad=True)
b  = torch.zeros(1, requires_grad=True)


# optimizer 설정
optimizer = optim.SGD([w1, w2, w3, b], lr=1e-5)

nb_epochs = 10000
for epoch in range(nb_epochs + 1):
    # 가설 설정 -> 값을 해당 가설에 넣어서 예측값을 구함
    hypothesis = x1_train * w1 + x2_train * w2 + x3_train * w3 + b
    cost = torch.mean((hypothesis - y_train) ** 2)
    optimizer.zero_grad()
    cost.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print('Epoch {:4d}/{} w1: {:.3f} w2: {:.3f} w3: {:.3f} b: {:.3f} Cost: {:.6f}'.format(
            epoch, nb_epochs, w1.item(), w2.item(), w3.item(), b.item(), cost.item()
        ))

# 해당 코드의 문제점 
# -> 데이터의 개수가 많아지면 선언부가 많아짐

# 해결 방법
# -> 행렬 연산을 통해 코드를 간단하게 작성


x_train  =  torch.FloatTensor([[73,  80,  75], 
                                [93,  88,  93], 
                                [89,  91,  80], 
                                [96,  98,  100],   
                                [73,  66,  70]])  
y_train  =  torch.FloatTensor([[152],  [185],  [180],  [196],  [142]])


W = torch.zeros((3, 1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)


optimizer = optim.SGD([W, b], lr=1e-5)

nb_epochs = 10000
for epoch in range(nb_epochs + 1):
    
    hypothesis = x_train.matmul(W) + b
    cost = torch.mean((hypothesis - y_train) ** 2)
    optimizer.zero_grad()
    cost.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print('Epoch {:4d}/{} w1: {:.3f} w2: {:.3f} w3: {:.3f} b: {:.3f} Cost: {:.6f}'.format(
            epoch, nb_epochs, W[0].item(), W[1].item(), W[2].item(), b.item(), cost.item()
        ))