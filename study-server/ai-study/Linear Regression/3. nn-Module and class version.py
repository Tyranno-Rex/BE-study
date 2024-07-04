import torch
import torch.nn as nn
import torch.nn.functional as F

def nn_module():
    torch.manual_seed(1)

    x_train = torch.FloatTensor([[1], [2], [3]])
    y_train = torch.FloatTensor([[2], [4], [6]])

    model = nn.Linear(1, 1)


    # print(list(model.parameters()))
    # [Parameter containing: tensor([[-0.0838]], requires_grad=True), 
    #  Parameter containing: tensor([-0.0343], requires_grad=True)]
    # requires_grad=True : 학습을 통해 계속 값이 변경되는 변수

    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    nb_epochs = 2000 # epoch : 전체 데이터 셋에 대해 한 번 학습을 완료한 상태, 전체 데이터셋을 학습한 횟수

    for epoch in range(nb_epochs + 1):
        prediction = model(x_train)
        cost = F.mse_loss(prediction, y_train)

        optimizer.zero_grad()
        cost.backward()
        optimizer.step()

        if epoch % 100 == 0:
            print('Epoch {:4d}/{} Cost: {:.6f}'.format(epoch, nb_epochs, cost.item()))

        # 출력 결과에서 Cost값이 점점 줄어드는 것을 확인할 수 있으며, 결국에는 0.00000의 값을 해당 실행의 Cost값으로 얻을 수 있다.

    # W와 b의 값이 최적화가 되었는지 확인
    new_var = torch.FloatTensor([[4.0]])
    pred_y = model(new_var)
    print('훈련 후 입력이 4일 때의 예측값 :', pred_y) 
    # 예측값이 8에 가까운 값이 나오면, W와 b의 값이 잘 최적화된 것
    # 결과 : 훈련 후 입력이 4일 때의 예측값 : tensor([[7.9989]], grad_fn=<AddmmBackward>)

    print(list(model.parameters())) # W의 값이 2에 가깝고, b의 값이 0에 가까운 것을 확인
    # [Parameter containing: tensor([[1.9994]], requires_grad=True),
    #  Parameter containing: tensor([0.0014], requires_grad=True)]


# 다중 회귀도 nn.Module로 구현 하는 것으로 앞선 코드와는 크게 다르지 않다.
    



# class version
import torch.nn as nn

class LinearRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(1, 1) # 단순 선형 회귀이므로 input_dim=1, output_dim=1.

    def forward(self, x):
        return self.linear(x)

model = LinearRegressionModel()