"""

problem: 행렬연산을 하나의 행렬로 선언해 전체 데이트를 한 번에 경하 하강법을 통해 학습하는 것은 매우 느리며, 많은 계산량이 필요하다.

해결책: 미니배치를 사용하여 데이터를 나누어 학습하는 방법을 사용한다.


--------------------------------------
|              전체 데이터            |
--------------------------------------
전환 ->
--------------------------------------
|미니배치1|미니배치2|미니배치3|미니배치4|
--------------------------------------

한 번에 경사 하강법을 수행하는 방법을 '배치 경사 하강법'이라고 한다.
미니배치를 사용하여 경사 하강법을 수행하는 방법을 '미니배치 경사 하강법'이라고 한다.

"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader



x_train = torch.FloatTensor([[73, 80, 75],
                                [93, 88, 93],
                                [89, 91, 90],
                                [96, 98, 100],
                                [73, 66, 70]])
y_train = torch.FloatTensor([[152], [185], [180], [196], [142]])

dataset = TensorDataset(x_train, y_train)

# 매개변수
# dataset : 미니배치로 만들 데이터셋
# batch_size : 미니배치의 크기
# shuffle : Epoch마다 데이터셋을 섞어 학습 순서를 바꿀지 여부 
#           -> 같은 순서로 학습을 하면 순서에 익숙해질 수 있으므로 섞어주는 것이 좋다.
data_loader = DataLoader(dataset, batch_size=2, shuffle=True)


model = nn.Linear(3, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=1e-5)

nb_epochs = 200
for epoch in range(nb_epochs + 1):
    for batch_idx, sample in enumerate(data_loader):
        x_train, y_train = sample

        prediction = model(x_train)

        cost = F.mse_loss(prediction, y_train)

        optimizer.zero_grad()
        cost.backward()
        optimizer.step()

        print('Epoch {:4d}/{} Batch {}/{} Cost: {:.6f}'.format(epoch, nb_epochs, batch_idx+1, len(data_loader), cost.item()))

new_var = torch.FloatTensor([[73, 80, 75]])
pred_y = model(new_var)
print("훈련 후 입력이 73, 80, 75일 때의 예측값 : ", pred_y)