class B_StopByByzh:
    def __init__(self, loss_rounds=20, loss_target=0.001, acc_rounds=50, acc_target=1):
        self.loss_rounds = loss_rounds
        self.loss_target = loss_target
        self.acc_rounds = acc_rounds
        self.acc_target = acc_target

        self.loss_list = [114514 for _ in range(loss_rounds)]
        self.acc_list = [0 for _ in range(acc_rounds)]

        self.loss_average_list = [114514 for _ in range(loss_rounds)]
        self.acc_average_list = [0 for _ in range(acc_rounds)]

        self.loss_avg_trend = None
        self.acc_avg_trend = None

        self.output = ""
    def __call__(self, train_loss, val_acc):
        if train_loss <= self.loss_target:
            self.output = f"train_loss小于{self.loss_target}"
            return True
        if val_acc >= self.acc_target:
            self.output = f"val_acc大于等于{self.acc_target}"
            return True
        self.update(self.loss_list, train_loss)
        self.update(self.acc_list, val_acc)

        self.update(self.loss_average_list, sum(self.loss_list) / self.loss_rounds)
        self.update(self.acc_average_list, sum(self.acc_list) / self.acc_rounds)

        self.loss_avg_trend = self.get_trend(self.loss_average_list)
        self.acc_avg_trend = self.get_trend(self.acc_average_list)
        if sum(self.loss_avg_trend) > 0:
            self.output = f"loss_avg_trend:{self.loss_avg_trend}"
            return True
        if sum(self.acc_avg_trend) < 0:
            self.output = f"acc_avg_trend:{self.acc_avg_trend}"
            return True
        return False

    def update(self, lst, train_loss):
        lst.append(train_loss)
        lst.pop(0)

    def get_trend(self, lst):
        temp = lst.copy()
        x = temp[0]
        for i in range(len(temp)):
            if temp[i] < x:
                temp[i] = -1
            elif temp[i] > x:
                temp[i] = 1
            else:
                temp[i] = 0
        return temp