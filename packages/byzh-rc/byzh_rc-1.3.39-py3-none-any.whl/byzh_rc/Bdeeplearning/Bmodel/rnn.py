import torch
import torch.nn as nn

class B_RNN(nn.Module):
    def __init__(self, num_classes, input_size, hidden_size, num_layers=1):
        super().__init__()
        self.rnn = nn.RNN(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
        )
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x): # x [B, C, L]
        x = x.permute(2, 0, 1) # x [L, B, C]

        out, h = self.rnn(x)
        x = out # x [L, B, H]

        # 取最后一个时间步的输出作为整个序列的表示
        x = x[-1]
        x = self.fc(x)
        return x

if __name__ == '__main__':
    model = B_RNN(num_classes=11, input_size=2, hidden_size=512, num_layers=4)
    x = torch.randn(64, 2, 128) # 输入形状 [batch_size, input_size, seq_len]
    y = model(x)
    print(y.shape)