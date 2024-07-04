import torch                        # pytorch  
import torch.optim as optim         # optimizer



# 데이터 -> 예측을 위한 실제 데이터
x_train = torch.FloatTensor([[1], [2], [3]]) # input data
y_train = torch.FloatTensor([[2], [4], [6]]) # output data

# print(x_train)
# print(x_train.shape)


W = torch.zeros(1, requires_grad=True) # 가중치 초기화
# print(W)
b = torch.zeros(1, requires_grad=True) # 편향 초기화
# print(b)

nb_epochs = 1000 # 1000번
for epoch  in range(nb_epochs + 1):
    hypothesis = x_train * W + b # 가설 설정 -> 이런 식의 모습으로 데이터는 존재할 것이다라고 가정
    # print(hypothesis)

    cost = torch.mean((hypothesis - y_train) ** 2) # 비용 함수 설정
    # print(cost)

    
    # [새로운 W] = [이전 W] - [학습률] * [W에 대한 미분]
    # [새로운 b] = [이전 b] - [학습률] * [b에 대한 미분]
    # W, b를 업데이트하는 식 -> W b가 SGD의 입력이 된다.
    optimizer = optim.SGD([W, b], lr=0.01) # optimizer 설정 (경사하강법, 학습률 0.01)

    # gradient를 0으로 초기화
    optimizer.zero_grad() # optimizer 초기화

    # 비용 함수를 미분하여 gradient 계산
    cost.backward() # 비용함수 미분

    # W, b 업데이트
    optimizer.step() # 경사하강법

    if epoch % 100 == 0:
        print('Epoch {:4d}/{} W: {:.3f}, b: {:.3f} Cost: {:.6f}'.format(
            epoch, nb_epochs, W.item(), b.item(), cost.item()
        ))
